# BOOTSTRAP — QUY TRÌNH CHO AGENT KHI NGƯỜI DÙNG MUỐN DỰNG DỰ ÁN

> **Bạn là AI coding agent** (Claude Code, Antigravity, Codex...). Người dùng có thể là fresher/vibe coder, **không biết repo này có tệp gì** và không biết dùng git thành thạo. Bạn phải **chủ động** làm theo quy trình này dựa trên lời mô tả hoặc cuộc trò chuyện của họ. Đừng bảo họ gõ lệnh hay chỉ tên tệp.
> Đọc hết tệp này, rồi thực hiện tuần tự. Trả lời bằng ngôn ngữ người dùng đang dùng.

Kho tài liệu (kit): `https://github.com/Dokhacgiakhoa/Project-Builder-Kit` · Chỉ mục ý định: [INDEX.md](INDEX.md)

---

## BƯỚC 0 — Chuẩn bị
1. Xác định **thư mục dự án**: thư mục hiện tại, hoặc hỏi người dùng muốn tạo ở đâu nếu chưa rõ.
2. Xem thư mục:
   * **Rỗng/chưa có**: dựng mới.
   * **Đã có nội dung (dự án đang làm dở)**: chế độ **MERGE** — chỉ **thêm** tệp còn thiếu, **không ghi đè** bất cứ thứ gì của họ. Tệp trùng tên thì ghi bản của kit thành `<tên>.kit-suggested` rồi báo họ.
3. Lấy nội dung kit về **thư mục tạm** (không đặt vào dự án): ưu tiên `git clone --depth 1 https://github.com/Dokhacgiakhoa/Project-Builder-Kit <tmp>`; nếu không có git, tải từng tệp qua raw URL (`https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-Kit/main/<đường dẫn>`). Ghi lại commit/tag đã dùng làm `kit_ref`.

## BƯỚC 1 — Dựng khung Core (chung cho mọi dự án)
Đây là phần **bắt buộc**, đặc tả đầy đủ ở [core/README.md](core/README.md). Không phụ thuộc ngôn ngữ hay kiến trúc.

1. Sao chép từ `core/templates/` vào gốc dự án (giữ đúng cấu trúc thư mục):
   * `AGENTS.md`, `CLAUDE.md`, `docs/project-brief.md`, `adrs/0000-template.md`
   * `.agents/skills/` (3 skill: `kit-consult`, `spec-first-task`, `health-check`)
   * `specs/`, `planning/`, `tasks/`
   * `.github/` (PR template, issue forms, SECURITY, CONTRIBUTING...) — **không** có workflow CI ở đây (CI thật tạo ở bước 3)
   * `.editorconfig`, `.env.example`
   * `gitignore.tpl` → đổi tên thành `.gitignore` (nếu đã có `.gitignore`: **gộp thêm các dòng còn thiếu**, không thay thế)
   * `.builder/kit.json`
2. Sao chép `core/standards/*` → `docs/standards/`.
3. **Lớp tương thích Agent** (theo công cụ đang chạy; xác minh lại đường dẫn theo tài liệu chính thức của công cụ vì chúng thay đổi nhanh):
   * `AGENTS.md`: Codex và Antigravity đọc trực tiếp. Claude Code đọc `CLAUDE.md` (đã chỉ import `AGENTS.md`).
   * Skills (chuẩn `SKILL.md`): nguồn ở `.agents/skills/`. Claude Code dùng `.claude/skills/` → **sao chép** sang đó (tránh symlink trên Windows).
   * Workflow/rule riêng của từng công cụ (nếu cần) sinh từ `AGENTS.md`, đừng viết hai nguồn sự thật.
4. Điền các `{{PLACEHOLDER}}` đã biết (tên dự án, ngày, `kit_ref`). Phần còn lại điền ở bước 2–3.
5. Nếu chưa phải repo git: `git init`. Không tự `commit`/`push` nếu người dùng chưa đồng ý.

## BƯỚC 2 — Phỏng vấn để chốt dự án
Làm theo [core/discovery.md](core/discovery.md): hỏi ít, gợi ý mặc định, giải thích đơn giản. Kết thúc bằng:
* `docs/project-brief.md` điền đủ (kèm giả định đã tự chọn)
* ADR stack và ADR kiến trúc (từ `adrs/0000-template.md`)
* Tóm tắt để người dùng **xác nhận** trước khi sang bước 3

## BƯỚC 3 — Áp profile đã chọn (cấu hình sâu theo dự án)
1. Đọc [profiles/README.md](profiles/README.md): chọn kiến trúc **từ tín hiệu** trong `docs/project-brief.md` (đừng hỏi người dùng tên kiến trúc), chọn mức rào chắn M1–M3, rồi đọc tài liệu profile đã chọn (tra thêm qua [INDEX.md](INDEX.md)).
2. Dựng **sơ đồ thư mục** theo profile kiến trúc; cài công cụ build/test/lint của stack **và rào chắn theo mức đã chọn** (ví dụ luật lint/tách project ép ranh giới import ở M2+).
3. Điền mục "Lệnh kiểm chứng" trong `AGENTS.md` bằng lệnh **thật** và đã chạy thử.
4. Tạo `.github/workflows/ci.yml` chạy đúng các lệnh đó (không dùng bước giả lập `echo`).
5. Bổ sung rule/skill riêng cho dự án nếu profile yêu cầu (ví dụ quy ước thêm tính năng, design system).
6. Cập nhật `.builder/kit.json` (`profiles`).

## BƯỚC 4 — Kiểm chứng
1. Chạy các lệnh test/lint/build; sửa đến khi xanh.
2. Chạy **Project Health Check** (xem [scripts/README.md](scripts/README.md)) → `project-review.md`; xử lý phát hiện mức Cao.
3. Báo cáo cho người dùng bằng lời đơn giản: đã tạo gì, kết quả kiểm chứng, họ nên làm gì tiếp theo.

## BƯỚC 5 — Đồng hành về sau
Từ đây dự án tự mang **Knowledge Router** trong `AGENTS.md`. Khi gặp việc kiến trúc, pattern, design system, test/CI, AI, hay có `project-review.md`, **chủ động tra [INDEX.md](INDEX.md)** (skill `kit-consult`) thay vì chờ người dùng chỉ dẫn. Chạy Health Check sau mỗi mốc lớn và trước khi mở PR.

---

## Quy tắc cho chính quy trình này
* **Không ghi đè** tệp của người dùng. **Không xóa** gì. Hỏi trước khi làm điều khó hoàn tác.
* **Không đặt** secret/API key vào tệp. Khuyên họ dùng `.env`.
* Không chắc điều gì → chọn mặc định an toàn, ghi vào mục "Giả định" của `docs/project-brief.md`, và nói với người dùng.
