# CONTRIBUTING GUIDELINES

Cảm ơn bạn đã quan tâm và mong muốn đóng góp cho dự án! Để duy trì chất lượng mã nguồn cao và đảm bảo sự phối hợp nhịp nhàng giữa Đội ngũ Kỹ sư và Hệ thống AI Coding Agents, vui lòng tuân thủ các hướng dẫn dưới đây.

---

## 🚦 1. NGUYÊN TẮC CỐT LÕI
1. **Spec-Driven**: Mọi thay đổi logic lớn hoặc tính năng mới bắt buộc phải có Issue hoặc Feature Spec tại `specs/features/` trước khi tiến hành viết code.
2. **Context Integrity**: Đọc kỹ `AGENTS.md` và các quyết định kiến trúc trong `adrs/` trước khi thực hiện thay đổi.
3. **The Anti-Crash Standard**: Tuân thủ triệt để nguyên tắc lập trình phòng vệ (Optional Chaining, Error Handling, Fallback values).

---

## 🌿 2. CHIẾN LƯỢC NHÁNH (GIT BRANCHING)
* Nhánh `main`: Nhánh ổn định, sẵn sàng deploy production. Tuyệt đối không push trực tiếp lên `main`.
* Nhánh tính năng: `feature/{issue-id}-{short-name}` (Ví dụ: `feature/US-004-auth-flow`).
* Nhánh sửa lỗi: `bugfix/{bug-id}-{short-name}` (Ví dụ: `bugfix/BUG-012-null-pointer`).
* Nhánh sửa gấp: `hotfix/{short-name}`.

---

## 📝 3. QUY ƯỚC COMMIT (CONVENTIONAL COMMITS)
Thông điệp commit phải viết bằng tiếng Anh, bắt đầu bằng động từ và tuân thủ định dạng chuẩn:
* `feat`: Thêm tính năng mới (Ví dụ: `feat: add semantic routing for agent supervisor`).
* `fix`: Sửa lỗi (Ví dụ: `fix: handle empty payload in project controller`).
* `docs`: Cập nhật tài liệu (Ví dụ: `docs: update deployment guide for docker`).
* `refactor`: Tái cấu trúc mã nguồn không làm đổi hành vi (Ví dụ: `refactor: extract repository interface in domain layer`).
* `test`: Thêm hoặc sửa test cases (Ví dụ: `test: add unit tests for token validation`).
* `chore`: Các tác vụ bảo trì, config CI/CD (Ví dụ: `chore: update dependencies`).

---

## 🔍 4. QUY TRÌNH PULL REQUEST (PR PROCESS)
1. Tạo Pull Request trỏ về nhánh `main` hoặc `develop`.
2. Điền đầy đủ thông tin theo mẫu `.github/PULL_REQUEST_TEMPLATE.md`.
3. Đảm bảo quy mô PR dưới **400 dòng code** thay đổi để reviewer có thể đánh giá kỹ lưỡng.
4. Đảm bảo 100% CI checks chạy XANH (PASS).
5. Cần ít nhất 1 Human Reviewer phê duyệt trước khi merge.
