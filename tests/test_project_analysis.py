"""Tests for the Project Model, Knowledge Pack, conclusions and the AI layer (ADR-0018)."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from auditor_engine import ProjectAuditor  # noqa: E402
from auditor_engine import knowledge  # noqa: E402
from auditor_engine.analysis import analyze_project  # noqa: E402
from auditor_engine.insights import build_insights  # noqa: E402
from auditor_engine.tree import ProjectTree  # noqa: E402
from reviewer_shell import llm_evaluator  # noqa: E402
from reviewer_shell import settings_manager as sm  # noqa: E402


def write(root: Path, rel: str, content: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def model_of(root: Path) -> dict:
    return analyze_project(root, ProjectTree(root))


def pack():
    return knowledge.load_pack(cache_file=Path("nonexistent-cache.json"))


def test_language_comes_from_code_not_from_one_manifest(tmp_path):
    for i in range(5):
        write(tmp_path, f"app/mod{i}.py", "x = 1\n" * 40)
    write(tmp_path, "shell/App.csproj", '<Project Sdk="Microsoft.NET.Sdk"><UseWindowsForms>true</UseWindowsForms></Project>')
    write(tmp_path, "shell/Program.cs", "using System;\nclass P { static void Main() {} }\n")
    m = model_of(tmp_path)
    assert m["primary_language"] == "Python"
    auditor = ProjectAuditor(tmp_path)
    auditor.run()
    assert auditor.profile["has_backend"] is False
    assert auditor.profile["languages"][0] == "Python"


def test_python_import_graph_and_cycle(tmp_path):
    write(tmp_path, "src/alpha/__init__.py", "")
    write(tmp_path, "src/alpha/a.py", "import beta\n" + "x = 1\n" * 10)
    write(tmp_path, "src/beta/__init__.py", "")
    write(tmp_path, "src/beta/b.py", "import alpha\n" + "y = 1\n" * 10)
    write(tmp_path, "src/gamma/g.py", "import alpha\nimport requests\n")
    m = model_of(tmp_path)
    edges = {(e["from"], e["to"]) for e in m["edges"]}
    assert ("src/alpha", "src/beta") in edges and ("src/beta", "src/alpha") in edges
    assert any(set(c) == {"src/alpha", "src/beta"} for c in m["cycles"])
    assert any(e["name"] == "requests" for e in m["externals"])
    ins = build_insights(m, pack())
    assert any(b["key"] == "cycle" for b in ins["bottlenecks"])


def test_js_imports_detect_frameworks_and_edges(tmp_path):
    write(tmp_path, "web/package.json", json.dumps({"dependencies": {"react": "18"}}))
    write(tmp_path, "web/src/pages/Home.tsx", "import React from 'react';\nimport { api } from '../services/api';\n")
    write(tmp_path, "web/src/services/api.ts", "import axios from 'axios';\nexport const api = axios;\n")
    m = model_of(tmp_path)
    names = {s["name"] for s in m["stack"]}
    assert {"React", "axios"} <= names
    assert m["primary_language"] == "TypeScript"


def test_layer_violation_is_reported_as_high(tmp_path):
    write(tmp_path, "src/domain/entity.py", "import infrastructure\n" + "a = 1\n" * 20)
    write(tmp_path, "src/infrastructure/repo.py", "import domain\n" + "b = 1\n" * 20)
    write(tmp_path, "src/application/use.py", "import domain\nimport infrastructure\n")
    m = model_of(tmp_path)
    ins = build_insights(m, pack())
    layer = [b for b in ins["bottlenecks"] if b["key"] == "layer"]
    assert layer and layer[0]["severity"] == "High"
    assert any("domain" in e for e in layer[0]["evidence"])


def test_missing_tests_on_real_code_is_high(tmp_path):
    for i in range(4):
        write(tmp_path, f"core/m{i}.py", "v = 1\n" * 100)
    ins = build_insights(model_of(tmp_path), pack())
    t = [b for b in ins["bottlenecks"] if b["key"] == "tests"]
    assert t and t[0]["severity"] == "High"


def test_docs_only_repo_has_no_architecture_profile(tmp_path):
    write(tmp_path, "README.md", "# Doc\n" + "line\n" * 50)
    m = model_of(tmp_path)
    assert m["kind"]["id"] == "docs-knowledge"
    assert build_insights(m, pack())["profile"]["slug"] is None


def test_custom_declared_profile_is_not_flagged(tmp_path):
    for i in range(3):
        write(tmp_path, f"core/m{i}.py", "v = 1\n" * 100)
    ins = build_insights(model_of(tmp_path), pack(), declared_arch="agent-brain-and-toolkit")
    assert not any(b["key"] == "profile" for b in ins["bottlenecks"])


def test_report_contains_analysis_section(tmp_path):
    for i in range(3):
        write(tmp_path, f"core/m{i}.py", "v = 1\n" * 100)
    a = ProjectAuditor(tmp_path)
    a.run()
    text = a.report_path.read_text(encoding="utf-8")
    assert "## 1.1 Project analysis" in text and "Python" in text
    data = a.serialize_report_data()
    assert data["analysis"]["languages"] and data["insights"]["summary"]


def test_sample_react_app_does_not_make_python_project_frontend(tmp_path):
    for i in range(3):
        write(tmp_path, f"core/m{i}.py", "v = 1\n" * 100)
    write(tmp_path, "examples/demo/package.json", json.dumps({"dependencies": {"react": "18"}}))
    write(tmp_path, "examples/demo/src/App.tsx", "import React from 'react';\n" * 30)
    m = model_of(tmp_path)
    assert "React" not in {s["name"] for s in m["stack"]}
    assert m["primary_language"] == "Python"


# ------------------------------------------------------------------ Knowledge Pack
def test_bundled_pack_loads_and_has_architecture_profiles():
    p = knowledge.load_pack(cache_file=Path("nonexistent-cache.json"))
    assert p["source"] == "bundled" and p["docs"]
    assert {"simple-layered", "clean-architecture", "vertical-slice", "modular-monolith"} <= set(knowledge.profile_docs(p))


def test_pack_is_in_sync_with_kit_docs():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_knowledge_pack.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_newer_cache_wins_and_bad_cache_is_ignored(tmp_path):
    base = knowledge.load_pack(cache_file=tmp_path / "none.json")
    newer = {**{k: v for k, v in base.items() if k != "source"}, "generated": "2999-01-01"}
    cache = tmp_path / "pack.json"
    cache.write_text(json.dumps(newer), encoding="utf-8")
    assert knowledge.load_pack(cache_file=cache)["source"] == "cache"
    cache.write_text("{broken", encoding="utf-8")
    assert knowledge.load_pack(cache_file=cache)["source"] == "bundled"


def test_update_pack_offline_does_not_raise(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise OSError("no network")
    monkeypatch.setattr(knowledge.urllib.request, "urlopen", boom)
    r = knowledge.update_pack(cache_file=tmp_path / "pack.json")
    assert r["ok"] is False and "existing" in r["message"]
    assert not (tmp_path / "pack.json").exists()


# ------------------------------------------------------------------ AI layer
def test_mask_secrets():
    text = 'API_KEY = "abcdef123456"\nkey=sk-abcdefghijklmnopqrstuvwxyz\n-----BEGIN RSA PRIVATE KEY-----\nxx\n-----END RSA PRIVATE KEY-----'
    out = llm_evaluator.mask_secrets(text)
    assert "abcdef123456" not in out and "sk-abcdefghijkl" not in out and "xx" not in out


def test_prompt_uses_model_and_sends_code_only_with_consent(tmp_path):
    write(tmp_path, "core/big.py", "token = 'supersecretvalue123'\n" + "z = 1\n" * 400)
    a = ProjectAuditor(tmp_path)
    a.run()
    data = {"target_dir": str(tmp_path), "analysis": a.analysis, "insights": a.insights,
            "findings": [], "total_score": 50, "grade": "C"}
    without = llm_evaluator.build_prompt(data, include_code=False)
    with_code = llm_evaluator.build_prompt(data, include_code=True)
    assert "components" in without and "core/big.py" in without  # file names are in the model, but no code
    assert "z = 1" not in without
    assert "z = 1" in with_code and "supersecretvalue123" not in with_code


def test_evaluate_requires_key_and_analysis():
    assert not llm_evaluator.LLMEvaluator.evaluate("claude", "", "", {"analysis": {"a": 1}})["success"]
    assert not llm_evaluator.LLMEvaluator.evaluate("claude", "k", "", {})["success"]
    assert not llm_evaluator.LLMEvaluator.test_connection("claude", "", "")["success"]


def test_evaluate_calls_provider_with_key(monkeypatch):
    seen = {}

    def fake_call(provider, key, model, prompt, max_tokens):
        seen.update(provider=provider, key=key, model=model, prompt=prompt)
        return "result"
    monkeypatch.setattr(llm_evaluator, "_call", fake_call)
    r = llm_evaluator.LLMEvaluator.evaluate("claude", " k1 ", "", {"analysis": {"kind": {}}})
    assert r["success"] and r["analysis"] == "result"
    assert seen["key"] == "k1" and seen["model"] == llm_evaluator.DEFAULT_MODELS["claude"]


@pytest.mark.skipif(os.name != "nt", reason="DPAPI exists only on Windows")
def test_api_key_is_encrypted_on_disk(tmp_path, monkeypatch):
    monkeypatch.setattr(sm, "SETTINGS_DIR", tmp_path)
    monkeypatch.setattr(sm, "SETTINGS_FILE", tmp_path / "s.json")
    sm.SettingsManager.save_settings({"claude_api_key": "sk-test-123456"})
    assert "sk-test-123456" not in (tmp_path / "s.json").read_text(encoding="utf-8")
    assert sm.SettingsManager.get_settings()["claude_api_key"] == "sk-test-123456"
    sm.SettingsManager.save_settings({"theme": "light"})  # saving again must not corrupt the key
    assert sm.SettingsManager.get_settings()["claude_api_key"] == "sk-test-123456"


def test_invalid_escape_sequence_in_scanned_code_produces_no_warning(tmp_path):
    import warnings
    bad_code = "def foo():\n    s = '\\g\\_'\n    return s\n"
    write(tmp_path, "src/bad_syntax.py", bad_code)
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        auditor = ProjectAuditor(tmp_path)
        auditor.run()
    syntax_warnings = [w for w in recorded if issubclass(w.category, SyntaxWarning)]
    assert syntax_warnings == []


def test_analysis_import_progress_callback(tmp_path):
    calls = []
    for i in range(250):
        write(tmp_path, f"pkg/mod_{i}.py", f"import os\nx = {i}\n")

    def cb(n, total):
        calls.append((n, total))

    tree = ProjectTree(tmp_path)
    analyze_project(tmp_path, tree, progress_callback=cb)
    assert (200, 250) in calls
    assert (250, 250) in calls
