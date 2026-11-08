#!/usr/bin/env python3
"""
Automatically generates MANIFEST.json at the repo root.
Lists the whole tree of valuable files in the repo with raw download paths (raw.githubusercontent.com).
Lets a remote AI Agent read and fetch each file exactly, without git clone or HTML scraping.

Usage:
    python scripts/generate_manifest.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPO_URL = "https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents"
RAW_BASE = "https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-4-Agents/main"

SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "bin",
    "obj",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    ".idea",
    ".venv",
    "venv",
    "coverage",
    ".mypy_cache",
}

SKIP_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "package-lock.json",
}


def categorize_file(rel_path: str) -> str:
    if rel_path in ("README.md", "BOOTSTRAP.md", "INDEX.md", "AGENTS.md", "HOW_IT_WORKS.md", "llms.txt"):
        return "root"
    if rel_path.startswith("core/"):
        return "core"
    if rel_path.startswith("profiles/"):
        return "profiles"
    if rel_path.startswith("knowledge-base/"):
        return "knowledge-base"
    if rel_path.startswith("scripts/"):
        return "scripts"
    if rel_path.startswith("adrs/"):
        return "adrs"
    return "other"


def list_repo_files():
    """File list that is stable between the dev machine and CI: prefer `git ls-files`, otherwise walk the folders."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            capture_output=True, check=True, text=True, encoding="utf-8",
        ).stdout
        files = [f for f in out.split(chr(0)) if f]
        if files:
            return sorted(files)
    except (OSError, subprocess.CalledProcessError):
        pass
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git")]
        for f in filenames:
            found.append((Path(dirpath) / f).relative_to(ROOT).as_posix())
    return sorted(found)


def generate():
    manifest_files = {}

    for rel_path in list_repo_files():
        parts = rel_path.split("/")
        if any(d in SKIP_DIRS or d.startswith(".git") for d in parts[:-1]):
            continue
        if parts[-1] in SKIP_FILES:
            continue

        full_path = ROOT / rel_path
        if not full_path.is_file():
            continue

        # Do not put MANIFEST.json itself in its own list
        if rel_path == "MANIFEST.json":
            continue

        category = categorize_file(rel_path)
        raw_url = f"{RAW_BASE}/{rel_path}"

        manifest_files[rel_path] = {
            "raw_url": raw_url,
            "category": category,
            "size_bytes": full_path.stat().st_size,
        }

    manifest = {
        "kit": "Project-Builder-4-Agents",
        "description": "Remote knowledge library and bootstrap procedure for AI Coding Agents",
        "repo": REPO_URL,
        "raw_base": RAW_BASE,
        "entry_points": {
            "bootstrap": f"{RAW_BASE}/BOOTSTRAP.md",
            "index": f"{RAW_BASE}/INDEX.md",
            "how_it_works": f"{RAW_BASE}/HOW_IT_WORKS.md",
            "llms_txt": f"{RAW_BASE}/llms.txt",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(manifest_files),
        "files": manifest_files,
    }

    out_file = ROOT / "MANIFEST.json"
    out_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Generated {out_file.name}: {len(manifest_files)} files indexed.")


if __name__ == "__main__":
    generate()
