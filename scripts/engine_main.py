#!/usr/bin/env python3
"""
Điểm vào duy nhất của Engine đóng gói (reviewer-engine.exe) cho Project Health Check, để người dùng KHÔNG cần cài Python.

  reviewer-engine serve [--server-only] [--port=N]   # giao diện/web server (Project-Health-Check.exe gọi lệnh này)
  reviewer-engine audit <thư_mục>                    # thanh tra dự án bất kỳ, xuất project-review.md

Khi chạy từ mã nguồn, cũng dùng được: python scripts/engine_main.py audit <thư_mục>
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Python 3.12 or newer is required (running %d.%d)." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

# Console Windows mặc định không in được tiếng Việt (cp1252): ép UTF-8, thay ký tự lỗi thay vì sập.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

USAGE = __doc__


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0

    command, rest = argv[0], argv[1:]

    if command == "serve":
        import reviewer_app
        sys.argv = ["reviewer_app"] + rest
        reviewer_app.main()
        return 0

    if command == "audit":
        from auditor_engine import ProjectAuditor
        if not rest:
            print("[ERROR] Missing project folder path.", file=sys.stderr)
            return 1
        auditor = ProjectAuditor(rest[0])
        score = auditor.run()
        report = auditor.generate_markdown_report(score)
        print(f"Score: {score}/100 — {auditor.get_letter_grade(score)}\nReport: {report}")
        return 0

    print(f"[ERROR] Invalid command: {command}\n{USAGE}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
