---
id: S-002
type: reference
when: "Designing automated tests, resolving test gaps, choosing test levels (unit/integration/e2e)"
---
# AUTOMATED TESTING STRATEGY (TEST PYRAMID & TDD)

---

## 1. Test Pyramid
* **Unit Tests (70%)**: Verify isolated domain logic, business services, calculations, and utility helpers. Mock all external I/O.
* **Integration Tests (20%)**: Verify data and contract flow across architectural layers (Controller $\rightarrow$ Service $\rightarrow$ Repository / Database).
* **Contract Tests / E2E (10%)**: Verify API request/response conformance against API specifications and end-to-end critical user journeys.

## 2. Test Discipline for AI Agents
* *"Tests are the executable behavioral contract of the codebase."*
* When implementing a task, write 1 Happy Path test and at least 2 Failure / Edge Case tests.
* Work is complete only when 100% of the test suite passes GREEN.
