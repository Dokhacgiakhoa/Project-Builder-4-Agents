---
name: spec-first-task
description: Dùng khi bắt đầu một tính năng hoặc thay đổi không tầm thường. Quy trình: nạp ngữ cảnh, lập kế hoạch, viết test trước, cài đặt, tự kiểm chứng theo Definition of Done.
---

# Quy trình một nhiệm vụ

1. **Nạp ngữ cảnh**: đọc `docs/project-brief.md`, ADR liên quan, các tệp sẽ bị ảnh hưởng.
2. **Lập kế hoạch**: mục tiêu, tiêu chí chấp nhận, tệp bị ảnh hưởng, rủi ro. Việc lớn thì chia nhỏ. Nếu đụng hợp đồng (API/schema) → dừng, đề xuất ADR và hỏi người dùng.
3. **Viết test trước** (hoặc song song): 1 trường hợp thành công + tối thiểu 2 trường hợp biên/lỗi.
4. **Cài đặt** theo quy ước ở `docs/standards/coding-conventions.md` và cấu trúc của profile kiến trúc đã chọn.
5. **Tự kiểm chứng**: chạy test, lint, build theo `AGENTS.md` mục 2; đối chiếu `docs/standards/definition-of-done.md`.
6. Báo cáo cho người dùng bằng lời đơn giản: đã làm gì, kết quả kiểm chứng, việc tiếp theo.
7. Ngắt mạch: cùng một lỗi sửa lần 2 vẫn chưa xong → dừng, phân tích kiến trúc, không vá lần 3.
