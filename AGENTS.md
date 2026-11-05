# AGENTS.md — DÀNH CHO AGENT ĐANG SỬA CHÍNH Project-Builder-4-Agents

> Tệp này chỉ áp dụng khi bạn chỉnh sửa **repo kit này**. Nếu người dùng muốn **dựng dự án của họ** bằng kit, hãy đọc [BOOTSTRAP.md](BOOTSTRAP.md). Chỉ dẫn mà dự án của người dùng nhận được nằm ở [core/templates/AGENTS.md](core/templates/AGENTS.md).

## Kit là gì (xem ADR-0012)
Hai sản phẩm: **Builder** (tri thức + quy trình cho Agent: `BOOTSTRAP.md`, `INDEX.md`, `core/`, `profiles/`, thư viện `knowledge-base/`, `templates/`) và **Project Health Check** (`scripts/`, `tools/`). Tài liệu viết **cho Agent đọc là chính**.

Kế hoạch và trạng thái công việc của kit: [TASKS.md](TASKS.md). Cập nhật nó khi hoàn thành hoặc đổi hướng một hạng mục.

## Quy tắc khi sửa kit
1. **Tầng nội dung**: Core = bắt buộc cho mọi repo; Profile = tùy biến theo dự án; Library = tham khảo. Đừng đẩy thứ phụ thuộc stack/kiến trúc vào `core/`.
2. **Mọi tài liệu Agent cần tìm đều phải có dòng trong `INDEX.md`** với cột "Khi nào dùng" viết theo cách người dùng nói. Thêm/đổi/xóa tài liệu → cập nhật `INDEX.md` và chạy `python scripts/check_links.py`.
3. **Khuôn tài liệu**: mọi tệp trong `core/` và `profiles/` (trừ `core/templates/`, `frontend/starter/`) có frontmatter `id`, `type` (`decision|router|playbook|reference`), `when`, khớp một dòng trong `INDEX.md`. Profile kiến trúc là `decision`: thêm `not_when`, đủ mục *Khi nào chọn / Không chọn khi / Thư mục mục tiêu / Ràng buộc / Thêm một tính năng / Lỗi thường gặp*, tối đa 120 dòng. Tài liệu chỉ chứa **quyết định và ràng buộc**, không dạy lại kiến thức công nghệ Agent đã biết. `check_links.py` kiểm tra tự động.
4. **Đổi mã nguồn Health Check**: lõi `scripts/auditor_engine/` thuần logic, không phụ thuộc UI; phát hiện mới phải có **mã + mức độ + tài liệu khắc phục** trong `remediation.py` (có test kiểm tra đường dẫn tồn tại).
5. **Python 3.12+**. Không thêm dependency runtime cho engine (chỉ stdlib).
6. Thay đổi quyết định định vị/kiến trúc của kit → ADR mới trong `adrs/`.
7. Chạy `make test` và `make check-links` trước khi báo xong. Không bỏ qua test thất bại.
8. Ngắt mạch 2 lần; dừng và hỏi khi: thay đổi phá tương thích, xóa tệp tri thức, thêm dependency nặng.
