#!/usr/bin/env python3
"""Token Dashboard: live local web dashboard of Claude Code token usage.

  python scripts/token_dashboard_cli.py            # serves http://127.0.0.1:8999 and opens the browser
  python scripts/token_dashboard_cli.py --no-open  # just serve

Read-only, loopback only, no network calls. Reads ~/.claude/projects/*/*.jsonl.
Only Claude Code transcripts are supported.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "token_dashboard"))
from server import start  # noqa: E402
from service import TokenService  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8999)
    ap.add_argument("--project", default=os.getcwd(), help="folder whose sessions are shown first (default: current directory)")
    ap.add_argument("--projects-root", help="override ~/.claude/projects")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    svc = TokenService(Path(a.projects_root) if a.projects_root else None, a.project)
    if not svc.root.is_dir():
        print(f"Log folder not found: {svc.root}", file=sys.stderr)
        return 2
    srv, port = start(svc, a.port)
    url = f"http://127.0.0.1:{port}/"
    print(f"Token Dashboard: {url}  (Ctrl+C to stop)")
    if not a.no_open:
        webbrowser.open(url)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        srv.shutdown()
        return 0


if __name__ == "__main__":
    sys.exit(main())
