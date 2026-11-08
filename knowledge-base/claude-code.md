# Dùng Claude Code hiệu quả — Phan Minh Tâm · Bùi Việt Hoàng (24/09)

Nguồn: `../cohort-4/mentor-g19/raw/claude-code-g19.html` (27 slide). Ghi ý. Áp dụng được cho mọi coding agent.

## 5 câu cốt lõi
1. Context là ngân sách, không phải bộ đệm. Chỉ tiêu vào thứ phục vụ task hiện tại.
2. Sau mỗi turn chủ động chọn: Continue · Rewind · Clear · Compact · Subagent.
3. Tách pha Explore → Plan → Implement → Verify, luôn có tín hiệu pass/fail.
4. CLAUDE.md càng ngắn càng tốt. Bỏ một dòng mà Claude không dễ sai → cắt dòng đó.
5. Task lớn: chốt spec trong repo trước khi code. Spec tốt làm Clear "rẻ".

## Context
- Context rot: context càng đầy, attention càng loãng, trả lời vẫn tự tin nhưng lệch intent, không có cảnh báo. Heuristic của đội mentor: giữ conversation active ở khoảng 1/3 cửa sổ. Kiểm bằng `/context`.
- Đáng giữ: file liên quan, ràng buộc, quyết định đã chốt, bằng chứng verify. Nhiễu: vòng debug thất bại, nhánh cũ, output dài hết giá trị, task không liên quan.

## Chọn gì sau mỗi turn (theo thứ tự)
- Task kế không phụ thuộc context vừa xây → **Clear**.
- Vừa đi sai hướng → **Rewind** (Esc Esc hoặc `/rewind`). Giữ phần đọc hiểu, bỏ nhánh sai. Trước khi rewind, bảo agent tóm tắt 3 dòng vì sao fail. Checkpoint không theo dõi thay đổi từ Bash, nên không thay được Git.
- Chỉ cần kết luận → **Subagent** (context riêng, "phòng sạch"): điều tra flow, review diff theo spec, draft docs, tìm edge case.
- History dài nhưng cần phần lớn → **Compact** sớm, kèm hướng dẫn giữ gì bỏ gì. Viết lại brief mất < 2 phút thì Clear.
- Còn lại → Continue.
- Quy tắc hai lần: sửa agent quá 2 lần cùng một lỗi → Clear và viết lại prompt.
- Tách session theo mục đích: implement / review / điều tra. Reviewer ở context sạch bắt lỗi tốt hơn.

## Làm việc
- Bỏ qua Plan khi mô tả được diff trong 1 câu. Đụng nhiều file, dependency ngầm, vùng code lạ → plan.
- Luôn cho cách tự verify: test, build, lint, script, screenshot đối chiếu. Đòi bằng chứng, không hỏi "xong chưa".
- Prompt cụ thể: file/thư mục · constraint · pattern có sẵn để làm theo · triệu chứng quan sát được.
- CLAUDE.md: giữ lệnh riêng của repo, code style khác mặc định, quy trình test/branch/PR, quyết định kiến trúc. Tránh giải thích dài, lời khuyên chung, tài liệu API, thông tin hay đổi.
- Spec-first: để agent phỏng vấn → viết `SPEC.md` → mở session mới để thực thi. GitHub Spec Kit (`/speckit.constitution` → `specify` → `clarify` → `plan` → `tasks` → `analyze` → `implement`) là tuỳ chọn. Spec không thay verify.

## 5 failure pattern
Kitchen sink session · sửa đi sửa lại · CLAUDE.md quá dài · tin mà không verify · khám phá vô hạn.
