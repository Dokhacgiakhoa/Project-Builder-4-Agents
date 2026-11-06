#!/usr/bin/env python3
"""Benchmark the Health Check engine (stdlib only).

Measures wall-clock time of `scripts/project_auditor.py` on:
  - this repository (repeated runs: median / min / max)
  - synthetic projects of increasing size (default 500, 1000, 5000 files)

Acceptance target from TASKS.md (A2): 5,000 files in < 30 s.
The auditor writes project-review.md into the scanned directory, so synthetic
projects are generated under the system temp dir and deleted afterwards; runs on
this repo restore project-review.md afterwards.

  python evals/bench_health_check.py [--runs 7] [--sizes 500 1000 5000]
"""
from __future__ import annotations

import argparse
import platform
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDITOR = ROOT / "scripts" / "project_auditor.py"
SNIPPETS = [
    "def f(x):\n    return x + 1\n",
    "export const add = (a: number, b: number) => a + b;\n",
    "# Notes\n\nSome documentation text.\n",
    "public class A { public int B() { return 1; } }\n",
]


def run_once(target: Path) -> float:
    t = time.perf_counter()
    r = subprocess.run([sys.executable, str(AUDITOR), str(target)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    dt = time.perf_counter() - t
    if r.returncode not in (0, 1):
        print(f"  auditor exit code {r.returncode}: {r.stderr[:200]}", file=sys.stderr)
    return dt


def make_project(n: int, base: Path) -> Path:
    rnd = random.Random(42)
    exts = [".py", ".ts", ".md", ".cs"]
    for i in range(n):
        d = base / f"pkg{i % 50}" / f"mod{i % 7}"
        d.mkdir(parents=True, exist_ok=True)
        e = exts[i % len(exts)]
        (d / f"file{i}{e}").write_text(rnd.choice(SNIPPETS) * rnd.randint(1, 20), encoding="utf-8")
    return base


def summarize(label: str, times: list[float]) -> str:
    return f"| {label} | {len(times)} | {statistics.median(times):.2f} | {min(times):.2f} | {max(times):.2f} |"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=7)
    ap.add_argument("--sizes", type=int, nargs="*", default=[500, 1000, 5000])
    a = ap.parse_args()

    print(f"Python {platform.python_version()} on {platform.platform()}\n")
    print("| target | runs | median s | min s | max s |\n| :-- | --: | --: | --: | --: |")

    review = ROOT / "project-review.md"
    backup = review.read_bytes() if review.exists() else None
    try:
        tracked = len(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split())
        print(summarize(f"this repo ({tracked} tracked files)", [run_once(ROOT) for _ in range(a.runs)]))
    finally:
        if backup is not None:
            review.write_bytes(backup)

    for n in a.sizes:
        tmp = Path(tempfile.mkdtemp(prefix="hc-bench-"))
        try:
            make_project(n, tmp)
            runs = max(3, a.runs // 2)
            print(summarize(f"synthetic {n} files", [run_once(tmp) for _ in range(runs)]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
