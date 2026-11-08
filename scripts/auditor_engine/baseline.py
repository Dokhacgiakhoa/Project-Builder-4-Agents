"""
Kiểm tra Core Baseline (core/README.md): những thứ mọi repo làm việc với Agent phải có,
không phụ thuộc ngôn ngữ hay kiểu kiến trúc. Chạy trên hệ thống tệp, không cần đọc code.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# Profile kiến trúc khai báo -> dấu hiệu thư mục kỳ vọng (một trong các nhóm) trên đa ngôn ngữ (.NET/Python/TS).
PROFILE_EXPECTATIONS: dict[str, tuple[list[set[str]], str]] = {
    "clean-architecture": (
        [{"domain", "entities", "core"}, {"application", "usecases", "interactors", "infrastructure", "adapters"}],
        "A-002",
    ),
    "vertical-slice": (
        [{"features", "slices", "modules"}],
        "A-004",
    ),
    "modular-monolith": (
        [{"modules", "bounded-contexts", "domains", "packages"}],
        "A-005",
    ),
    "simple-layered": (
        [{"services", "routes", "controllers", "handlers", "api", "pages", "views", "models", "components"}],
        "A-001",
    ),
}

# Mức rào chắn mặc định theo profile nếu chưa khai báo tường minh trong .builder/kit.json
DEFAULT_PROFILE_GUARDRAIL = {
    "simple-layered": "M1",
    "vertical-slice": "M2",
    "clean-architecture": "M2",
    "modular-monolith": "M3",
}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def read_kit_config(root: Path) -> dict:
    """Đọc `.builder/kit.json`; trả {} nếu thiếu/hỏng (không bao giờ ném lỗi)."""
    cfg = root / ".builder" / "kit.json"
    if not cfg.is_file():
        return {}
    try:
        data = json.loads(_read(cfg))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def declared_architecture(kit_cfg: dict) -> str | None:
    value = (kit_cfg.get("profiles") or {}).get("architecture") if isinstance(kit_cfg.get("profiles"), dict) else None
    if not isinstance(value, str) or not value.strip() or "{{" in value:
        return None
    return value.strip().lower()


def declared_guardrail_level(kit_cfg: dict) -> str | None:
    """Lấy mức rào chắn M1/M2/M3 khai báo trong kit.json (hoặc suy ra từ profile tiêu chuẩn)."""
    raw = kit_cfg.get("guardrail_level") or (
        (kit_cfg.get("profiles") or {}).get("guardrails") if isinstance(kit_cfg.get("profiles"), dict) else None
    )
    if isinstance(raw, str) and raw.strip().upper() in {"M1", "M2", "M3"}:
        return raw.strip().upper()
    arch = declared_architecture(kit_cfg)
    return DEFAULT_PROFILE_GUARDRAIL.get(arch or "")


def check_baseline(root: Path) -> list[dict]:
    """Trả về danh sách {id, name, ok, detail} cho B1..B9."""
    root = Path(root)
    agents = _read(root / "AGENTS.md")
    has_agents = (root / "AGENTS.md").is_file()
    skills_dirs = [root / ".agents" / "skills", root / ".claude" / "skills"]
    has_skills = any(d.is_dir() and any(d.glob("*/SKILL.md")) for d in skills_dirs)
    claude = _read(root / "CLAUDE.md")

    adr_dirs = [root / "adrs", root / "docs" / "adr", root / "docs" / "adrs"]
    adr_files = [f for d in adr_dirs if d.is_dir() for f in d.glob("*.md") if not f.name.startswith("0000")]

    workflows = list((root / ".github" / "workflows").glob("*.y*ml")) if (root / ".github" / "workflows").is_dir() else []
    unresolved = "{{" in agents

    items = [
        ("B1", "AGENTS.md (chỉ dẫn Agent)", has_agents, "Thiếu AGENTS.md" if not has_agents else ""),
        ("B2", "Lớp tương thích Agent (CLAUDE.md + skills)",
         bool(claude) and has_skills,
         "Thiếu CLAUDE.md" if not claude else ("Thiếu skills (.agents/skills hoặc .claude/skills có */SKILL.md)" if not has_skills else "")),
        ("B3", "docs/project-brief.md", (root / "docs" / "project-brief.md").is_file(), "Thiếu docs/project-brief.md"),
        ("B4", "Nhật ký quyết định (adrs/ có ADR thật)", bool(adr_files), "Chưa có ADR nào ngoài mẫu"),
        ("B5", "Chuẩn làm việc (docs/standards/)",
         (root / "docs" / "standards" / "coding-conventions.md").is_file()
         and (root / "docs" / "standards" / "definition-of-done.md").is_file(),
         "Thiếu docs/standards/coding-conventions.md hoặc definition-of-done.md"),
        ("B6", "Lệnh kiểm chứng đã điền + CI chạy được",
         has_agents and not unresolved and bool(workflows),
         "AGENTS.md còn {{PLACEHOLDER}}" if unresolved else ("Thiếu workflow CI trong .github/workflows/" if not workflows else "")),
        ("B7", "Vệ sinh repo (.gitignore, .env.example)",
         (root / ".gitignore").is_file() and (root / ".env.example").is_file(),
         "Thiếu .gitignore hoặc .env.example"),
        ("B8", "Hồ sơ kit (.builder/kit.json)", (root / ".builder" / "kit.json").is_file(), "Thiếu .builder/kit.json"),
        ("B9", "Quy trình PR (PULL_REQUEST_TEMPLATE)",
         (root / ".github" / "PULL_REQUEST_TEMPLATE.md").is_file(), "Thiếu .github/PULL_REQUEST_TEMPLATE.md"),
    ]
    return [{"id": i, "name": n, "ok": bool(ok), "detail": "" if ok else d} for i, n, ok, d in items]


def check_declared_profile(root: Path, all_dirs: set[str], declared: str | None) -> tuple[bool, str, str | None]:
    """So khớp profile khai báo với cấu trúc thư mục. Trả (ok, thông điệp, doc_id)."""
    if not declared:
        return True, "", None
    expectation = PROFILE_EXPECTATIONS.get(declared)
    if not expectation:
        return True, "", None  # profile tùy biến: không đánh giá
    groups, doc_id = expectation
    dirs = {d.lower() for d in all_dirs}
    missing = [sorted(g)[0] for g in groups if not (g & dirs)]
    if missing:
        return False, (f"Dự án khai báo profile `{declared}` nhưng cấu trúc thư mục chưa thấy dấu hiệu tương ứng "
                       f"(chưa có thư mục kiểu: {', '.join(missing)})."), doc_id
    return True, "", doc_id


def check_guardrails(root: Path, kit_cfg: dict) -> tuple[bool, str, list[str]]:
    """
    Kiểm tra ARCH-008: dự án khai báo profile/mức rào chắn M1-M3 nhưng thiếu công cụ kiểm soát ranh giới hoặc CI.
    Trả về (ok, message, doc_ids).
    """
    root = Path(root)
    declared_arch = declared_architecture(kit_cfg)
    explicit_level = kit_cfg.get("guardrail_level") or (
        (kit_cfg.get("profiles") or {}).get("guardrails") if isinstance(kit_cfg.get("profiles"), dict) else None
    )
    level = declared_guardrail_level(kit_cfg)
    if not level:
        return True, "", []

    # Nếu chỉ khai báo profile (không khai báo guardrail_level tường minh) và chưa có mã nguồn/cấu trúc profile -> để ARCH-007 xử lý trước
    if not explicit_level and declared_arch in PROFILE_EXPECTATIONS:
        workflows_dir = root / ".github" / "workflows"
        if not workflows_dir.is_dir():
            return True, "", []

    workflows_dir = root / ".github" / "workflows"
    workflows = list(workflows_dir.glob("*.y*ml")) if workflows_dir.is_dir() else []
    if not workflows:
        return (
            False,
            f"Dự án yêu cầu mức rào chắn `{level}` nhưng chưa có workflow CI tự động trong `.github/workflows/`.",
            ["K-004", "S-002"],
        )

    if level in ("M2", "M3"):
        # Kiểm tra dấu hiệu rào chắn ranh giới (boundary lint rules, import-linter, eslint boundary, nhiều .csproj, hoặc test kiến trúc)
        has_boundary_guard = False
        boundary_patterns = re.compile(
            r"(no-restricted-imports|boundaries|eslint-plugin-boundaries|import-linter|depcruiser|archunit|netarchtest|enforce-module-boundaries|check_links|test_doc_format|test_health_check)",
            re.IGNORECASE,
        )

        # Kiểm tra các tệp cấu hình lint / test / csproj
        candidate_files = [
            root / "package.json",
            root / "pyproject.toml",
            root / ".eslintrc.js",
            root / ".eslintrc.cjs",
            root / ".eslintrc.json",
            root / "eslint.config.js",
            root / "eslint.config.mjs",
            root / ".importlinter",
        ]
        candidate_files.extend(workflows)
        if (root / "tests").is_dir():
            candidate_files.extend((root / "tests").glob("test_*.py"))

        csproj_files = list(root.rglob("*.csproj"))
        if len(csproj_files) >= 2:
            has_boundary_guard = True

        if not has_boundary_guard:
            for cf in candidate_files:
                if cf.is_file() and boundary_patterns.search(_read(cf)):
                    has_boundary_guard = True
                    break

        if not has_boundary_guard:
            doc_id = PROFILE_EXPECTATIONS.get(declared_arch or "", ([], "K-004"))[1]
            return (
                False,
                f"Dự án khai báo mức rào chắn `{level}` ({declared_arch or 'custom'}) nhưng thiếu rào chắn kiểm soát ranh giới kiến trúc (luật chặn import chéo, tách project, hoặc test kiến trúc trong CI).",
                ["K-004", doc_id] if doc_id != "K-004" else ["K-004", "S-002"],
            )

    return True, "", []


AGENT_MARKER_FILES = ("AGENTS.md", "CLAUDE.md", ".cursorrules", ".windsurfrules")
AGENT_MARKER_DIRS = (".agents", ".claude")


def is_agent_driven(root: Path) -> bool:
    root = Path(root)
    if any((root / f).is_file() for f in AGENT_MARKER_FILES):
        return True
    if any((root / d).is_dir() for d in AGENT_MARKER_DIRS):
        return True
    return False


WORKLOG_FILES = ("docs/worklog.md", "WORKLOG.md", "worklog.md")
_DATED_ENTRY = re.compile(r"^(?:#{1,6}\s*|[-*]\s*|\|\s*)\[?\d{4}-\d{2}-\d{2}", re.MULTILINE)


def check_worklog(root: Path) -> tuple[str | None, str]:
    """
    Kiểm tra work log (core/standards/worklog.md). Trả về (mã, thông điệp); mã None nghĩa là đạt.
    WLOG-001/002 chỉ kích hoạt khi dự án có marker Agent (AGENTS.md, CLAUDE.md, .cursorrules, .windsurfrules, .agents/, .claude/).
    Không đánh giá độ mới (mtime đổi khi git clone nên không đáng tin khi chạy offline).
    """
    root = Path(root)
    if not is_agent_driven(root):
        return None, ""
    candidates = [root / rel for rel in WORKLOG_FILES]
    folder = root / "docs" / "worklog"
    if folder.is_dir():
        candidates.extend(sorted(folder.glob("*.md")))
    files = [p for p in candidates if p.is_file()]
    if not files:
        return "WLOG-001", "Chưa có work log (docs/worklog.md): phiên Agent sau không biết đã làm gì và còn gì dở."
    for p in files:
        try:
            if _DATED_ENTRY.search(p.read_text(encoding="utf-8-sig", errors="replace")):
                return None, ""
        except OSError:
            continue
    return "WLOG-002", "Work log đã có nhưng chưa có mục nào bắt đầu bằng ngày (YYYY-MM-DD)."
