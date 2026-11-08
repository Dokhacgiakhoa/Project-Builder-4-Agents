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
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    AGENT_DIR_MARKERS, AGENT_FILE_NAMES, SAFETY_IGNORE_DIRS, SAFETY_MAX_BYTES, SAFETY_SKIP_FILES,
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
    r"forget\s+(all\s+|everything\s+)?((all\s+)?your\s+)?(previous|prior|above|your)\s+(instructions?|rules?|prompts?)",
    r"(override|bypass)\s+(the\s+|your\s+)?(system\s+prompt|safety|guardrails?|instructions?)",
    r"you\s+are\s+now\s+(a|an|in)\b",
    r"new\s+(system\s+)?instructions?\s*:",
    r"(reveal|print|show|leak|exfiltrate|send)\s+(me\s+)?(your\s+|the\s+)?(system\s+prompt|api[\s_-]?keys?|secrets?|credentials|\.env|tokens?)",
    r"do\s+not\s+(tell|inform|mention\s+(this\s+)?to)\s+the\s+user",
    r"(without|don'?t)\s+(telling|asking|informing)\s+the\s+user",
    r"(as|if\s+you\s+are)\s+an?\s+(ai|llm|assistant|agent|language\s+model)\b.{0,60}\b(must|should|need\s+to|always)\b",
    r"(bỏ\s*qua|phớt\s*lờ|quên)\s+(tất\s+cả\s+|mọi\s+)?(các\s+)?(hướng\s*dẫn|chỉ\s*dẫn|lệnh|quy\s*tắc)\s+(trước|ở\s+trên|trước\s+đó)",
    r"(đừng|không\s+được|không\s+cần)\s+(nói|báo|cho)\s+(cho\s+|với\s+)?(người\s+dùng|user)\s*(biết)?",
    r"(từ\s+bây\s+giờ|bây\s+giờ)\s+bạn\s+là\b",
    r"(gửi|chuyển|đăng)\s+.{0,40}(api[\s_-]?key|mật\s*khẩu|token|biến\s+môi\s+trường|\.env)\s+.{0,30}(đến|tới|cho|lên)\b",
]
_DIRECTIVE = re.compile("|".join(f"(?:{p})" for p in _DIRECTIVE_PATTERNS), re.IGNORECASE)

_DIRECTIVE_GATE_PATTERN_COUNT = 14


def _normalize_for_gate(text: str) -> str:
    """Chuan hoa ky tu truoc khi kiem tra pregate (anh xa U+0130 va U+0131 ve i roi casefold)."""
    return text.replace("\u0130", "i").replace("\u0131", "i").casefold()


def directive_pregate(folded: str) -> bool:
    """Kiểm tra nhanh từ khóa thô trên chuỗi đã casefold() trước khi chạy regex nặng."""
    # Pattern 0: ignore ... (previous|prior|above|earlier) ... (instruction|prompt|rule|message)
    if "ignore" in folded:
        if "previous" in folded or "prior" in folded or "above" in folded or "earlier" in folded:
            if "instruction" in folded or "prompt" in folded or "rule" in folded or "message" in folded:
                return True

    # Pattern 1: disregard ... (previous|prior|above|earlier|your) ... (instruction|prompt|rule)
    if "disregard" in folded:
        if "previous" in folded or "prior" in folded or "above" in folded or "earlier" in folded or "your" in folded:
            if "instruction" in folded or "prompt" in folded or "rule" in folded:
                return True

    # Pattern 2: forget ... (previous|prior|above|your) ... (instruction|rule|prompt)
    if "forget" in folded:
        if "previous" in folded or "prior" in folded or "above" in folded or "your" in folded:
            if "instruction" in folded or "rule" in folded or "prompt" in folded:
                return True

    # Pattern 3: (override|bypass) ... (system|safety|guardrail|instruction)
    if "override" in folded or "bypass" in folded:
        if "system" in folded or "safety" in folded or "guardrail" in folded or "instruction" in folded:
            return True

    # Pattern 4: you are now (a|an|in)
    if "you" in folded and "are" in folded and "now" in folded:
        return True

    # Pattern 5: new (system )?instruction :
    if "new" in folded and "instruction" in folded and ":" in folded:
        return True

    # Pattern 6: (reveal|print|show|leak|exfiltrate|send) ... (system|api|secret|credential|.env|token)
    if ("reveal" in folded or "print" in folded or "show" in folded or "leak" in folded
            or "exfiltrate" in folded or "send" in folded):
        if ("system" in folded or "api" in folded or "secret" in folded
                or "credential" in folded or ".env" in folded or "token" in folded):
            return True

    # Pattern 7: do not (tell|inform|mention) the user
    if "user" in folded:
        if "do" in folded and "not" in folded:
            if "tell" in folded or "inform" in folded or "mention" in folded:
                return True
        # Pattern 8: (without|don't|dont) (telling|asking|informing) the user
        if "without" in folded or "don't" in folded or "dont" in folded:
            if "telling" in folded or "asking" in folded or "informing" in folded:
                return True

    # Pattern 9: (as|if you are) an (ai|llm|assistant|agent|language model) ... (must|should|need to|always)
    if ("ai" in folded or "llm" in folded or "assistant" in folded or "agent" in folded or "language" in folded):
        if "must" in folded or "should" in folded or "need" in folded or "always" in folded:
            return True

    # Vietnamese patterns
    # Pattern 10: (bỏ qua|phớt lờ|quên) ... (hướng dẫn|chỉ dẫn|lệnh|quy tắc) ... (trước|trên)
    if "trước" in folded or "trên" in folded:
        if "bỏ" in folded or "phớt" in folded or "quên" in folded:
            if "hướng" in folded or "chỉ" in folded or "lệnh" in folded or "quy" in folded:
                return True

    # Pattern 11: (đừng|không) ... (nói|báo|cho) ... (người|user)
    if "người" in folded or "user" in folded:
        if "đừng" in folded or "không" in folded:
            if "nói" in folded or "báo" in folded or "cho" in folded:
                return True

    # Pattern 12: (từ bây giờ|bây giờ) bạn là
    if "bây" in folded and "giờ" in folded and "bạn" in folded and "là" in folded:
        return True

    # Pattern 13: (gửi|chuyển|đăng) ... (api|mật khẩu|token|biến|env) ... (đến|tới|cho|lên)
    if "gửi" in folded or "chuyển" in folded or "đăng" in folded:
        if "đến" in folded or "tới" in folded or "cho" in folded or "lên" in folded:
            if ("api" in folded or "mật" in folded or "token" in folded
                    or "biến" in folded or ".env" in folded or "env" in folded):
                return True

    return False


