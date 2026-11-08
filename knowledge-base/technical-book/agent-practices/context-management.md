---
title: "Context Management"
description: "PROJECT_CONTEXT, session handoffs, and ADRs to prevent agent drift"
weight: 4
---

# Context Management — Preventing Agent Drift

## The Challenge

Every time an AI Coding Agent launches a new session, it re-ingests the repository. Without a structured context gateway, agents spend excessive tokens exploring, hallucinate past architecture, or resurrect previously discarded approaches. 9 of 12 teams in Cohort 1 lacked a structured context management layer.

## Pattern 1: PROJECT_CONTEXT.md — Quick Rehydration (Team 001 Memio)

The designated entry point read by the agent upon starting work. Target: rehydrate full mental context in under 60 seconds:

```markdown
## 0. Quick Rehydration (≤ 60s)
- Project: [Name] — [1-sentence summary]
- Stack: Python / FastAPI / LangGraph
- Dev Server: uvicorn src.main:app --reload
- Test Suite: pytest. Evaluation: python eval/run_eval.py

## 0.1 Current Invariants (Prevent Drift)
- Technical Single Source of Truth: executable code in src/. Docs summarize — CODE WINS.
- Agent Orchestration: src/agents/graph.py.

## 0.2 Known Ambiguities / Mismatches
- [Explicitly list known doc-vs-code discrepancies to prevent hallucination]
```

Why it works: The agent immediately knows canonical file coordinates, and the "Known Ambiguities" register (Team 011) stops the agent from acting on stale documentation.

## Pattern 2: Token-Efficient Session Handoffs (Team 001)

When wrapping up a session or handing off work, append notes to `handoff/SESSION_NOTES.md`:

```markdown
## Handoff — [Date] — [Developer]
**In Progress**: [1 sentence]
**Touched Files** (5–15 files max):
- path/file1.py — [concise modification]
**Next Action**: [1 sentence]
**Active Blockers**: [if any]
```

Rule: List only the 5–15 most critical files; never dump voluminous raw diffs. Saves context tokens during rehydration.

## Pattern 3: Embedded Architecture Decision Records (ADRs) (Team 010)

Document significant architectural choices in ADR format:

```markdown
### [ADR-001] — Mock-First Model Provider — [Date]
**Context**: Developers need to test workflows locally without requiring external API keys.
**Options**:
- A: Require live API keys → high developer onboarding friction.
- B: Provide mock provider when keys are absent → seamless local startup.
**Decision**: Option B.
**Consequences**: (+) Immediate setup; (−) Live output requires populating valid keys in `.env`.
```

ADRs help subsequent agents and developers understand **WHY** code was structured in a specific manner, preventing regressions.

## Pattern 4: Decouple Templates from Instances (Team 001)

Maintain `docs/templates/JOURNAL.template.md` separately from active `JOURNAL.md` instances to keep working files clean and token-efficient.
