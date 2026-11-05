# AGENTS.md — CHỈ DẪN CHO AI AGENT (NGUỒN SỰ THẬT DUY NHẤT)

> Mọi Agent (Claude Code, Antigravity, Codex, Cursor...) làm việc trong repo này **phải đọc và tuân thủ** tệp này. `CLAUDE.md` chỉ import tệp này. Giữ tệp ngắn: chỉ ghi điều Agent dễ làm sai nếu không được dặn.

## 1. Tóm tắt dự án
<!-- Agent điền sau bước phỏng vấn; chi tiết ở docs/project-brief.md -->
* **Tên**: {{PROJECT_NAME}}
* **Mục đích (1 câu)**: {{ONE_LINE_PURPOSE}}
* **Stack**: {{STACK}}  (quyết định: `adrs/0001-*.md`)
* **Kiến trúc**: {{ARCHITECTURE_PROFILE}}  (quyết định: `adrs/0002-*.md`; sơ đồ thư mục: `docs/project-brief.md`)

## 2. Lệnh kiểm chứng (bắt buộc chạy trước khi báo "xong")
<!-- Agent điền lệnh thật của stack. Không để TODO khi đã sang bước 3. -->
| Việc | Lệnh |
| :-- | :-- |
| Cài phụ thuộc | `{{INSTALL_CMD}}` |
| Chạy thử | `{{RUN_CMD}}` |
| Test | `{{TEST_CMD}}` |
| Lint / format | `{{LINT_CMD}}` |
| Build | `{{BUILD_CMD}}` |

## 3. Quy tắc làm việc (áp dụng cho mọi dự án)
1. **Đọc trước khi sửa.** Đọc các tệp liên quan; không đoán. Đọc `docs/project-brief.md` và ADR liên quan trước khi làm tính năng mới.
2. **Spec trước code** cho thay đổi không tầm thường: ghi ngắn gọn mục tiêu, tiêu chí chấp nhận, tệp bị ảnh hưởng (mẫu: `tasks/task-spec.md`). Không tự ý đổi **hợp đồng** (API, schema DB, route, kiểu dữ liệu dùng chung): cần ADR mới và người dùng đồng ý.
3. **Phòng vệ ở ranh giới**: kiểm tra dữ liệu từ ngoài vào (người dùng, mạng, tệp, DB, JSON), xử lý lỗi tường minh kèm log, **không nuốt lỗi im lặng**, luôn có giá trị mặc định an toàn. Dạng cụ thể theo ngôn ngữ: xem `docs/standards/coding-conventions.md`.
4. **Test đi cùng thay đổi**: ít nhất 1 trường hợp thành công và 2 trường hợp biên/lỗi. Chạy lệnh ở mục 2; chỉ báo "xong" khi tất cả xanh. Đối chiếu `docs/standards/definition-of-done.md`.
5. **Ngắt mạch 2 lần**: cùng một vấn đề (lỗi, giao diện, kết nối) sửa lần thứ hai vẫn chưa đạt → **dừng**, không sửa lần ba. Phân tích xem có phải xung đột nền tảng/kiến trúc, nêu phương án đổi hướng cho người dùng quyết định.
6. **Dừng và hỏi người dùng** khi: yêu cầu mơ hồ, thay đổi phá tương thích ngược, thao tác xóa hoặc không thể hoàn tác, thêm dependency nặng ngoài stack đã chốt.
7. **Không bao giờ** đưa secret/API key vào code hoặc commit. Dùng `.env` (đã nằm trong `.gitignore`), cập nhật `.env.example` khi thêm biến mới.
8. Thay đổi nhỏ, từng commit một mục đích; mô tả PR theo mẫu `.github/PULL_REQUEST_TEMPLATE.md`.
9. Giữ nguyên comment và docstring không liên quan đến thay đổi.

## 4. Giao tiếp với người dùng
Người dùng có thể là người mới. Giải thích bằng ngôn ngữ đời thường, ngắn gọn; nói rõ việc đã làm, kết quả kiểm chứng, và việc tiếp theo. Dùng đúng ngôn ngữ họ đang dùng.

## 5. KNOWLEDGE ROUTER — tra cứu Project-Builder-Kit một cách chủ động
Dự án này được dựng bằng **Project-Builder-Kit**. Cấu hình ở `.builder/kit.json`.

* Kho tài liệu: `{{KIT_REPO_URL}}` (ghim phiên bản: `{{KIT_REF}}`)
* Chỉ mục định tuyến theo ý định: `{{KIT_RAW_BASE}}/INDEX.md`

**Quy tắc**: người dùng **không biết** kit có tài liệu gì. Khi gặp một trong các tình huống dưới đây mà repo chưa có hướng dẫn, **tự tải `INDEX.md`, chọn tài liệu theo cột "Khi nào dùng", đọc rồi áp dụng**. Không tự bịa quy ước.

| Tình huống | Hành động |
| :-- | :-- |
| Thêm tính năng lớn, module mới, đổi cấu trúc thư mục | Tra tài liệu profile kiến trúc đã chọn (`.builder/kit.json`) |
| Chọn/đổi pattern, refactor, "code đang rối" | Tra danh mục design pattern + tư duy chống vá víu |
| Làm giao diện, màu sắc, theme, design system | Tra nhóm `design` trong INDEX |
| Tính năng dùng LLM/Agent/RAG | Tra nhóm `ai-apps` trong INDEX |
| Viết/thiếu test, CI, DoD | Tra `docs/standards/` rồi nhóm `core/standards` trong INDEX |
| Báo cáo `project-review.md` có phát hiện | Tra tài liệu khắc phục ghi cạnh từng phát hiện |
| Cần thêm rule/skill/workflow cho Agent | Tra nhóm `agents` trong INDEX |

Sau mỗi mốc lớn (xong tính năng, trước khi mở PR) hãy chạy **Project Health Check** để cập nhật `project-review.md`, sửa các phát hiện mức Cao/Trung bình hoặc ghi chúng vào backlog.

## 6. Cổng chọn công nghệ (Technology Selection Gate)
Trước khi thêm công cụ/framework/module mới, lập bảng đánh giá ngắn và ghi vào ADR:
1. Hiển thị & hiệu năng phù hợp loại ứng dụng.
2. Cá nhân hóa/theme/cấu hình tách khỏi mã nguồn (không hardcode).
3. Quản trị cấu hình và secret an toàn.
4. Khả năng tiến hóa: tích hợp được AI/LLM, tự động cập nhật, kiểm thử được.
Công nghệ không đáp ứng đủ thì không chọn làm giải pháp chính.

## 7. Tách lõi logic và giao diện
Mọi tool/script/module tiện ích phải tách **lõi logic** (kiểm thử được, chạy không giao diện) khỏi **lớp trình bày**. Không viết tệp nguyên khối trộn UI, state và truy vấn dữ liệu.