# Directive bổ sung chỉ áp dụng cho chú thích HTML / phần tử ẩn (SAFE-003):
# Trong phần tử ẩn, việc ra lệnh mà không có danh từ (ví dụ "forget everything previous")
# là dấu hiệu tiêm nhiễm rõ rệt vì văn bản đã bị cố tình giấu khỏi mắt người dùng.
_HIDDEN_DIRECTIVE = re.compile(
    r"forget\s+(all\s+|everything\s+)?(previous|prior|above|earlier)\b",
    re.IGNORECASE,
)


def _directive_matches(text: str, in_hidden: bool = False) -> bool:
    """Ket hop tien loc (pre-gate) tren chuoi da chuan hoa truoc khi chay regex day du."""
    if not text.isascii():
        text = unicodedata.normalize("NFC", text)
    folded = _normalize_for_gate(text)
    if directive_pregate(folded):
        if bool(_DIRECTIVE.search(text)):
            return True
    if in_hidden:
        if "forget" in folded and ("previous" in folded or "prior" in folded or "above" in folded or "earlier" in folded):
            if bool(_HIDDEN_DIRECTIVE.search(text)):
                return True
    return False

# Ký tự ẩn: zero-width, bidi override/isolate, BOM giữa tệp, tag characters
_HIDDEN_CHARS = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]")

# Tập hợp tất cả ký tự ẩn (để kiểm tra độ cô lập và chuỗi liên tiếp)
_ALL_INVISIBLE_CHARS = set(
    [chr(c) for c in range(0x200B, 0x2010)]
    + [chr(c) for c in range(0x202A, 0x202F)]
    + [chr(c) for c in range(0x2060, 0x2065)]
    + [chr(c) for c in range(0x2066, 0x206A)]
    + ["\uFEFF"]
    + [chr(c) for c in range(0xE0000, 0xE0080)]
)

# Ký tự có thể được xem xét miễn trừ trong ngữ cảnh hợp lệ (ZWNJ, ZWJ, LRM, RLM)
_EXEMPTION_CANDIDATES = {"\u200c", "\u200d", "\u200e", "\u200f"}

# Mẫu ký tự lân cận hợp lệ: Emoji, Indic, Arabic/Persian, CJK (Item 5 / ADR-0016)
_EMOJI_PATTERN = r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2300-\u23FF\u2B50\u2B55\u25A0-\u25FF\uFE0E\uFE0F\U0001F1E6-\U0001F1FF]"
_INDIC_PATTERN = r"[\u0900-\u0DFF\u1CD0-\u1CFF\uA8E0-\uA8FF]"
_ARABIC_PATTERN = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFE]"
_CJK_PATTERN = r"[\u4E00-\u9FFF\u3400-\u4DBF\u2E80-\u30FF\u3100-\u318F\uAC00-\uD7AF\uF900-\uFAFF\U00020000-\U0002EBEF]"
_VALID_NEIGHBOR = re.compile(
    f"^(?:{_EMOJI_PATTERN}|{_INDIC_PATTERN}|{_ARABIC_PATTERN}|{_CJK_PATTERN})$"
)

