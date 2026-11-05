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

## Cấu trúc mã
* `project_auditor.py`: CLI mỏng.
* `auditor_engine/`: lõi logic (tree, profiler, các pillar, báo cáo, bảng ánh xạ phát hiện → tài liệu `remediation.py`). Thuần Python stdlib, chạy headless, có test trong `tests/`.
* `reviewer_app.py` + `reviewer_shell/`: giao diện web cục bộ (chỉ lắng nghe `127.0.0.1`, chống CSRF/DNS rebinding).
* `engine_main.py`: điểm vào của engine đóng gói (`serve` | `audit`).
* `build_exe.py`: đóng gói engine (PyInstaller) và vỏ .NET (`tools/ProjectReviewer`).
* `check_links.py`: kiểm tra link tài liệu (chạy trong CI để `INDEX.md` không dẫn Agent vào ngõ cụt).
