---
id: D-003
type: reference
when: "Chọn phong cách giao diện, theme sáng/tối, design system"
---
# ADR 0009: UI/UX DESIGN ARCHETYPES AND THEME PRESET CATALOG

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04
* **Người quyết định**: UI/UX Specialist & Principal Architect

---

## 1. BỐI CẢNH (CONTEXT)

Trong các bộ khởi tạo dự án truyền thống (Starter Kits), giao diện thường bị bó buộc trong một phong cách cố định (thường là Tailwind mặc định hoặc Bootstrap xám/xanh). Khi người dùng hoặc AI Coding Agents muốn triển khai một sản phẩm thuộc phân khúc khác (ví dụ: một ứng dụng hoài niệm Retro Windows XP, một giao diện Cyberpunk HUD cho hệ thống bảo mật, hay một phong cách phá cách Neubrutalism cho sản phẩm Creator), họ phải tốn rất nhiều thời gian để cấu hình lại toàn bộ hệ thống màu sắc, bo góc, bóng đổ và phông chữ.

Hơn nữa, các mô hình ngôn ngữ lớn (LLM) thường có xu hướng sinh ra giao diện "chung chung", thiếu bản sắc thị giác mạnh mẽ nếu không được cung cấp bộ ràng buộc thiết kế (Visual DNA Constraints) rõ ràng.

---

## 2. QUYẾT ĐỊNH (DECISION)

Chúng ta quyết định tích hợp hệ thống **UI/UX Design Archetypes & AI Visual DNA Prompt Kit** vào `Project-Starter-Kit`:

1. **Chuẩn hóa 7 Vũ trụ Thẩm mỹ & 14+ Style Presets**:
   - Tài liệu hóa toàn diện tại `profiles/design/design-archetypes-catalog.md`.
   - Kết nối trực tiếp với các dự án mã nguồn mở uy tín (`98.css`, `XP.css`, `NES.css`, `RPGUI`, `Arwes`, `PaperCSS`, `Terminal.css`, `Magic UI`, `neobrutalism-components`).

2. **Cung cấp AI Visual DNA Prompt Cookbook**:
   - Đặt tại `profiles/design/visual-dna-prompts.md`.
   - Cung cấp các đoạn System Prompt chuẩn hóa cho từng phong cách thị giác (Linear Pro Max, iOS Glassmorphism, Neubrutalism, Cyberpunk HUD, Windows XP, Hacker Terminal, Hand-Drawn Paper) để người dùng có thể kích hoạt phong cách tức thì khi làm việc với AI Agent (Cursor, Claude Code, Antigravity, v0).

3. **Tách rời Logic Component và Visual DNA**:
   - Giữ nguyên cấu trúc logic của Headless Components (state, accessibility, form handling).
   - Biến thể phong cách (Aesthetics) được điều khiển qua các bộ Token (Tailwind classes, CSS variables, shadow profiles).

4. **Trang bị Interactive Theme Showcase trong Frontend**:
   - Xây dựng module `profiles/frontend/starter/src/features/theme-showcase/` cho phép người dùng click chuyển đổi trực tiếp giữa các phong cách để trải nghiệm trước khi quyết định chọn phong cách cho dự án.

---

## 3. HỆ QUẢ (CONSEQUENCES)

* **Ưu điểm [Pros]**:
  - Tăng tốc độ khởi tạo dự án lên mức tối đa: Chỉ cần chọn 1 preset là toàn bộ nhận diện thị giác được thiết lập nhất quán.
  - Định hướng AI Agent chính xác: Giảm thiểu 90% lỗi sinh giao diện lệch lạc hoặc "nhàm chán" từ AI.
  - Độc lập nền tảng: Bất kỳ team nào dùng React, Vue, Svelte hay HTML thuần đều có thể tham khảo bảng Design Tokens để áp dụng.
* **Nhược điểm [Cons]**:
  - Cần bảo trì tài liệu và cập nhật các xu hướng thiết kế mới theo chu kỳ.
* **Tác động hệ thống [System Impact]**:
  - Không làm phát sinh thêm dependency nặng trong `profiles/frontend/starter/`.
  - Giữ vững tiêu chuẩn Anti-Crash và tính module hóa của Bulletproof React.
