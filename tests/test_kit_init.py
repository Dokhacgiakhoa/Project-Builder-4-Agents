"""Kiểm thử Kit Init Engine: khởi tạo dự án từ thư mục rỗng / đang làm dở."""

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from auditor_engine import ProjectAuditor  # noqa: E402
from kit_init import InitError, init_project  # noqa: E402
import init_project as cli  # noqa: E402


def test_init_empty_dir_creates_standard_skeleton(tmp_path):
    target = tmp_path / "my-app"
    result = init_project(target, "my-app")
    assert result.created and not result.overwritten and not result.skipped
    for rel in ["AGENTS.md", "adrs/0003-coding-conventions.md", "specs/product-vision.md",
                "README.md", "Makefile", ".github/workflows/ci.yml", "src/Domain/.gitkeep", "tests/.gitkeep"]:
        assert (target / rel).exists(), rel


def test_generated_files_are_project_specific(tmp_path):
    target = tmp_path / "x"
    init_project(target, "Cool App")
    assert (target / "README.md").read_text(encoding="utf-8").startswith("# Cool App")
    assert "Cool App" in (target / "specs/product-vision.md").read_text(encoding="utf-8").splitlines()[0]
    ci = (target / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "pytest" not in ci and "npm" not in ci          # không rò CI của Starter Kit
    makefile = (target / "Makefile").read_text(encoding="utf-8")
    assert "\ttest" not in makefile and "build-exe" not in makefile
    assert "\t@if [ ! -f .env ]" in makefile              # dùng tab thật


def test_kit_only_files_are_not_copied(tmp_path):
    target = tmp_path / "x"
    init_project(target, "x", frontend=True)
    for rel in ["scripts", "tools", "examples", "knowledge-base", "LICENSE", "PLAN.md", "Project-Review.exe"]:
        assert not (target / rel).exists(), rel
    assert not list(target.rglob("node_modules"))
    assert (target / "frontend/package.json").exists()


def test_non_empty_dir_is_rejected_without_flag(tmp_path):
    (tmp_path / "keep.txt").write_text("mine")
    with pytest.raises(InitError):
        init_project(tmp_path, "x")


def test_merge_never_overwrites_existing_files(tmp_path):
    (tmp_path / "README.md").write_text("MY README", encoding="utf-8")
    result = init_project(tmp_path, "x", merge=True)
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "MY README"
    assert "README.md" in result.skipped
    assert (tmp_path / "AGENTS.md").exists()


def test_force_overwrites(tmp_path):
    (tmp_path / "README.md").write_text("MY README", encoding="utf-8")
    result = init_project(tmp_path, "x", force=True)
    assert "README.md" in result.overwritten
    assert (tmp_path / "README.md").read_text(encoding="utf-8").startswith("# x")


def test_dry_run_writes_nothing(tmp_path):
    target = tmp_path / "x"
    result = init_project(target, "x", dry_run=True)
    assert result.created and not target.exists()


@pytest.mark.parametrize("bad", ["   ", "a/b", "a<b", "x" * 101])
def test_invalid_project_name(tmp_path, bad):
    with pytest.raises(InitError):
        init_project(tmp_path / "x", bad)


def test_target_is_a_file(tmp_path):
    f = tmp_path / "file"
    f.write_text("x")
    with pytest.raises(InitError):
        init_project(f, "x")


def test_cli_returns_error_code_on_non_empty(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("x")
    assert cli.main([str(tmp_path)]) == 1
    assert "--merge" in capsys.readouterr().err


def test_fresh_project_passes_auditor_with_good_grade(tmp_path):
    target = tmp_path / "x"
    init_project(target, "x")
    auditor = ProjectAuditor(target)
    assert auditor.run() >= 70
