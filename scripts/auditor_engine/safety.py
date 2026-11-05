"""
Quét chống prompt injection trong tệp văn bản mà Agent sẽ đọc (md, json, html, txt, yaml...).

Nguyên tắc:
- Chỉ phát hiện tín hiệu theo mẫu (heuristic). KHÔNG phát hiện ≠ an toàn.
- KHÔNG BAO GIỜ trả về nội dung gốc của tệp: chỉ mã, vị trí và loại tín hiệu. Nếu không, chính
  báo cáo sẽ thành đường truyền lệnh độc tới Agent.
- Không quét mã nguồn (.py, .ts...) và không tìm virus: ngoài phạm vi.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    AGENT_DIR_MARKERS, AGENT_FILE_NAMES, IGNORE_DIRS, SAFETY_MAX_BYTES, SAFETY_SKIP_FILES,
    TEXT_EXTENSIONS, TEXT_FILENAMES,
)

# Tiêu đề cố định cho từng loại tín hiệu (không chứa nội dung từ tệp)
KINDS = {
    "SAFE-001": ("Cao", "Câu chữ ra lệnh cho AI/Agent nằm trong tệp dữ liệu"),
    "SAFE-002": ("Cao", "Ký tự ẩn (zero-width/bidi/tag) có thể giấu nội dung"),
    "SAFE-003": ("Cao", "Lệnh cho AI giấu trong chú thích HTML hoặc phần tử bị ẩn"),
    "SAFE-004": ("Trung bình", "Khối base64 dài trong tài liệu (có thể giấu nội dung mã hóa)"),
    "SAFE-005": ("Trung bình", "Cấu hình Agent có thể thực thi lệnh (hook/MCP)"),
}

# Lệnh nhắm vào AI: tiếng Anh và tiếng Việt. Khớp không phân biệt hoa thường.
_DIRECTIVE_PATTERNS = [
    r"ignore\s+(all\s+|any\s+|the\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|messages?)",
    r"disregard\s+(all\s+|any\s+|the\s+)?(previous|prior|above|earlier|your)\s+(instructions?|prompts?|rules?)",
    r"forget\s+(all\s+|everything\s+)?(previous|prior|above|your)\s+(instructions?|rules?)",
    r"(override|bypass)\s+(the\s+|your\s+)?(system\s+prompt|safety|guardrails?|instructions?)",
    r"you\s+are\s+now\s+(a|an|in)\b",
    r"new\s+(system\s+)?instructions?\s*:",
    r"(reveal|print|show|leak|exfiltrate|send)\s+(me\s+)?(your\s+|the\s+)?(system\s+prompt|api[\s_-]?keys?|secrets?|credentials|\.env|tokens?)",
    r"do\s+not\s+(tell|inform|mention\s+(this\s+)?to)\s+the\s+user",
    r"(without|don'?t)\s+(telling|asking|informing)\s+the\s+user",
    r"(as|if\s+you\s+are)\s+an?\s+(ai|llm|assistant|agent|language\s+model)\b.{0,60}\b(must|should|need\s+to|always)\b",
    r"(bỏ\s*qua|phớt\s*lờ|quên)\s+(tất\s+cả\s+|mọi\s+)?(các\s+)?(hướng\s*dẫn|chỉ\s*dẫn|lệnh|quy\s*tắc)\s+(trước|ở\s+trên|trước\s+đó)",
    r"(đừng|không\s+được|không\s+cần)\s+(nói|báo|cho)\s+(với\s+)?(người\s+dùng|user)\s+(biết)?",
    r"(từ\s+bây\s+giờ|bây\s+giờ)\s+bạn\s+là\b",
    r"(gửi|chuyển|đăng)\s+.{0,40}(api[\s_-]?key|mật\s*khẩu|token|biến\s+môi\s+trường|\.env)\s+.{0,30}(đến|tới|cho|lên)\b",
]
_DIRECTIVE = re.compile("|".join(f"(?:{p})" for p in _DIRECTIVE_PATTERNS), re.IGNORECASE)

# Ký tự ẩn: zero-width, bidi override/isolate, BOM giữa tệp, tag characters
_HIDDEN_CHARS = re.compile("[​-‏‪-‮⁠-⁤⁦-⁩﻿\U000e0000-\U000e007f]")

_HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
_HIDDEN_ELEMENT = re.compile(
    r"<[a-z][^>]*(?:display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0(?:px)?\b|hidden\b)[^>]*>(.*?)</[a-z0-9]+>",
    re.IGNORECASE | re.DOTALL,
)
_BASE64_BLOB = re.compile(r"(?<![A-Za-z0-9+/=,])[A-Za-z0-9+/]{300,}={0,2}(?![A-Za-z0-9+/=])")


@dataclass
class SafetyFinding:
    code: str
    file: str
    line: int
    severity: str
    title: str


@dataclass
class SafetyResult:
    findings: list[SafetyFinding]
    scanned: int = 0
    skipped_large: int = 0
    agent_files: list[str] = None

    def __post_init__(self):
        if self.agent_files is None:
            self.agent_files = []


def clean_path(text: str, limit: int = 160) -> str:
    """Làm sạch đường dẫn để in an toàn: tên tệp cũng có thể bị cài lệnh."""
    text = re.sub(r"[\x00-\x1f\x7f`|<>\[\]]", "?", text)
    text = _HIDDEN_CHARS.sub("?", text)
    return text if len(text) <= limit else text[:limit] + "…"


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _is_text_candidate(name: str) -> bool:
    lower = name.lower()
    return Path(lower).suffix in TEXT_EXTENSIONS or lower in TEXT_FILENAMES


def _is_agent_file(rel: str, name: str) -> bool:
    lower_rel = rel.lower()
    if name.lower() in AGENT_FILE_NAMES:
        return True
    return any(lower_rel == m or lower_rel.startswith(m + "/") for m in AGENT_DIR_MARKERS)


def _scan_text(rel: str, name: str, text: str, out: list[SafetyFinding]) -> None:
    suffix = Path(name.lower()).suffix
    markup = suffix in {".md", ".mdx", ".mdc", ".html", ".htm", ".xml", ".txt"}
    hidden_lines: set[int] = set()

    def add(code: str, line: int) -> None:
        severity, title = KINDS[code]
        out.append(SafetyFinding(code, rel, line, severity, title))

    # SAFE-003: lệnh giấu trong chú thích/phần tử ẩn
    if markup:
        for m in _HTML_COMMENT.finditer(text):
            if _DIRECTIVE.search(m.group(1)):
                line = _line_of(text, m.start())
                hidden_lines.add(line)
                add("SAFE-003", line)
        for m in _HIDDEN_ELEMENT.finditer(text):
            if _DIRECTIVE.search(m.group(1) or ""):
                line = _line_of(text, m.start())
                hidden_lines.add(line)
                add("SAFE-003", line)

    # SAFE-002: ký tự ẩn (gom mỗi dòng một lần)
    seen_hidden: set[int] = set()
    for m in _HIDDEN_CHARS.finditer(text):
        line = _line_of(text, m.start())
        if line not in seen_hidden:
            seen_hidden.add(line)
            add("SAFE-002", line)
        if len(seen_hidden) >= 20:
            break

    # SAFE-001: lệnh nhắm vào AI, mỗi dòng một lần, bỏ dòng đã tính là SAFE-003
    for lineno, content in enumerate(text.splitlines(), 1):
        if lineno in hidden_lines:
            continue
        if _DIRECTIVE.search(content):
            add("SAFE-001", lineno)

    # SAFE-004: base64 dài trong tài liệu (không áp cho json/yaml vì thường chứa dữ liệu hợp lệ)
    if suffix in {".md", ".mdx", ".mdc", ".txt", ".html", ".htm"}:
        for m in _BASE64_BLOB.finditer(text):
            add("SAFE-004", _line_of(text, m.start()))
            break


def _scan_agent_json(rel: str, text: str, out: list[SafetyFinding]) -> None:
    """Hook và máy chủ MCP có lệnh sẽ chạy trên máy người dùng khi Agent mở dự án."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return
    if not isinstance(data, dict):
        return
    risky = bool(data.get("hooks")) or any(
        isinstance(cfg, dict) and cfg.get("command")
        for cfg in (data.get("mcpServers") or {}).values()
        if isinstance(cfg, dict)
    )
    if risky:
        severity, title = KINDS["SAFE-005"]
        out.append(SafetyFinding("SAFE-005", rel, 1, severity, title))


