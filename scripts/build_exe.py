#!/usr/bin/env python3
"""
Đóng gói Project-Review.exe (Native .NET 10 + WebView2 Shell, ADR-0011).
Thay thế build-exe.bat: chạy được bằng `python scripts/build_exe.py` hoặc `make build-exe`.
Yêu cầu: Windows, Python 3.12+, .NET 10 SDK.
"""

import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 12):
    print("[ERROR] Cần Python 3.12 trở lên (đang chạy %d.%d)." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "tools" / "ProjectReviewer" / "ProjectReviewer.csproj"
DIST = ROOT / "tools" / "ProjectReviewer" / "dist"
ICON = ROOT / "assets" / "app-icon.ico"
OUTPUT_EXE = ROOT / "Project-Review.exe"


def kill_running_instance():
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Project-Review.exe"],
                       capture_output=True, check=False)


def main() -> int:
    if sys.platform != "win32":
        print("[ERROR] Project-Review.exe chỉ build được trên Windows.", file=sys.stderr)
        return 1

    if shutil.which("dotnet") is None:
        print("[ERROR] Không tìm thấy .NET SDK. Cài .NET 10 SDK: https://dotnet.microsoft.com/download",
              file=sys.stderr)
        return 1

    kill_running_instance()

    if not ICON.exists():
        print("[INFO] Đang tạo icon assets/app-icon.ico ...")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_icon.py")], check=True)

    print("[INFO] Đang biên dịch Project-Review.exe (.NET 10 + WebView2) ...")
    result = subprocess.run(
        ["dotnet", "publish", str(PROJECT), "-c", "Release", "-r", "win-x64",
         "--self-contained", "false", "-o", str(DIST)],
        check=False,
    )
    if result.returncode != 0:
        print("[ERROR] Biên dịch thất bại, xem log ở trên.", file=sys.stderr)
        return result.returncode

    built = DIST / "Project-Review.exe"
    if not built.exists():
        print("[ERROR] Không thấy %s sau khi biên dịch." % built, file=sys.stderr)
        return 1

    kill_running_instance()
    shutil.copy2(built, OUTPUT_EXE)
    shutil.rmtree(DIST, ignore_errors=True)

    print("[THÀNH CÔNG] Đã tạo %s" % OUTPUT_EXE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
