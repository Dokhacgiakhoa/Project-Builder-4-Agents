# ADR 0015: STAGED FEATURE WORKFLOW WITH VERIFICATION GATES

* **Status**: Accepted
* **Date**: 2026-11-06
* **Builds on**: [ADR-0012](0012-agent-first-builder-and-health-check.md), [ADR-0014](0014-english-as-primary-language-for-token-efficiency.md)

---

## 1. Context

* The kit's `spec-first-task` skill was a flat 7-step list. It had no clarification gate, no cross-artifact consistency check, and no defined loop until acceptance criteria pass.
* GitHub Spec Kit (open source, MIT) offers a staged flow: constitution, specify, clarify, plan, tasks, analyze, implement, converge. Published reviews praise its structure and criticize its overhead (thousands of markdown lines for small changes), non-deterministic output, spec/code drift, and lack of verification.
* This kit's strengths are different: decision rails, token-lean docs (<120 lines), real verification commands, a 2-attempt circuit breaker, and a zero-token Health Check.

## 2. Decision

Adopt Spec Kit's strongest ideas as a **lean, scale-aware, verification-gated** workflow, without adding the CLI or any runtime dependency:

1. **Scale Gate**: Tiny / Standard / Large paths so spec length never exceeds change size (answers the overhead critique).
2. **Clarify gate**: unknowns are written as `[NEEDS CLARIFICATION: ...]` markers; zero markers allowed before planning; max 3 questions per turn.
3. **Analyze**: read-only consistency pass (every acceptance scenario has a task and test, no orphan tasks, no conflict with `AGENTS.md`/ADRs) that fixes artifacts, not code.
4. **Implement-and-converge loop**, bounded by the existing 2-attempt circuit breaker, ending with an Evidence table (scenario -> test) (answers the "no verification" critique).
5. **Spec Change Protocol**: spec is edited before code to limit drift.
6. Delivered as `core/standards/feature-workflow.md` (S-008, Core), templates `feature-spec.md` and `feature-plan.md`, and an upgraded `spec-first-task` skill. `AGENTS.md` itself remains the constitution; no separate constitution artifact.

## 3. Consequences

* **Positive**: clearer pre-code gates; verifiable done-ness per scenario; works in any agent without installing a tool; stays within the token budget.
* **Negative**: one more Core doc for agents to know; Large path adds artifacts for big features.
* **Not adopted**: the `specify` CLI, extension catalog, per-agent command files, a standalone constitution file.
* **Follow-up (not done)**: a Health Check finding for features with unresolved markers or scenarios lacking evidence. Requires a new finding code, severity, remediation doc, and tests per `AGENTS.md` rule 4.
