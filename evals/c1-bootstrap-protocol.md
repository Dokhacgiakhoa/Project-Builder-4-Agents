# C1 — KỊCH BẢN KIỂM CHỨNG BOOTSTRAP VỚI AGENT THẬT

> Dành cho người bảo trì kit. Mục tiêu: xem Agent **tự** đọc `BOOTSTRAP.md`, phỏng vấn, chọn profile và dựng dự án đúng không. Chạy bằng **Claude Code** và **Antigravity** (Codex chưa kiểm chứng). Ghi kết quả vào mục 5 và cập nhật `TASKS.md` (C1, C4).

## 1. Điều kiện để phép thử có giá trị
* **Phiên mới, không ngữ cảnh**: không dán nội dung kit, không nhắc tên tệp. Agent chỉ có câu prompt ở mục 2.
* **Thư mục thử nằm ngoài repo kit**, không có sẵn `AGENTS.md`/`.agents/` (kịch bản S1) hoặc chỉ có dự án dở (S2).
* Kit phải lấy được: sau khi **B1 (đổi tên repo) + push** thì dùng URL; trước đó dùng biến thể đường dẫn cục bộ (mục 2b). Ghi rõ biến thể đã dùng.
* Người thử trả lời **đúng theo vai (mục 3)**, không gợi ý thêm.

## 2. Prompt (đúng một câu)
a. Có URL: `Hãy dùng https://github.com/Dokhacgiakhoa/Project-Builder-Kit để dựng dự án giúp mình. Mình muốn làm: <mô tả ở mục 3>`
b. Chưa có URL (thử sớm): `Hãy dùng bộ tài liệu ở <đường dẫn thư mục kit trên máy> để dựng dự án giúp mình, bắt đầu từ BOOTSTRAP.md. Mình muốn làm: <mô tả ở mục 3>`

## 3. Kịch bản và vai người dùng
| Mã | Thư mục thử | Mô tả đưa cho Agent | Kỳ vọng kiến trúc | Mức rào chắn |
| :-- | :-- | :-- | :-- | :-: |
| S1 | Rỗng | "một web nhỏ để mình ghi chi tiêu hằng ngày, làm đồ án môn học" | Layered đơn giản | M1 |
| S2 | Có dự án dở (ví dụ app Node/React nhỏ, đã có `package.json`, `src/`, chưa có `AGENTS.md`) | "dự án này đang làm dở, hãy thiết lập cho chuẩn" | Giữ nguyên cấu trúc hiện có; chế độ MERGE, không ghi đè | M1 |
| S3 | Rỗng | "hệ thống đặt lịch cho nhiều chi nhánh phòng khám, có quy tắc giá, sẽ phát triển nhiều năm" | Clean Architecture hoặc Modular Monolith, có lý do | M2 trở lên |

**Vai người dùng**: fresher, biết chút ít về git, không biết thuật ngữ kiến trúc. Khi Agent hỏi:
* về công nghệ: "mình không rành, bạn chọn giúp";
* về ngân sách: "miễn phí";
* về người làm: "một mình" (S1, S2), "nhóm 3 người" (S3);
* thuật ngữ lạ: nhờ giải thích, rồi đồng ý với đề xuất.

## 4. Checklist chấm (mỗi mục Đạt/Không đạt + ghi chú)
**Chủ động và định tuyến**
1. Agent tự mở `BOOTSTRAP.md` (không cần nhắc tên tệp).
2. Agent tra `INDEX.md`/`profiles/README.md`, không hỏi người dùng tên kiến trúc.
3. Số tài liệu kit đã mở hợp lý (không đọc cả thư mục `knowledge-base/`).
4. Chọn đúng profile kỳ vọng, nêu **lý do một câu** và phương án đã loại.

**Phỏng vấn**
5. ≤ 3 câu mỗi lượt; bắt đầu bằng người dùng/vấn đề, không bằng công nghệ.
6. Có bước tóm tắt và **chờ xác nhận** trước khi dựng khung.

**Dựng khung Core**
7. Có `AGENTS.md`, `CLAUDE.md` (import `AGENTS.md`), skills đúng chỗ công cụ đọc được, `docs/project-brief.md`, ADR stack + kiến trúc, `.builder/kit.json`.
8. Không còn `{{PLACEHOLDER}}` sau khi hoàn tất.
9. S2: không ghi đè hay xóa tệp của người dùng; tệp trùng có bản `.kit-suggested`.
10. Không tự `commit`/`push` khi chưa được đồng ý.

**Rào chắn và kiểm chứng**
11. Lệnh test/lint/build trong `AGENTS.md` là lệnh **thật** và đã chạy.
12. CI chạy đúng các lệnh đó (không `echo` giả lập).
13. Cài rào chắn đúng mức đã chọn (M2+: có luật ép ranh giới import).
14. Chạy Health Check; điểm ≥ 80; Core Baseline B1–B9 đạt.
15. Báo cáo cuối cho người dùng bằng lời đơn giản.

**An toàn**
16. Không đặt secret vào tệp; có `.env.example`.

## 5. Mẫu ghi kết quả
| Ngày | Agent + phiên bản | Kịch bản | Biến thể prompt | Đạt/16 | Điểm Health Check | Chỗ sai/lệch (mục checklist, mô tả) | Sửa gì trong kit |
| :-- | :-- | :-- | :-: | :-: | :-: | :-- | :-- |
| | | | | | | | |

Đính kèm: bản ghi hội thoại (hoặc ảnh chụp), cây thư mục kết quả, `project-review.md`.
