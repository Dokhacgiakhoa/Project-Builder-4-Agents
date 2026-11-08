"""Hằng số dùng chung của Auditor Engine."""

# Thư mục không bao giờ nên đọc: sinh ra tự động hoặc là bản sao thư viện (tốn token, không có giá trị review).
# Giá trị là lý do ngắn, được in vào mục "Phạm vi quét" của project-review.md.
SKIP_REASONS = {
    'node_modules': 'thư viện cài tự động (npm/yarn/pnpm)',
    '.git': 'dữ liệu nội bộ của git',
    'dist': 'kết quả build',
    'build': 'kết quả build',
    'bin': 'kết quả build/nhị phân',
    'obj': 'kết quả build (.NET)',
    '.vscode': 'cấu hình trình soạn thảo',
    '.idea': 'cấu hình trình soạn thảo',
    '__pycache__': 'bytecode Python',
    '.next': 'cache build Next.js',
    'coverage': 'báo cáo độ phủ test',
    'vendor': 'thư viện bên thứ ba chép vào repo',
    'target': 'kết quả build (Rust/Java)',
    '.turbo': 'cache build',
    '.cache': 'cache',
    '.venv': 'môi trường ảo Python',
    'venv': 'môi trường ảo Python',
    '.tox': 'môi trường test Python',
    '.mypy_cache': 'cache kiểm tra kiểu',
    '.pytest_cache': 'cache test',
    '.gradle': 'cache build Gradle',
    'site-packages': 'thư viện Python cài tự động',
    # Vùng mã mẫu: không phải mã của chính dự án, nếu quét sẽ làm sai hồ sơ (vd. bật nhầm Frontend)
    'examples': 'mã ví dụ minh họa, không phải mã của dự án',
    'example': 'mã ví dụ minh họa, không phải mã của dự án',
    'fixtures': 'dữ liệu/mã mẫu cho test',
    'samples': 'mã mẫu, không phải mã của dự án',
}

# Thư mục mẫu theo đường dẫn tương đối (posix, so khớp từng đoạn bằng fnmatch).
SKIP_REL_PATTERNS = {
    'profiles/*/starter': 'mã khởi tạo mẫu của profile',
    'core/templates': 'mẫu tài liệu cấp cho dự án khác',
}

# SAFETY_IGNORE_DIRS: Thư mục thực sự bị bỏ qua khi quét an toàn prompt injection (tách riêng khỏi indexer).
# Bắt buộc đúng tập tên ở HEAD để không bỏ qua examples/, fixtures/, samples/, core/templates/.
SAFETY_IGNORE_DIRS = {
    'node_modules', '.git', 'dist', 'build', 'bin', 'obj', '.vscode', '.idea',
    '__pycache__', '.next', 'coverage', 'vendor', 'target', '.turbo', '.cache',
    '.venv', 'venv', '.tox', '.mypy_cache', '.pytest_cache', '.gradle', 'site-packages',
}

IGNORE_DIRS = set(SKIP_REASONS)

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py', '.go', '.java', '.rs', '.php'}

# Tệp văn bản mà Agent thường đọc: nơi kẻ xấu có thể cài lệnh (quét chống prompt injection)
TEXT_EXTENSIONS = {'.md', '.mdx', '.mdc', '.txt', '.json', '.html', '.htm', '.yaml', '.yml', '.toml', '.rst', '.xml'}
TEXT_FILENAMES = {'.cursorrules', '.windsurfrules', '.clinerules'}
# Tệp sinh tự động, rất lớn và nhiễu: không quét
SAFETY_SKIP_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock', 'poetry.lock', 'cargo.lock'}
SAFETY_MAX_BYTES = 1_000_000

# Tệp chỉ dẫn/cấu hình cho Agent: coi là chưa tin cậy nếu dự án không do người dùng tạo
AGENT_FILE_NAMES = {'agents.md', 'claude.md', 'gemini.md', '.cursorrules', '.windsurfrules', '.clinerules', '.mcp.json', 'skill.md'}
AGENT_DIR_MARKERS = ('.claude', '.agents', '.cursor', '.gemini', '.codex', '.windsurf', '.github/copilot')
ALLOWED_DOT_DIRS = {'.agents', '.claude', '.cursor', '.gemini', '.codex', '.windsurf', '.github', '.builder'}

# Tệp cấu hình/điểm vào nên đọc trước để nắm dự án nhanh
ENTRY_FILES = (
    'README.md', 'AGENTS.md', 'CLAUDE.md', 'package.json', 'pyproject.toml', 'requirements.txt', 'go.mod',
    'Cargo.toml', 'pom.xml', 'build.gradle', 'composer.json', 'Dockerfile', 'docker-compose.yml', 'Makefile',
    '.builder/kit.json',
)

# Tên tệp báo cáo xuất ra thư mục dự án được quét (cả người và Agent đều đọc)
REPORT_NAME = "project-review.md"
