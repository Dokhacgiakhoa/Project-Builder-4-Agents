"""Tests for scripts/token_dashboard (service + local HTTP server)."""
import http.client
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "token_dashboard"))
sys.path.insert(0, str(ROOT / "scripts"))

from service import TokenService  # noqa: E402
from server import start  # noqa: E402

T0 = datetime(2026, 11, 7, 10, 0, 0, tzinfo=timezone.utc)


def rec(i, out=50, cc=100, cr=1000, inp=5, ts=None, side=False):
    ts = ts or T0 + timedelta(minutes=i)
    return json.dumps({
        "type": "assistant", "timestamp": ts.isoformat().replace("+00:00", "Z"), "requestId": f"r{i}",
        "isSidechain": side, "sessionId": "s",
        "message": {"id": f"m{i}", "model": "claude-x", "usage": {
            "input_tokens": inp, "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr, "output_tokens": out}}})


def write(path: Path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_root(tmp_path):
    root = tmp_path / "projects"
    write(root / "proj-a" / "sess1.jsonl", [rec(1), rec(1), rec(2, cr=2000)])  # rec(1) duplicated
    write(root / "proj-b" / "sess2.jsonl", [rec(3)])
    (root / "empty-proj").mkdir()
    return root


def test_projects_lists_only_folders_with_sessions(tmp_path):
    svc = TokenService(make_root(tmp_path))
    assert {p["id"] for p in svc.projects()} == {"proj-a", "proj-b"}


def test_default_project_falls_back_to_most_recent(tmp_path):
    root = make_root(tmp_path)
    os.utime(root / "proj-a" / "sess1.jsonl", (1, 1))
    assert TokenService(root, r"C:\nowhere").pick_default_project() == "proj-b"
    assert TokenService(root, "proj-a").pick_default_project() == "proj-a"


def test_payload_deduplicates_and_reports_context(tmp_path):
    p = TokenService(make_root(tmp_path)).payload("proj-a")
    assert p["turns"] == 2 and p["totals"]["output"] == 100
    assert p["context_now"] == 5 + 100 + 2000
    assert [s["ctx"] for s in p["series"]] == [1105, 2105]
    assert p["series"][0]["in"] == 105 and p["session"] == "sess1"


def test_payload_is_incremental(tmp_path):
    root = make_root(tmp_path)
    svc = TokenService(root)
    assert svc.payload("proj-a")["turns"] == 2
    with open(root / "proj-a" / "sess1.jsonl", "a", encoding="utf-8") as f:
        f.write(rec(9, out=999) + "\n")
    p = svc.payload("proj-a")
    assert p["turns"] == 3 and p["totals"]["output"] == 1099


def test_session_all_merges_sessions(tmp_path):
    root = make_root(tmp_path)
    write(root / "proj-a" / "sess3.jsonl", [rec(7)])
    p = TokenService(root).payload("proj-a", "all")
    assert p["turns"] == 3 and p["session"] == "all"


def test_unknown_session_and_project(tmp_path):
    svc = TokenService(make_root(tmp_path))
    assert svc.payload("proj-a", "nope")["error"] == "unknown session"
    assert svc.payload("zzz")["error"] == "unknown project"


def test_project_id_cannot_escape_root(tmp_path):
    root = make_root(tmp_path)
    write(tmp_path / "outside" / "x.jsonl", [rec(1)])
    svc = TokenService(root)
    for bad in ["..", ".", "../outside", "..\\outside", "proj-a/..", "", str(tmp_path / "outside")]:
        assert svc.payload(bad)["error"] == "unknown project", bad
        assert svc.sessions(bad) == []


def test_max_points_truncates_series_not_totals(tmp_path):
    root = tmp_path / "projects"
    write(root / "p" / "s.jsonl", [rec(i) for i in range(1, 31)])
    p = TokenService(root).payload("p", max_points=10)
    assert len(p["series"]) == 10 and p["truncated"] == 20 and p["turns"] == 30


def test_top_n_is_respected(tmp_path):
    root = tmp_path / "projects"
    write(root / "p" / "s.jsonl", [rec(i, cc=i * 10) for i in range(1, 9)])
    assert len(TokenService(root).payload("p", top_n=5)["top_turns"]) == 5


def get(port, path, host=None, method="GET"):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    c.request(method, path, headers={"Host": host or f"127.0.0.1:{port}"})
    r = c.getresponse()
    body = r.read()
    c.close()
    return r.status, body


def test_server_api_and_loopback_guard(tmp_path):
    svc = TokenService(make_root(tmp_path), "proj-a")
    srv, port = start(svc, 18999)
    try:
        st, body = get(port, "/api/projects")
        assert st == 200 and json.loads(body)["default"] == "proj-a"
        st, body = get(port, "/api/tokens?project=proj-a&warn=5")  # warn clamps to minimum
        d = json.loads(body)
        assert st == 200 and d["turns"] == 2 and d["warn_context"] == 1000
        assert json.loads(get(port, "/api/tokens?project=proj-a")[1])["warn_context"] == 0  # no default threshold
        assert get(port, "/api/tokens?project=..")[0] == 404
        assert get(port, "/api/projects", host="evil.example.com")[0] == 403  # DNS-rebinding guard
        assert get(port, "/api/projects", method="POST")[0] == 405            # read-only
        st, html = get(port, "/")
        assert st == 200 and b"<html" in html
    finally:
        srv.shutdown()
        srv.server_close()
