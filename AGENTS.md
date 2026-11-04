# AGENTS.MD: CONSTITUTION FOR AI AGENTS (CLAUDE, ANTIGRAVITY, CURSOR, CODEX)

> **Mục đích**: Đây là bản quy chuẩn hành vi ("Hiến pháp") bắt buộc đối với tất cả AI Coding Agents làm việc trong dự án này. Mọi Agent khi tham gia dự án PHẢI đọc, thấu hiểu và tuân thủ 100% các điều khoản dưới đây trước khi thực hiện bất kỳ thay đổi nào.

---

## 🏛️ 1. NGUYÊN TẮC CỐT LÕI (CORE PRINCIPLES)

1. **Context-Driven (Ngữ Cảnh Là Nền Tảng)**:
   - AI không tự biên tự diễn. Mọi dòng code sinh ra phải bắt nguồn từ bối cảnh trong `/specs`, `/adrs` và `/contracts`.
   - Bắt buộc đọc toàn bộ file liên quan trước khi áp dụng chỉnh sửa (Edits).

2. **Spec-Driven & Contract-First**:
   - Không viết code trước khi có Feature Spec (`specs/features/`) và API Contract (`specs/contracts/`).
   - Tuyệt đối KHÔNG tự ý thay đổi API Contract (Request/Response schemas, routes, types) mà không có sự đồng ý của Human Tech Lead qua một ADR mới.

3. **Anti-Crash Standard (Tiêu Chuẩn Chống Đổ Vỡ)**:
   - **Defensive Programming**: Bắt buộc dùng Optional Chaining (`?.`) và Nullish Coalescing (`??`) khi truy xuất object/props.
   - **Safe Fallbacks**: Luôn cung cấp giá trị mặc định (`[]`, `{}`, `""`, `0`) để tránh màn hình trắng (Blank page) hoặc runtime crash.
   - **Robust Error Handling**: Bao bọc toàn bộ các lời gọi I/O, Network API, DB Query, JSON Parse trong khối `try...catch` có logging rõ ràng.
   - **Data Validation**: Luôn xác thực kiểu dữ liệu và dùng `Array.isArray()` trước khi duyệt mảng (`.map()`, `.filter()`).

4. **Test-Driven Development (TDD)**:
   - Luôn viết test cases (Unit test / Integration test) bám sát Acceptance Criteria trước hoặc song song với mã logic.
   - Tự chạy test và xác minh (Self-verification) trước khi thông báo hoàn tất nhiệm vụ.

---

## 🚦 2. QUY TRÌNH THỰC THI NHIỆM VỤ (TASK EXECUTION PROTOCOL)

Khi được giao một Task (`T-xxx`) hoặc User Story (`US-xxx`), Agent phải tuân thủ nghiêm ngặt 5 bước:

```mermaid
flowchart LR
    S1[1. Ingest Context] --> S2[2. Plan & Break Subtasks]
    S2 --> S3[3. Write Tests First]
    S3 --> S4[4. Implement Code]
    S4 --> S5[5. Self-Verify & DoD Check]
```

1. **Bước 1 - Nạp Ngữ Cảnh (Ingest Context)**:
   - Đọc kỹ `specs/product-vision.md`, `specs/domains.md`, các ADR trong `adrs/`, và file đặc tả task tương ứng.
   - Xác định ranh giới (Domain boundary) và các file sẽ bị ảnh hưởng.
2. **Bước 2 - Lập Kế Hoạch (Plan & Subtasks)**:
   - Lập kế hoạch các bước triển khai chi tiết. Nếu task quá lớn, chủ động phân rã thành các subtask logic.
3. **Bước 3 - Viết Kiểm Thử Trước (Tests First)**:
   - Khởi tạo file test trong thư mục `tests/`.
   - Định nghĩa các test case cho Happy Path và ít nhất 2 Edge Cases / Error Cases.
4. **Bước 4 - Triển Khai Mã Nguồn (Implement Code)**:
   - Viết code sạch (Clean Code), tuân thủ `adrs/0003-coding-conventions.md`.
   - Giữ nguyên các comment và docstring hiện hữu không liên quan đến thay đổi.
5. **Bước 5 - Tự Kiểm Tra & Nghiệm Thu (Self-Verify & DoD Check)**:
   - Chạy test suite và linting. Đảm bảo 100% test pass.
   - Đối chiếu với `adrs/0005-definition-of-done.md` trước khi báo cáo hoàn tất.

---

## ⛔ 3. ĐIỀU KHOẢN CẤM & KHI NÀO PHẢI DỪNG LẠI HỎI (STOP & ASK)

Agent **BẮT BUỘC DỪNG LẠI VÀ XIN Ý KIẾN CON NGƯỜI (HUMAN TECH LEAD / PM)** khi gặp các trường hợp sau:
* Yêu cầu người dùng mơ hồ, thiếu ràng buộc kỹ thuật (data types, payload format, error codes).
* Xuất hiện xung đột giữa Spec hiện tại và mã nguồn cũ.
* Thao tác có nguy cơ phá vỡ tính tương thích ngược (Breaking Changes).
* Đề xuất cài đặt thêm thư viện (dependencies) nặng ngoài tech stack đã chốt trong `adrs/0002-tech-stack.md`.
* Thao tác có tính phá hủy dữ liệu (Drop table, broad delete, xóa file kiến trúc).
