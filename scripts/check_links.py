#!/usr/bin/env python3
"""
Kiểm tra link tương đối trong các tệp Markdown của repo (Agent tra cứu tài liệu theo đường dẫn,
nên link hỏng = Agent lạc đường).

  python scripts/check_links.py            # kiểm tra toàn repo, exit 1 nếu có link hỏng
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "engine", "examples", "__pycache__"}
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:")


def tracked_markdown() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "*.md"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        files = [ROOT / line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        files = list(ROOT.rglob("*.md"))
    return [f for f in files if not (set(f.relative_to(ROOT).parts) & SKIP_DIRS) and f.exists()]


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
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
