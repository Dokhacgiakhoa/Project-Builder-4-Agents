"""Token usage engine for AI coding agent transcripts (pure logic, stdlib only).

No UI, no network, no model calls. It turns transcript lines into usage events,
removes duplicates, and computes snapshots. Presentation lives in the CLI.

Verified source format (Claude Code, checked on 2026-11-07 against real local
transcripts): each `assistant` line carries `message.id`, `requestId`,
`message.model`, `timestamp` and `message.usage` with `input_tokens`,
`cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`.
The same API response is written several times (one line per content block)
with identical usage, so summing lines naively overcounts (about 2.3x on the
sample session). Events are therefore de-duplicated by (message.id, requestId).

Not verified: other agents (Codex, Cursor, Antigravity). Do not assume them.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path


@dataclass(frozen=True)
class UsageEvent:
    ts: datetime
    session_id: str
    message_id: str
    request_id: str
    model: str
    input_tokens: int          # fresh input not served from cache
    cache_creation: int        # new content written to the prompt cache
    cache_read: int            # context re-read from cache this turn
    output_tokens: int
    sidechain: bool = False    # sub-agent traffic

    @property
    def key(self) -> tuple[str, str]:
        return (self.message_id, self.request_id)

    @property
    def context_tokens(self) -> int:
        """Size of the prompt sent this turn (what fills the context window)."""
        return self.input_tokens + self.cache_creation + self.cache_read

    @property
    def new_tokens(self) -> int:
        """Tokens that are new work this turn (not cache re-reads)."""
        return self.input_tokens + self.cache_creation + self.output_tokens


def _int(v) -> int:
    return v if isinstance(v, int) and v >= 0 else 0


def _parse_ts(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_line(line: str, session_id: str = "") -> UsageEvent | None:
    """Parse one transcript line; None when it is not an assistant usage record."""
    line = line.strip()
    if not line or '"usage"' not in line:
        return None
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(d, dict) or d.get("type") != "assistant":
        return None
    m = d.get("message")
    if not isinstance(m, dict):
        return None
    u = m.get("usage")
    ts = _parse_ts(d.get("timestamp"))
    if not isinstance(u, dict) or ts is None:
        return None
    return UsageEvent(
        ts=ts,
        session_id=str(d.get("sessionId") or session_id),
        message_id=str(m.get("id") or ""),
        request_id=str(d.get("requestId") or ""),
        model=str(m.get("model") or "unknown"),
        input_tokens=_int(u.get("input_tokens")),
        cache_creation=_int(u.get("cache_creation_input_tokens")),
        cache_read=_int(u.get("cache_read_input_tokens")),
        output_tokens=_int(u.get("output_tokens")),
        sidechain=bool(d.get("isSidechain")),
    )


def project_dir_name(project_path: str) -> str:
    """Claude Code stores a project's transcripts in a folder named after its path."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(project_path))


@dataclass
class Totals:
    input_tokens: int = 0
    cache_creation: int = 0
    cache_read: int = 0
    output_tokens: int = 0
    turns: int = 0

    def add(self, e: UsageEvent) -> None:
        self.input_tokens += e.input_tokens
        self.cache_creation += e.cache_creation
        self.cache_read += e.cache_read
        self.output_tokens += e.output_tokens
        self.turns += 1

    @property
    def new_tokens(self) -> int:
        return self.input_tokens + self.cache_creation + self.output_tokens


@dataclass
class Snapshot:
    totals: Totals
    by_model: dict[str, Totals]
    context_now: int                  # context size of the most recent turn
    context_peak: int
    last_event_at: datetime | None
    first_event_at: datetime | None
    new_tokens_per_min: float         # recent burn rate of new work (excl. cache re-reads)
    output_tokens_per_min: float
    top_turns: list[UsageEvent]       # heaviest turns by new tokens
    sessions: int
    warnings: list[str] = field(default_factory=list)


