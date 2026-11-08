"""Every tracked text file in the repository must be English (AGENTS.md rule 7, ADR-0014, ADR-0026).

Vietnamese is allowed only where it is the subject matter, never as the language of the repo itself:
language packs, detection patterns for Vietnamese content in scanned projects, and a few proper names.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Any letter carrying a Vietnamese diacritic.
VIETNAMESE = re.compile("[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.IGNORECASE)

# Words that are not Vietnamese text: proper names and the language's own name in a language selector.
ALLOWED_TOKENS = ("Diátaxis", "DIÁTAXIS", "Đỗ Khắc Gia Khoa", "Tiếng Việt")

# Files where Vietnamese is the intended content (reason in the comment).
ALLOWED_FILES = {
    "scripts/reviewer_shell/static/js/i18n.js",           # UI strings of the Vietnamese language pack (DICT.vi)
    "scripts/reviewer_shell/static/js/lang/vi.engine.js",  # Vietnamese language pack for engine text
    "scripts/token_monitor_cli.py",                       # the Vietnamese column of its language table
    "scripts/auditor_engine/safety.py",                   # prompt-injection phrases in Vietnamese (detection patterns)
    "scripts/auditor_engine/pillars_docs.py",             # README/agent-rule keywords in Vietnamese (detection patterns)
    "tests/test_safety_scan.py",                          # Vietnamese injection samples fed to the scanner
    "tests/test_engine_english.py",                       # contains the regex of Vietnamese letters it guards with
    "tests/test_repo_english.py",                         # this file
    "evals/results/raw/009-equivalence.json",             # Unicode sweep over the letters of the Vietnamese patterns
    ".githooks/pre-commit",                               # guard pattern for personal wording
    "scripts/auditor_engine/knowledge_pack.json",         # generated from document titles (follows knowledge-base)
    "MANIFEST.json",                                      # generated file list (follows knowledge-base)
}

# Translation still in progress (TASKS.md I3). This list must only ever shrink.
PENDING_PREFIXES = (
    "knowledge-base/",
    "examples/before-vibe-code/",
)

TEXT_SUFFIXES = {
    ".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".yml", ".yaml", ".txt", ".cs", ".csproj",
    ".sh", ".ps1", ".cjs", ".mjs", ".toml", ".mdc", ".xml", ".svg", ".cfg", ".ini", ".example", "",
}


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [f for f in out.decode("utf-8").split("\0") if f and (ROOT / f).exists()]  # skip files deleted but not yet staged


def vietnamese_lines(text: str) -> list[str]:
    hits = []
    for line in text.splitlines():
        cleaned = line
        for token in ALLOWED_TOKENS:
            cleaned = cleaned.replace(token, "")
        if VIETNAMESE.search(cleaned):
            hits.append(line.strip()[:100])
    return hits


def test_tracked_files_are_english():
    offenders: dict[str, list[str]] = {}
    for rel in tracked_files():
        if rel in ALLOWED_FILES or rel.startswith(PENDING_PREFIXES):
            continue
        path = ROOT / rel
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits = vietnamese_lines(text)
        if hits:
            offenders[rel] = hits
    assert not offenders, "Vietnamese text outside the allowed files:\n" + "\n".join(
        f"  {rel}: {len(h)} lines, e.g. {h[0]!r}" for rel, h in sorted(offenders.items())[:15])


def test_file_names_are_english():
    bad = [rel for rel in tracked_files() if VIETNAMESE.search(rel)]
    assert not bad, f"Vietnamese letters in tracked file names: {bad[:5]}"


def test_allowlists_do_not_hide_translated_files():
    """An allowed or pending file that no longer contains Vietnamese must leave the list, so the lists only shrink."""
    stale = []
    for rel in ALLOWED_FILES:
        path = ROOT / rel
        if not path.is_file() or rel in {"tests/test_repo_english.py", "tests/test_engine_english.py", ".githooks/pre-commit"}:
            continue
        if not vietnamese_lines(path.read_text(encoding="utf-8")) and rel not in {"MANIFEST.json", "scripts/auditor_engine/knowledge_pack.json"}:
            stale.append(rel)
    assert not stale, f"These files are listed as allowed but contain no Vietnamese; remove them: {stale}"
