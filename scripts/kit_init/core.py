"""Core Engine khởi tạo dự án từ Starter Kit (thuần logic, không phụ thuộc UI/CLI)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import templates

# Luôn được copy nguyên bản.
BASE_PATHS = [
    "AGENTS.md", "adrs", "specs", "planning", "tasks",
    "docs/guides", "docs/system-architecture.md", "docs/deployment-guide.md",
    "src", "tests", ".github", ".editorconfig", ".gitignore", ".env.example",
]

# Bật bằng cờ tương ứng.
OPTIONAL_PATHS = {
    "frontend": ["frontend"],
    "docker": ["docker-compose.yml"],
    "pitch": ["templates/pitch-deck"],
}

# Tệp được sinh mới thay cho bản của Starter Kit (không áp dụng cho dự án khác).
GENERATED = ("README.md", "Makefile", ".github/workflows/ci.yml")

EXCLUDED_DIR_NAMES = {"node_modules", "dist", "__pycache__", ".git", "bin", "obj", ".turbo", ".cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

NAME_PATTERN = re.compile(r"^[^\x00-\x1f<>:\"/\\|?*]{1,100}$")


class InitError(Exception):
    """Lỗi người dùng có thể sửa được (thư mục không rỗng, tên không hợp lệ...)."""


@dataclass
class Action:
    dst: str                      # đường dẫn tương đối trong dự án mới
    src: Path | None = None       # copy từ tệp này...
    content: str | None = None    # ...hoặc ghi nội dung này


@dataclass
class Result:
    created: list[str] = field(default_factory=list)
    overwritten: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def default_kit_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def validate_name(name: str) -> str:
    name = (name or "").strip()
    if not NAME_PATTERN.match(name):
        raise InitError("Tên dự án không hợp lệ (1-100 ký tự, không chứa < > : \" / \\ | ? *).")
    return name


def _iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for p in sorted(path.rglob("*")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(path).parts
        if any(part in EXCLUDED_DIR_NAMES for part in rel_parts):
            continue
        if p.suffix in EXCLUDED_SUFFIXES:
            continue
        yield p


def build_plan(kit_root: Path, name: str, *, frontend=False, docker=False, pitch=False) -> list[Action]:
    kit_root = Path(kit_root)
    wanted = list(BASE_PATHS)
    for flag, paths in OPTIONAL_PATHS.items():
        if {"frontend": frontend, "docker": docker, "pitch": pitch}[flag]:
            wanted += paths

    actions: dict[str, Action] = {}
    for rel in wanted:
        src = kit_root / rel
        if not src.exists():
            raise InitError(f"Starter Kit thiếu '{rel}' (kit_root={kit_root}).")
        for f in _iter_files(src):
            dst = f.relative_to(kit_root).as_posix()
            if dst in GENERATED:
                continue
            actions[dst] = Action(dst=dst, src=f)

    vision = actions.get("specs/product-vision.md")
    if vision is not None and vision.src is not None:
        text = vision.src.read_text(encoding="utf-8")
        first, sep, rest = text.partition("\n")
        actions[vision.dst] = Action(dst=vision.dst, content=f"{first.rstrip()} — {name}{sep}{rest}")

    actions["README.md"] = Action("README.md", content=templates.README.format(name=name))
    actions["Makefile"] = Action("Makefile", content=templates.MAKEFILE.format())
    actions[".github/workflows/ci.yml"] = Action(".github/workflows/ci.yml", content=templates.CI)
    return list(actions.values())


def check_target(target: Path, *, force: bool, merge: bool) -> None:
    if target.exists() and not target.is_dir():
        raise InitError(f"'{target}' tồn tại nhưng không phải thư mục.")
    if target.is_dir() and any(target.iterdir()) and not (force or merge):
        raise InitError(
            f"Thư mục '{target}' không rỗng. Dùng --merge để chỉ thêm tệp còn thiếu (không ghi đè), "
            "hoặc --force để ghi đè các tệp trùng tên."
        )


def apply_plan(plan: list[Action], target: Path, *, force=False, merge=False, dry_run=False) -> Result:
    target = Path(target)
    check_target(target, force=force, merge=merge)
    result = Result()
    root = target.resolve()

    for action in plan:
        dst = (root / action.dst).resolve()
        if root != dst and root not in dst.parents:
            raise InitError(f"Đường dẫn đích nằm ngoài dự án: {action.dst}")

        exists = dst.exists()
        if exists and not force:
            result.skipped.append(action.dst)
            continue
        (result.overwritten if exists else result.created).append(action.dst)
        if dry_run:
            continue

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if action.content is not None:
                dst.write_text(action.content, encoding="utf-8", newline="\n")
            elif action.src is not None:
                dst.write_bytes(action.src.read_bytes())
        except OSError as e:
            raise InitError(f"Không ghi được '{action.dst}': {e}") from e
    return result


def init_project(target, name=None, *, kit_root=None, frontend=False, docker=False, pitch=False,
                 force=False, merge=False, dry_run=False) -> Result:
    target = Path(target)
    project_name = validate_name(name if name else (target.resolve().name or "my-project"))
    plan = build_plan(Path(kit_root) if kit_root else default_kit_root(), project_name,
                      frontend=frontend, docker=docker, pitch=pitch)
    return apply_plan(plan, target, force=force, merge=merge, dry_run=dry_run)
