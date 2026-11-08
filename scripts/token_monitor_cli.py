#!/usr/bin/env python3
"""Token Monitor CLI: live view of token usage from local Claude Code transcripts.

Read-only. Makes no network or model calls. Reads ~/.claude/projects/<project>/*.jsonl.

  python scripts/token_monitor_cli.py                 # latest session of the current folder, once
  python scripts/token_monitor_cli.py --watch         # live, refresh every 2 s
  python scripts/token_monitor_cli.py --all --json    # all sessions of this project, JSON
  python scripts/token_monitor_cli.py --project D:\\path\\to\\app --watch

Only Claude Code transcripts are supported (format verified 2026-11-07).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from token_monitor import Aggregator, Snapshot, TranscriptTailer, find_transcripts, parse_line  # noqa: E402

L = {
    "vi": {
        "title": "THEO DÕI TOKEN", "project": "dự án", "scope": "phạm vi", "latest": "phiên mới nhất", "all": "tất cả phiên",
        "ctx": "Ngữ cảnh hiện tại", "peak": "đỉnh", "turns": "Số lượt trả lời", "total": "Tổng (đã loại trùng)",
        "new_in": "vào mới", "cache_w": "ghi cache", "cache_r": "đọc cache", "out": "ra", "rate": "Tốc độ gần đây",
        "per_min": "token mới/phút", "out_min": "ra/phút", "models": "Theo model", "top": "Lượt nặng nhất",
        "none": "Chưa có dữ liệu. Hãy chat với agent trong thư mục này rồi chạy lại.",
        "warn": "Ngữ cảnh lớn: mỗi lượt phải đọc lại toàn bộ. Cân nhắc tóm tắt (/compact) hoặc mở phiên mới.",
        "note": "Số liệu đọc từ log cục bộ của Claude Code, không phải hoá đơn chính thức.",
        "hint": "Ctrl+C để thoát", "of": "so với giới hạn",
    },
    "en": {
        "title": "TOKEN MONITOR", "project": "project", "scope": "scope", "latest": "latest session", "all": "all sessions",
        "ctx": "Context now", "peak": "peak", "turns": "Assistant turns", "total": "Totals (de-duplicated)",
        "new_in": "fresh in", "cache_w": "cache write", "cache_r": "cache read", "out": "out", "rate": "Recent rate",
        "per_min": "new tokens/min", "out_min": "out/min", "models": "By model", "top": "Heaviest turns",
        "none": "No data yet. Chat with the agent in this folder, then run again.",
        "warn": "Large context: every turn re-reads all of it. Consider /compact or a new session.",
        "note": "Read from Claude Code's local logs; not an official bill.",
        "hint": "Ctrl+C to quit", "of": "of limit",
    },
}


def n(v: int | float) -> str:
    return f"{int(v):,}"


def render(s: Snapshot, a, files: list[Path]) -> str:
    t = L[a.lang]
    if s.totals.turns == 0:
        return t["none"]
    scope = t["all"] if a.all else f"{t['latest']} ({files[0].stem[:8]})"
    lim = f"  ({100 * s.context_now / a.context_limit:.0f}% {t['of']})" if a.context_limit else ""
    lines = [
        f"{t['title']}  |  {t['project']}: {Path(a.project).name}  |  {t['scope']}: {scope}  |  {datetime.now():%H:%M:%S}",
        "",
        f"{t['ctx']:<24}: {n(s.context_now)} token{lim}   [{t['peak']} {n(s.context_peak)}]",
        f"{t['turns']:<24}: {n(s.totals.turns)}",
        f"{t['total']:<24}: {t['new_in']} {n(s.totals.input_tokens)} | {t['cache_w']} {n(s.totals.cache_creation)} | "
        f"{t['cache_r']} {n(s.totals.cache_read)} | {t['out']} {n(s.totals.output_tokens)}",
        f"{t['rate']:<24}: {n(s.new_tokens_per_min)} {t['per_min']} ({n(s.output_tokens_per_min)} {t['out_min']})",
    ]
    if len(s.by_model) > 0:
        lines.append(f"{t['models']:<24}: " + " | ".join(f"{m} ×{x.turns}" for m, x in sorted(s.by_model.items())))
    lines.append(f"{t['top']}:")
    for e in s.top_turns:
        lines.append(f"  {e.ts.astimezone():%H:%M:%S}  {n(e.new_tokens):>9} {t['per_min'].split('/')[0]}  "
                     f"({t['cache_w']} {n(e.cache_creation)}, {t['out']} {n(e.output_tokens)})")
    if a.warn_context and s.context_now >= a.warn_context:
        lines += ["", "! " + t["warn"]]
    lines += ["", t["note"]]
    return "\n".join(lines)


def to_json(s: Snapshot) -> dict:
    return {
        "turns": s.totals.turns, "sessions": s.sessions,
        "fresh_input": s.totals.input_tokens, "cache_write": s.totals.cache_creation,
        "cache_read": s.totals.cache_read, "output": s.totals.output_tokens,
        "context_now": s.context_now, "context_peak": s.context_peak,
        "new_tokens_per_min": round(s.new_tokens_per_min, 1), "output_tokens_per_min": round(s.output_tokens_per_min, 1),
        "by_model": {m: {"turns": x.turns, "output": x.output_tokens} for m, x in s.by_model.items()},
        "warnings": s.warnings,
    }


def projects_root(a) -> Path:
    if a.projects_root:
        return Path(a.projects_root)
    cfg = os.environ.get("CLAUDE_CONFIG_DIR")
    return (Path(cfg) if cfg else Path.home() / ".claude") / "projects"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default=os.getcwd(), help="project folder (default: current directory)")
    ap.add_argument("--projects-root", help="override ~/.claude/projects")
    ap.add_argument("--session", help="session id (file name without .jsonl)")
    ap.add_argument("--all", action="store_true", help="aggregate all sessions of the project")
    ap.add_argument("--watch", action="store_true", help="refresh continuously")
    ap.add_argument("--interval", type=float, default=2.0)
    ap.add_argument("--json", action="store_true", help="print JSON once and exit")
    ap.add_argument("--lang", choices=sorted(L), default="vi")
    ap.add_argument("--context-limit", type=int, default=0, help="show context as %% of this limit")
    ap.add_argument("--warn-context", type=int, default=0, help="warn above this context size (0 = off; no default threshold is recommended by any source)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    root = projects_root(a)
    files = find_transcripts(root, a.project)
    if a.session:
        files = [f for f in files if f.stem == a.session]
    if not files:
        print(f"{L[a.lang]['none']}\n({root})", file=sys.stderr)
        return 2
    if not a.all:
        files = files[:1]

    agg, tail = Aggregator(), TranscriptTailer()

    def pull() -> None:
        for f in files if a.all else files[:1]:
            for line in tail.read_new(f):
                e = parse_line(line, f.stem)
                if e:
                    agg.add(e)

    pull()
    if a.json:
        print(json.dumps(to_json(agg.snapshot()), ensure_ascii=False, indent=2))
        return 0
    if not a.watch:
        print(render(agg.snapshot(), a, files))
        return 0
    os.system("")  # enable ANSI escape codes on Windows terminals
    try:
        while True:
            if not a.all:  # follow the newest session as it changes
                newest = find_transcripts(root, a.project)[:1]
                if newest and newest[0] != files[0]:
                    files, agg, tail = newest, Aggregator(), TranscriptTailer()
            pull()
            sys.stdout.write("\x1b[2J\x1b[H" + render(agg.snapshot(), a, files) + f"\n\n{L[a.lang]['hint']}\n")
            sys.stdout.flush()
            time.sleep(a.interval)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
