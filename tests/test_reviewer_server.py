"""Kiểm thử bảo mật cho Reviewer Shell local server (ADR-0011)."""

import http.client
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from reviewer_shell import server as srv  # noqa: E402
from reviewer_shell.settings_manager import SettingsManager  # noqa: E402


@pytest.fixture()
def live_server(tmp_path, monkeypatch):
    """Khởi chạy server thật trên cổng ngẫu nhiên với settings tách biệt."""
    import reviewer_shell.settings_manager as sm

    monkeypatch.setattr(sm, "SETTINGS_DIR", tmp_path)
    monkeypatch.setattr(sm, "SETTINGS_FILE", tmp_path / "settings.json")
    server, port, _ = srv.start_server(0)
    port = server.server_address[1]
    yield port
    server.shutdown()
    server.server_close()


def call(port, method, path, body=None, headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    hdrs = {"Host": f"127.0.0.1:{port}"}
    hdrs.update(headers or {})
    payload = None
    if body is not None:
        payload = json.dumps(body)
        hdrs["Content-Type"] = "application/json"
    conn.request(method, path, body=payload, headers=hdrs)
    resp = conn.getresponse()
    raw = resp.read()
    conn.close()
    return resp, raw


# ---- Happy path ----
def test_status_ok(live_server):
    resp, raw = call(live_server, "GET", "/api/status")
    assert resp.status == 200
    assert json.loads(raw)["status"] == "ready"
    assert resp.getheader("Access-Control-Allow-Origin") is None


def test_settings_never_return_api_key(live_server):
    dummy_key = "dummy_val_123"
    resp, _ = call(live_server, "POST", "/api/settings", {"claude_api_key": dummy_key})
    assert resp.status == 200
    resp, raw = call(live_server, "GET", "/api/settings")
    assert dummy_key not in raw.decode()
    data = json.loads(raw)
    assert data["claude_api_key"] == ""
    assert data["has_claude_api_key"] is True
    assert data["has_openai_api_key"] is False


def test_empty_key_keeps_saved_key(live_server):
    call(live_server, "POST", "/api/settings", {"gemini_api_key": "abc"})
    call(live_server, "POST", "/api/settings", {"gemini_api_key": "", "theme": "light"})
    assert SettingsManager.get_settings()["gemini_api_key"] == "abc"


# ---- Edge / error cases ----
def test_foreign_origin_rejected(live_server):
    resp, _ = call(live_server, "POST", "/api/shutdown",
                   {}, {"Origin": "https://evil.example"})
    assert resp.status == 403
    assert not srv.SHUTDOWN_EVENT.is_set()


def test_dns_rebinding_host_rejected(live_server):
    resp, _ = call(live_server, "GET", "/api/settings", None,
                   {"Host": "evil.example:80"})
    assert resp.status == 403


def test_open_report_requires_allowlist(live_server, tmp_path):
    target = tmp_path / "secret.txt"
    target.write_text("x")
    resp, raw = call(live_server, "POST", "/api/open-report", {"path": str(target)})
    assert json.loads(raw)["success"] is False


def test_open_folder_requires_allowlist(live_server, tmp_path):
    resp, raw = call(live_server, "POST", "/api/open-folder", {"path": str(tmp_path)})
    assert json.loads(raw)["success"] is False


def test_invalid_json_body_does_not_crash(live_server):
    conn = http.client.HTTPConnection("127.0.0.1", live_server, timeout=5)
    conn.request("POST", "/api/heartbeat", body="not-json",
                 headers={"Host": f"127.0.0.1:{live_server}", "Content-Length": "8"})
    assert conn.getresponse().status == 200
    conn.close()


# ---- Unit ----
@pytest.mark.parametrize("a,b", [("2.10.0", "2.9.0"), ("v3.0.0", "2.99.99"), ("2.1.1", "2.1.0")])
def test_parse_version_orders_numerically(a, b):
    assert srv.parse_version(a) > srv.parse_version(b)


def test_parse_version_garbage_is_safe():
    assert srv.parse_version("abc") == (0,)


def test_run_audit_returns_full_12_categories_and_extended_sections(live_server, tmp_path):
    (tmp_path / "README.md").write_text("# Test Project\n\n```bash\nnpm test\n```\n", encoding="utf-8")
    resp, raw = call(live_server, "POST", "/api/run-audit", {"target_dir": str(tmp_path)})
    assert resp.status == 200
    data = json.loads(raw)
    assert data["success"] is True
    assert len(data["categories"]) == 12
    assert "05_anticrash" in data["categories"]
    assert not data["categories"]["05_anticrash"]["is_na"]
    assert "findings" in data and isinstance(data["findings"], list)
    assert "baseline" in data and len(data["baseline"]) == 9
    assert "safety" in data and "scanned" in data["safety"]
    assert "scope" in data and "scanned_total" in data["scope"]
    assert "kit_config" in data
