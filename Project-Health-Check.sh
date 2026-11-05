#!/usr/bin/env bash
# Project-Builder-4-Agents - Project Health Check (Linux/macOS)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "  PROJECT-BUILDER-KIT - PROJECT HEALTH CHECK"
echo "  Thanh Tra Kiến Trúc & Đối Chiếu Chuẩn Mực (Zero-Token, Offline)"
echo "======================================================================"
echo ""

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[ERROR] Không tìm thấy Python trên hệ thống!"
    echo "Vui lòng cài đặt Python 3 để chạy bộ thanh tra kiến trúc."
    exit 1
fi

# Chọn trình thông dịch Python >= 3.12 đầu tiên chạy được (bỏ qua stub của Microsoft Store)
PYTHON_CMD=""
for cand in python3 python; do
    if command -v "$cand" &> /dev/null && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' &> /dev/null; then
        PYTHON_CMD="$cand"
        break
    fi
done
if [ -z "$PYTHON_CMD" ]; then
    echo "[ERROR] Cần Python 3.12 trở lên (khuyến nghị 3.14)."
    exit 1
fi

# Dùng: ./Project-Health-Check.sh [thư_mục_dự_án]  (mặc định: thư mục chứa script này)
TARGET="${1:-$SCRIPT_DIR}"
if [ ! -d "$TARGET" ]; then
    echo "[ERROR] Thư mục không tồn tại: $TARGET"
    exit 1
fi
echo "[INFO] Thư mục được thanh tra: $TARGET"

# Không để set -e thoát sớm: cần in hướng dẫn rồi trả về mã thoát của auditor
set +e
$PYTHON_CMD "$SCRIPT_DIR/scripts/project_auditor.py" "$TARGET"
EXIT_CODE=$?

echo ""
echo "======================================================================"
echo "  [HƯỚNG DẪN SỬ DỤNG CHO AI AGENT]"
echo "  1. Mở tệp: project-review.md vừa được tạo."
echo "  2. Cuộn xuống Mục 6, sao chép đoạn Prompt sẵn có (hoặc bảo Agent đọc thẳng tệp)."
echo "  3. Dán vào Claude Code, Cursor, hoặc Antigravity để AI tự sửa code!"
echo "======================================================================"
echo ""

exit $EXIT_CODE
