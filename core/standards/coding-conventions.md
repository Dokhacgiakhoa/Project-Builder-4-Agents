---
id: S-001
type: reference
when: "Writing code: naming, explicit error handling, defensive crash guards, zero hardcoded values"
---
# CODING CONVENTIONS & THE ANTI-CRASH STANDARD

> **Scope**: Defensive principles apply to all languages. For non-TypeScript languages, maintain the architectural semantics (defensive access, strict typing, error encapsulation for I/O, zero hardcoding) using idiomatic patterns.

---

## 1. Naming Conventions
* **Files & Folders**: `kebab-case.extension` (e.g., `user-auth-service.ts`, `task-repository.py`).
* **Variables & Functions**: `camelCase` (e.g., `getUserById`, `calculateDiscountRate`).
* **Classes & Components**: `PascalCase` (e.g., `UserProfileCard`, `OrderService`).
* **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT_MS`).
* **Database Tables & Columns**: `snake_case` (e.g., `order_items`, `created_at`).

## 2. Technical Defensive Standards (Anti-Crash Rules)
1. **Defensive Access**: Always use Optional Chaining (`user?.profile?.avatar`) and Fallback defaults (`items ?? []`).
2. **Safe Array Iteration**: Always verify arrays (`Array.isArray(data)`) before invoking `.map()` or `.filter()`.
3. **Async Error Encapsulation**: All Promises, external API calls, and File I/O must be enclosed in explicit `try...catch` blocks with structured logs. Never swallow errors silently.
4. **No Hardcoded Values**: Never hardcode API URLs, magic numbers, or credentials in business logic. Extract to configuration modules.
