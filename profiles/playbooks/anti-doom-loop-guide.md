---
id: S-006
type: playbook
when: "When Agent is **caught in a debugging doom loop**, where fixes produce new errors and corrupt architecture"
---

# PLAYBOOK: PREVENTING VIBE CODING DOOM LOOPS

> **For AI Agents**: The "Doom Loop" is the most catastrophic failure pattern in Vibe Coding: The AI patches Bug A, inadvertently causing Bug B; patching Bug B breaks Architecture C, quickly deteriorating into unrecoverable spaghetti. This playbook enforces 3 deterministic Operating Loops to trip the circuit breaker and stabilize the codebase.

---

## 1. Warning Indicators: You Are Entering a Doom Loop
* You have attempted to fix the same issue or view twice, yet tests remain red or the user reports cascading regressions.
* You begin adding defensive hacks like arbitrary `if (data && data.item && ...)` chains, `@ts-ignore`, or `any` casts to disguise type errors.
* You find yourself editing or deleting files outside the original task boundaries.
* **MANDATORY ACTION**: **TRIP THE CIRCUIT BREAKER IMMEDIATELY.** Cease all code edits until the following protocol is completed.

---

## 2. The 3 Defensive Operating Loops

### Loop 1: The Spec-First Loop (No Spec, No Code)
* Before modifying or implementing any non-trivial logic, open `tasks/task-spec.md`.
* Define explicitly:
  1. The single objective of this specific change.
  2. The strict file boundary (exact files permitted to change).
  3. Machine-verifiable acceptance criteria (commands and expected outcomes).
* Never touch files outside the pre-declared boundary.

### Loop 2: The CI Green Loop (Green Baseline Precedes New Features)
* **Golden Rule**: *Never write new features while the build, test suite, or linter is red.*
* When regressions occur:
  1. Freeze all new feature development.
  2. Run `npm test` or `pytest` to isolate the exact failing unit test.
  3. Resolve the underlying logic failure and restore the system to full GREEN status before moving forward.

### Loop 3: The Git Micro-Checkpoint Loop (The Safe Rollback Lifeline)
* Vibe coders fear losing working code. The Agent must proactively generate atomic Git checkpoints:
  * As soon as a small task or bug is resolved and all tests pass green $\rightarrow$ create an immediate micro-commit:
    ```bash
    git add . && git commit -m "checkpoint: <task_name> (tests pass)"
    ```
* **Safe Rollback Protocol**:
  * If a second fix attempt introduces secondary regressions or architectural drift, proactively propose a rollback:
    > *"Fix attempt #2 introduced secondary errors. I recommend rolling back to our last green checkpoint via `git reset --hard HEAD~1` to try a cleaner approach. Would you like to proceed?"*

---

## 3. Circuit Breaker Protocol (Stop & Ask)
When the circuit breaker trips after 2 unsuccessful fix attempts, the Agent must present a structured diagnostic to the user:
1. **Root Cause**: The real architectural source of failure (not just the surface symptom).
2. **The Blocker**: Structural conflict, missing prerequisite, or contract mismatch?
3. **Two Viable Paths**:
   * Option A: Refactor the originating data/logic layer cleanly (+5 min).
   * Option B: Simplify business requirements or temporarily drop non-essential features.
4. **Wait for user confirmation** before resuming any code changes.
