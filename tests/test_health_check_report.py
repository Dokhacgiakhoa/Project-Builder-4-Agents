"""Kiểm thử Health Check: mã phát hiện, tài liệu khắc phục, Core Baseline, profile khai báo."""

import json
import re
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from auditor_engine import ProjectAuditor  # noqa: E402
from auditor_engine.baseline import check_baseline, check_declared_profile, declared_architecture  # noqa: E402
from auditor_engine.remediation import CODE_RULES, DOCS, VIOLATION_RULES, from_text, from_violation  # noqa: E402
from auditor_engine.safety import KINDS as SAFETY_KINDS  # noqa: E402


def simulate_bootstrap_step1(dest: Path):
    """Làm đúng Bước 1 của BOOTSTRAP.md: chép core/templates + core/standards."""
    templates = ROOT / "core" / "templates"
    shutil.copytree(templates, dest, dirs_exist_ok=True)
    (dest / ".gitignore").write_text((dest / "gitignore.tpl").read_text(encoding="utf-8"), encoding="utf-8")
    (dest / "gitignore.tpl").unlink()
    shutil.copytree(ROOT / "core" / "standards", dest / "docs" / "standards", dirs_exist_ok=True)


# ---- Tài liệu khắc phục phải có thật và nằm trong INDEX ----
def test_every_remediation_doc_exists_in_kit():
    for doc_id, (path, _title) in DOCS.items():
        assert (ROOT / path).is_file(), f"{doc_id} -> {path}"


def test_every_remediation_doc_is_listed_in_index_with_same_id():
    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    for doc_id, (path, _title) in DOCS.items():
        row = next((ln for ln in index.splitlines() if f"| {doc_id} |" in ln), None)
        assert row is not None, f"{doc_id} thiếu trong INDEX.md"
        assert f"({path})" in row, f"{doc_id}: đường dẫn trong INDEX khác DOCS"


def test_every_index_link_target_exists():
    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+)\)", index):
        if target.startswith("http"):
            continue
        assert (ROOT / target).exists(), target


def test_all_rules_reference_known_docs():
    from auditor_engine.remediation import TEXT_RULES
    for _p, _c, _s, docs in TEXT_RULES:
        assert all(d in DOCS for d in docs), docs
    for _code, _sev, docs in VIOLATION_RULES.values():
        assert all(d in DOCS for d in docs), docs
    for _sev, docs in CODE_RULES.values():
        assert all(d in DOCS for d in docs), docs


def test_every_safety_code_has_remediation_with_same_severity():
    for code, (sev, _title) in SAFETY_KINDS.items():
        assert code in CODE_RULES, f"{code} thiếu trong CODE_RULES"
        assert CODE_RULES[code][0] == sev, code


def test_arch_profile_and_guardrail_codes_have_remediation():
    for code in ("ARCH-007", "ARCH-008"):
        assert code in CODE_RULES, code


# ---- Phân loại phát hiện ----
def test_violation_maps_to_code_severity_and_location():
    f = from_violation({"file": "src/a.ts", "line": 7, "type": "HARDCODED SECRET IN CODE", "desc": "x"})
    assert (f.code, f.severity, f.location) == ("SEC-001", "Cao", "src/a.ts:7")


def test_unknown_text_falls_back_to_generic_and_summary_is_dropped():
    assert from_text("điều gì đó lạ").code == "GEN-001"
    assert from_text("Phát hiện 3 vị trí vi phạm tiêu chuẩn ANTI-CRASH trong mã nguồn.") is None


# ---- Core Baseline ----
def test_baseline_fails_on_empty_project(tmp_path):
    items = check_baseline(tmp_path)
    assert not any(i["ok"] for i in items)


def test_bootstrap_payload_satisfies_core_baseline_except_filled_items(tmp_path):
    simulate_bootstrap_step1(tmp_path)
    ok = {i["id"]: i["ok"] for i in check_baseline(tmp_path)}
    for must in ("B1", "B2", "B3", "B5", "B7", "B8", "B9"):
        assert ok[must], f"{must} phải đạt ngay sau Bước 1"
    # Chưa phỏng vấn/dựng CI nên các mục sau phải còn đỏ để Agent biết cần làm
    assert not ok["B4"] and not ok["B6"]


