---
name: health-check
description: Dùng khi người dùng hỏi dự án đang bị gì, trước khi mở PR, sau mốc lớn, hoặc khi có tệp project-review.md. Chạy Project Health Check, đọc báo cáo, tra tài liệu khắc phục và sửa theo thứ tự ưu tiên.
---

# Project Health Check

1. Nếu chưa có báo cáo mới: chạy Health Check cho thư mục dự án (exe `Project-Health-Check.exe`, hoặc `python scripts/project_auditor.py <thư_mục>` từ Project-Builder-4-Agents). Kết quả: `project-review.md` ở gốc dự án.
2. Đọc `project-review.md`: xử lý phát hiện theo mức **Cao → Trung bình → Thấp**.
3. Với mỗi phát hiện, mở **tài liệu khắc phục** ghi cạnh nó (đường dẫn/URL trong kit; dùng skill `kit-consult` nếu thiếu).
4. Sửa, chạy lệnh kiểm chứng ở `AGENTS.md`, rồi chạy lại Health Check để xác nhận điểm cải thiện.
5. Phát hiện không sửa ngay → ghi vào `planning/backlog.md` kèm lý do.
