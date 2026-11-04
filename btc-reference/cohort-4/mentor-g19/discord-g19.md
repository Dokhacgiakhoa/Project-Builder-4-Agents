# Discord G19 #thảo-luận-nhóm — chỉ dẫn mentor

Nguồn: ảnh chụp do Khoa cung cấp ngày 2026-09-26. Trích ý, không nguyên văn.

## 19/09 23:46 · Hoàng
- Gửi `slides_1.html`, `slides_2.html`, `sample_prd.md`.

## 19/09 23:57 · Hoàng: cách estimate (tham khảo, "không chuẩn 100%")
- 19/09 chốt architecture và bắt đầu implement → tới 17/10 còn khoảng 27–28 ngày.
- Team 4 người → 4 × 28 = **112 manday**.
- Mục tiêu: 3–5 feature nhưng đủ sâu. 1 feature ≈ 3–5 user story. 1 story ≈ 4 task (FE, BE, AI, DevOps). 1 task ≈ 1 ngày.
- → 1 feature ≈ 4 story × 4 task = **16 manday**.
- Dành **60%** thời gian cho implement feature, 40% cho tích hợp, fix bug, tài liệu.
- → 112 × 60% ≈ 67 manday → 67 / 16 ≈ **4 feature chính**. Có thể giảm còn 3 feature làm thật chỉn chu.
- Team 3 người → tối đa 3 feature. Thành viên non-technical không tính vào manday dev.

## 20/09 00:09 · Hoàng: cách làm việc
- Conflict: mỗi tuần 1 Tech Lead, chịu trách nhiệm feature tuần đó, quyết cuối khi team bất đồng. Còn phân vân thì hỏi mentor, nhưng người quyết vẫn là team.
- Nhịp: 3–4 feature trong khoảng 5 tuần, mỗi tuần cố hoàn thành 1 feature và live demo ở mentor duty. Tuần đầu: design architecture + interface, integrate 1 luồng end-to-end (cố tích hợp xong ít nhất 1 user story trong feature đầu).
- Giao tiếp: raise issue ngay trong nhóm chat Discord. Mentor trả lời trong ngày (sáng → tối). Platform BTC review theo gate BTC. Kênh làm việc chính với mentor là Discord.
- Gửi `slides_3.html` (build project, kanban board).

## 22/09 · Hoàng trả lời Khoa
- 11:36: deadline chấm Gate 1 của mentor là **27/09**.
- 11:44: có blocker thì nhắn nhóm chat riêng, mentor trả lời trong tối đa 2 buổi. Buổi mentor duty để demo tiến độ liên tục và cùng các nhóm khác hỏi đáp.
- 12:36: mentor thường review sát deadline. Theo đúng lịch BTC để không bị trừ XP.
- 12:40: **làm xong thì merge vào `main`**. Mentor chỉ review trên `main`, không theo dõi các nhánh. Best practice: tạo PR vào `main`, assign reviewer.

## 24/09 20:57 · Tâm
- Gửi slide "Dùng Claude Code hiệu quả" (`claude-code-g19.html`).

## Ghi chú cho agent
- Các số 112 / 60% / 16 manday / 4 feature **có nguồn** là tin Discord 19/09 23:57 ở trên, không nằm trong 3 deck slide. `docs/planning/FACTS.md` dòng 82 hiện ghi "không tồn tại trong 3 deck", đúng với slide nhưng thiếu nguồn Discord → cần PM quyết có đưa vào FACTS (kèm `[Discord 19/09]`) không.
- Git: slide buổi 1 mô tả luồng `feat → dev → test → stg → main`. Chỉ dẫn Discord 22/09 là **PR thẳng vào `main`**. Repo hiện theo Discord.
