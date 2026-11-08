#!/usr/bin/env python3
"""
UNIVERSAL PROJECT REVIEWER & ARCHITECTURE AUDITOR ENGINE v3.0
Thin CLI entry point: the logic lives in the `auditor_engine` package (see scripts/auditor_engine/).
Pure Python Standard Library (100% Offline, Zero-Token, Zero-Dependency).
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Python 3.12 or newer is required (running %d.%d). 3.14 is recommended." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

# The default Windows console (cp1252) cannot print many Unicode characters: force UTF-8, replace bad characters instead of crashing.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

from auditor_engine import ProjectAuditor, ProjectProfiler, ProjectTree  # noqa: F401

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    auditor = ProjectAuditor(target)
    auditor.run()
