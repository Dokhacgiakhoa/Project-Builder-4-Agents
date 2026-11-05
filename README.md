<div align="center">

  <img src="assets/banner.svg" alt="Project-Builder-Kit" width="100%" />

  <h3>Project-Builder-Kit</h3>
  <p><b>Để AI agent dựng dự án chuẩn kiến trúc cho bạn — không cần clone, không cần biết repo có gì.</b></p>
  <p>Dùng được với <b>Claude Code · Antigravity · Codex</b></p>

</div>

---

> ## 🤖 DÀNH CHO AI AGENT
> Nếu người dùng nhờ bạn dựng/khởi tạo dự án, thiết lập rule–skill–workflow cho Agent, hoặc "làm cho repo này chuẩn hơn": **đọc [BOOTSTRAP.md](BOOTSTRAP.md) và làm theo**. Cần hướng dẫn kiến trúc/pattern/design system/test/CI: **tra [INDEX.md](INDEX.md)** theo ý định, đừng chờ người dùng chỉ tên tệp. Muốn biết dự án đang "bị" gì: dùng **Project Health Check** ([scripts/README.md](scripts/README.md)).

---

## Dùng thế nào (cho người)

1. Mở Claude Code, Antigravity hoặc Codex trong một thư mục trống (hoặc thư mục dự án đang làm dở).
2. Dán đúng một câu:

   ```text
   Hãy dùng https://github.com/Dokhacgiakhoa/Project-Builder-Kit để dựng dự án giúp mình. Mình muốn làm: <mô tả ngắn dự án của bạn>
   ```
3. Trò chuyện với Agent: nó sẽ hỏi bạn vài câu đơn giản, đề xuất công nghệ và kiến trúc, rồi tự dựng khung, cấu hình rule/skill/workflow cho chính nó, cài lệnh test/lint và CI.
4. Về sau cứ nhờ Agent làm việc bình thường. Nó đã mang sẵn "bộ định tuyến tri thức" trong `AGENTS.md` nên tự tra kit khi cần kiến trúc, pattern, giao diện, test.
5. Muốn biết dự án đang "bị" gì: bấm **Project Health Check** (mục dưới) hoặc nhờ Agent chạy; kết quả là tệp `project-review.md`.

## Kit có gì (3 tầng)

| Tầng | Thư mục | Vai trò |
| :-- | :-- | :-- |
| **Core** — bắt buộc cho mọi repo dùng Agent | [core/](core/README.md) | `AGENTS.md`, lớp tương thích Agent, project brief, ADR, chuẩn làm việc, lệnh kiểm chứng + CI, vệ sinh repo, PR template |
| **Profiles** — chọn theo từng dự án | [profiles/](profiles/README.md) | Kiểu kiến trúc (Layered đơn giản, Clean Architecture, Vertical Slice, Modular Monolith), pattern, frontend, design system, ứng dụng AI, stack, tài liệu |
| **Library** — tham khảo / tùy chọn | `knowledge-base/`, `templates/` | Sách kỹ thuật, tư duy, quản trị dự án, pitch deck |

Cấu hình sâu (kiến trúc, pattern, rule, skill) **không dùng chung**: Agent chọn theo dự án của bạn sau bước phỏng vấn. Chỉ Core là bắt buộc.

## Project Health Check

Quét **một thư mục dự án bất kỳ** (mọi ngôn ngữ), offline, không tốn token, rồi xuất **`project-review.md`** — người đọc được, Agent cũng đọc được. Mỗi phát hiện có **mã, mức độ, vị trí tệp:dòng và tài liệu khắc phục** trong kit để Agent tra và sửa.

| Cách chạy | Ghi chú |
| :-- | :-- |
| `Project-Health-Check.exe` (Windows) | Giao diện: chọn thư mục, xem kết quả |
| `python scripts/project_auditor.py <thư_mục>` | Cần Python 3.12+ (Linux/macOS/CI) |
| `./Project-Health-Check.sh <thư_mục>` | Linux/macOS |

Chi tiết: [scripts/README.md](scripts/README.md). Đóng gói exe: `make build-exe` (người dùng cuối không cần Python; cần .NET 10 Desktop Runtime và WebView2).

> ⚠️ `Project-Health-Check.exe` trong repo là bản dựng cũ (vẫn cần Python 3.12+ trên máy). Cần `make build-exe` để có bản dùng engine đóng gói.

## Cho người phát triển kit

```bash
make test         # pytest + vitest
make check-links  # INDEX.md không được dẫn Agent vào ngõ cụt
make review       # Health Check chính repo này
```
Quy tắc đóng góp: [AGENTS.md](AGENTS.md) · Quyết định định vị: [ADR-0012](adrs/0012-agent-first-builder-and-health-check.md), [ADR-0011](adrs/0011-desktop-and-tooling-architecture.md).

## Giấy phép
[MIT](LICENSE).
