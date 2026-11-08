---
name: spec-first-task
description: Use when initiating any non-trivial feature or refactoring. Staged workflow: scale gate, specify, clarify, plan with tasks, analyze, implement until converged, close with evidence.
---

# Spec-First Task Workflow

Full rules: `docs/standards/feature-workflow.md`. Artifacts live in `specs/features/NNN-slug/` (`spec.md`, `plan.md`).

1. **Scale Gate**: Classify Tiny / Standard / Large and tell the user in one line. Tiny -> skip to step 5 (tests + verification only). Unsure -> Standard.
2. **Specify**: Read `docs/project-brief.md`, relevant ADRs, and affected files. Write `spec.md` from `specs/features/feature-spec.md`: what/why only (no stack), numbered acceptance scenarios `AS-n`, `[NEEDS CLARIFICATION: ...]` for every unknown. Never guess requirements.
3. **Clarify** (Large or any markers left): ask the user at most 3 questions per turn, record answers under *Decisions*. Gate: zero markers before planning.
4. **Plan**: Write `plan.md` from `specs/features/feature-plan.md`: approach, affected files, constitution check, risks, tasks (tests first, each citing an `AS-n`). Contract change (API, DB schema, routes) -> stop, draft an ADR, ask the user. **Analyze** (Large): read-only check that every `AS-n` has a task and test, no task is orphaned, nothing contradicts `AGENTS.md` or ADRs; fix artifacts, not code.
5. **Implement and Converge**: Execute tasks in order, following `docs/standards/coding-conventions.md` and the architecture profile layout. After each batch run the test, lint, and build commands in `AGENTS.md` Section 2. Loop until every `AS-n` has a passing test and `docs/standards/definition-of-done.md` holds. Behavior must change -> edit `spec.md` first, then code.
6. **Close**: Fill the Evidence table (scenario -> test/command output), run `python scripts/sync_docs.py`, then report in the user's language: what was completed, verification results, next steps.
7. **Circuit Breaker**: If fixing the same failure on attempt 2 fails -> stop, diagnose architectural root causes, never attempt a 3rd blind patch. This applies inside every converge loop.
