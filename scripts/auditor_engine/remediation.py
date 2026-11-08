"""
Mapping of Analytics findings -> stable codes, severity and remediation documents in Project-Builder-4-Agents.

An Agent reads `project-review.md`, sees the code + document link, then looks up exactly that document to fix.
The DOCS list must match the kit's `INDEX.md` (a test checks that every path exists).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

KIT_REPO = "https://github.com/Dokhacgiakhoa/Project-Builder-4-Agents"
DEFAULT_REF = "main"

# id -> (path in the kit, title). Same ids as INDEX.md.
DOCS: dict[str, tuple[str, str]] = {
    "K-001": ("BOOTSTRAP.md", 'Project bootstrap procedure for AI Agents'),
    "K-002": ("core/discovery.md", 'Discovery interview & locking the project scope'),
    "K-003": ("core/README.md", 'Core Baseline: minimum standard for every repo that uses Agents'),
    "K-004": ("profiles/README.md", 'Choosing an architecture profile & guardrail level M1-M3'),
    "K-005": ("scripts/README.md", 'Project Builder Analytics: static auditor & guardrails'),
    "K-006": ("core/untrusted-content.md", 'Untrusted content & prompt-injection defense'),
    "K-007": ("HOW_IT_WORKS.md", 'Zero-Clone mechanism & Hosted Agent Brain'),
    "S-001": ("core/standards/coding-conventions.md", 'Code conventions & crash defense'),
    "S-002": ("core/standards/test-strategy.md", 'Test strategy'),
    "S-003": ("core/standards/definition-of-done.md", "Definition of Done"),
    "S-008": ("core/standards/feature-workflow.md", "Staged feature workflow with verification gates"),
    "S-009": ("core/standards/worklog.md", 'Work log: short-term memory between Agent sessions'),
    "S-004": ("knowledge-base/tu-duy/anti-patching-architectural-thinking.md", 'Anti-patchwork mindset & circuit breaker'),
    "S-006": ("profiles/playbooks/anti-doom-loop-guide.md", 'Anti-Doom-Loop playbook for Agents'),
    "S-007": ("profiles/playbooks/living-documentation-sync.md", 'Living documentation & 4-layer automatic sync'),
    "A-001": ("profiles/architecture/simple-layered.md", 'Simple Layered profile'),
    "A-002": ("profiles/architecture/clean-architecture.md", "Profile Clean Architecture"),
    "A-003": ("profiles/architecture/clean-architecture-layout.md", 'Multi-language Clean Architecture folder structure'),
    "A-004": ("profiles/architecture/vertical-slice.md", "Profile Vertical Slice"),
    "A-005": ("profiles/architecture/modular-monolith.md", "Profile Modular Monolith"),
    "A-006": ("profiles/patterns/design-patterns-catalog.md", 'Design pattern catalog'),
    "D-001": ("profiles/frontend/bulletproof-react.md", 'Feature-based frontend'),
    "D-003": ("profiles/design/ui-ux-archetypes-and-presets.md", "Design system & theme"),
    "D-006": ("profiles/design/screenshot-to-code-reverse-engineering.md", 'Reverse-engineering a UI from a screenshot'),
    "G-001": ("knowledge-base/technical-book/agent-practices/multi-tool-config.md", 'Rule/skill configuration for multiple Agents'),
    "G-005": ("profiles/skills-catalog/curated-agent-skills.md", 'Curated Agent skills matrix'),
    "G-006": ("profiles/agent-configs/curated-mcp-matrix.md", 'Curated MCP Server configuration matrix'),
    "G-007": ("profiles/knowledge-map/agent-ecosystem-taxonomy.md", 'Agent ecosystem map & lookup keywords'),
    "I-001": ("profiles/ai-apps/agentic-patterns-and-evals.md", 'AI applications: patterns & evals'),
    "T-001": ("profiles/stacks/cloud-free-tier-stack.md", 'Free-tier cloud infrastructure for MVPs'),
    "T-003": ("knowledge-base/technical-book/devops/docker-cicd.md", "Docker & CI/CD"),
    "T-005": ("profiles/deployment/go-live-production-checklist.md", 'Checklist of 5 review gates before Go-Live'),
    "O-001": ("profiles/documentation/documentation-and-pitch-standards.md", 'Documentation by Diátaxis'),
}

SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

# Source-code level findings (violations): type -> (code, level, [doc ids])
VIOLATION_RULES: dict[str, tuple[str, str, list[str]]] = {
    "HARDCODED SECRET IN CODE": ("SEC-001", "High", ["S-001", "K-003"]),
    "LAYER LEAKAGE": ("ARCH-001", "High", ["A-002", "S-004"]),
    "SQL INJECTION RISK": ("SEC-004", "High", ["S-001", "A-002"]),
    "NAKED JSON.PARSE": ("AC-001", "Medium", ["S-001"]),
    "PYTHON SILENT EXCEPTION EATER": ("AC-003", "Medium", ["S-001"]),
    "REACT MEMORY LEAK RISK": ("AC-004", "Medium", ["S-001", "D-001"]),
    "STRICT TYPING VIOLATION": ("AC-002", "Low", ["S-001"]),
}

# Text findings (gap / bloat / missing criterion): (regex, code, level, [doc ids]) — the first match wins.
TEXT_RULES: list[tuple[str, str, str, list[str]]] = [
    ('\\.ENV.*(GIT|sensitive)|sensitive.*\\.ENV|SECRET', "SEC-003", "High", ["K-003", "S-001"]),
    (r"\.gitignore|cache BUILD", "HYG-001", "Medium", ["K-003"]),
    ('AGENTS\\.md|CURSORRULES|AI AGENT|NEGATIVE CONSTRAINTS|STOP & ASK|mandatory ANTI-CRASH|DOOM LOOP', "AGT-001", "High", ["K-003", "G-001", "S-006"]),
    (r"SKILL", "AGT-002", "Medium", ["G-001", "G-005"]),
    (r"WORKFLOW|SELF-VERIFICATION|MCP", "AGT-003", "Low", ["G-001", "G-006", "S-006"]),
    (r"LIVING DOCUMENTATION|SYNC_DOCS|AUTO-GEN:STATS|PRE-COMMIT", "DOC-003", "Low", ["S-007"]),
    (r"ARCHITECTURE DECISION|ADRS", "ARCH-002", "Medium", ["K-003", "K-004"]),
    (r"API CONTRACT|OPENAPI", "ARCH-003", "Medium", ["K-003"]),
    ('DOMAIN, APPLICATION|layer boundar', "ARCH-004", "Medium", ["A-002", "K-004"]),
    (r"GOD COMPONENT", "ARCH-005", "Medium", ["A-006", "S-004"]),
    (r"DEPENDENCY INJECTION|DTO|GRACEFUL", "ARCH-006", "Low", ["A-002", "S-002"]),
    (r"DESIGN TOKENS|THEME", "UI-001", "Low", ["D-003", "D-006"]),
    (r"API CLIENT|ERROR BOUNDARY|LAZY", "UI-002", "Low", ["D-001"]),
    (r"LOCKFILE", "SEC-002", "Medium", ["K-003"]),
    (r"SECURITY HEADERS|RATE LIMITING|RAW SQL|SQL", "SEC-004", "Medium", ["S-001", "T-005"]),
    (r"MIGRATION|CONNECTION POOL|TRANSACTION|N\+1", "DATA-001", "Medium", ["A-002", "S-002"]),
    (r"TTL|Data Contracts|SCHEMA", "DATA-002", "Low", ["A-002"]),
    (r"DOCKER|LIVENESS|INFRASTRUCTURE AS CODE|MULTI-STAGE|NON-ROOT", "OPS-001", "Low", ["T-003", "T-005"]),
    (r"GATEWAY|CIRCUIT BREAKER|CORRELATION|gRPC", "OPS-002", "Low", ["A-005"]),
    (r"LOGGING|OPENTELEMETRY|PROMETHEUS", "OPS-003", "Low", ["T-003", "T-005"]),
    (r"README", "DOC-001", "Medium", ["O-001", "K-003"]),
    (r"QUICK START|PRODUCT VISION|ARCHITECTURE|\.ENV", "DOC-002", "Low", ["O-001"]),
]

GENERIC = ("GEN-001", "Medium", ["K-003"])

# Codes emitted directly by the engine (not via VIOLATION_RULES/TEXT_RULES): code -> (level, [doc ids]).
# Every finding code must appear here or in the tables above (a test checks it).
CODE_RULES: dict[str, tuple[str, list[str]]] = {
    "SAFE-001": ("High", ["K-006"]),
    "SAFE-002": ("High", ["K-006"]),
    "SAFE-003": ("High", ["K-006"]),
    "SAFE-004": ("Medium", ["K-006"]),
    "SAFE-005": ("Medium", ["K-006"]),
    "ARCH-007": ("Medium", ["K-004"]),
    "ARCH-008": ("Medium", ["K-004"]),
    "WLOG-001": ("Medium", ["S-009", "S-003"]),
    "WLOG-002": ("Low", ["S-009"]),
    "SEC-005": ("High", ["K-003", "S-001"]),
    "HYG-002": ("Medium", ["K-003"]),
    "SUP-001": ("High", ["K-006", "K-003"]),
    "SUP-002": ("Medium", ["K-003"]),
    "SUP-003": ("Medium", ["K-003"]),
    "SUP-004": ("Low", ["K-003"]),
    "AGT-004": ("Medium", ["G-006"]),
    "AGT-005": ("Medium", ["G-006", "K-006"]),
    "SPEC-001": ("Medium", ["S-008"]),
}

# Gaps that are only summaries (already listed in detail elsewhere) -> dropped to avoid duplicates.
SUMMARY_GAP = re.compile('locations violating ANTI-CRASH standards', re.IGNORECASE)


@dataclass
class Finding:
    code: str
    severity: str
    title: str
    location: str = ""
    docs: list[str] = field(default_factory=list)


def from_violation(v: dict) -> Finding:
    code, sev, docs = VIOLATION_RULES.get(str(v.get("type")), ("VIO-000", "Medium", ["S-001"]))
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
    """Return the remediation document info as dicts for the UI/API."""
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
