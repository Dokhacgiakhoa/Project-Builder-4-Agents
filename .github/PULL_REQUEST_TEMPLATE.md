## 📌 TỔNG QUAN PULL REQUEST

* **Mã User Story / Task**: `[US-xxx]` / `[T-xxx]`
* **Tiêu đề thay đổi**: [Mô tả ngắn gọn 1 câu]
* **Người thực hiện**: [Human / Agent]
* **Người phụ trách review (Human Tech Lead)**: @[username]

---

## 🎯 1. BỐI CẢNH & THAY ĐỔI (WHAT & WHY)
* **Vấn đề giải quyết**: [Tại sao cần thay đổi này?]
* **Giải pháp kỹ thuật**: [Tóm tắt giải pháp đã áp dụng]
* **Các file chính bị ảnh hưởng**:
  - `path/to/file1`: [Mô tả thay đổi]
  - `path/to/file2`: [Mô tả thay đổi]

---

## 🛡️ 2. CHECKLIST ĐỐI CHIẾU DEFINITION OF DONE (DoD)
*(Bắt buộc đánh dấu tích trước khi xin review)*

- [ ] **Specs & Contracts**: Đã đối chiếu đúng `specs/features/` và không làm vỡ API Contract.
- [ ] **Anti-Crash Standard**: Đã sử dụng Optional Chaining (`?.`), Nullish Coalescing (`??`) và Safe Fallbacks.
- [ ] **Error Handling**: Đã bọc `try...catch` ở các điểm I/O, API, JSON parse.
- [ ] **Testing**: Đã bổ sung Unit / Integration Tests bao phủ Happy Path & Edge Cases.
- [ ] **Self-Verification**: Toàn bộ tests chạy PASS 100% trên môi trường local.
- [ ] **Code Hygiene**: Không còn code thừa (Dead code), không hardcode secrets/API keys.
- [ ] **Documentation**: Đã cập nhật tài liệu liên quan nếu có thay đổi hành vi hệ thống.