def scan_safety(root: Path) -> SafetyResult:
    root = Path(root).resolve()
    findings: list[SafetyFinding] = []
    result = SafetyResult(findings)

    for dirpath, dirnames, filenames in os.walk(root):
        # Giữ thư mục ẩn (.claude, .github, .cursor...) vì đó là nơi chỉ dẫn Agent; bỏ thư mục rác
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            rel = clean_path(path.relative_to(root).as_posix())
            rel_raw = path.relative_to(root).as_posix()

            if _is_agent_file(rel_raw, name):
                result.agent_files.append(rel)

            if not _is_text_candidate(name) or name.lower() in SAFETY_SKIP_FILES:
                continue
            try:
                if path.stat().st_size > SAFETY_MAX_BYTES:
                    result.skipped_large += 1
                    continue
                text = path.read_text(encoding="utf-8-sig", errors="replace")  # bỏ BOM đầu tệp (hợp lệ)
            except OSError:
                continue

            result.scanned += 1
            _scan_text(rel, name, text, findings)
            if name.lower().endswith(".json") and _is_agent_file(rel_raw, name):
                _scan_agent_json(rel, text, findings)

    findings.sort(key=lambda f: ({"Cao": 0, "Trung bình": 1, "Thấp": 2}.get(f.severity, 9), f.file, f.line))
    result.agent_files.sort()
    return result
