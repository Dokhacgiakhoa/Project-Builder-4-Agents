---
name: spec-first-task
description: Use when initiating any non-trivial feature or refactoring. Workflow: ingest context, draft task spec, write tests first, implement changes, and self-verify against Definition of Done.
---

# Spec-First Task Workflow

1. **Ingest Context**: Read `docs/project-brief.md`, relevant ADRs, and all files directly affected.
2. **Draft Plan**: Outline objective, acceptance criteria, affected files, and risks. Break large tasks into sub-tasks. If modifying architectural contracts (APIs, DB schema, routes) $\rightarrow$ stop, draft an ADR, and ask the user.
3. **Tests First (or parallel)**: Write 1 happy path test + at least 2 edge/failure cases.
4. **Implement**: Follow conventions in `docs/standards/coding-conventions.md` and the directory layout of the selected architecture profile.
5. **Self-Verification**: Execute test, lint, and build commands defined in `AGENTS.md` Section 2; verify against `docs/standards/definition-of-done.md`.
6. Report to the user in concise language: what was completed, verification results, and recommended next steps.
7. **Circuit Breaker**: If fixing the same failure on attempt 2 fails $\rightarrow$ stop, diagnose architectural root causes, and never attempt a 3rd blind patch.
