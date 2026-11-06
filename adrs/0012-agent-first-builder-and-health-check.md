# ADR 0012: AGENT-FIRST BUILDER KIT & PROJECT HEALTH CHECK

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-05
* **Thay thế định vị cũ của**: Starter Kit "clone về rồi tự gõ lệnh" (ADR-0001..0010 cũ đã được chuyển thành tài liệu trong `core/` và `profiles/`)

---

## 1. BỐI CẢNH (CONTEXT)
* Người dùng mục tiêu là **fresher IT và người "vibe coding"**, chỉ biết chút ít về git. Họ **không biết repo có những tệp nào**, nên không thể chỉ đích danh tài liệu cho Agent.
* Họ dùng một **Agent lập trình** (Claude Code, Antigravity, Codex). Phần lớn thời gian họ nhờ Agent viết và review, rất ít khi tự đọc code. Tài liệu trong repo chủ yếu **dành cho Agent đọc** (~90%), con người ~10%.
* Các dự án khác nhau cần **kiểu Clean Architecture, design pattern, rule, skill khác nhau**. Không thể có một cấu hình sâu dùng chung.

## 2. QUYẾT ĐỊNH (DECISION)

### 2.1. Hai sản phẩm trong một repo
| | **Project-Builder-4-Agents** | **Project Health Check** |
|---|---|---|
| Là gì | Bộ tri thức + quy trình để Agent dựng và đồng hành cùng dự án | Công cụ (exe/CLI) kiểm tra dự án đang "bị" gì |
| Ai dùng | Agent, qua trò chuyện với người dùng | Người dùng bấm exe, hoặc Agent chạy dòng lệnh |
| Đầu ra | Dự án có khung chuẩn, rule, skill, workflow | Tệp **`project-review.md`** cho cả người và Agent |

### 2.2. Agent chủ động, không cần người dùng chỉ tên tệp
* Điểm vào duy nhất: `README.md` → `BOOTSTRAP.md` (quy trình cho Agent) → `INDEX.md` (bảng định tuyến **ý định → tài liệu**).
* Người dùng chỉ cần nói ý muốn bằng ngôn ngữ thường. Agent tự đối chiếu `INDEX.md` để chọn tài liệu cần đọc.
* Sau khi dựng xong, dự án mang theo **Knowledge Router** trong `AGENTS.md` (địa chỉ kit + quy tắc "khi gặp tình huống X thì tra INDEX"), để Agent tiếp tục chủ động ở các bước sau.

### 2.3. Ba tầng nội dung (tách rõ cái gì bắt buộc, cái gì tùy biến)
1. **Core Baseline** (`core/`): bắt buộc cho **mọi** repo làm việc với Agent, không phụ thuộc ngôn ngữ/kiến trúc.
2. **Profiles** (`profiles/`): cấu hình sâu, **chọn theo dự án** sau bước phỏng vấn (kiểu kiến trúc, stack, pattern, design system, loại ứng dụng).
3. **Library** (`knowledge-base/`, `templates/`): tài liệu tham khảo và mô-đun tùy chọn (pitch deck, quản trị dự án...).

### 2.4. Chuẩn Agent dùng chung, lớp tương thích mỏng
* Nguồn sự thật duy nhất: **`AGENTS.md`** và **Agent Skills** (`SKILL.md`, chuẩn mở). Codex và Antigravity đọc `AGENTS.md`; Claude Code đọc `CLAUDE.md` nên tạo `CLAUDE.md` chỉ import `AGENTS.md`.
* Skills đặt tại `.agents/skills/<tên>/SKILL.md` (Codex, Antigravity); Claude Code đọc `.claude/skills/` nên **sao chép** sang đó.
* Quy tắc/Workflow riêng của từng công cụ chỉ là lớp mỏng sinh từ nguồn chung.
* **Cần xác minh lại** đường dẫn theo tài liệu chính thức khi Agent thực thi, vì các công cụ thay đổi nhanh (một số nguồn còn mâu thuẫn về đường dẫn global của Antigravity).

### 2.5. Health Check xuất `project-review.md`
* Một tệp Markdown duy nhất, cả người lẫn Agent đọc được: điểm tổng quan, từng phát hiện kèm **mã ổn định, mức độ, vị trí tệp:dòng** và **tài liệu khắc phục trong kit** (đường dẫn + URL).
* Agent đọc báo cáo, tra tài liệu được chỉ dẫn, sửa theo thứ tự ưu tiên, chạy lại để xác nhận.
* Health Check **nhận biết profile** đã chọn (`.builder/kit.json`), không áp một kiểu kiến trúc cho mọi dự án.
* Engine được đóng gói để người dùng **không cần cài Python**; Python chỉ là đường chạy cho CI/Linux/macOS và cho người phát triển kit.

## 3. HỆ QUẢ (CONSEQUENCES)
* **Tích cực (kỳ vọng, chưa kiểm chứng với người dùng thật)**: người mới chỉ cần trò chuyện; mỗi dự án nhận cấu hình đúng cỡ; tài liệu tra cứu được bằng ý định; báo cáo đóng vòng "phát hiện → tra cứu → sửa → kiểm lại".
* **Hạn chế**: Agent phải có khả năng tải tệp từ GitHub; chất lượng phụ thuộc vào việc `INDEX.md` luôn đúng (đã có `scripts/check_links.py` chạy trong CI); các định dạng Agent cần theo dõi định kỳ.
* **Việc kế tiếp**: gói stack cụ thể (Profiles), kiểm tra Health Check theo profile, quy trình phát hành (GitHub Releases: exe + engine + checksum).
