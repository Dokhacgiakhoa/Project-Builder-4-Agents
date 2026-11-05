#!/usr/bin/env python3
"""
Khởi tạo dự án mới (hoặc bổ sung chuẩn Starter Kit cho dự án đang làm dở).

  python scripts/init_project.py <thư_mục_đích> [--name TÊN] [--frontend] [--docker] [--pitch]
                                 [--merge | --force] [--dry-run] [--git]

Entrypoint CLI mỏng: toàn bộ logic nằm trong package `kit_init`.
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Cần Python 3.12 trở lên (đang chạy %d.%d). Khuyến nghị 3.14." % sys.version_info[:2],
          file=sys.stderr)
    sys.exit(1)

import argparse
import shutil
import subprocess
from pathlib import Path

from kit_init import InitError, init_project


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Khởi tạo dự án từ Universal Project Starter Kit.")
    p.add_argument("target", help="Thư mục đích (tạo mới hoặc đang có sẵn).")
    p.add_argument("--name", help="Tên dự án (mặc định: tên thư mục đích).")
    p.add_argument("--frontend", action="store_true", help="Kèm Bulletproof React frontend.")
    p.add_argument("--docker", action="store_true", help="Kèm docker-compose.yml (Postgres+pgvector, Redis).")
    p.add_argument("--pitch", action="store_true", help="Kèm Pitch Deck Kit (templates/pitch-deck).")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--merge", action="store_true",
                      help="Thư mục đã có nội dung: chỉ thêm tệp còn thiếu, KHÔNG ghi đè.")
    mode.add_argument("--force", action="store_true", help="Ghi đè các tệp trùng tên.")
    p.add_argument("--dry-run", action="store_true", help="Chỉ liệt kê, không ghi gì.")
    p.add_argument("--git", action="store_true", help="Chạy `git init` nếu thư mục chưa phải repo git.")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    target = Path(args.target)

    try:
        result = init_project(
            target, args.name,
            frontend=args.frontend, docker=args.docker, pitch=args.pitch,
            force=args.force, merge=args.merge, dry_run=args.dry_run,
        )
    except InitError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    prefix = "[DRY-RUN] " if args.dry_run else ""
    print(f"{prefix}Tạo mới: {len(result.created)} | Ghi đè: {len(result.overwritten)} | "
          f"Bỏ qua (đã có): {len(result.skipped)}")
    if args.dry_run:
        for f in result.created + result.overwritten:
            print("  +", f)
        return 0

    if args.git and not (target / ".git").exists():
        if shutil.which("git") is None:
            print("[WARN] Không tìm thấy git, bỏ qua --git.", file=sys.stderr)
        else:
            subprocess.run(["git", "init", "-q", str(target)], check=False)
            print("Đã chạy git init.")

    print(f"""
Hoàn tất: {target.resolve()}

Bước tiếp theo:
  1. Điền specs/product-vision.md và specs/domains.md
  2. Chốt tech stack trong adrs/0002-tech-stack.md
  3. Chấm điểm: Project-Review.exe (hoặc python scripts/project_auditor.py "{target}")
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
