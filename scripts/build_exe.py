#!/usr/bin/env python3
"""
Package Project Builder Analytics so USERS DO NOT NEED TO INSTALL PYTHON:

  1. engine/reviewer-engine.exe : Core Engine Python packaged with PyInstaller (serve | audit), only an intermediate step
  2. Project-Builder-Analytics.exe   : Native Host Shell .NET 10 + WebView2 (ADR-0011) EMBEDDING the engine above (ADR-0022)

The deliverable for users is ONLY Project-Builder-Analytics.exe; the engine/ folder is not released.

Run: python scripts/build_exe.py [--engine-only | --shell-only] [--self-contained]   (or: make build-exe)
By default the shell is framework-dependent (small, needs the .NET 10 Desktop Runtime on the user's machine);
--self-contained bundles the runtime to run on machines without .NET (tried with DOTNET_ROOT unset and a minimal PATH).
Requirements at BUILD time (end users do not need them): Windows, Python 3.12+, PyInstaller, .NET 10 SDK.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 12):
    print("[ERROR] Python 3.12 or newer is required (running %d.%d)." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PROJECT = ROOT / "tools" / "ProjectReviewer" / "ProjectReviewer.csproj"
DIST = ROOT / "tools" / "ProjectReviewer" / "dist"
ICON = ROOT / "assets" / "app-icon.ico"
OUTPUT_EXE = ROOT / "Project-Builder-Analytics.exe"
ENGINE_DIR = ROOT / "engine"
BUILD_DIR = ROOT / "build" / "engine"


def kill_running_instance():
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Project-Builder-Analytics.exe"], capture_output=True, check=False)
        subprocess.run(["taskkill", "/F", "/IM", "reviewer-engine.exe"], capture_output=True, check=False)


def build_engine() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[ERROR] PyInstaller is not installed (needed only for building): python -m pip install pyinstaller",
              file=sys.stderr)
        return 1

    print("[INFO] Packaging the Core Engine (PyInstaller) ...")

    sep = os.pathsep
    cmd = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--name", "reviewer-engine",
        "--paths", str(SCRIPTS),
        "--add-data", f"{SCRIPTS / 'reviewer_shell' / 'static'}{sep}reviewer_shell/static",
        "--add-data", f"{SCRIPTS / 'auditor_engine' / 'knowledge_pack.json'}{sep}auditor_engine",
        "--distpath", str(ENGINE_DIR),
        "--workpath", str(BUILD_DIR / "work"),
        "--specpath", str(BUILD_DIR),
        str(SCRIPTS / "engine_main.py"),
    ]
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("[ERROR] Engine packaging failed.", file=sys.stderr)
        return result.returncode
    print(f"[SUCCESS] {ENGINE_DIR / 'reviewer-engine.exe'}")
    return 0


def build_shell(self_contained: bool = False) -> int:
    if shutil.which("dotnet") is None:
        print("[ERROR] .NET SDK not found. Install the .NET 10 SDK: https://dotnet.microsoft.com/download",
              file=sys.stderr)
        return 1

    engine = ENGINE_DIR / "reviewer-engine.exe"
    if not engine.exists():
        print("[ERROR] Missing %s: the shell would have no embedded engine (ADR-0022). "
              "Run without --shell-only, or build --engine-only first." % engine, file=sys.stderr)
        return 1

    if not ICON.exists():
        print("[INFO] Generating icon assets/app-icon.ico ...")
        subprocess.run([sys.executable, str(SCRIPTS / "generate_icon.py")], check=True)

    mode = "self-contained (~50 MB, no .NET install needed)" if self_contained else "framework-dependent (needs the .NET 10 Desktop Runtime)"
    print(f"[INFO] Compiling Project-Builder-Analytics.exe (.NET 10 + WebView2), {mode} ...")
    cmd = ["dotnet", "publish", str(PROJECT), "-c", "Release", "-r", "win-x64",
           "--self-contained", "true" if self_contained else "false", "-o", str(DIST)]
    if self_contained:
        cmd.append("-p:EnableCompressionInSingleFile=true")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("[ERROR] Build failed, see the log above.", file=sys.stderr)
        return result.returncode

    built = DIST / "Project-Builder-Analytics.exe"
    if not built.exists():
        print("[ERROR] %s not found after the build." % built, file=sys.stderr)
        return 1

    shutil.copy2(built, OUTPUT_EXE)
    shutil.rmtree(DIST, ignore_errors=True)
    print(f"[SUCCESS] {OUTPUT_EXE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Package Project Builder Analytics (engine + shell).")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--engine-only", action="store_true", help="Package only the Python engine.")
    group.add_argument("--shell-only", action="store_true", help="Compile only the .NET shell.")
    parser.add_argument("--self-contained", action="store_true",
                        help="Bundle the .NET runtime into the exe (~50 MB) to run on machines without .NET. "
                             "Do not commit this build to git: release it through GitHub Releases.")
    args = parser.parse_args()

    if sys.platform != "win32":
        print("[ERROR] The exe build supports Windows only.", file=sys.stderr)
        return 1

    kill_running_instance()
    if not args.shell_only:
        code = build_engine()
        if code:
            return code
    if not args.engine_only:
        code = build_shell(args.self_contained)
        if code:
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
