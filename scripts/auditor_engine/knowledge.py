"""Knowledge Pack: a versioned snapshot of kit knowledge for offline comparison (ADR-0018).

Load order: the user's cache update if newer, otherwise the pack bundled with the engine.
The online update only runs when `update_pack()` is called explicitly; it never breaks an offline scan.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

PACK_NAME = "knowledge_pack.json"
CACHE_FILE = Path.home() / ".starter-kit" / "knowledge" / PACK_NAME
RAW_URL = ("https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/{ref}/"
           "scripts/auditor_engine/" + PACK_NAME)
SUPPORTED_SCHEMA = 1


def _bundled_paths() -> list[Path]:
    paths = [Path(__file__).with_name(PACK_NAME)]
    base = getattr(sys, "_MEIPASS", None)
    if base:
        paths.append(Path(base) / "auditor_engine" / PACK_NAME)
    return paths


def _valid(pack) -> bool:
    return (isinstance(pack, dict) and pack.get("schema") == SUPPORTED_SCHEMA
            and isinstance(pack.get("docs"), list) and all(isinstance(d, dict) and d.get("id") for d in pack["docs"]))


def _read(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if _valid(data) else None
    except (OSError, ValueError):
        return None


def load_pack(cache_file: Path | None = None) -> dict:
    """Return the pack with `source` ('bundled' | 'cache' | 'empty'). Never raises."""
    candidates = []
    for p in _bundled_paths():
        data = _read(p)
        if data:
            candidates.append(("bundled", data))
            break
    cached = _read(cache_file or CACHE_FILE)
    if cached:
        candidates.append(("cache", cached))
    if not candidates:
        return {"schema": SUPPORTED_SCHEMA, "docs": [], "source": "empty", "generated": ""}
    source, pack = max(candidates, key=lambda c: c[1].get("generated", ""))
    return {**pack, "source": source}


def update_pack(ref: str = "main", timeout: int = 8, cache_file: Path | None = None) -> dict:
    """Download a new pack from GitHub (needs network). Returns {'ok', 'message', 'generated'}; network errors are reported, not raised."""
    url = RAW_URL.format(ref=ref)
    if not url.startswith("https://raw.githubusercontent.com/"):
        return {"ok": False, "message": 'Invalid URL.', "generated": ""}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Project-Health-Check"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read(2_000_000).decode("utf-8"))
    except Exception as e:  # network/broken JSON: keep the existing pack
        return {"ok": False, "message": f"Could not update kit knowledge ({e}). Using the existing copy.", "generated": ""}
    if not _valid(data):
        return {"ok": False, "message": 'The downloaded pack is invalid; keeping the current one.', "generated": ""}
    target = cache_file or CACHE_FILE
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except OSError as e:
        return {"ok": False, "message": f"Could not save the cache ({e}).", "generated": data.get("generated", "")}
    return {"ok": True, "message": f"Kit knowledge updated ({len(data['docs'])} documents).",
            "generated": data.get("generated", "")}


def doc_by_id(pack: dict, doc_id: str) -> dict | None:
    return next((d for d in pack.get("docs", []) if d.get("id") == doc_id), None)


def profile_docs(pack: dict) -> dict[str, dict]:
    """slug -> architecture profile document (type: decision)."""
    return {d["slug"]: d for d in pack.get("docs", []) if d.get("slug")}
