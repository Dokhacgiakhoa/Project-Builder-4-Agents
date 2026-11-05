"""Hằng số dùng chung của Auditor Engine."""

IGNORE_DIRS = {

    'node_modules', '.git', 'dist', 'build', 'bin', 'obj',

    '.vscode', '.idea', '__pycache__', '.next', 'coverage',

    'vendor', 'target', '.turbo', '.cache'

}

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py', '.go', '.java', '.rs', '.php'}

# Tên tệp báo cáo xuất ra thư mục dự án được quét (cả người và Agent đều đọc)
REPORT_NAME = "project-review.md"