# Ngưỡng mật độ tối đa ký tự ẩn được miễn trừ trong 1 tệp văn bản (chống steganography phân tán)
_MAX_EXEMPTED_CHARS = 20

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
            if _directive_matches(m.group(1), in_hidden=True):
                line = _line_of(text, m.start())
                hidden_lines.add(line)
                add("SAFE-003", line)
        for m in _HIDDEN_ELEMENT.finditer(text):
            if _directive_matches(m.group(1) or "", in_hidden=True):
                line = _line_of(text, m.start())
                hidden_lines.add(line)
                add("SAFE-003", line)

    # SAFE-002: ký tự ẩn (ngữ cảnh: miễn trừ ZWJ/ZWNJ/LRM/RLM đơn lẻ giữa emoji/Indic/Arabic/CJK)
    seen_hidden: set[int] = set()
    exempted_positions: list[int] = []
    textlen = len(text)

    for m in _HIDDEN_CHARS.finditer(text):
        idx = m.start()
        ch = m.group()

        # U+FEFF (BOM) ở đầu tệp là hợp lệ
        if ch == "\ufeff" and idx == 0:
            continue

        # Kiểm tra chuỗi liền kề 3+ ký tự ẩn
        b_count = 0
        p = idx - 1
        while p >= 0 and text[p] in _ALL_INVISIBLE_CHARS:
            b_count += 1
            p -= 1
        f_count = 0
        p = idx + 1
        while p < textlen and text[p] in _ALL_INVISIBLE_CHARS:
            f_count += 1
            p += 1

        if b_count + 1 + f_count >= 3:
            line = _line_of(text, idx)
            if line not in seen_hidden:
                seen_hidden.add(line)
                add("SAFE-002", line)
            if len(seen_hidden) >= 20:
                break
            continue

        # Nếu là ứng viên miễn trừ (ZWJ, ZWNJ, LRM, RLM)
        if ch in _EXEMPTION_CANDIDATES:
            is_isolated = (idx == 0 or text[idx - 1] not in _ALL_INVISIBLE_CHARS) and (
                idx == textlen - 1 or text[idx + 1] not in _ALL_INVISIBLE_CHARS
            )
            if is_isolated and idx > 0 and idx < textlen - 1:
                prev_c = text[idx - 1]
                next_c = text[idx + 1]
                if _VALID_NEIGHBOR.match(prev_c) and _VALID_NEIGHBOR.match(next_c):
                    exempted_positions.append(idx)
                    continue

        # Không thỏa điều kiện miễn trừ -> gắn cờ
        line = _line_of(text, idx)
        if line not in seen_hidden:
            seen_hidden.add(line)
            add("SAFE-002", line)
        if len(seen_hidden) >= 20:
            break

    # Quy tắc mật độ: tệp có hơn 20 ký tự ẩn được miễn trừ -> kích hoạt cảnh báo SAFE-002
    if len(exempted_positions) > _MAX_EXEMPTED_CHARS and len(seen_hidden) < 20:
        line_21 = _line_of(text, exempted_positions[_MAX_EXEMPTED_CHARS])
        if line_21 not in seen_hidden:
            seen_hidden.add(line_21)
            add("SAFE-002", line_21)

    # SAFE-001: lệnh nhắm vào AI, mỗi dòng một lần, bỏ dòng đã tính là SAFE-003
    for lineno, content in enumerate(text.splitlines(), 1):
        if lineno in hidden_lines:
            continue
        if _directive_matches(content):
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


def scan_safety(root: Path, on_progress=None) -> SafetyResult:
    root = Path(root).resolve()
    findings: list[SafetyFinding] = []
    result = SafetyResult(findings)

    root_str = str(root)
    root_len = len(root_str)
    for dirpath, dirnames, filenames in os.walk(root):
        # Giữ thư mục ẩn (.claude, .github, .cursor...) vì đó là nơi chỉ dẫn Agent; bỏ thư mục rác
        dirnames[:] = [d for d in dirnames if d not in SAFETY_IGNORE_DIRS]
        rel_dir = dirpath[root_len:].lstrip('\\/').replace('\\', '/')
        for name in filenames:
            rel_raw = f'{rel_dir}/{name}' if rel_dir else name
            rel = clean_path(rel_raw)
            path = Path(dirpath) / name

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
            if on_progress and result.scanned % 200 == 0:
                on_progress(result.scanned)
            _scan_text(rel, name, text, findings)
            if name.lower().endswith(".json") and _is_agent_file(rel_raw, name):
                _scan_agent_json(rel, text, findings)

    findings.sort(key=lambda f: ({"Cao": 0, "Trung bình": 1, "Thấp": 2}.get(f.severity, 9), f.file, f.line))
    result.agent_files.sort()
    return result
