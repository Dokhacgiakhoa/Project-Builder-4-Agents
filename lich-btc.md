# Lịch & quy định chính thức — AI20K Cohort 4 (BTC)

> **Hạng 1, bắt buộc.** Nguồn: deck *"AI20K Cohort 4 - Workshop 1 Kick off"* (Google Slides, 25 slide, chia sẻ bởi BTC), đọc ngày 27/09/2026 qua Claude in Chrome. Ghi ý, không chép nguyên văn.
> Deck ghi *"lịch trình dự kiến"*. Mốc cụ thể từng tuần (ngày giờ gate, hạn nộp) xem lịch Phoenix Agent, đã ghi trong `docs/planning/FACTS.md` `[F-01]`–`[F-01j]`.

## Master timeline (6 tuần, 10/09 – 22/10/2026)
| Tuần | Nội dung | Mốc |
|---|---|---|
| 1 | Kick-off & lập đội | 10/09. Hạn lập đội **13/09** (sau đó ghép ngẫu nhiên) |
| 2 | **Gate 1 — Chốt đề tài**. Khảo sát, phân tích đề, thu thập thông tin | Hạn **20/09** |
| 3 | Xây dựng MVP đầu tiên | — |
| 4 | **Gate 2 — MVP**. Tối ưu, cải thiện theo feedback | Lịch Phoenix: hạn MVP **04/10** `[F-01j]` |
| 5 | **Nộp hồ sơ Demo Day** (hồ sơ doanh nghiệp), hoàn thiện sản phẩm | — |
| 6 | **Demo Day** | **22/10/2026** |

Khuyến khích làm việc với khách hàng tiềm năng từ sớm để hiểu pain point.

## Nhịp tuần
- 2 workshop: tối T5 và CN (tăng ở các tuần sau).
- Office Hours: thường tối T2 hoặc T6.
- 2 buổi Mentoring Duty: tối **T4 và T7** (tiến độ, chấm điểm, gỡ khó).
- Từ tuần 4: thêm Build Hours buổi chiều, tập trung optimize, deploy, chuẩn bị demo.
- Mentor cố định với nhóm team suốt 6 tuần. Có mentoring 1-1 khi cần.

## Đội & quy ước tên
- Tối đa 4 người/đội. Chọn đề từ ngân hàng đề (tối đa 2 đội/đề).
- Discord nickname: `<Mã đội>-<Họ và tên>-<5 số cuối MSSV>`.
- Zoom: `<Mã nhóm>-<Mã đội>-<Họ và tên>-<5 số cuối MSSV>`.
- **Deploy URL phải chứa `c4-app-XXX`** (tên miền cấp 2 hoặc subdomain). Đội tự lo tên miền, BTC không cấp.

## 5 hoạt động bắt buộc
| Hoạt động | Cách nộp | XP |
|---|---|---|
| Tham gia đội | Mục "Đội của tôi" trên nền tảng | — |
| Daily stand-up, **mọi thành viên, mỗi ngày** | `/daily-standup` trong thread Thảo luận: yesterday · today · blocker | +5/người/lần |
| Weekly report trước mỗi buổi Mentor Duty (1 người đại diện) | `/mentor-duty submit`: done · doing · blocked · link · questions (≥ 30 ký tự) | +10/người |
| Gate đúng hạn (1 người đại diện) | `/gate submit`: chọn gate_key, link, ghi chú cho reviewer | +100/đội khi đạt |
| Hồ sơ Demo Day, **tuần 5** (1 người đại diện) | Mục Demo Day: tên, mô tả, link MVP · video demo · slides · thumbnail. **% đóng góp tổng = 100%**, **mỗi thành viên ≥ 50 AI log** | — |

- Gate **không chặn** đội đi tiếp. Gate dùng để đánh giá tiến độ và giúp mentor phát hiện đội cần hỗ trợ.
- Cấp XP: LV1 200 · LV2 500 · LV3 1.000 · LV4 1.500. Tham gia workshop +10/buổi.

## 10 deliverables bắt buộc (theo deck)
Source code · README · Sơ đồ kiến trúc · Tài liệu đặc tả, thiết kế · Tài liệu kiểm thử · Nhật ký làm việc (GitHub repo) · Live URL · Video demo · Pitch deck · AI Log.
- Nộp tại Demo Day và trên Phoenix Agent. Tài liệu đặt trong repo (thư mục `docs/`), cập nhật liên tục. Dán link vào `/gate submit` và hồ sơ Demo Day.
- Ví dụ file từ cohort trước: `README.md`, `ARCHITECTURE.md`, `WORKLOG.md`, `evaluation.md`.
- AI Log: mỗi thành viên tự tạo API key riêng và tự setup.
- ⚠️ Danh sách này **khác** checklist trong sách (`deliverables/checklist/`: có Weekly Journal, Evaluation Evidence…). **Theo deck** vì mới hơn và do BTC phát trực tiếp. Checklist sách chỉ để tham khảo cách làm.

## Workshop (14 buổi + 1 bổ sung)
Kick-off · Problem → MVP Canvas · PM & team cowork · Vibe coding 101 · AI Product Design · Tư duy Product · First Working Agent · RAG Pipeline · Multi-Step Agent · MCP & Multi-Agent · Optimize & Evaluate · Guardrails & Reliability · Go Live (CI/CD, deploy, observability) · The Pitch · (+ Data pipeline).

## Hỗ trợ
- Bot hệ thống: nhắc stand-up, deadline, theo dõi độ active, cảnh báo đội at-risk.
- KuteBot (`@Trợ lý Kute`): hỏi đáp 24/7 về chương trình.
- Lệnh Discord: `/daily-standup` · `/mentor-duty submit|view|update|history|suggest` · `/topic available|pick|view|change` · `/gate list|status|submit|view` · `/myteam members` · `/rank` · `/ticket create|close`.
- Nguyên tắc: *"Scope down sớm tốt hơn scope creep."*
