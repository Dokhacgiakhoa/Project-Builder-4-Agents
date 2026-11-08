#!/usr/bin/env python3
"""
Single entry point of the packaged Engine (reviewer-engine.exe) for Project Builder Analytics, so users do NOT need to install Python.

  reviewer-engine serve [--server-only] [--port=N]   # UI/web server (Project-Builder-Analytics.exe calls this command)
  reviewer-engine audit <folder>                     # audit any project, writes project-review.md

When run from source it also works: python scripts/engine_main.py audit <folder>
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Python 3.12 or newer is required (running %d.%d)." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

# The default Windows console (cp1252) cannot print many Unicode characters: force UTF-8, replace bad characters instead of crashing.
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
