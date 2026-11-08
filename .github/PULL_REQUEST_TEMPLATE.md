## 📌 Pull Request Overview

* **User Story / Task ID**: `[US-xxx]` / `[T-xxx]`
* **Title**: [Brief 1-sentence summary]
* **Author**: [Human / Agent]
* **Reviewer (Tech Lead)**: @[username]

---

## 🎯 1. Context & Changes (What & Why)
* **Problem Solved**: [Why was this change necessary?]
* **Technical Solution**: [Summary of the approach taken]
* **Key Files Affected**:
  - `path/to/file1`: [Summary of changes]
  - `path/to/file2`: [Summary of changes]

---

## 🛡️ 2. Definition of Done (DoD) Checklist
*(Must be checked before requesting review)*

- [ ] **Specs & Contracts**: Matches `specs/` and does not break API contracts.
- [ ] **Anti-Crash Standard**: Uses optional chaining (`?.`), nullish coalescing (`??`), and safe fallbacks.
- [ ] **Error Handling**: Wrapped `try...catch` at I/O boundaries, API calls, and JSON parse sites.
- [ ] **Testing**: Added unit and integration tests covering happy paths and edge cases.
- [ ] **Self-Verification**: All tests pass (100%) in local environment.
- [ ] **Code Hygiene**: No dead code, no hardcoded secrets or API keys.
- [ ] **Documentation**: Updated relevant documentation to match any system behavior changes.