class Aggregator:
    """Accumulates events with de-duplication; call snapshot() any time."""

    def __init__(self) -> None:
        self._events: dict[tuple[str, str], UsageEvent] = {}

    def add(self, e: UsageEvent) -> bool:
        """Add an event. Returns True if it changed state. Duplicate responses keep the larger output."""
        if not e.message_id and not e.request_id:
            # Cannot de-duplicate safely; key on timestamp + counts so repeats collapse.
            key = (f"anon:{e.ts.isoformat()}", f"{e.input_tokens}:{e.cache_read}:{e.output_tokens}")
        else:
            key = e.key
        old = self._events.get(key)
        if old is not None and old.output_tokens >= e.output_tokens:
            return False
        self._events[key] = e
        return True

    def __len__(self) -> int:
        return len(self._events)

    def events(self, include_sidechain: bool = True) -> list[UsageEvent]:
        """De-duplicated events in chronological order."""
        evs = sorted(self._events.values(), key=lambda e: e.ts)
        return evs if include_sidechain else [e for e in evs if not e.sidechain]

    def snapshot(self, now: datetime | None = None, window_min: float = 10.0,
                 include_sidechain: bool = True, top_n: int = 3) -> Snapshot:
        evs = sorted(self._events.values(), key=lambda e: e.ts)
        if not include_sidechain:
            evs = [e for e in evs if not e.sidechain]
        totals, by_model = Totals(), {}
        for e in evs:
            totals.add(e)
            by_model.setdefault(e.model, Totals()).add(e)
        now = now or (evs[-1].ts if evs else datetime.now(timezone.utc))
        recent = [e for e in evs if now - e.ts <= timedelta(minutes=window_min)]
        new_rate = out_rate = 0.0
        if recent:
            span = max((recent[-1].ts - recent[0].ts).total_seconds() / 60.0, 1.0)
            new_rate = sum(e.new_tokens for e in recent) / span
            out_rate = sum(e.output_tokens for e in recent) / span
        main = [e for e in evs if not e.sidechain] or evs
        warnings = []
        if any(not e.message_id and not e.request_id for e in evs):
            warnings.append("some records lack ids; de-duplication is approximate")
        return Snapshot(
            totals=totals,
            by_model=by_model,
            context_now=main[-1].context_tokens if main else 0,
            context_peak=max((e.context_tokens for e in main), default=0),
            last_event_at=evs[-1].ts if evs else None,
            first_event_at=evs[0].ts if evs else None,
            new_tokens_per_min=new_rate,
            output_tokens_per_min=out_rate,
            top_turns=sorted(evs, key=lambda e: e.new_tokens, reverse=True)[:top_n],
            sessions=len({e.session_id for e in evs}),
            warnings=warnings,
        )


class TranscriptTailer:
    """Incrementally reads appended lines of JSONL files (safe for partial lines and truncation)."""

    def __init__(self) -> None:
        self._offsets: dict[Path, int] = {}
        self._partial: dict[Path, bytes] = {}

    def read_new(self, path: Path) -> list[str]:
        try:
            size = path.stat().st_size
        except OSError:
            return []
        off = self._offsets.get(path, 0)
        if size < off:                      # file was truncated or replaced
            off, self._partial[path] = 0, b""
        if size == off:
            return []
        with open(path, "rb") as f:
            f.seek(off)
            chunk = f.read()
        self._offsets[path] = off + len(chunk)
        data = self._partial.get(path, b"") + chunk
        parts = data.split(b"\n")
        self._partial[path] = parts.pop()   # last element is an incomplete line (or empty)
        return [p.decode("utf-8", errors="replace").rstrip("\r") for p in parts if p.strip(b"\r")]


def find_transcripts(projects_root: Path, project_path: str | None = None) -> list[Path]:
    """Transcript files, newest first. With project_path, only that project's folder."""
    if not projects_root.is_dir():
        return []
    folders = [projects_root / project_dir_name(project_path)] if project_path else \
        [p for p in projects_root.iterdir() if p.is_dir()]
    files = [f for d in folders if d.is_dir() for f in d.glob("*.jsonl")]
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
