#!/usr/bin/env python3
"""
Check relative links in the repo's Markdown files (Agents look up documents by path,
so a broken link means a lost Agent).

  python scripts/check_links.py            # check links + document format, exit 1 on any error

Document format (applies only to core/ and profiles/, except core/templates and frontend/starter):
  * frontmatter has id, type (decision|router|playbook|reference), when
  * id and path match a row in INDEX.md
  * type=decision: also has not_when, all mandatory sections, at most DECISION_MAX_LINES lines
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "engine", "examples", "__pycache__"}
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:")

GOVERNED_ROOTS = ("core/", "profiles/")
GOVERNED_EXCLUDES = ("core/templates/", "profiles/frontend/starter/")
DOC_TYPES = {"decision", "router", "playbook", "reference"}
DECISION_SECTION_ALIASES = (
    ("when to choose",),
    ("when not to choose", "not when"),
    ("target directory", "target structure", "target folder"),
    ("constraints",),
    ("adding a feature", "how to add a feature"),
    ("common mistakes", "common errors"),
)
DECISION_MAX_LINES = 120
INDEX_ROW = re.compile(r"^\| ([A-Z]-\d{3}) \| [CPL] \| .*? \| \[[^\]]*\]\(([^)]+)\) \|\s*$", re.M)


def tracked_markdown() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "*.md"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        files = [ROOT / line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        files = list(ROOT.rglob("*.md"))
    return [f for f in files if not (set(f.relative_to(ROOT).parts) & SKIP_DIRS) and f.exists()]


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip().strip('"')
    return None


def index_entries(root: Path = ROOT) -> dict[str, str]:
    """path -> id, read from INDEX.md."""
    text = (root / "INDEX.md").read_text(encoding="utf-8")
    return {m.group(2): m.group(1) for m in INDEX_ROW.finditer(text)}


def governed_docs(root: Path = ROOT) -> list[Path]:
    docs = []
    for md in tracked_markdown():
        rel = md.relative_to(root).as_posix()
        if rel.startswith(GOVERNED_ROOTS) and not rel.startswith(GOVERNED_EXCLUDES):
            docs.append(md)
    return docs


def check_doc_format(root: Path = ROOT, docs: list[Path] | None = None) -> list[str]:
    """Return the list of document format errors (empty if fine)."""
    errors = []
    entries = index_entries(root)
    for md in (docs if docs is not None else governed_docs(root)):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None:
            errors.append(f"{rel}: missing frontmatter (id, type, when)")
            continue
        for key in ("id", "type", "when"):
            if not meta.get(key):
                errors.append(f"{rel}: frontmatter missing '{key}'")
        if meta.get("type") and meta["type"] not in DOC_TYPES:
            errors.append(f"{rel}: invalid type '{meta['type']}' ({'|'.join(sorted(DOC_TYPES))})")
        indexed_id = entries.get(rel)
        if indexed_id is None:
            errors.append(f"{rel}: no row in INDEX.md yet")
        elif meta.get("id") and meta["id"] != indexed_id:
            errors.append(f"{rel}: id '{meta['id']}' differs from INDEX.md ('{indexed_id}')")
        if meta.get("type") == "decision":
            if not meta.get("not_when"):
                errors.append(f"{rel}: type=decision is missing 'not_when'")
            headings = [re.sub(r"^[#\s\d.]+", "", h).strip().lower() for h in re.findall(r"^##\s+(.+)$", text, re.M)]
            for aliases in DECISION_SECTION_ALIASES:
                if not any(any(h.startswith(alias) for alias in aliases) for h in headings):
                    errors.append(f"{rel}: missing section '## {' / '.join(aliases[:2])}'")
            if len(text.splitlines()) > DECISION_MAX_LINES:
                errors.append(f"{rel}: longer than {DECISION_MAX_LINES} lines (decision documents must be short)")
    return errors


def main() -> int:
    broken = []
    for md in tracked_markdown():
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        in_code = False
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for target in LINK.findall(line):
                if target.startswith(SKIP_PREFIXES):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                resolved = (ROOT / path.lstrip("/")) if path.startswith("/") else (md.parent / path)
                if not resolved.exists():
                    broken.append(f"{md.relative_to(ROOT).as_posix()}:{lineno}: {target}")
    for item in broken:
        print("BROKEN", item)
    print(f"{len(broken)} broken links.")
    format_errors = check_doc_format()
    for item in format_errors:
        print("BADFORMAT", item)
    print(f"{len(format_errors)} document format errors.")
    return 1 if (broken or format_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
