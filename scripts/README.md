# PROJECT HEALTH CHECK — KIỂM TRA "DỰ ÁN ĐANG BỊ GÌ"

> Công cụ thứ hai của repo (ADR-0012). Quét một thư mục dự án bất kỳ (mọi ngôn ngữ), **không gọi mạng, không tốn token**, và xuất **`project-review.md`** ở gốc dự án — cả người và Agent đều đọc được.

## Cách chạy
| Cách | Lệnh | Ai dùng |
| :-- | :-- | :-- |
| Giao diện (Windows) | Bấm `Project-Health-Check.exe`, chọn thư mục dự án | Người dùng |
| Engine đóng gói (không cần Python) | `engine\reviewer-engine.exe audit <thư_mục>` | Agent / CI trên Windows |
| Python 3.12+ | `python scripts/project_auditor.py <thư_mục>` | Agent / CI / Linux / macOS |
| Linux/macOS | `./Project-Health-Check.sh <thư_mục>` | Agent / CI |

Mặc định (không truyền thư mục) quét chính repo kit.

## Agent đọc `project-review.md` thế nào
1. Phần đầu: điểm, xếp hạng, **profile kiến trúc đã khai báo** trong `.builder/kit.json`.
2. Mục **Phát hiện cần xử lý**: mỗi dòng có **mã**, **mức độ** (Cao/Trung bình/Thấp), **vị trí** (`tệp:dòng`) và **Tài liệu khắc phục** (đường dẫn trong kit + URL).
3. Mở tài liệu khắc phục (hoặc dùng skill `kit-consult`), sửa theo thứ tự ưu tiên, chạy lại để xác nhận.
4. **Mục 0 (Cảnh báo an toàn)**: đọc đầu tiên. Health Check quét tệp văn bản (md, json, html, txt, yaml...) tìm lệnh nhắm vào AI, ký tự ẩn, lệnh giấu trong chú thích HTML, hook/MCP có thể chạy lệnh (`SAFE-001`…`SAFE-005`). Báo cáo **không trích nguyên văn** nội dung bị gắn cờ. Xử lý: [core/untrusted-content.md](../core/untrusted-content.md). Không có tín hiệu **không có nghĩa là an toàn**; không quét mã nguồn và không tìm virus.
5. **Mục 7 (Phạm vi quét)**: thư mục đã quét, thư mục bỏ qua kèm lý do (đừng mở lại), tệp nên đọc trước, và phần chưa được kiểm tra.

## Cấu trúc mã
* `project_auditor.py`: CLI mỏng.
* `auditor_engine/`: lõi logic (tree, profiler, các pillar, báo cáo, bảng ánh xạ phát hiện → tài liệu `remediation.py`). Thuần Python stdlib, chạy headless, có test trong `tests/`.
* `reviewer_app.py` + `reviewer_shell/`: giao diện web cục bộ (chỉ lắng nghe `127.0.0.1`, chống CSRF/DNS rebinding).
* `engine_main.py`: điểm vào của engine đóng gói (`serve` | `audit`).
* `build_exe.py`: đóng gói engine (PyInstaller) và vỏ .NET (`tools/ProjectReviewer`).
* `check_links.py`: kiểm tra link tài liệu (chạy trong CI để `INDEX.md` không dẫn Agent vào ngõ cụt).
