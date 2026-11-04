#!/usr/bin/env bash
# Universal Project Starter Kit - Architecture & System Design Auditor (Linux/macOS)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "  UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE AUDITOR"
echo "  Thanh Tra Kiến Trúc & Đối Chiếu Chuẩn Mực (Zero-Token, Offline)"
echo "======================================================================"
echo ""

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[ERROR] Không tìm thấy Python trên hệ thống!"
    echo "Vui lòng cài đặt Python 3 để chạy bộ thanh tra kiến trúc."
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

$PYTHON_CMD "$SCRIPT_DIR/scripts/project_auditor.py" "$SCRIPT_DIR/."
EXIT_CODE=$?

echo ""
echo "======================================================================"
echo "  [HƯỚNG DẪN SỬ DỤNG CHO AI AGENT]"
echo "  1. Mở tệp: PROJECT_REVIEW_REPORT.md vừa được tạo."
echo "  2. Cuộn xuống Mục 7, sao chép đoạn Prompt sẵn có."
echo "  3. Dán vào Claude Code, Cursor, hoặc Antigravity để AI tự sửa code!"
echo "======================================================================"
echo ""

exit $EXIT_CODE
