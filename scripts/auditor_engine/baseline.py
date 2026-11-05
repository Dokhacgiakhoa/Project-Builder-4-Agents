"""
Kiểm tra Core Baseline (core/README.md): những thứ mọi repo làm việc với Agent phải có,
không phụ thuộc ngôn ngữ hay kiểu kiến trúc. Chạy trên hệ thống tệp, không cần đọc code.
"""

from __future__ import annotations

import json
from pathlib import Path

# Profile kiến trúc khai báo -> dấu hiệu thư mục kỳ vọng (một trong các nhóm).
PROFILE_EXPECTATIONS: dict[str, tuple[list[set[str]], str]] = {
    "clean-architecture": ([{"domain", "entities", "core"}, {"application", "usecases", "interactors", "infrastructure", "adapters"}], "A-002"),
    "vertical-slice": ([{"features", "slices"}], "A-004"),
    "modular-monolith": ([{"modules"}], "A-005"),
    "simple-layered": ([{"services", "routes", "controllers", "handlers", "api", "pages"}], "A-001"),
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
