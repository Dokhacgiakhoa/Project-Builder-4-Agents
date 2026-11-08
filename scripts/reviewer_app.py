#!/usr/bin/env python3
"""
PROJECT ARCHITECTURE BENCHMARK SUITE - MODERN ANTIGRAVITY 2.0 SHELL
Universal Desktop Launcher (Decoupled Core Engine + Edge WebView2 App Mode)
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Cần Python 3.12 trở lên (đang chạy %d.%d). Khuyến nghị 3.14." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

import os
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

# Thêm đường dẫn scripts vào sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from reviewer_shell.server import start_server


def find_free_port(start_port=8998):
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port


def find_edge_path():
    candidates = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def main():
    target_port = 8998
    watchdog_timeout = 180.0
    for arg in sys.argv[1:]:
        if arg.startswith("--port="):
            try:
                target_port = int(arg.split("=")[1])
            except ValueError:
                pass
        elif arg.startswith("--watchdog="):
            try:
                watchdog_timeout = float(arg.split("=")[1])
            except ValueError:
                pass

    if "--server-only" in sys.argv:
        server, active_port, shutdown_event = start_server(target_port, watchdog_timeout=watchdog_timeout)
        print(f"[SERVER_READY] port={active_port}", flush=True)
        try:
            while not shutdown_event.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
        return

    port = find_free_port(target_port)
    server, active_port, shutdown_event = start_server(port, watchdog_timeout=watchdog_timeout)
    app_url = f"http://127.0.0.1:{active_port}"

    edge_exe = find_edge_path()
    
    if edge_exe:
        # Khởi chạy ở chế độ App Mode không thanh địa chỉ, không tab, chuẩn Desktop Studio
        profile_dir = Path.home() / ".starter-kit" / "edge_profile"
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            edge_exe,
            f"--app={app_url}",
            f"--user-data-dir={str(profile_dir)}",
            "--window-size=1260,840",
            "--disable-extensions",
            "--disable-default-apps",
            "--disable-features=Translate,msEdgeTranslate",
            "--no-first-run",
            "--no-default-browser-check",
            "--lang=vi-VN"
        ]
        subprocess.Popen(cmd)
    else:
        # Fallback mở trình duyệt mặc định
        webbrowser.open(app_url)

    try:
        # Giữ backend server chạy suốt phiên làm việc của giao diện
        while not shutdown_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
