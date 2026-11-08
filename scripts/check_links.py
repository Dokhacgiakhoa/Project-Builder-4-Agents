#!/usr/bin/env python3
"""
Kiểm tra link tương đối trong các tệp Markdown của repo (Agent tra cứu tài liệu theo đường dẫn,
nên link hỏng = Agent lạc đường).

  python scripts/check_links.py            # kiểm tra link + khuôn tài liệu, exit 1 nếu có lỗi

Khuôn tài liệu (chỉ áp cho core/ và profiles/, trừ core/templates và frontend/starter):
  * frontmatter có id, type (decision|router|playbook|reference), when
  * id và đường dẫn khớp một dòng trong INDEX.md
  * type=decision: có thêm not_when, đủ các mục bắt buộc, tối đa DECISION_MAX_LINES dòng
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
    ("khi nào chọn", "when to choose"),
    ("không chọn khi", "when not to choose", "not when"),
    ("thư mục mục tiêu", "target directory", "target structure", "target folder"),
    ("ràng buộc", "constraints"),
    ("thêm một tính năng", "adding a feature", "how to add a feature"),
    ("lỗi thường gặp", "common mistakes", "common errors"),
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
    """path -> id, đọc từ INDEX.md."""
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
    """Trả về danh sách lỗi khuôn tài liệu (rỗng nếu ổn)."""
    errors = []
    entries = index_entries(root)
    for md in (docs if docs is not None else governed_docs(root)):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None:
            errors.append(f"{rel}: thiếu frontmatter (id, type, when)")
            continue
        for key in ("id", "type", "when"):
            if not meta.get(key):
                errors.append(f"{rel}: frontmatter thiếu '{key}'")
        if meta.get("type") and meta["type"] not in DOC_TYPES:
            errors.append(f"{rel}: type '{meta['type']}' không hợp lệ ({'|'.join(sorted(DOC_TYPES))})")
        indexed_id = entries.get(rel)
        if indexed_id is None:
            errors.append(f"{rel}: chưa có dòng trong INDEX.md")
        elif meta.get("id") and meta["id"] != indexed_id:
            errors.append(f"{rel}: id '{meta['id']}' khác INDEX.md ('{indexed_id}')")
        if meta.get("type") == "decision":
            if not meta.get("not_when"):
                errors.append(f"{rel}: type=decision thiếu 'not_when'")
            headings = [re.sub(r"^[#\s\d.]+", "", h).strip().lower() for h in re.findall(r"^##\s+(.+)$", text, re.M)]
            for aliases in DECISION_SECTION_ALIASES:
                if not any(any(h.startswith(alias) for alias in aliases) for h in headings):
                    errors.append(f"{rel}: thiếu mục '## {aliases[0]} / {aliases[1]}'")
            if len(text.splitlines()) > DECISION_MAX_LINES:
                errors.append(f"{rel}: dài quá {DECISION_MAX_LINES} dòng (tài liệu quyết định phải ngắn)")
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
    print(f"{len(broken)} link hỏng.")
    format_errors = check_doc_format()
    for item in format_errors:
        print("BADFORMAT", item)
    print(f"{len(format_errors)} lỗi khuôn tài liệu.")
    return 1 if (broken or format_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
