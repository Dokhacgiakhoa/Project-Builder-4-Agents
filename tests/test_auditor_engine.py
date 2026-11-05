"""Kiểm thử Core Engine (auditor_engine) ở chế độ headless, không phụ thuộc UI."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auditor_engine import ProjectAuditor, ProjectTree  # noqa: E402
from auditor_engine.constants import IGNORE_DIRS  # noqa: E402


@pytest.fixture()
def sample_project(tmp_path):
    (tmp_path / "README.md").write_text("# Demo\n\n## Quick Start\nrun it\n", encoding="utf-8")
    (tmp_path / "app.py").write_text(
        "def f():\n    try:\n        1/0\n    except Exception: pass\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "junk.js").write_text("x", encoding="utf-8")
    return tmp_path


def test_tree_prunes_ignored_dirs(sample_project):
    tree = ProjectTree(sample_project)
    names = {p.name for p in tree.all_files}
    assert "app.py" in names
    assert "junk.js" not in names
    assert "node_modules" in IGNORE_DIRS


def test_auditor_scores_within_bounds_and_writes_report(sample_project):
    auditor = ProjectAuditor(sample_project)
    score = auditor.run()
    assert 0 <= score <= 100
    assert auditor.get_letter_grade(score)
    report = auditor.generate_markdown_report(score)
    assert report.exists()
    assert report.name == "project-review.md"
    text = report.read_text(encoding="utf-8")
    assert text.startswith("---") and "report: project-review" in text.splitlines()[1]
    assert "## 2. Phát hiện cần xử lý" in text


def test_auditor_detects_silent_exception_eater(sample_project):
    auditor = ProjectAuditor(sample_project)
    auditor.run()
    types = " ".join(str(v.get("type")) for v in auditor.violations)
    assert "SILENT EXCEPTION" in types.upper()


def test_auditor_handles_empty_project(tmp_path):
    auditor = ProjectAuditor(tmp_path)
    score = auditor.run()
    assert isinstance(score, (int, float))
    assert auditor.get_ai_prompt()
