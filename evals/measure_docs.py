#!/usr/bin/env python3
"""Measure the documentation claims of this kit (stdlib only).

What it measures (reproducible, no model calls unless a token counter is chosen):
  1. size      : lines/words/chars/bytes per document and a proxy token estimate
  2. line-limit: which governed docs exceed a line limit (claim: "< 120 lines")
  3. path      : total read budget of the bootstrap path an agent follows
  4. lang      : bytes/words ratio between Vietnamese (old git revision) and
                 English (HEAD) versions of the same files (claim: ADR-0014)

Token counters (--counter):
  proxy   (default) chars/4. NOT a Claude tokenizer; it systematically
          underestimates non-English text. Use only for relative size within
          one language.
  api     Anthropic count_tokens endpoint. Needs ANTHROPIC_API_KEY. Free, but
          sends the text to the API.
  cli     Differential count through `claude -p` (needs a logged-in Claude Code).
          Sends the text to the model; costs a small amount of usage.

Examples:
  python evals/measure_docs.py size  core profiles
  python evals/measure_docs.py limit 120
  python evals/measure_docs.py path
  python evals/measure_docs.py lang 58e5df8
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOVERNED_ROOTS = ("core", "profiles")
GOVERNED_EXCLUDES = ("core/templates/", "profiles/frontend/starter/")

# Characters used in Vietnamese but not in plain English text.
VI_CHARS = set(
    "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
    "ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ"
)


# ---------------------------------------------------------------- counters
def count_proxy(text: str) -> int:
    return math.ceil(len(text) / 4)


def count_api(text: str) -> int:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set")
    model = os.environ.get("ANTHROPIC_COUNT_MODEL", "claude-sonnet-5-5")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": text}]}).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages/count_tokens",
        data=body,
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["input_tokens"]


def _cli_total(prompt: str) -> int:
    out = subprocess.run(
        ["claude", "-p", "--output-format", "json", "--no-session-persistence", "--tools", "",
         "--system-prompt", "Reply with the single word OK."],
        input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=os.environ.get("TEMP", "."),
    ).stdout
    d = json.loads(out)
    if d.get("is_error"):
        sys.exit(f"claude CLI error: {d.get('result')}")
    u = d["usage"]
    return u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)


_CLI_BASE: int | None = None


def count_cli(text: str) -> int:
    global _CLI_BASE
    if _CLI_BASE is None:
        _CLI_BASE = _cli_total("x")
    return max(0, _cli_total(text) - _CLI_BASE)


COUNTERS = {"proxy": count_proxy, "api": count_api, "cli": count_cli}


# ----------------------------------------------------------------- helpers
def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def stats(text: str) -> dict:
    return {
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "words": len(text.split()),
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
    }


def vi_density(text: str) -> float:
    letters = sum(1 for c in text if c.isalpha())
    return (sum(1 for c in text if c in VI_CHARS) / letters) if letters else 0.0


def governed_docs() -> list[Path]:
    files = []
    for r in GOVERNED_ROOTS:
        for p in sorted((ROOT / r).rglob("*.md")):
            rel = p.relative_to(ROOT).as_posix()
            if not any(rel.startswith(x) for x in GOVERNED_EXCLUDES):
                files.append(p)
    return files


def md_table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(":--" if i == 0 else "--:" for i in range(len(headers))) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# ---------------------------------------------------------------- commands
def cmd_size(a) -> None:
    ctr = COUNTERS[a.counter]
    rows, tot = [], 0
    for r in a.roots:
        for p in sorted((ROOT / r).rglob("*.md")):
            t = read(p)
            s = stats(t)
            n = ctr(t)
            tot += n
            rows.append([p.relative_to(ROOT).as_posix(), s["lines"], s["words"], s["bytes"], n])
    print(md_table(["file", "lines", "words", "bytes", f"tokens[{a.counter}]"], rows))
    print(f"\nTotal tokens[{a.counter}]: {tot}")


def cmd_limit(a) -> None:
    rows = []
    docs = governed_docs()
    for p in docs:
        n = stats(read(p))["lines"]
        if n > a.max_lines:
            rows.append([p.relative_to(ROOT).as_posix(), n])
    rows.sort(key=lambda r: -r[1])
    print(f"Governed docs (core/, profiles/ minus templates and starter): {len(docs)}")
    print(f"Over {a.max_lines} lines: {len(rows)}\n")
    if rows:
        print(md_table(["file", "lines"], rows))


BOOTSTRAP_PATH = [
    ("Phase 0", ["BOOTSTRAP.md", "core/README.md", "core/templates/AGENTS.md"]),
    ("Phase 1", ["core/discovery.md", "INDEX.md", "profiles/README.md"]),
    ("Phase 2", ["profiles/architecture/{profile}.md"]),
    ("Phase 4", ["profiles/deployment/go-live-production-checklist.md"]),
]


def cmd_path(a) -> None:
    ctr = COUNTERS[a.counter]
    rows, total_b, total_t = [], 0, 0
    for phase, docs in BOOTSTRAP_PATH:
        for d in docs:
            rel = d.format(profile=a.profile)
            p = ROOT / rel
            if not p.exists():
                print(f"MISSING {rel}", file=sys.stderr)
                continue
            t = read(p)
            s = stats(t)
            n = ctr(t)
            total_b += s["bytes"]
            total_t += n
            rows.append([phase, rel, s["lines"], s["bytes"], n])
    print(md_table(["phase", "file", "lines", "bytes", f"tokens[{a.counter}]"], rows))
    print(f"\nBootstrap read budget (profile={a.profile}): {total_b} bytes, {total_t} tokens[{a.counter}]")


def git_show(rev: str, rel: str) -> str | None:
    r = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else None


def cmd_lang(a) -> None:
    rows, agg = [], {"bytes": [0, 0], "words": [0, 0], "chars": [0, 0]}
    for p in governed_docs():
        rel = p.relative_to(ROOT).as_posix()
        old = git_show(a.rev, rel)
        if old is None:
            continue
        new = read(p)
        d_old, d_new = vi_density(old), vi_density(new)
        if d_old >= a.vi_threshold and d_new < a.vi_threshold:  # Vietnamese then, English now
            so, sn = stats(old), stats(new)
            for k in agg:
                agg[k][0] += so[k]
                agg[k][1] += sn[k]
            rows.append([rel, so["bytes"], sn["bytes"], so["words"], sn["words"], f"{d_old:.1%}", f"{d_new:.1%}"])
    print(md_table(["file", "bytes vi", "bytes en", "words vi", "words en", "vi-char% then", "now"], rows))
    print(f"\nFiles compared: {len(rows)} (Vietnamese at {a.rev}, English at HEAD)")
    for k, (o, n) in agg.items():
        if o:
            print(f"{k}: vi={o} en={n} en/vi={n / o:.2f}")
    print("\nCAVEAT: the files are NOT line-by-line translations (content also changed), and bytes/words are NOT tokens.")
    print("Use --counter api|cli on a true parallel corpus to measure the token claim.")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--counter", choices=COUNTERS, default="proxy")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("size"); s.add_argument("roots", nargs="+"); s.set_defaults(fn=cmd_size)
    s = sub.add_parser("limit"); s.add_argument("max_lines", type=int); s.set_defaults(fn=cmd_limit)
    s = sub.add_parser("path"); s.add_argument("--profile", default="vertical-slice"); s.set_defaults(fn=cmd_path)
    s = sub.add_parser("lang"); s.add_argument("rev"); s.add_argument("--vi-threshold", type=float, default=0.03); s.set_defaults(fn=cmd_lang)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
