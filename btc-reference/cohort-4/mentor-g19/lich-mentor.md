# Mentor G19 — lịch, mốc, chỉ dẫn riêng cho đội (tham khảo)

> ⚠️ **Mentor, tham khảo.** Thời gian luôn theo BTC ([`../lich-btc.md`](../lich-btc.md)). Mốc dưới đây là nhịp đề xuất, không phải hạn.
> Nguồn: slide buổi 1 và 3 (`raw/slides_1.html`, `raw/slides_3.html`). Tin Discord: [`discord-g19.md`](discord-g19.md). Phương pháp: [`../../khung-chung/phuong-phap-mentor.md`](../../khung-chung/phuong-phap-mentor.md).

## Mentor & phạm vi
- Bùi Việt Hoàng (Senior AI/MLOps Engineer) · Phan Minh Tâm. Nhóm G19, team 149–156.
- Duty T7 20:00–22:00 (Hoàng): 19/09, 26/09, 03/10, 10/10, 17/10. Track T4 (Tâm) theo lịch BTC `[F-01b]`.

## Mốc đề xuất (mentor)
| Ngày | Mốc | Ghi chú đối chiếu BTC |
|---|---|---|
| 19/09 | Kickoff: problem, role, scope, happy path | — |
| 26/09 | Design: architecture tối thiểu, contract, backlog, DoD | — |
| 03/10 | **Design freeze** + architecture review (nộp tech design doc + diagram trước duty) | Trùng tuần Gate 2 MVP của BTC |
| 10/10 | **Walking skeleton** chạy trên env chung, mentor bấm thử | — |
| 15/10 | Code freeze, chỉ fix bug. Feature chưa xong bị loại khỏi review 17/10 | — |
| 16/10 | Deploy env chung | — |
| 17/10 | Final review của mentor | **Không phải Demo Day.** Demo Day theo BTC: 22/10 |

## Chỉ dẫn vận hành đội (mentor đề xuất, đội được tự chia)
- Vai: technical (own module, code + test, interface, deploy) · non-technical tối đa 1 (PO, BA, E2E, wireframe).
- Xoay vòng Tech Lead + PO mỗi tuần. TL quyết cuối technical. (Đội P-062 chọn vai cố định, xem `AGENTS.md` → `phan-vai.md`.)
- Cadence: T7 duty → CN–T5 build → T6 gom evidence (URL, commit, test, câu hỏi). Trước 20:00 T7: TL gom progress, blocker, quyết định cần hỗ trợ.
- Git (slide buổi 1): `feat → dev → test → stg → main`. ⚠️ Discord 22/09: **PR thẳng vào `main`**, mentor chỉ review `main`. Repo theo Discord.
- Estimate (Discord 19/09): 112 manday, 60% implement, ~4 feature → `[F-17]` trong `FACTS.md` (tham khảo, MVP dùng `[F-16b]`).
