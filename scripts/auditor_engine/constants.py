"""Shared constants of the Auditor Engine."""

# Folders that should never be read: generated or library copies (token cost, no review value).
# The value is a short reason, printed in the "Scan scope" section of project-review.md.
SKIP_REASONS = {
    'node_modules': 'auto-installed libraries (npm/yarn/pnpm)',
    '.git': 'git internal data',
    'dist': 'build output',
    'build': 'build output',
    'bin': 'build output/binaries',
    'obj': 'build output (.NET)',
    '.vscode': 'editor configuration',
    '.idea': 'editor configuration',
    '__pycache__': 'bytecode Python',
    '.next': 'cache build Next.js',
    'coverage': 'test coverage reports',
    'vendor': 'third-party libraries copied into the repo',
    'target': 'build output (Rust/Java)',
    '.turbo': 'cache build',
    '.cache': 'cache',
    '.venv': 'Python virtual environment',
    'venv': 'Python virtual environment',
    '.tox': 'Python test environment',
    '.mypy_cache': 'type-check cache',
    '.pytest_cache': 'cache test',
    '.gradle': 'cache build Gradle',
    'site-packages': 'auto-installed Python libraries',
    # Sample-code zone: not the project's own code; scanning it would distort the profile (e.g. wrongly enabling Frontend)
    'examples': "illustrative example code, not the project's code",
    'example': "illustrative example code, not the project's code",
    'fixtures': 'sample data/code for tests',
    'samples': "sample code, not the project's code",
}

# Sample folders by relative path (posix, matched segment by segment with fnmatch).
SKIP_REL_PATTERNS = {
    'profiles/*/starter': 'profile starter code',
    'core/templates': 'documentation templates issued for other projects',
}

# SAFETY_IGNORE_DIRS: folders really skipped by the prompt-injection safety scan (separate from the indexer).
# Must be exactly the set at HEAD so examples/, fixtures/, samples/, core/templates/ are not skipped.
SAFETY_IGNORE_DIRS = {
    'node_modules', '.git', 'dist', 'build', 'bin', 'obj', '.vscode', '.idea',
    '__pycache__', '.next', 'coverage', 'vendor', 'target', '.turbo', '.cache',
    '.venv', 'venv', '.tox', '.mypy_cache', '.pytest_cache', '.gradle', 'site-packages',
}

IGNORE_DIRS = set(SKIP_REASONS)

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py', '.go', '.java', '.rs', '.php'}

# Text files Agents usually read: where an attacker could plant commands (prompt-injection scan)
TEXT_EXTENSIONS = {'.md', '.mdx', '.mdc', '.txt', '.json', '.html', '.htm', '.yaml', '.yml', '.toml', '.rst', '.xml'}
TEXT_FILENAMES = {'.cursorrules', '.windsurfrules', '.clinerules'}
# Generated files, very large and noisy: not scanned
SAFETY_SKIP_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock', 'poetry.lock', 'cargo.lock'}
SAFETY_MAX_BYTES = 1_000_000

# Agent instruction/config files: treated as untrusted if the project was not created by the user
AGENT_FILE_NAMES = {'agents.md', 'claude.md', 'gemini.md', '.cursorrules', '.windsurfrules', '.clinerules', '.mcp.json', 'skill.md'}
AGENT_DIR_MARKERS = ('.claude', '.agents', '.cursor', '.gemini', '.codex', '.windsurf', '.github/copilot')
ALLOWED_DOT_DIRS = {'.agents', '.claude', '.cursor', '.gemini', '.codex', '.windsurf', '.github', '.builder'}

# Configuration/entry-point files worth reading first to grasp the project quickly
ENTRY_FILES = (
    'README.md', 'AGENTS.md', 'CLAUDE.md', 'package.json', 'pyproject.toml', 'requirements.txt', 'go.mod',
    'Cargo.toml', 'pom.xml', 'build.gradle', 'composer.json', 'Dockerfile', 'docker-compose.yml', 'Makefile',
    '.builder/kit.json',
)

# Name of the report file written into the scanned project folder (read by both humans and Agents)
REPORT_NAME = "project-review.md"
