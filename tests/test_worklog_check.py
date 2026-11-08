"""Tests for the work log check (WLOG-001/002, core/standards/worklog.md)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auditor_engine import ProjectAuditor  # noqa: E402
from auditor_engine.baseline import check_worklog  # noqa: E402
from auditor_engine.remediation import CODE_RULES  # noqa: E402


def test_missing_worklog_is_wlog_001(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    code, msg = check_worklog(tmp_path)
    assert code == "WLOG-001" and "work log" in msg.lower()


def test_template_only_worklog_is_wlog_002(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "worklog.md").write_text(
        "# WORK LOG\n\n<!-- ## YYYY-MM-DD — Short title -->\n", encoding="utf-8")
    assert check_worklog(tmp_path)[0] == "WLOG-002"


def test_dated_heading_passes(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "worklog.md").write_text(
        "# WORK LOG\n\n## 2026-11-07 — First entry\n* Done: x\n", encoding="utf-8")
    assert check_worklog(tmp_path) == (None, "")


def test_alternative_locations_and_entry_styles(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    (tmp_path / "WORKLOG.md").write_text("- 2026-11-07 fixed bug\n", encoding="utf-8")
    assert check_worklog(tmp_path)[0] is None


def test_worklog_folder_counts(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    folder = tmp_path / "docs" / "worklog"
    folder.mkdir(parents=True)
    (folder / "2026-11.md").write_text("## 2026-11-07 entry\n", encoding="utf-8")
    assert check_worklog(tmp_path)[0] is None


def test_date_in_prose_does_not_count(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    (tmp_path / "WORKLOG.md").write_text("Last updated on 2026-11-07 by someone.\n", encoding="utf-8")
    assert check_worklog(tmp_path)[0] == "WLOG-002"


def test_project_without_agent_file_gets_no_wlog_finding(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')\n", encoding="utf-8")
    assert check_worklog(tmp_path) == (None, "")
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    codes = [f.code for f in auditor.collect_findings()]
    assert "WLOG-001" not in codes
    assert "WLOG-002" not in codes


def test_wlog_codes_have_remediation():
    for code in ("WLOG-001", "WLOG-002"):
        severity, docs = CODE_RULES[code]
        assert severity and "S-009" in docs


def test_audit_reports_wlog_finding_then_clears(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Test\n", encoding="utf-8")
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    codes = [f.code for f in auditor.collect_findings()]
    assert "WLOG-001" in codes

    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "worklog.md").write_text("## 2026-11-07 — start\n", encoding="utf-8")
    auditor2 = ProjectAuditor(tmp_path)
    auditor2.run()
    assert "WLOG-001" not in [f.code for f in auditor2.collect_findings()]