def test_baseline_b6_requires_ci_and_no_placeholders(tmp_path):
    simulate_bootstrap_step1(tmp_path)
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8").replace("{{", "(").replace("}}", ")")
    (tmp_path / "AGENTS.md").write_text(agents, encoding="utf-8")
    (tmp_path / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    assert {i["id"]: i["ok"] for i in check_baseline(tmp_path)}["B6"]


# ---- Profile khai báo ----
def test_declared_architecture_parsing(tmp_path):
    assert declared_architecture({"profiles": {"architecture": "Clean-Architecture"}}) == "clean-architecture"
    assert declared_architecture({"profiles": {"architecture": "{{ARCHITECTURE_PROFILE}}"}}) is None
    assert declared_architecture({}) is None


def test_declared_profile_mismatch_is_reported():
    ok, msg, doc = check_declared_profile(Path("."), {"src", "tests"}, "clean-architecture")
    assert not ok and "clean-architecture" in msg and doc == "A-002"
    ok, _msg, _doc = check_declared_profile(Path("."), {"domain", "application"}, "clean-architecture")
    assert ok
    assert check_declared_profile(Path("."), set(), "custom-thing")[0]  # profile tùy biến: không phạt


def test_broken_kit_json_does_not_crash_audit(tmp_path):
    (tmp_path / ".builder").mkdir()
    (tmp_path / ".builder" / "kit.json").write_text("{not json", encoding="utf-8")
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    assert auditor.generate_markdown_report(0).exists()


# ---- Báo cáo end-to-end ----
def test_report_contains_findings_with_docs_and_declared_profile(tmp_path):
    (tmp_path / ".builder").mkdir()
    (tmp_path / ".builder" / "kit.json").write_text(
        json.dumps({"kit_ref": "v1.2.3", "profiles": {"architecture": "clean-architecture"}}), encoding="utf-8")
    (tmp_path / "app.py").write_text("def f():\n    try:\n        1/0\n    except Exception: pass\n", encoding="utf-8")
    auditor = ProjectAuditor(tmp_path)
    report = auditor.generate_markdown_report(auditor.run()).read_text(encoding="utf-8")
    assert "declared_architecture: clean-architecture" in report
    assert "`AC-003`" in report and "app.py:4" in report
    assert "/blob/v1.2.3/core/standards/coding-conventions.md" in report   # ghim đúng phiên bản kit
    assert "ARCH-007" in report                                             # khai báo clean nhưng không có domain/application


def test_bootstrapped_project_scores_better_than_bare_project(tmp_path):
    bare = tmp_path / "bare"
    bare.mkdir()
    (bare / "README.md").write_text("# x\n", encoding="utf-8")
    built = tmp_path / "built"
    built.mkdir()
    (built / "README.md").write_text("# x\n", encoding="utf-8")
    simulate_bootstrap_step1(built)
    assert ProjectAuditor(built).run() > ProjectAuditor(bare).run()


def test_guardrails_arch008_detected_when_missing_boundary_or_ci(tmp_path):
    from auditor_engine.baseline import check_guardrails

    # 1. Khai báo M2 nhưng chưa có CI workflow -> báo ARCH-008
    cfg = {"guardrail_level": "M2", "profiles": {"architecture": "vertical-slice"}}
    ok, msg, docs = check_guardrails(tmp_path, cfg)
    assert not ok and "M2" in msg and "K-004" in docs

    # 2. Đã có CI workflow nhưng chưa có boundary lint/test -> vẫn báo ARCH-008
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    ok, msg, docs = check_guardrails(tmp_path, cfg)
    assert not ok and "ranh giới" in msg

    # 3. Khi có luật chặn import chéo (eslint-plugin-boundaries) -> đạt
    (tmp_path / "package.json").write_text('{"devDependencies": {"eslint-plugin-boundaries": "^4.0.0"}}', encoding="utf-8")
    ok, _msg, _docs = check_guardrails(tmp_path, cfg)
    assert ok


def test_serialize_report_data_contains_all_sections(tmp_path):
    simulate_bootstrap_step1(tmp_path)
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    data = auditor.serialize_report_data()
    assert "findings" in data and isinstance(data["findings"], list)
    assert "baseline" in data and len(data["baseline"]) == 9
    assert "safety" in data and "scanned" in data["safety"]
    assert "scope" in data and "entry_files" in data["scope"]
    assert "kit_config" in data and data["kit_config"]["present"] is True
