# ADR 0013: REMOTE KNOWLEDGE HUB VÀ CƠ CHẾ ZERO-CLONE BOOTSTRAP CHO VIBE CODER

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-06
* **Phát triển tiếp từ**: [ADR-0012](0012-agent-first-builder-and-health-check.md)

---

## 1. BỐI CẢNH (CONTEXT)
* Người dùng mục tiêu là **Vibe Coder / Fresher**: khi bắt đầu một dự án mới, họ mở một thư mục hoàn toàn trống và nhờ AI Agent của họ (Claude Code, Antigravity, Cursor, Codex...) đọc repo GitHub của kit để khởi tạo dự án.
* Vibe coder có thể làm các bài toán khác nhau với tech stack hoàn toàn khác nhau (Python, .NET, TypeScript, Go...). Nếu bắt họ clone toàn bộ repo kit về máy:
  1. Gây rác và nặng máy người dùng bởi hàng trăm tệp của các ngôn ngữ khác mà họ không dùng tới.
  2. Dễ làm Agent hiểu sai cấu trúc và copy nhầm các file template không phù hợp vào dự án.
* Đồng thời, các AI Agent hiện đại đã đủ mạnh về mặt cú pháp code, nhưng thường thiếu **tư duy hệ thống (System Design), ranh giới kiến trúc (Clean Architecture), Product Mindset và phòng vệ chống đổ vỡ (Anti-Crash)**. Mục tiêu không chỉ là chạy `localhost` mà phải hướng tới **Go-Live thật** trên môi trường Production.

---

## 2. QUYẾT ĐỊNH (DECISION)

### 2.1. Định vị Remote Knowledge Hub (Hosted Agent Brain)
* Repo `Project-Builder-4-Agents` đóng vai trò là một **Bộ não tập trung trên GitHub**, không phải là template boilerplate để người dùng clone về.
* Cung cấp các giao diện máy đọc chuẩn hóa:
  * `llms.txt` và `llms-full.txt`: Chuẩn mở cho LLM/Agent đọc nhanh toàn bộ cấu trúc và ý đồ repo chỉ trong 1 request.
  * `MANIFEST.json`: Cây thư mục máy đọc kèm link tải thô `raw.githubusercontent.com/...` để Agent nhìn thấy từng file trong repo mà không cần cào giao diện HTML của GitHub.
  * `HOW_IT_WORKS.md`: Bản đặc tả chi tiết cơ chế vận hành để người phát triển và Agent không hiểu nhầm.

### 2.2. Quy trình Zero-Clone 4 Giai đoạn
1. **Phase 1: Discovery & Tech Selection Gate**: Agent đóng vai trò Tech Lead phỏng vấn người dùng, đề xuất stack và kiến trúc phù hợp. **Tuyệt đối chưa tải bất kỳ file nào về máy khi người dùng chưa chốt.**
2. **Phase 2: Dựng khung Core Baseline & Áp Profile**: Chỉ kéo đúng Core (B1–B9) và Profile kiến trúc của ngôn ngữ đã chọn qua HTTP raw fetch hoặc shallow clone vào thư mục tạm của hệ điều hành (`%TEMP%` hoặc `/tmp`) rồi xóa ngay sau đó.
3. **Phase 3: Đồng hành theo từng Sprint**: Dự án mang theo `AGENTS.md` chứa Knowledge Router tự động tra cứu `INDEX.md` trên GitHub khi cần giải quyết bài toán kiến trúc, design system, AI app hay phòng vệ lỗi.
4. **Phase 4: Production-Readiness & Go-Live**: Hướng dẫn đóng gói Docker, CI/CD, cấu hình Cloud Free-Tier và quét Project Health Check đạt điểm A+ trước khi release.

---

## 3. HỆ QUẢ (CONSEQUENCES)
* **Tích cực**:
  - Máy vibe coder hoàn toàn sạch sẽ, chỉ chứa mã nguồn và cấu hình của stack họ chọn.
  - Agent đọc và tải file từ xa một cách chính xác, không bị phụ thuộc vào việc cào HTML của GitHub.
  - Dự án được định hướng kiến trúc bài bản và có khả năng triển khai thực tế thay vì chỉ là bài tập đồ chơi.
* **Đánh đổi / Ràng buộc**:
  - Cần duy trì tính thông suốt của `MANIFEST.json` và `llms.txt` bằng script tự động kiểm tra trong CI.
  - Agent cần có kết nối internet để tải tài liệu từ GitHub khi thực hiện quy trình.
