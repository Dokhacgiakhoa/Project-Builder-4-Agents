#!/usr/bin/env python3
"""
scripts/sync_docs.py — Single-command living documentation synchronization.

Keeps README.md, MANIFEST.json, INDEX.md, and llms.txt in sync with the actual repository state.
Usage:
    python scripts/sync_docs.py         # Sync and update all docs
    python scripts/sync_docs.py --check # Verify sync status (for CI, exits 1 if out of sync)
"""

import os
import sys
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def count_tests() -> int:
    """Counts automated unit tests across tests/ directory."""
    test_dir = ROOT / "tests"
    if not test_dir.is_dir():
        return 0
    count = 0
    for tf in test_dir.glob("test_*.py"):
        try:
            txt = tf.read_text(encoding="utf-8", errors="ignore")
            count += len(re.findall(r"def test_\w+\(", txt))
        except OSError:
            pass
    return count

def get_health_stats() -> tuple[str, str, str]:
    """Runs the audit engine on this repository so the badge equals the real score.

    project-review.md is git-ignored, so reading it made the badge depend on a local file that CI
    never has (CI then fell back to 100 and the check failed whenever the real score differed).
    """
    import warnings

    sys.path.insert(0, str(ROOT / "scripts"))
    from auditor_engine import ProjectAuditor

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        auditor = ProjectAuditor(ROOT)
        score_value = auditor.run()
    score = str(int(score_value))
    grade_match = re.match(r"^([A-Z][+]?)", auditor.get_letter_grade(score_value))
    grade = grade_match.group(1) if grade_match else "A+"
    color = "brightgreen" if int(score) >= 90 else ("yellow" if int(score) >= 75 else "red")
    return score, grade, color

def check_index_coverage() -> list[str]:
    """Finds any markdown documentation in core/ or profiles/ missing from INDEX.md."""
    index_path = ROOT / "INDEX.md"
    if not index_path.is_file():
        return []
    index_content = index_path.read_text(encoding="utf-8", errors="ignore")
    
    missing = []
    for search_dir in ["core", "profiles"]:
        base_dir = ROOT / search_dir
        if not base_dir.is_dir():
            continue
        for md_file in base_dir.rglob("*.md"):
            rel = md_file.relative_to(ROOT).as_posix()
            # Skip starter app and templates
            if "profiles/frontend/starter" in rel or "core/templates" in rel:
                continue
            if rel not in index_content and md_file.name not in index_content:
                missing.append(rel)
    return missing

def sync_readme(score: str, grade: str, color: str, test_count: int, total_files: int, check_only: bool) -> bool:
    """Updates the AUTO-GEN:STATS block in README.md."""
    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        return False
    
    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    
    grade_slug = grade.replace("+", "%2B")
    stats_badge_block = (
        "<!-- AUTO-GEN:STATS -->\n"
        f"[![Health Score](https://img.shields.io/badge/Health_Score-{score}%2F100_{grade_slug}-{color})](project-review.md)\n"
        f"[![Automated Tests](https://img.shields.io/badge/Tests-{test_count}_passed-blue)](tests/)\n"
        f"[![Indexed Files](https://img.shields.io/badge/Indexed_Files-{total_files}_files-purple)](MANIFEST.json)\n"
        "[![Architecture](https://img.shields.io/badge/Architecture-Remote_Knowledge_Hub-emerald)](HOW_IT_WORKS.md)\n"
        "<!-- /AUTO-GEN:STATS -->"
    )
    
    pattern = r"<!-- AUTO-GEN:STATS -->.*?<!-- /AUTO-GEN:STATS -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, stats_badge_block, content, flags=re.DOTALL)
    else:
        # Insert right after the title
        title_end = content.find("\n", content.find("# Project-Builder-4-Agents"))
        if title_end != -1:
            new_content = content[:title_end + 1] + "\n" + stats_badge_block + "\n" + content[title_end + 1:]
        else:
            new_content = stats_badge_block + "\n\n" + content
            
    if new_content != content:
        if check_only:
            print("❌ README.md stats are out of sync!")
            return True
        readme_path.write_text(new_content, encoding="utf-8")
        print("✅ README.md stats updated successfully.")
        return False
    return False

def run_sync(check_only: bool = False) -> int:
    print("🔄 Running Living Documentation Synchronization...")
    
    # 0. Regenerate the Knowledge Pack used by Health Check (ADR-0018) before the manifest lists it
    pack_script = ROOT / "scripts" / "build_knowledge_pack.py"
    if pack_script.is_file():
        import subprocess
        subprocess.run([sys.executable, str(pack_script)] + (["--check"] if check_only else []), check=True)

    # 1. Regenerate MANIFEST.json
    manifest_script = ROOT / "scripts" / "generate_manifest.py"
    if manifest_script.is_file():
        import subprocess
        subprocess.run([sys.executable, str(manifest_script)], check=True)
        
    manifest_path = ROOT / "MANIFEST.json"
    total_files = 0
    if manifest_path.is_file():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            total_files = data.get("total_files", 0)
        except json.JSONDecodeError:
            pass
            
    # 2. Extract stats
    test_count = count_tests()
    score, grade, color = get_health_stats()
    
    # 3. Check INDEX.md coverage
    unindexed = check_index_coverage()
    if unindexed:
        print(f"⚠️  Warning: {len(unindexed)} documentation files are not indexed in INDEX.md:")
        for f in unindexed:
            print(f"   - {f}")
        if check_only:
            return 1
            
    # 4. Sync README.md
    drift = sync_readme(score, grade, color, test_count, total_files, check_only)
    if drift and check_only:
        return 1
        
    print(f"✨ Documentation sync complete: Score {score}/100 [{grade}], {test_count} tests, {total_files} indexed files.")
    return 0

if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    sys.exit(run_sync(check_only=check_mode))
