"""Data service for the Token Dashboard (no HTTP, no UI): turns transcript files into JSON payloads.

Security: callers pass a project *id* (a folder name inside the projects root), never a path.
Anything that is not exactly an existing direct child folder of the root is rejected.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from token_monitor import Aggregator, TranscriptTailer, parse_line, parse_prompt, project_dir_name  # noqa: E402

MAX_STATES = 8


def default_projects_root() -> Path:
    cfg = os.environ.get("CLAUDE_CONFIG_DIR")
    return (Path(cfg) if cfg else Path.home() / ".claude") / "projects"


def _iso(dt: datetime | None) -> str | None:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if dt else None


class TokenService:
    def __init__(self, root: Path | None = None, default_project_path: str | None = None) -> None:
        self.root = Path(root) if root else default_projects_root()
        self.default_project_id = project_dir_name(default_project_path) if default_project_path else None
        self._states: dict[tuple[str, str], dict] = {}

    # ---- lookups -----------------------------------------------------
    def _project_dir(self, project_id: str) -> Path | None:
        if not project_id or any(c in project_id for c in "/\\") or project_id in (".", ".."):
            return None
        d = self.root / project_id
        return d if d.is_dir() and d.parent == self.root else None

    def projects(self) -> list[dict]:
        if not self.root.is_dir():
            return []
        out = []
        for d in self.root.iterdir():
            if not d.is_dir():
                continue
            files = list(d.glob("*.jsonl"))
            if files:
                out.append({"id": d.name, "sessions": len(files), "mtime": max(f.stat().st_mtime for f in files)})
        out.sort(key=lambda p: p["mtime"], reverse=True)
        for p in out:
            p["last_activity"] = _iso(datetime.fromtimestamp(p.pop("mtime"), timezone.utc))
        return out

    def pick_default_project(self) -> str | None:
        ps = self.projects()
        ids = {p["id"] for p in ps}
        if self.default_project_id in ids:
            return self.default_project_id
        return ps[0]["id"] if ps else None

    def sessions(self, project_id: str) -> list[dict]:
        d = self._project_dir(project_id)
        if not d:
            return []
        files = sorted(d.glob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
        return [{"id": f.stem, "modified": _iso(datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)),
                 "size": f.stat().st_size} for f in files]

    # ---- payload -----------------------------------------------------
    def payload(self, project_id: str, session: str = "latest", warn_context: int = 0,
                window_min: float = 10.0, max_points: int = 300, top_n: int = 5) -> dict:
        d = self._project_dir(project_id)
        if not d:
            return {"error": "unknown project"}
        sessions = self.sessions(project_id)
        if not sessions:
            return {"error": "no sessions", "sessions": []}
        if session == "all":
            files = [d / f"{s['id']}.jsonl" for s in sessions]
        else:
            sid = sessions[0]["id"] if session == "latest" else session
            if sid not in {s["id"] for s in sessions}:
                return {"error": "unknown session", "sessions": sessions}
            files = [d / f"{sid}.jsonl"]
        resolved = "all" if session == "all" else files[0].stem

        key = (project_id, resolved)
        st = self._states.get(key)
        if st is None:
            if len(self._states) >= MAX_STATES:
                self._states.pop(next(iter(self._states)))
            st = self._states[key] = {"agg": Aggregator(), "tail": TranscriptTailer()}
        for f in files:
            for line in st["tail"].read_new(f):
                e = parse_line(line, f.stem)
                if e:
                    st["agg"].add(e)
                    continue
                q = parse_prompt(line, f.stem)
                if q:
                    st["agg"].add_prompt(q)

        agg: Aggregator = st["agg"]
        snap = agg.snapshot(window_min=window_min, top_n=top_n)
        evs = agg.events()
        series = [{"t": _iso(e.ts), "ctx": e.context_tokens, "in": e.input_tokens + e.cache_creation,
                   "out": e.output_tokens, "cr": e.cache_read, "m": e.model, "side": e.sidechain}
                  for e in evs[-max_points:]]
        today = datetime.now().astimezone().date()
        t = {"in_new": 0, "cache_read": 0, "out": 0, "calls": 0}
        for e in evs:
            if e.ts.astimezone().date() == today:
                t["in_new"] += e.input_tokens + e.cache_creation
                t["cache_read"] += e.cache_read
                t["out"] += e.output_tokens
                t["calls"] += 1
        exchanges = agg.exchanges()
        return {
            "project": project_id,
            "session": resolved,
            "sessions": sessions,
            "turns": snap.totals.turns,
            "totals": {"fresh_input": snap.totals.input_tokens, "cache_write": snap.totals.cache_creation,
                       "cache_read": snap.totals.cache_read, "output": snap.totals.output_tokens},
            "context_now": snap.context_now,
            "context_peak": snap.context_peak,
            "warn_context": warn_context,
            "new_tokens_per_min": round(snap.new_tokens_per_min, 1),
            "output_tokens_per_min": round(snap.output_tokens_per_min, 1),
            "last_event_at": _iso(snap.last_event_at),
            "by_model": [{"model": m, "turns": t.turns, "output": t.output_tokens} for m, t in sorted(snap.by_model.items())],
            "top_turns": [{"t": _iso(e.ts), "new": e.new_tokens, "cache_write": e.cache_creation, "out": e.output_tokens}
                          for e in snap.top_turns[:top_n]],
            "today": t,
            "prompts": len(exchanges),
            "exchanges": [{"t": _iso(x.ts), "preview": x.preview, "calls": x.calls, "in_new": x.input_new,
                           "cache_read": x.cache_read, "out": x.output, "secs": round(x.seconds)}
                          for x in exchanges[-40:]],
            "series": series,
            "truncated": max(0, len(evs) - len(series)),
            "warnings": snap.warnings,
        }
