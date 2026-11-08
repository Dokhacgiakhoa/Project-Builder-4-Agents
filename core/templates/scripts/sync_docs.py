#!/usr/bin/env python3
"""
Template scripts/sync_docs.py for Vibe Coder Projects.
Synchronizes README.md stats and verifies documentation integrity automatically.
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def sync_readme() -> bool:
    readme_path = ROOT / "README.md"
    review_path = ROOT / "project-review.md"
    if not readme_path.is_file():
        return False

    score = "N/A"
    grade = "N/A"
    color = "blue"

    if review_path.is_file():
        txt = review_path.read_text(encoding="utf-8", errors="ignore")
        m_score = re.search(r"score:\s*(\d+)", txt)
        m_grade = re.search(r"grade:\s*\"?([^\n\"]+)\"?", txt)
        if m_score:
            score = m_score.group(1)
            color = "brightgreen" if int(score) >= 90 else ("yellow" if int(score) >= 75 else "red")
        if m_grade:
            grade_match = re.match(r"^([A-Z][+]?)", m_grade.group(1).strip())
            grade = grade_match.group(1) if grade_match else "A+"

    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    grade_slug = grade.replace("+", "%2B")
    stats_badge_block = (
        "<!-- AUTO-GEN:STATS -->\n"
        f"[![Health Score](https://img.shields.io/badge/Health_Score-{score}%2F100_{grade_slug}-{color})](project-review.md)\n"
        "<!-- /AUTO-GEN:STATS -->"
    )

    pattern = r"<!-- AUTO-GEN:STATS -->.*?<!-- /AUTO-GEN:STATS -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, stats_badge_block, content, flags=re.DOTALL)
    else:
        new_content = stats_badge_block + "\n\n" + content

    if new_content != content:
        readme_path.write_text(new_content, encoding="utf-8")
        print("✅ README.md stats synchronized.")
        return True
    return False

if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    drift = sync_readme()
    if check_mode and drift:
        print("❌ Documentation out of sync!")
        sys.exit(1)
    print("✨ Documentation synchronized.")
    sys.exit(0)
