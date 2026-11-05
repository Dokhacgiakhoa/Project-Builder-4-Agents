---
id: K-003
type: reference
when: "Cần biết **thế nào là đạt chuẩn tối thiểu** cho mọi repo dùng Agent"
---
# CORE BASELINE — NHỮNG THỨ BẮT BUỘC CHO MỌI REPO DÙNG AGENT

> Dành cho Agent. Áp dụng cho **mọi** dự án, bất kể ngôn ngữ hay kiểu kiến trúc. Cấu hình sâu hơn thuộc `../profiles/` và được chọn sau bước phỏng vấn (`discovery.md`).

## Danh mục bắt buộc

| Mã | Thành phần | Vị trí trong dự án | Nguồn mẫu trong kit |
| :-- | :-- | :-- | :-- |
| B1 | **Chỉ dẫn Agent** (nguồn sự thật duy nhất) | `AGENTS.md` | `templates/AGENTS.md` |
| B2 | **Lớp tương thích Agent** | `CLAUDE.md` (import `AGENTS.md`); skills ở `.agents/skills/` và bản sao `.claude/skills/` | `templates/CLAUDE.md`, `templates/.agents/skills/` |
| B3 | **Bản tóm tắt dự án** (kết quả phỏng vấn: ai dùng, làm gì, luồng chính, stack, ràng buộc) | `docs/project-brief.md` | `templates/docs/project-brief.md` |
| B4 | **Nhật ký quyết định** (ADR): ít nhất quyết định stack + kiến trúc | `adrs/` | `templates/adrs/0000-template.md` |
| B5 | **Chuẩn làm việc** | `docs/standards/` (quy ước code, chiến lược test, Definition of Done) | `standards/` |
| B6 | **Lệnh kiểm chứng chạy được** (test, lint, build) và **CI chạy chúng** | `AGENTS.md` mục Commands + `.github/workflows/ci.yml` | `templates/.github/` |
| B7 | **Vệ sinh repo**: không secret trong code | `.gitignore`, `.env.example`, `.editorconfig` | `templates/gitignore.tpl`, `templates/.env.example`, `templates/.editorconfig` |
| B8 | **Hồ sơ kit** (profile đã chọn, phiên bản kit) | `.builder/kit.json` | `templates/.builder/kit.json` |
| B9 | **Quy trình PR/Issue** | `.github/PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/` | `templates/.github/` |
| B10 | **Health Check** chạy định kỳ, kết quả ở `project-review.md` | gốc dự án | công cụ Project Health Check |

## Quy tắc làm việc cốt lõi (đã nằm trong `AGENTS.md` mẫu)
1. **Đọc trước khi sửa**; không đoán ngữ cảnh.
2. **Spec trước code** với thay đổi không tầm thường; đổi hợp đồng (API, schema, route) phải qua ADR và được người dùng đồng ý.
3. **Phòng vệ ở ranh giới**: kiểm tra dữ liệu vào, xử lý lỗi tường minh, không nuốt lỗi im lặng, có giá trị mặc định an toàn. (Cách viết cụ thể theo ngôn ngữ nằm trong profile của stack.)
4. **Test đi cùng thay đổi**; chạy lệnh kiểm chứng trước khi báo "xong".
5. **Ngắt mạch 2 lần**: sửa cùng một lỗi lần thứ hai vẫn chưa xong thì dừng, phân tích gốc rễ kiến trúc, không vá lần ba.
6. **Dừng và hỏi** khi: yêu cầu mơ hồ, thay đổi phá tương thích, thao tác xóa/không thể hoàn tác, thêm dependency nặng ngoài stack đã chốt.
7. **Không bao giờ** commit secret.
8. **Chủ động tra cứu kit** (Knowledge Router) thay vì tự bịa quy ước.

## Cái gì KHÔNG thuộc Core (tùy biến theo dự án)
Kiểu kiến trúc (Clean/Hexagonal/Modular Monolith/Vertical Slice/Layered đơn giản), ngôn ngữ và framework, design pattern, design system/UI, kiểu ứng dụng (web, API, mobile, ứng dụng AI), chiến lược dữ liệu, rule và skill chuyên biệt. Xem `../profiles/README.md`.
