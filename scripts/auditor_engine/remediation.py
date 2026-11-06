"""
Ánh xạ phát hiện của Health Check → mã ổn định, mức độ và tài liệu khắc phục trong Project-Builder-4-Agents.

Agent đọc `project-review.md`, thấy mã + liên kết tài liệu, rồi tra đúng tài liệu để sửa.
Danh sách DOCS phải khớp `INDEX.md` của kit (có test kiểm tra mỗi đường dẫn đều tồn tại).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

KIT_REPO = "https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents"
DEFAULT_REF = "main"

# id -> (đường dẫn trong kit, tiêu đề). Trùng ID với INDEX.md.
DOCS: dict[str, tuple[str, str]] = {
    "K-001": ("BOOTSTRAP.md", "Quy trình Bootstrap dự án cho AI Agent"),
    "K-002": ("core/discovery.md", "Phỏng vấn Discovery & khóa phạm vi dự án"),
    "K-003": ("core/README.md", "Core Baseline: chuẩn tối thiểu cho mọi repo dùng Agent"),
    "K-004": ("profiles/README.md", "Chọn profile kiến trúc & mức rào chắn M1-M3"),
    "K-005": ("scripts/README.md", "Project Health Check: bộ thanh tra tĩnh & rào chắn"),
    "K-006": ("core/untrusted-content.md", "Nội dung chưa tin cậy & chống prompt injection"),
    "K-007": ("HOW_IT_WORKS.md", "Cơ chế Zero-Clone & Hosted Agent Brain"),
    "S-001": ("core/standards/coding-conventions.md", "Quy ước code & phòng vệ crash"),
    "S-002": ("core/standards/test-strategy.md", "Chiến lược kiểm thử"),
    "S-003": ("core/standards/definition-of-done.md", "Definition of Done"),
    "S-008": ("core/standards/feature-workflow.md", "Staged feature workflow with verification gates"),
    "S-004": ("knowledge-base/tu-duy/anti-patching-architectural-thinking.md", "Tư duy chống vá víu & ngắt mạch"),
    "S-006": ("profiles/playbooks/anti-doom-loop-guide.md", "Playbook chống vòng lặp Doom Loop cho Agent"),
    "S-007": ("profiles/playbooks/living-documentation-sync.md", "Tài liệu sống & đồng bộ tự động 4 lớp"),
    "A-001": ("profiles/architecture/simple-layered.md", "Profile Layered đơn giản"),
    "A-002": ("profiles/architecture/clean-architecture.md", "Profile Clean Architecture"),
    "A-003": ("profiles/architecture/clean-architecture-layout.md", "Cấu trúc thư mục Clean Architecture đa ngôn ngữ"),
    "A-004": ("profiles/architecture/vertical-slice.md", "Profile Vertical Slice"),
    "A-005": ("profiles/architecture/modular-monolith.md", "Profile Modular Monolith"),
    "A-006": ("profiles/patterns/design-patterns-catalog.md", "Danh mục design pattern"),
    "D-001": ("profiles/frontend/bulletproof-react.md", "Frontend theo tính năng"),
    "D-003": ("profiles/design/ui-ux-archetypes-and-presets.md", "Design system & theme"),
    "D-006": ("profiles/design/screenshot-to-code-reverse-engineering.md", "Dịch ngược giao diện từ ảnh chụp màn hình"),
    "G-001": ("knowledge-base/technical-book/agent-practices/multi-tool-config.md", "Cấu hình rule/skill cho nhiều Agent"),
    "G-005": ("profiles/skills-catalog/curated-agent-skills.md", "Ma trận kỹ năng Agent tuyển chọn (Curated Skills)"),
    "G-006": ("profiles/agent-configs/curated-mcp-matrix.md", "Ma trận cấu hình MCP Server tuyển chọn"),
    "G-007": ("profiles/knowledge-map/agent-ecosystem-taxonomy.md", "Bản đồ hệ sinh thái & từ khóa tra cứu Agent"),
    "I-001": ("profiles/ai-apps/agentic-patterns-and-evals.md", "Ứng dụng AI: pattern & evals"),
    "T-001": ("profiles/stacks/cloud-free-tier-stack.md", "Hạ tầng Cloud Free-Tier cho MVP"),
    "T-003": ("knowledge-base/technical-book/devops/docker-cicd.md", "Docker & CI/CD"),
    "T-005": ("profiles/deployment/go-live-production-checklist.md", "Checklist 5 cổng kiểm duyệt trước khi Go-Live"),
    "O-001": ("profiles/documentation/documentation-and-pitch-standards.md", "Tài liệu theo Diátaxis"),
}

SEVERITY_ORDER = {"Cao": 0, "Trung bình": 1, "Thấp": 2}

# Phát hiện cấp mã nguồn (violations): type -> (mã, mức, [doc ids])
VIOLATION_RULES: dict[str, tuple[str, str, list[str]]] = {
    "HARDCODED SECRET IN CODE": ("SEC-001", "Cao", ["S-001", "K-003"]),
    "LAYER LEAKAGE": ("ARCH-001", "Cao", ["A-002", "S-004"]),
    "SQL INJECTION RISK": ("SEC-004", "Cao", ["S-001", "A-002"]),
    "NAKED JSON.PARSE": ("AC-001", "Trung bình", ["S-001"]),
    "PYTHON SILENT EXCEPTION EATER": ("AC-003", "Trung bình", ["S-001"]),
    "REACT MEMORY LEAK RISK": ("AC-004", "Trung bình", ["S-001", "D-001"]),
    "STRICT TYPING VIOLATION": ("AC-002", "Thấp", ["S-001"]),
}

# Phát hiện dạng văn bản (gap / bloat / tiêu chí thiếu): (regex, mã, mức, [doc ids]) — khớp đầu tiên thắng.
TEXT_RULES: list[tuple[str, str, str, list[str]]] = [
    (r"\.ENV.*(GIT|nhạy cảm)|nhạy cảm.*\.ENV|SECRET", "SEC-003", "Cao", ["K-003", "S-001"]),
    (r"\.gitignore|cache BUILD", "HYG-001", "Trung bình", ["K-003"]),
    (r"AGENTS\.md|CURSORRULES|AI AGENT|NEGATIVE CONSTRAINTS|STOP & ASK|ANTI-CRASH bắt buộc|DOOM LOOP", "AGT-001", "Cao", ["K-003", "G-001", "S-006"]),
    (r"SKILL", "AGT-002", "Trung bình", ["G-001", "G-005"]),
    (r"WORKFLOW|SELF-VERIFICATION|MCP", "AGT-003", "Thấp", ["G-001", "G-006", "S-006"]),
    (r"LIVING DOCUMENTATION|SYNC_DOCS|AUTO-GEN:STATS|PRE-COMMIT", "DOC-003", "Thấp", ["S-007"]),
    (r"ARCHITECTURE DECISION|ADRS", "ARCH-002", "Trung bình", ["K-003", "K-004"]),
    (r"API CONTRACT|OPENAPI", "ARCH-003", "Trung bình", ["K-003"]),
    (r"DOMAIN, APPLICATION|ranh giới", "ARCH-004", "Cao", ["A-002", "K-004"]),
    (r"GOD COMPONENT", "ARCH-005", "Trung bình", ["A-006", "S-004"]),
    (r"DEPENDENCY INJECTION|DTO|GRACEFUL", "ARCH-006", "Thấp", ["A-002", "S-002"]),
    (r"DESIGN TOKENS|THEME", "UI-001", "Thấp", ["D-003", "D-006"]),
    (r"API CLIENT|ERROR BOUNDARY|LAZY", "UI-002", "Thấp", ["D-001"]),
    (r"LOCKFILE", "SEC-002", "Trung bình", ["K-003"]),
    (r"SECURITY HEADERS|RATE LIMITING|RAW SQL|SQL", "SEC-004", "Trung bình", ["S-001", "T-005"]),
    (r"MIGRATION|CONNECTION POOL|TRANSACTION|N\+1", "DATA-001", "Trung bình", ["A-002", "S-002"]),
    (r"TTL|Data Contracts|SCHEMA", "DATA-002", "Thấp", ["A-002"]),
    (r"DOCKER|LIVENESS|INFRASTRUCTURE AS CODE|MULTI-STAGE|NON-ROOT", "OPS-001", "Thấp", ["T-003", "T-005"]),
    (r"GATEWAY|CIRCUIT BREAKER|CORRELATION|gRPC", "OPS-002", "Thấp", ["A-005"]),
    (r"LOGGING|OPENTELEMETRY|PROMETHEUS", "OPS-003", "Thấp", ["T-003", "T-005"]),
    (r"README", "DOC-001", "Trung bình", ["O-001", "K-003"]),
    (r"QUICK START|PRODUCT VISION|ARCHITECTURE|\.ENV", "DOC-002", "Thấp", ["O-001"]),
]

GENERIC = ("GEN-001", "Trung bình", ["K-003"])

# Mã phát ra trực tiếp từ engine (không qua VIOLATION_RULES/TEXT_RULES): mã -> (mức, [doc ids]).
# Mọi mã phát hiện phải có mặt ở đây hoặc trong các bảng trên (có test kiểm tra).
CODE_RULES: dict[str, tuple[str, list[str]]] = {
    "SAFE-001": ("Cao", ["K-006"]),
    "SAFE-002": ("Cao", ["K-006"]),
    "SAFE-003": ("Cao", ["K-006"]),
    "SAFE-004": ("Trung bình", ["K-006"]),
    "SAFE-005": ("Trung bình", ["K-006"]),
    "ARCH-007": ("Trung bình", ["K-004"]),
    "ARCH-008": ("Trung bình", ["K-004"]),
}

# Các gap chỉ là tổng kết (đã liệt kê chi tiết ở nơi khác) -> bỏ để khỏi trùng.
SUMMARY_GAP = re.compile(r"vị trí vi phạm tiêu chuẩn ANTI-CRASH", re.IGNORECASE)


@dataclass
class Finding:
    code: str
    severity: str
    title: str
    location: str = ""
    docs: list[str] = field(default_factory=list)


def from_violation(v: dict) -> Finding:
    code, sev, docs = VIOLATION_RULES.get(str(v.get("type")), ("VIO-000", "Trung bình", ["S-001"]))
    loc = v.get("file", "")
    if v.get("line"):
        loc = f"{loc}:{v.get('line')}"
    return Finding(code, sev, str(v.get("desc") or v.get("type")), loc, docs)


def from_text(text: str) -> Finding | None:
    if SUMMARY_GAP.search(text):
        return None
    for pattern, code, sev, docs in TEXT_RULES:
        if re.search(pattern, text, re.IGNORECASE):
            return Finding(code, sev, text, "", docs)
    return Finding(GENERIC[0], GENERIC[1], text, "", list(GENERIC[2]))


def doc_markdown(doc_id: str, ref: str = DEFAULT_REF) -> str:
    path, title = DOCS[doc_id]
    return f"[{title}]({KIT_REPO}/blob/{ref}/{path}) (`{path}`)"


def doc_info_list(doc_ids: list[str], ref: str = DEFAULT_REF) -> list[dict]:
    """Trả về danh sách thông tin tài liệu khắc phục dạng dict cho UI/API."""
    out = []
    for doc_id in doc_ids:
        if doc_id in DOCS:
            path, title = DOCS[doc_id]
            out.append({
                "id": doc_id,
                "path": path,
                "title": title,
                "url": f"{KIT_REPO}/blob/{ref}/{path}",
            })
    return out
