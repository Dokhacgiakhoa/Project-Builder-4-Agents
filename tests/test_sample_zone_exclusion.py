"""Regression: sample code (examples/, starter/, fixtures/) must not distort the project profile."""

import json
import shutil
import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auditor_engine import ProjectAuditor  # noqa: E402
from auditor_engine.tree import ProjectTree  # noqa: E402
from auditor_engine.hygiene import git_tracked_files, check_tracked_files  # noqa: E402


def _write(root: Path, rel: str, content: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


REACT_PKG = json.dumps({"dependencies": {"react": "18.0.0"}})
needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="needs git")


def test_sample_zones_are_skipped(tmp_path):
    _write(tmp_path, "examples/app/package.json", REACT_PKG)
    _write(tmp_path, "profiles/frontend/starter/package.json", REACT_PKG)
    _write(tmp_path, "tests/fixtures/x/package.json", REACT_PKG)
    _write(tmp_path, "core/templates/package.json", REACT_PKG)
    tree = ProjectTree(tmp_path)
    assert tree.find_by_name("package.json") == []
    skipped = {rel for rel, _ in tree.skipped}
    assert {"examples", "profiles/frontend/starter", "core/templates"} <= skipped


def test_real_package_json_still_scanned(tmp_path):
    _write(tmp_path, "web/package.json", REACT_PKG)
    _write(tmp_path, "profiles/frontend/notes/package.json", REACT_PKG)
    tree = ProjectTree(tmp_path)
    assert len(tree.find_by_name("package.json")) == 2


def test_repo_with_only_sample_react_has_no_frontend(tmp_path):
    _write(tmp_path, "examples/app/package.json", REACT_PKG)
    _write(tmp_path, "README.md", "# demo")
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    assert auditor.profile.get("has_frontend") is False


@needs_git
def test_tracked_secret_in_sample_zone_is_still_flagged(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    _write(repo, "examples/.env", "API_KEY=k9F8m2L0pQ4vX7wZ1aB3cE5r\n")
    _write(repo, "src/main.py", "print('ok')\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A", "-f"], check=True)

    # 1. ProjectTree excludes examples from indexing
    tree = ProjectTree(repo)
    rel_files = {p.relative_to(repo).as_posix() for p in tree.all_files}
    assert "src/main.py" in rel_files
    assert "examples/.env" not in rel_files

    # 2. check_tracked_files uses git ls-files, so examples/.env is STILL flagged as SEC-005
    tracked = git_tracked_files(repo)
    findings = check_tracked_files(repo, tracked)
    sec_005 = [f for f in findings if f.code == "SEC-005"]
    assert len(sec_005) == 1
    assert "examples/.env" in sec_005[0].message
