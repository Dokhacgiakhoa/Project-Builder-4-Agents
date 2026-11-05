#!/usr/bin/env python3
"""
UNIVERSAL PROJECT REVIEWER & ARCHITECTURE AUDITOR ENGINE v3.0
Entrypoint CLI mỏng: logic nằm trong package `auditor_engine` (xem scripts/auditor_engine/).
Pure Python Standard Library (100% Offline, Zero-Token, Zero-Dependency).
"""

import sys

if sys.version_info < (3, 12):
    print("[ERROR] Cần Python 3.12 trở lên (đang chạy %d.%d). Khuyến nghị 3.14." % sys.version_info[:2], file=sys.stderr)
    sys.exit(1)

from auditor_engine import ProjectAuditor, ProjectProfiler, ProjectTree  # noqa: F401

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    auditor = ProjectAuditor(target)
    auditor.run()
