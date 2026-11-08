"""ADR-0024: the Cloud/DevOps pillar applies only to projects that can be deployed."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auditor_engine.profiler import ProjectProfiler  # noqa: E402
from auditor_engine.tree import ProjectTree  # noqa: E402


def _write(root: Path, rel: str, content: str = "x\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _profile(root: Path) -> dict:
    return ProjectProfiler(root, ProjectTree(root)).profile()


CI = "name: ci\non: [push]\njobs: {}\n"
EXPRESS = json.dumps({"dependencies": {"express": "4.0.0"}})


def test_ci_only_docs_repo_has_no_cloud_pillar(tmp_path):
    _write(tmp_path, "README.md", "# docs\n")
    _write(tmp_path, ".github/workflows/ci.yml", CI)
    assert _profile(tmp_path)["has_cloud"] is False


def test_dockerfile_enables_cloud_pillar(tmp_path):
    _write(tmp_path, "README.md", "# docs\n")
    _write(tmp_path, "Dockerfile", "FROM scratch\n")
    assert _profile(tmp_path)["has_cloud"] is True


def test_compose_enables_cloud_pillar(tmp_path):
    _write(tmp_path, "README.md", "# docs\n")
    _write(tmp_path, "docker-compose.yml", "services: {}\n")
    assert _profile(tmp_path)["has_cloud"] is True


def test_kubernetes_manifests_enable_cloud_pillar(tmp_path):
    _write(tmp_path, "k8s/deployment.yaml", "kind: Deployment\n")
    assert _profile(tmp_path)["has_cloud"] is True


def test_ci_with_deployable_backend_keeps_cloud_pillar(tmp_path):
    _write(tmp_path, "package.json", EXPRESS)
    _write(tmp_path, ".github/workflows/ci.yml", CI)
    prof = _profile(tmp_path)
    assert prof["has_backend"] is True
    assert prof["has_cloud"] is True


def test_backend_without_ci_or_container_has_no_cloud_pillar(tmp_path):
    _write(tmp_path, "package.json", EXPRESS)
    assert _profile(tmp_path)["has_cloud"] is False
