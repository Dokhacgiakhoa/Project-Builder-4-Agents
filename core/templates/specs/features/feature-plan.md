# FEATURE PLAN: [NNN-slug — title]

* **Spec**: `spec.md` (must have zero `[NEEDS CLARIFICATION]` markers)
* **Architecture profile / ADRs**: [reference `.builder/kit.json`, `adrs/`]

## 1. Approach
[Technical approach in 5-10 lines. Contract change (API, DB schema, routes) -> draft ADR and stop for user approval.]

## 2. Affected Files
* [path — create | modify — reason]

## 3. Constitution Check
- [ ] Complies with `AGENTS.md` Section 3 rules and Technology Selection Gate (Section 6).
- [ ] No new heavy dependency outside the agreed stack.
- [ ] Core logic is separated from presentation (Section 7).

## 4. Risks
* [risk -> mitigation]

## 5. Tasks (tests first; `[P]` = safe to run in parallel)
| # | Task | Satisfies | Done when |
| :-- | :-- | :-- | :-- |
| 1 | Write failing tests for AS-1, AS-2 | AS-1, AS-2 | Tests exist and fail for the right reason |
| 2 | [implementation step] | AS-1 | Test for AS-1 passes |
| 3 | Run verification commands + Definition of Done | all | Evidence recorded below |

## 6. Evidence (filled at Close)
| Scenario | Evidence (test name / command output) |
| :-- | :-- |
| AS-1 | |
