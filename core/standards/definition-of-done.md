---
id: S-003
type: reference
when: "Verification criteria before reporting \"Done\" or opening PR"
---
# DEFINITION OF DONE (DOD) & QUALITY GATE

---

## 1. Definition of "Done"
A Task or Pull Request is considered **DONE** if and only if all of the following criteria are satisfied:

1. [x] **Logic & Specs**: Source code accurately satisfies acceptance criteria in `tasks/task-spec.md` or feature specs.
2. [x] **Zero Regressions**: No existing functionality or tests are broken.
3. [x] **Anti-Crash Compliance**: Adheres to defensive coding conventions in `docs/standards/coding-conventions.md`.
4. [x] **Automated Tests**: Added Unit/Integration tests; 100% test suite passes GREEN locally.
5. [x] **Lint & Static Check**: Zero lint errors, zero critical security warnings.
6. [x] **Atomic PR**: Pull Request contains < 400 lines of changes and follows PR template format.
7. [x] **Health Check Clean**: No High or Medium severity findings in `project-review.md`.
8. [x] **Living Documentation**: Run `python scripts/sync_docs.py` to ensure `README.md` and documentation reflect all feature changes.
