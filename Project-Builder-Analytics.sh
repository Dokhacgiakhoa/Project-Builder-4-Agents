#!/usr/bin/env bash
# Project-Builder-4-Agents - Project Builder Analytics (Linux/macOS)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "  PROJECT-BUILDER-4-AGENTS — PROJECT BUILDER ANALYTICS"
echo "  Architecture Audit & Standards Verification (Zero-Token, Offline)"
echo "======================================================================"
echo ""

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[ERROR] Python was not found on your system PATH."
    echo "Please install Python 3.12+ to run the architecture audit engine."
    exit 1
fi

# Select first working Python interpreter >= 3.12 (skip Microsoft Store stubs)
PYTHON_CMD=""
for cand in python3 python; do
    if command -v "$cand" &> /dev/null && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' &> /dev/null; then
        PYTHON_CMD="$cand"
        break
    fi
done
if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] Python 3.12 or newer is required (Python 3.12+ recommended)."
    exit 1
fi

# Usage: ./Project-Builder-Analytics.sh [target_directory] (default: directory containing this script)
TARGET="${1:-$SCRIPT_DIR}"
if [ ! -d "$TARGET" ]; then
    echo "[ERROR] Target directory does not exist: $TARGET"
    exit 1
fi
echo "[INFO] Auditing workspace directory: $TARGET"

# Allow non-zero exit to display AI Agent guidance before returning the auditor code
set +e
$PYTHON_CMD "$SCRIPT_DIR/scripts/project_auditor.py" "$TARGET"
EXIT_CODE=$?

echo ""
echo "======================================================================"
echo "  [AI AGENT NEXT STEPS]"
echo "  1. Open: project-review.md generated at the project root."
echo "  2. Review Section 0 (Safety) and Section 7 (Scope), then resolve Section 2 findings."
echo "  3. Paste Section 6 prompt into Claude Code, Antigravity, Cursor, or Codex!"
echo "======================================================================"
echo ""

exit $EXIT_CODE
