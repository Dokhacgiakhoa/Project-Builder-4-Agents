"""Local HTTP server for the Token Dashboard. Loopback only, read-only, no outbound calls."""
from __future__ import annotations

import json
import sys
import threading
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from service import TokenService  # noqa: E402

STATIC_DIR = Path(__file__).resolve().parent / "static"


def _int(q: dict, name: str, default: int, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(q.get(name, [default])[0])))
    except (ValueError, IndexError):
        return default


def make_handler(service: TokenService):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(STATIC_DIR), **kw)

        def log_message(self, *a):  # keep the terminal quiet
            pass

        def _local(self) -> bool:
            port = self.server.server_address[1]
            hosts = {f"127.0.0.1:{port}", f"localhost:{port}", f"[::1]:{port}"}
            if (self.headers.get("Host") or "").lower() not in hosts:
                return False
            origin = self.headers.get("Origin")
            return origin is None or origin.lower() in {f"http://{h}" for h in hosts}

        def _json(self, data, status: int = 200) -> None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if not self._local():
                self.send_error(403, "Forbidden")
                return
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            if u.path == "/api/projects":
                self._json({"projects": service.projects(), "default": service.pick_default_project()})
            elif u.path == "/api/tokens":
                pid = (q.get("project") or [service.pick_default_project() or ""])[0]
                data = service.payload(
                    pid, (q.get("session") or ["latest"])[0],
                    warn_context=_int(q, "warn", 200_000, 1_000, 10_000_000),
                    window_min=_int(q, "window", 10, 1, 120),
                    max_points=_int(q, "points", 300, 10, 2000),
                )
                self._json(data, 404 if data.get("error") == "unknown project" else 200)
            else:
                super().do_GET()

        def do_POST(self) -> None:  # noqa: N802
            self.send_error(405, "Read-only")

    return Handler


def start(service: TokenService, port: int = 8999, tries: int = 20) -> tuple[ThreadingHTTPServer, int]:
    last = None
    for p in range(port, port + tries):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", p), make_handler(service))
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            return srv, p
        except OSError as e:
            last = e
    raise RuntimeError(f"no free port in {port}-{port + tries - 1}: {last}")
