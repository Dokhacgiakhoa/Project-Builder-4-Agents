# ADR 0003: CODING CONVENTIONS & THE ANTI-CRASH STANDARD

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04

---

## 1. NGUYÊN TẮC ĐẶT TÊN (NAMING CONVENTIONS)
* **Files & Folders**: `kebab-case.extension` (Ví dụ: `user-auth-service.ts`, `task-repository.py`).
* **Variables & Functions**: `camelCase` (Ví dụ: `getUserById`, `calculateDiscountRate`).
* **Classes & Components**: `PascalCase` (Ví dụ: `UserProfileCard`, `OrderService`).
* **Constants**: `SCREAMING_SNAKE_CASE` (Ví dụ: `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT_MS`).
* **Database Tables & Columns**: `snake_case` (Ví dụ: `order_items`, `created_at`).

## 2. BỘ QUY CHUẨN KỸ THUẬT PHÒNG VỆ (ANTI-CRASH RULES)
1. **Defensive Access**: Luôn dùng Optional Chaining (`user?.profile?.avatar`) và Fallback (`items ?? []`).
2. **Safe Array Iteration**: Luôn kiểm tra `Array.isArray(data)` trước khi gọi `.map()`, `.filter()`.
3. **Async Error Encapsulation**: Tất cả Promise, API call, File I/O phải nằm trong `try...catch`.
4. **No Hardcoded Values**: Không hardcode URLs, magic numbers, credentials trong code logic.
