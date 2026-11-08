"""
Kiểm tra vệ sinh repo, chuỗi cung ứng offline, cấu hình MCP và marker spec (logic thuần, chỉ dùng thư viện chuẩn).

Nguyên tắc:
- Chỉ phát hiện theo mẫu (heuristic). KHÔNG phát hiện ≠ an toàn; đây không phải antivirus và không tra cứu lỗ hổng.
- Không bao giờ trả về nội dung tệp: chỉ mã, tên tệp (đã làm sạch) và số lượng.
- Cần `git ls-files` để biết tệp nào đã bị commit; nếu không có git/không phải repo git thì bỏ qua các kiểm tra đó.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .safety import clean_path

GIT_TIMEOUT_SECONDS = 10
MAX_JSON_BYTES = 1_000_000
MAX_TEXT_BYTES = 200_000
MAX_LISTED = 5

# Gói MCP đã kiểm chứng bằng npm/GitHub API ngày 2026-11-07 (ghi lại trong TASKS.md, nhật ký 2026-11-07).
# Nguồn sự thật cho người đọc: profiles/agent-configs/curated-mcp-matrix.md (G-006).
KNOWN_BAD_MCP_PACKAGES = {
    "@modelcontextprotocol/server-playwright": "không tồn tại trên npm; dùng @playwright/mcp",
    "@modelcontextprotocol/server-github": "đã deprecated và archived; dùng github/github-mcp-server",
    "@modelcontextprotocol/server-postgres": "đã deprecated và archived; dùng crystaldba/postgres-mcp",
}

MCP_CONFIG_FILES = (
    ".mcp.json", ".cursor/mcp.json", ".vscode/mcp.json",
    ".claude/settings.json", ".claude/settings.local.json", ".gemini/settings.json",
)

ENV_SAFE_SUFFIXES = (".example", ".sample", ".template", ".dist", ".defaults")
PRIVATE_KEY_SUFFIXES = (".p12", ".pfx")
BINARY_SUFFIXES = (".exe", ".dll", ".so", ".dylib", ".msi", ".apk", ".jar", ".bin")
INSTALL_SCRIPT_KEYS = ("preinstall", "install", "postinstall")
SUSPICIOUS_INSTALL = re.compile(
    r"(curl|wget|invoke-webrequest|\biwr\b|certutil|bitsadmin|base64|\beval\b|\bnc\b|powershell|(?:ba)?sh\s+-c)|https?://",
    re.IGNORECASE,
)
UNPINNED_VERSIONS = {"", "*", "latest", "x"}
NEEDS_CLARIFICATION = re.compile(r"\[NEEDS CLARIFICATION", re.IGNORECASE)


@dataclass
class HygieneFinding:
    code: str
    message: str
    location: str = ""


def git_tracked_files(root: Path) -> list[str] | None:
    """Danh sách tệp đã được git theo dõi (đường dẫn tương đối, dấu /), hoặc None nếu không xác định được."""
    root = Path(root)
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True,
                                timeout=GIT_TIMEOUT_SECONDS, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return [p for p in result.stdout.decode("utf-8", "replace").split("\0") if p]


def _read_head(path: Path, limit: int = 2048) -> str:
    try:
        with open(path, "rb") as fh:
            return fh.read(limit).decode("utf-8", "replace")
    except OSError:
        return ""


def _summarize(names: list[str]) -> str:
    shown = ", ".join(clean_path(n) for n in names[:MAX_LISTED])
    more = len(names) - MAX_LISTED
    return shown + (f" và {more} tệp khác" if more > 0 else "")


TEST_PATH_SEGMENTS = {"tests", "test", "testing", "__tests__", "fixtures", "spec"}
SECRET_KEY_WORDS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASS", "PRIVATE", "CREDENTIAL", "DSN")
KNOWN_TOKEN_PREFIXES = (
    "ghp_", "gho_", "github_pat_", "sk-", "sk_live_", "pk_live_",
    "AKIA", "ASIA", "xoxb-", "xoxp-", "AIza", "glpat-",
)
URL_CREDENTIALS = re.compile(r"^[a-z][a-z0-9+.-]*://[^/:\s@]+:([^/@\s]+)@", re.IGNORECASE)


def _is_test_path(rel: str) -> bool:
    parts = set(rel.replace("\\", "/").lower().split("/"))
    return bool(parts & TEST_PATH_SEGMENTS)


def _is_placeholder_secret(val: str) -> bool:
    v = val.strip().strip("'\"")
    if not v:
        return True
    vl = v.lower()
    if "changeme" in vl:
        return True
    if re.match(r"^your[-_.]", v, re.IGNORECASE):
        return True
    if re.fullmatch(r"x+", vl):
        return True
    if v.startswith("<") and v.endswith(">"):
        return True
    return False


def _has_secret_in_env_file(path: Path) -> bool:
    try:
        content = _read_head(path, limit=32768)
    except OSError:
        return False
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, val = line.partition("=")
            key = key.strip().upper()
            val = val.strip()
            # 1. URL chứa credentials
            url_match = URL_CREDENTIALS.search(val)
            if url_match and not _is_placeholder_secret(url_match.group(1)):
                return True
            # 2. Token prefix nhận diện rõ ràng
            if any(val.startswith(p) for p in KNOWN_TOKEN_PREFIXES) and not _is_placeholder_secret(val):
                return True
            # 3. Tên key nhạy cảm và giá trị không phải placeholder
            if any(w in key for w in SECRET_KEY_WORDS) and not _is_placeholder_secret(val):
                return True
    return False


def check_tracked_files(root: Path, tracked: list[str] | None) -> list[HygieneFinding]:
    """SEC-005 (.env/khóa riêng bị commit), HYG-002 (log bị commit), SUP-004 (tệp thực thi/nhị phân bị commit)."""
    if tracked is None:
        return []
    root = Path(root)
    secrets, logs, binaries = [], [], []
    for rel in tracked:
        name = rel.rsplit("/", 1)[-1]
        lower = name.lower()
        is_test = _is_test_path(rel)
        if re.fullmatch(r"\.env(\..+)?", lower) and not lower.endswith(ENV_SAFE_SUFFIXES):
            if _has_secret_in_env_file(root / rel):
                secrets.append(rel)
        elif not is_test and (lower.endswith(PRIVATE_KEY_SUFFIXES) or (lower.startswith(("id_rsa", "id_ed25519", "id_ecdsa"))
                                                                       and not lower.endswith(".pub"))):
            secrets.append(rel)
        elif not is_test and lower.endswith((".pem", ".key")) and "PRIVATE KEY" in _read_head(root / rel):
            secrets.append(rel)
        elif lower.endswith(".log"):
            logs.append(rel)
        elif lower.endswith(BINARY_SUFFIXES):
            binaries.append(rel)

    out = []
    if secrets:
        out.append(HygieneFinding(
            "SEC-005", f"{len(secrets)} tệp có thể chứa bí mật đã bị commit vào git: {_summarize(secrets)}. "
                       "Xoay khóa/mật khẩu rồi gỡ khỏi lịch sử, thêm vào .gitignore.", clean_path(secrets[0])))
    if logs:
        out.append(HygieneFinding(
            "HYG-002", f"{len(logs)} tệp log đã bị commit: {_summarize(logs)}. Log dễ chứa token và dữ liệu cá nhân; "
                       "thêm *.log vào .gitignore.", clean_path(logs[0])))
    if binaries:
        out.append(HygieneFinding(
            "SUP-004", f"{len(binaries)} tệp thực thi/nhị phân nằm trong git: {_summarize(binaries)}. "
                       "Không thể đọc nội dung để kiểm; chỉ giữ khi có nguồn và checksum rõ ràng.",
            clean_path(binaries[0])))
    return out


def _load_json(path: Path) -> dict | None:
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            return None
        data = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _is_pinned_spec(spec: str) -> bool:
    spec = spec.strip()
    if spec.lower() in UNPINNED_VERSIONS:
        return False
    if re.match(r"^(https?://|git\+|git://|github:)", spec, re.IGNORECASE):
        return "#" in spec  # URL/git chỉ coi là ghim khi có commit/tag sau dấu #
    return True


def check_package_json(root: Path, package_files: list[Path]) -> list[HygieneFinding]:
    """SUP-001 (script cài đặt tải/chạy nội dung từ xa), SUP-002 (phụ thuộc không ghim phiên bản)."""
    install_hits, unpinned = [], []
    for path in package_files:
        data = _load_json(path)
        if not data:
            continue
        rel = path.relative_to(root).as_posix()
        scripts = data.get("scripts") if isinstance(data.get("scripts"), dict) else {}
        for key in INSTALL_SCRIPT_KEYS:
            cmd = scripts.get(key)
            if isinstance(cmd, str) and SUSPICIOUS_INSTALL.search(cmd):
                install_hits.append(f"{rel}:{key}")
        for section in ("dependencies", "devDependencies", "optionalDependencies"):
            deps = data.get(section)
            if not isinstance(deps, dict):
                continue
            for dep, spec in deps.items():
                if isinstance(spec, str) and not _is_pinned_spec(spec):
                    unpinned.append(f"{rel}:{dep}")

    out = []
    if install_hits:
        out.append(HygieneFinding(
            "SUP-001", f"{len(install_hits)} script cài đặt (preinstall/install/postinstall) tải hoặc thực thi nội dung "
                       f"từ xa hoặc mã hóa: {_summarize(install_hits)}. Script này chạy ngay khi cài đặt.",
            clean_path(install_hits[0].split(":")[0])))
    if unpinned:
        out.append(HygieneFinding(
            "SUP-002", f"{len(unpinned)} phụ thuộc không ghim phiên bản (*, latest, URL/git không kèm commit): "
                       f"{_summarize(unpinned)}.", clean_path(unpinned[0].split(":")[0])))
    return out


def check_requirements(root: Path, requirement_files: list[Path]) -> list[HygieneFinding]:
    """SUP-003 (index gói ngoài PyPI hoặc http thường: nguy cơ dependency confusion), SUP-002 (git+ không ghim)."""
    index_hits, unpinned = [], []
    for path in requirement_files:
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                continue
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        for line in lines:
            text = line.split("#", 1)[0].strip()
            m = re.match(r"^(?:--extra-index-url|--index-url|-i)[=\s]+(\S+)", text)
            if m:
                url = m.group(1).lower()
                if url.startswith("http://") or "pypi.org" not in url:
                    index_hits.append(rel)
            elif re.match(r"^(?:-e\s+)?git\+\S+", text) and "@" not in text.split("git+", 1)[1].split("://", 1)[-1]:
                unpinned.append(rel)

    out = []
    if index_hits:
        out.append(HygieneFinding(
            "SUP-003", f"requirements dùng index gói ngoài PyPI hoặc http thường ({_summarize(sorted(set(index_hits)))}): "
                       "gói trùng tên có thể bị lấy từ index khác.", clean_path(index_hits[0])))
    if unpinned:
        out.append(HygieneFinding(
            "SUP-002", f"requirements cài từ git không ghim commit/tag: {_summarize(sorted(set(unpinned)))}.",
            clean_path(unpinned[0])))
    return out


def _parse_npm_spec(arg: str) -> tuple[str, str]:
    m = re.match(r"^(@[^/@]+/[^@]+|[^@]+)(?:@(.+))?$", arg)
    return (m.group(1), m.group(2) or "") if m else (arg, "")


def check_mcp_configs(root: Path) -> list[HygieneFinding]:
    """AGT-004 (gói MCP không tồn tại/deprecated), AGT-005 (npx chạy gói không ghim phiên bản)."""
    root = Path(root)
    bad, unpinned = [], []
    for rel in MCP_CONFIG_FILES:
        path = root / rel
        data = _load_json(path) if path.is_file() else None
        if not data:
            continue
        servers = data.get("mcpServers") or data.get("servers")
        if not isinstance(servers, dict):
            continue
        for name, cfg in servers.items():
            if not isinstance(cfg, dict) or str(cfg.get("command", "")).lower() not in ("npx", "bunx"):
                continue
            args = [a for a in (cfg.get("args") or []) if isinstance(a, str)]
            pkg_arg = next((a for a in args if not a.startswith("-")), None)
            if not pkg_arg:
                continue
            pkg, version = _parse_npm_spec(pkg_arg)
            if pkg in KNOWN_BAD_MCP_PACKAGES:
                bad.append((rel, pkg, KNOWN_BAD_MCP_PACKAGES[pkg]))
            elif not version or version.lower() == "latest":
                unpinned.append((rel, pkg))

    out = []
    if bad:
        detail = "; ".join(f"{clean_path(p)} ({why})" for _r, p, why in bad[:MAX_LISTED])
        out.append(HygieneFinding("AGT-004", f"Cấu hình MCP dùng gói sai/lỗi thời: {detail}.", bad[0][0]))
    if unpinned:
        pkgs = ", ".join(clean_path(p) for _r, p in unpinned[:MAX_LISTED])
        out.append(HygieneFinding(
            "AGT-005", f"{len(unpinned)} máy chủ MCP chạy bằng npx không ghim phiên bản ({pkgs}): mỗi lần mở dự án "
                       "sẽ chạy bản mới nhất, kể cả bản bị chiếm quyền.", unpinned[0][0]))
    return out


def check_spec_markers(root: Path, markdown_files: list[Path]) -> list[HygieneFinding]:
    """SPEC-001: marker [NEEDS CLARIFICATION] còn sót trong spec/task (core/standards/feature-workflow.md)."""
    hits, first = [], ""
    for path in markdown_files:
        rel_parts = [p.lower() for p in path.relative_to(root).parts]
        if "templates" in rel_parts or not ({"specs", "spec", "tasks"} & set(rel_parts[:-1])):
            continue
        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                continue
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            if NEEDS_CLARIFICATION.search(line):
                rel = path.relative_to(root).as_posix()
                hits.append(rel)
                first = first or f"{rel}:{lineno}"
    if not hits:
        return []
    files = sorted(set(hits))
    return [HygieneFinding(
        "SPEC-001", f"{len(hits)} marker [NEEDS CLARIFICATION] còn sót trong {len(files)} tệp spec/task: "
                    f"{_summarize(files)}. Làm rõ với người dùng trước khi code.", clean_path(first))]


def run_hygiene_checks(root: Path, tree_files: list[Path]) -> list[HygieneFinding]:
    """Chạy toàn bộ kiểm tra; tree_files là danh sách tệp tuyệt đối từ ProjectTree (đã cắt thư mục rác)."""
    root = Path(root).resolve()
    findings = check_tracked_files(root, git_tracked_files(root))
    findings += check_package_json(root, [p for p in tree_files if p.name == "package.json"])
    findings += check_requirements(root, [p for p in tree_files if re.fullmatch(r"requirements.*\.txt", p.name)])
    findings += check_mcp_configs(root)
    findings += check_spec_markers(root, [p for p in tree_files if p.suffix.lower() == ".md"])
    return findings
