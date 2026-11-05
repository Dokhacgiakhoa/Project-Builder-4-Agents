#!/usr/bin/env python3
"""
Đóng gói công cụ Project Health Check để NGƯỜI DÙNG KHÔNG CẦN CÀI PYTHON:

  1. engine/reviewer-engine.exe : Core Engine Python đóng gói bằng PyInstaller (serve | audit)
  2. Project-Health-Check.exe         : Native Host Shell .NET 10 + WebView2 (ADR-0011), gọi engine ở trên

Chạy: python scripts/build_exe.py [--engine-only | --shell-only]   (hoặc: make build-exe)
Yêu cầu khi BUILD (người dùng cuối không cần): Windows, Python 3.12+, PyInstaller, .NET 10 SDK.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 12):
    print("[ERROR] Cần Python 3.12 trở lên (đang chạy %d.%d)." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PROJECT = ROOT / "tools" / "ProjectReviewer" / "ProjectReviewer.csproj"
DIST = ROOT / "tools" / "ProjectReviewer" / "dist"
ICON = ROOT / "assets" / "app-icon.ico"
OUTPUT_EXE = ROOT / "Project-Health-Check.exe"
ENGINE_DIR = ROOT / "engine"
BUILD_DIR = ROOT / "build" / "engine"


def kill_running_instance():
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Project-Health-Check.exe"], capture_output=True, check=False)
        subprocess.run(["taskkill", "/F", "/IM", "reviewer-engine.exe"], capture_output=True, check=False)


def build_engine() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[ERROR] Chưa cài PyInstaller (chỉ cần khi build): python -m pip install pyinstaller",
              file=sys.stderr)
        return 1

    print("[INFO] Đang đóng gói Core Engine (PyInstaller) ...")

    sep = os.pathsep
    cmd = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--name", "reviewer-engine",
        "--paths", str(SCRIPTS),
        "--add-data", f"{SCRIPTS / 'reviewer_shell' / 'static'}{sep}reviewer_shell/static",
        "--distpath", str(ENGINE_DIR),
        "--workpath", str(BUILD_DIR / "work"),
        "--specpath", str(BUILD_DIR),
        str(SCRIPTS / "engine_main.py"),
    ]
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("[ERROR] Đóng gói engine thất bại.", file=sys.stderr)
        return result.returncode
    print(f"[THÀNH CÔNG] {ENGINE_DIR / 'reviewer-engine.exe'}")
    return 0


def build_shell() -> int:
    if shutil.which("dotnet") is None:
        print("[ERROR] Không tìm thấy .NET SDK. Cài .NET 10 SDK: https://dotnet.microsoft.com/download",
              file=sys.stderr)
        return 1

    if not ICON.exists():
        print("[INFO] Đang tạo icon assets/app-icon.ico ...")
        subprocess.run([sys.executable, str(SCRIPTS / "generate_icon.py")], check=True)

    print("[INFO] Đang biên dịch Project-Health-Check.exe (.NET 10 + WebView2) ...")
    result = subprocess.run(
        ["dotnet", "publish", str(PROJECT), "-c", "Release", "-r", "win-x64",
         "--self-contained", "false", "-o", str(DIST)],
        check=False,
    )
    if result.returncode != 0:
        print("[ERROR] Biên dịch thất bại, xem log ở trên.", file=sys.stderr)
        return result.returncode

    built = DIST / "Project-Health-Check.exe"
    if not built.exists():
        print("[ERROR] Không thấy %s sau khi biên dịch." % built, file=sys.stderr)
        return 1

    shutil.copy2(built, OUTPUT_EXE)
    shutil.rmtree(DIST, ignore_errors=True)
    print(f"[THÀNH CÔNG] {OUTPUT_EXE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Đóng gói Project Review (engine + shell).")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--engine-only", action="store_true", help="Chỉ đóng gói engine Python.")
    group.add_argument("--shell-only", action="store_true", help="Chỉ biên dịch shell .NET.")
    args = parser.parse_args()

    if sys.platform != "win32":
        print("[ERROR] Build exe chỉ hỗ trợ Windows.", file=sys.stderr)
        return 1

    kill_running_instance()
    if not args.shell_only:
        code = build_engine()
        if code:
            return code
    if not args.engine_only:
        code = build_shell()
        if code:
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
