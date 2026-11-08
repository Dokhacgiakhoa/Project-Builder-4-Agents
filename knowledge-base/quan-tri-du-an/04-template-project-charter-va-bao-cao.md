# Mẫu Điều Lệ Dự Án (Project Charter) & Báo Cáo Tuần (VinUni / AI20K)

> Được trích xuất đầy đủ và chuyển đổi định dạng Markdown từ bảng tính mẫu chính thức của AI20K & VinUni.

---

## Sheet 1: Quy Định

| Quy định vận hành — Giai đoạn RA | Cột B |
| --- | --- |
| 1. Thời gian làm việc |  |
| Giờ làm việc | Full-time: tối thiểu 40 giờ/tuần, từ Thứ 2 đến Thứ 7 |
| Giờ core | 09:00-11:30 và 14:00-17:00 — tất cả thành viên phải online |
| Daily Standup | 09:00 mỗi sáng (15 phút). Báo cáo về mentor: what done / doing / blockers |
| Nghỉ phép | Báo trước 24h cho team lead + mentor. Tối đa 2 ngày/6 tuần |
| 2. Báo cáo &amp; Trách nhiệm giải trình |  |
| Daily Standup Report | Gửi hàng ngày cho mentor (Discord hoặc email). Nội dung: done / doing / blockers |
| Báo cáo tuần | Tổng hợp trước mỗi Mentor Meeting T4. Sử dụng mẫu ở sheet 'Mẫu Báo Cáo Tuần' |
| Nội dung bắt buộc | Tiến độ, Metrics, Blockers, Kế hoạch tuần sau, Screenshots, Link File Quản Trị |
| Báo cáo muộn | Cảnh báo lần 1. Quá 3 lần → meeting với lead mentor |
| Mentor Meeting | Tối T4: chung 1h30 (bắt buộc). T7: riêng 45p/team (bắt buộc) |
| 3. Tài liệu dự án (Song song) |  |
| GitHub | Code + README.md + Architecture. Commit ít nhất 1 lần/ngày khi có coding |
| File Quản Trị Dự Án | Google Sheet hoặc Excel. Chứa: mọi đường link quan trọng, đặc tả tính năng, progress tracking, risks, meeting notes |
| Branching | GitFlow hoặc GitHub Flow. PR phải được ít nhất 1 thành viên review |
| Documentation | README.md cập nhật liên tục. Architecture diagram update khi thay đổi |
| Testing | Viết test cho core features. Tối thiểu unit tests cho business logic |
| 4. Quản lý đối tác |  |
| Xác định stakeholder | Hoàn thành trong W1. Mentor hỗ trợ kết nối |
| Meeting với stakeholder | W1 (giới thiệu) → W2 (đề xuất solution) → End W3 (Demo 1) → End W5 (Demo 2) |
| Feedback thu thập | Ghi chép mọi feedback. Báo cáo trong File Quản Trị + báo cáo tuần |
| Tác phong chuyên nghiệp | Đúng giờ, chuẩn bị kỹ, follow-up email sau mỗi meeting |
| 5. Xử lý vấn đề &amp; Hỗ trợ |  |
| Blocker kỹ thuật | Post trên Discord #support → mentor phản hồi trong 24h |
| Blocker stakeholder | Báo mentor ngay → mentor hỗ trợ kết nối/giải quyết |
| Xung đột team | Team lead giải quyết trước. Không được → escalate mentor |
| Thành viên thiếu trách nhiệm | Cảnh báo lần 1 → meeting với mentor → quyết định program |
| 6. Đánh giá &amp; Chấm điểm |  |
| Tiêu chí chính | 1) Sản phẩm V1 chạy với real data <br> 2) Stakeholder satisfaction <br> 3) Code quality <br> 4) Team collaboration &amp; accountability |
| Đánh giá liên tục | Mentor cho feedback mỗi meeting. Không chờ đến cuối |
| Đánh giá cuối kỳ (W6) | Demo + Q&amp;A + scoring. Dựa trên Impact Report + Presentation |
| Tiếp tục khởi nghiệp hay không | Sau W6, team + mentor đánh giá tiềm năng → quyết định tiếp startup |
| 7. Nguyên tắc văn hóa |  |
| Trách nhiệm | Ai làm nấy chịu. Việc của mình thì mình phải hoàn thành, không đùn cho người khác |
| Nói thật | Báo cáo thật, kể cả khi chưa tốt. Giấu vấn đề còn nguy hiểm hơn vấn đề |
| Chạy được quan trọng hơn hoàn hảo | Sản phẩm chạy được với người dùng thật quan trọng hơn code đẹp nhưng không xong kịp |
| Sai thì sửa nhanh | Làm sai không sao, quan trọng là nhận ra và sửa nhanh. Không ai blame ai |
| Tôn trọng nhau | Đúng giờ, trân trọng thời gian của người khác. Đã hẹn thì phải có mặt |


---

## Sheet 2: Mẫu Quy Định Nội Bộ

| Mẫu quy định nội bộ team | Cột B | Cột C | Cột D | Cột E | Cột F |
| --- | --- | --- | --- | --- | --- |
| Mỗi team điền 1 bản trong tuần 1, chốt cùng team lead. Cập nhật khi có thay đổi. |  |  |  |  |  |
| 1. Thông tin nhóm |  |  |  |  |  |
| Tên team | [Alpha / Beta / Gamma / Delta] |  |  |  |  |
| Tên dự án | [Tên sản phẩm] |  |  |  |  |
| Ngày lập | [DD/MM/YYYY] |  |  |  |  |
| Ngày cập nhật gần nhất | [DD/MM/YYYY] |  |  |  |  |
| 2. Vai trò trong nhóm |  |  |  |  |  |
| Họ tên | Vai trò chính | Vai trò phụ (nếu có) | Trách nhiệm cụ thể | Thời gian cam kết <br> (giờ/tuần) | Ghi chú |
| [Tên] | Team Lead | 51 |  | 40 |  |
| [Tên] | [Backend / Frontend / AI / Design] | 55 |  | 40 |  |
| [Tên] | [Vai trò] | 59 |  | 40 |  |
| [Tên] | [Vai trò] | 59 |  | 40 |  |
| 3. Quy tắc giao việc &amp; phân công |  |  |  |  |  |
| Ai phân việc | Team Lead là người phân việc chính. Nếu lead bận, deputy (thành viên được ủy quyền) phân thay. |  |  |  |  |
| Nguyên tắc phân việc | Rõ ràng: mỗi việc có 1 người chịu trách nhiệm chính, deadline cụ thể, kết quả mong đợi viết rõ. <br> Không giao chung chung 'ai rảnh thì làm'. |  |  |  |  |
| Cập nhật tiến độ | Thành viên cập nhật trạng thái việc qua daily standup + cột status trên GitHub Issues hoặc Notion. |  |  |  |  |
| Khi nhận việc | Người nhận xác nhận trong vòng 2 giờ. Nếu không hiểu yêu cầu → hỏi ngay, không im lặng rồi làm sai. |  |  |  |  |
| Khi sắp trễ deadline | Báo team lead trước ít nhất 4 giờ. Không đợi đến lúc hết hạn mới nói 'em chưa xong'. |  |  |  |  |
| Khi cần nhờ giúp | Tag trực tiếp người cần giúp trên Discord, kèm mô tả ngắn gọn vấn đề. Không nhắn chung chung 'ai giúp em với'. |  |  |  |  |
| Code review | Mọi PR phải được ít nhất 1 người khác review trước khi merge. PR dưới 400 dòng — nếu lớn hơn thì chia nhỏ. |  |  |  |  |
| 4. Phương thức liên lạc |  |  |  |  |  |
| Kênh | Mục đích | Thời gian phản hồi | Quy tắc | Ghi chú |  |
| Discord — #team-xxx | Tin nhắn hàng ngày, hỏi đáp nhanh, standup text | Trong vòng 2 giờ (giờ làm việc) | Tag người cần trả lời. Không spam. |  |  |
| Discord — #team-xxx-standup | Daily standup text mỗi sáng | Gửi trước 09:30 | Theo mẫu Daily Standup sheet bên cạnh |  |  |
| Call / Voice chat Discord | Thảo luận cần nói chuyện trực tiếp | Thỏa thuận trước | Ghi quyết định vào text channel sau khi call |  |  |
| GitHub Issues / PR | Thảo luận kỹ thuật, bug, feature | Trong vòng 1 ngày làm việc | Mọi thay đổi code phải qua PR, có mô tả rõ |  |  |
| Google Drive / Google Docs | Tài liệu chung, báo cáo, bản nháp | — | Đặt tên file rõ ràng. Không để 'Bản sao không tiêu đề' |  |  |
| Email | Liên hệ mentor, đối tác ngoài, chính thức | Trong vòng 24 giờ | Dùng cho nội dung cần lưu vết rõ ràng |  |  |
| 5. Quản lý mã nguồn (Git / GitHub) |  |  |  |  |  |
| Repository | 1 repo GitHub cho mỗi team. Tên repo rõ ràng, không viết tắt khó hiểu. |  |  |  |  |
| Branch chính | main → chỉ merge code đã review và test. Không push thẳng lên main. |  |  |  |  |
| Branch quy ước | feature/tên-tính-năng — cho tính năng mới <br> bugfix/tên-lỗi — cho sửa lỗi <br> hotfix/... — cho sửa gấp trên production |  |  |  |  |
| Commit message | Viết tiếng Anh, ngắn gọn, bắt đầu bằng động từ: <br> Thêm: feature thêm trang dashboard <br> Sửa: fix crash khi đăng nhập <br> Cập nhật: update API trả về đúng format |  |  |  |  |
| Pull Request | Mọi thay đổi qua PR. Tiêu đề PR ghi rõ làm gì. Mô tả: thay đổi gì, tại sao, test thế nào. Gắn link issue nếu có. |  |  |  |  |
| Code review | Ít nhất 1 người review trước khi merge. Review trong vòng 4 giờ làm việc. Góp ý cụ thể, không nói chung chung. |  |  |  |  |
| Merge | Chỉ merge khi pass review + không conflict. Xóa branch sau khi merge. |  |  |  |  |
| .gitignore | Không commit: node_modules, .env, API keys, file build, file tạm. Thêm vào .gitignore từ đầu. |  |  |  |  |
| README.md | Giữ cập nhật: cách chạy project, cấu trúc thư mục, biến môi trường cần thiết, link tài liệu liên quan. |  |  |  |  |
| 6. Lịch làm việc &amp; điểm danh |  |  |  |  |  |
| Giờ làm việc | Thứ Hai — Thứ Sáu, 09:00 — 18:00. Trưa nghỉ 12:00 — 13:30. <br> Team tự sắp xếp nhưng phải đảm bảo overlapping hours (ít nhất 4 tiếng trùng nhau). |  |  |  |  |
| Daily standup | 09:00 mỗi sáng. Xem chi tiết ở sheet Mẫu Daily Standup. |  |  |  |  |
| Vắng mặt | Báo team lead trước 1 ngày (hoặc sớm nhất có thể nếu đột xuất). Gửi standup text dù không tham gia. |  |  |  |  |
| Nghỉ phép | Tối đa 2 ngày/6 tuần. Sắp xếp trước với team lead để phân việc lại. Không nghỉ liên tiếp gần deadline. |  |  |  |  |
| Overtime | Tránh tối đa. Nếu deadline ép → team cùng quyết định, không ép cá nhân. Overtime phải có lý do rõ ràng. |  |  |  |  |
| Cuối tuần | Thứ Bảy: mentor meeting (bắt buộc). Chủ Nhật: nghỉ, trừ trường hợp khẩn cấp do team cùng chốt. |  |  |  |  |
| 7. Xử lý xung đột &amp; ra quyết định |  |  |  |  |  |
| Nguyên tắc chính | Bất đồng ý kiến là bình thường. Cách xử lý mới quan trọng: <br> 1. Nêu rõ quan điểm + lý do <br> 2. Lắng nghe phía kia <br> 3. Tìm điểm chung <br> 4. Nếu không tự hòa giải → team lead quyết định |  |  |  |  |
| Ai quyết định | Vấn đề kỹ thuật → người có chuyên môn mạnh nhất quyết định. <br> Vấn đề tiến độ/phạm vi → team lead quyết định. <br> Vấn đề ảnh hưởng cả team → cả team vote, lead phá vỡ thế hòa. |  |  |  |  |
| Không ai đồng tình | Team lead có quyền quyết định cuối. Mọi người thực hiện đúng quyết định đã chốt, không âm ỉ phản đối. |  |  |  |  |
| KHI nào nhờ mentor | Xung đột kéo dài quá 2 ngày không giải quyết được. Hoặc ảnh hưởng đến tiến độ chung → lead báo mentor ngay. |  |  |  |  |
| 8. Tiêu chuẩn chất lượng |  |  |  |  |  |
| Code | Chạy được chưa đủ. Code phải dễ đọc, có comment ở chỗ phức tạp, tên biến/hàm rõ nghĩa. <br> Không để dead code (code không dùng đến). |  |  |  |  |
| Test | Mỗi tính năng chính phải có test. Ít nhất test được happy path + 1 trường hợp lỗi. |  |  |  |  |
| Documentation | README luôn cập nhật. API phải có mô tả endpoint. Architecture diagram cập nhật khi thay đổi cấu trúc. |  |  |  |  |
| UI / UX | Không cần đẹp hoàn hảo, nhưng phải dùng được. Không có lỗi hiển thị rõ ràng (layout vỡ, text đè nhau, button không bấm được). |  |  |  |  |
| Performance | Trang chính load dưới 3 giây. API phản hồi dưới 1 giây. Nếu chậm hơn → ghi lý do và kế hoạch tối ưu. |  |  |  |  |
| Security | Không hardcode API key, password. Dùng .env cho biến môi trường. Validate input từ người dùng. |  |  |  |  |
| 9. Cam kết của từng thành viên |  |  |  |  |  |
| Mỗi thành viên ký xác nhận đã đọc và đồng ý với quy định trên. |  |  |  |  |  |
| Họ tên | Vai trò | Xác nhận <br> (Có / Chưa) | Ngày | Chữ ký |  |
| [Tên] | Team Lead | 22 |  |  |  |
| [Tên] | [Vai trò] | 22 |  |  |  |
| [Tên] | [Vai trò] | 22 |  |  |  |
| [Tên] | [Vai trò] | 22 |  |  |  |
| 10. Phê duyệt |  |  |  |  |  |
| Vai trò | Họ tên | Ngày | Xác nhận |  |  |
| Team Lead | [Tên] | [DD/MM/YYYY] |  |  |  |
| Mentor | [Tên mentor] | [DD/MM/YYYY] |  |  |  |


---

## Sheet 3: Mẫu Báo Cáo Tuần

| Mẫu báo cáo tuần — Giai đoạn RA | Cột B | Cột C | Cột D |
| --- | --- | --- | --- |
| Nộp hàng ngày qua Daily Standup \| Tổng hợp nộp trước mỗi Mentor Meeting (T4 tối) |  |  |  |
| Phần 1: Thông tin cơ bản |  |  |  |
| Team: | [Alpha / Beta / Gamma / Delta] |  |  |
| Tuần: | [W1-W6] — [Ngày bắt đầu] đến [Ngày kết thúc] |  |  |
| Người báo cáo: | [Tên Team Lead] |  |  |
| Ngày nộp: | [DD/MM/YYYY] |  |  |
| Phần 2: Tiến độ |  |  |  |
| # | Mục tiêu / Task | Trạng thái | Ghi chú |
| 1.0 | [Mô tả task] | Done / In Progress / Blocked | [Ghi chú] |
| 2.0 | [Mô tả task] | Done / In Progress / Blocked | [Ghi chú] |
| 3.0 | [Mô tả task] | Done / In Progress / Blocked | [Ghi chú] |
| 4.0 | [Mô tả task] | Done / In Progress / Blocked | [Ghi chú] |
| 5.0 | [Mô tả task] | Done / In Progress / Blocked | [Ghi chú] |
| Phần 3: Số liệu |  |  |  |
| Metric | Giá trị | Ghi chú |  |
| Features hoàn thành | [X/Y] |  |  |
| Bugs còn mở | [số] |  |  |
| Stakeholder meetings tuần này | [số] |  |  |
| Deployment status | [Local / Staging / Production] |  |  |
| File Quản Trị cập nhật? | [Yes / No] | Link đính kèm |  |
| Phần 4: Vướng mắc &amp; Rủi ro |  |  |  |
| [Liệt kê blockers, rủi ro, đề xuất giải pháp. Nếu không có, ghi 'Không có blockers.'] |  |  |  |
| Phần 5: Kế hoạch tuần sau |  |  |  |
| # | Task | Assignee | Priority |
| 1.0 | [Task cho tuần sau] | [Tên] | High / Medium / Low |
| 2.0 | [Task cho tuần sau] | [Tên] | High / Medium / Low |
| 3.0 | [Task cho tuần sau] | [Tên] | High / Medium / Low |
| Phần 6: Bằng chứng (Screenshots / Links / File quản trị) |  |  |  |
| [Dán link screenshots, demo recordings, File Quản Trị Dự Án. Tối thiểu 1 screenshot/tuần.] |  |  |  |


---

## Sheet 4: Mẫu Project Charter

| Project Charter — Mẫu theo chuẩn PMP | Cột B | Cột C | Cột D | Cột E |
| --- | --- | --- | --- | --- |
| Mỗi team điền 1 bản trong tuần 1. Nộp trước Mentor Meeting T4. |  |  |  |  |
| 1. Thông tin dự án |  |  |  |  |
| Tên dự án | [Tên sản phẩm / dự án] |  |  |  |
| Team | [Alpha / Beta / Gamma / Delta] |  |  |  |
| Người lập | [Tên Team Lead] |  |  |  |
| Ngày lập | [DD/MM/YYYY] |  |  |  |
| Phiên bản | [1.0 — cập nhật mỗi khi thay đổi lớn] |  |  |  |
| 2. Lý do thực hiện &amp; Mục tiêu |  |  |  |  |
| Vấn đề đang gặp | [Mô tả bài toán thực tế tại VinUni mà team đang giải quyết. Ví dụ: Phòng Tuyển sinh mất nhiều giờ trả lời câu hỏi lặp, sinh viên không có hướng dẫn học cá nhân hóa...] |  |  |  |
| Giải pháp đề xuất | [Mô tả ngắn gọn sản phẩm sẽ xây dựng. Tránh viết dài, tập trung vào: làm gì cho ai, giải quyết vấn đề gì] |  |  |  |
| Mục tiêu SMART (6 tuần) | [Ví dụ: Triển khai chatbot tư vấn tuyển sinh cho Phòng Tuyển sinh VinUni, phục vụ 100+ lượt hỏi/tháng, giảm 50% thời gian trả lời câu hỏi lặp] |  |  |  |
| 3. Phạm vi dự án |  |  |  |  |
| # | Trong phạm vi (In-scope) | Ngoài phạm vi (Out-of-scope) |  |  |
| 1.0 | [Tính năng/công việc sẽ làm] | [Tính năng/công việc KHÔNG làm] |  |  |
| 2.0 | [Tính năng/công việc sẽ làm] | [Tính năng/công việc KHÔNG làm] |  |  |
| 3.0 | [Tính năng/công việc sẽ làm] | [Tính năng/công việc KHÔNG làm] |  |  |
| 4.0 | [Tính năng/công việc sẽ làm] | [Tính năng/công việc KHÔNG làm] |  |  |
| 5.0 | [Tính năng/công việc sẽ làm] | [Tính năng/công việc KHÔNG làm] |  |  |
| 4. Đối tác liên quan (Stakeholders) |  |  |  |  |
| Vai trò | Họ tên / Đơn vị | Mức ảnh hưởng <br> (Cao/Trung bình/Thấp) | Trách nhiệm |  |
| Sponsor / Người quyết định | [Ai phê duyệt và cấp nguồn lực] | 199 |  |  |
| Khách hàng / Người dùng | [Ai sẽ sử dụng sản phẩm] | 205 |  |  |
| Team Lead | [Tên] | Cao | [Điều phối team, báo cáo mentor, phân việc] |  |
| Thành viên 1 | [Tên] | 215 |  |  |
| Thành viên 2 | [Tên] | 221 |  |  |
| Thành viên 3 | [Tên] | 221 |  |  |
| Mentor | [Tên mentor] | Cao | [Hướng dẫn, kết nối đối tác, review] |  |
| 5. Cột mốc chính (Milestones) |  |  |  |  |
| Cột mốc | Tuần | Ngày dự kiến | Sản phẩm nộp | Người chịu trách nhiệm |
| Kickoff &amp; Project Charter | W1 | 25-31/05 | Project Charter + Quy chế | Team Lead |
| Đề xuất giải pháp với đối tác | W2 | 01-07/06 | Solution Design + Architecture | Team Lead |
| Demo 1 với đối tác | W3 | 08-14/06 | Bản Demo 1 + Phản hồi đối tác | Team |
| Hoàn thiện sản phẩm | W4-W5 | 15-28/06 | Sản phẩm hoàn thiện + Deploy | Team |
| Demo 2 với đối tác | W5 | 22-28/06 | Bản Demo 2 + Đánh giá hài lòng | Team |
| Đánh giá cuối kỳ | W6 | 29-05/07 | Báo cáo tác động + Slide thuyết trình | Team Lead |
| 6. Nguồn lực &amp; Ngân sách |  |  |  |  |
| Nhân sự (số người x giờ/tuần) | [4 người x 40 giờ/tuần = 160 người-giờ/tuần] |  |  |  |
| Công cụ (miễn phí) | [GitHub, Discord, Render free tier, Supabase free, Google Drive...] |  |  |  |
| Công cụ (cần duyệt chi phí) | [Nếu cần: VPS ~$10/tháng, API key ~$20/tháng — ghi rõ ở sheet Hỗ Trợ Teams] |  |  |  |
| Tổng ngân sách dự kiến | [$0 — ưu tiên dùng gói miễn phí. Nếu cần thêm, nộp yêu cầu qua Mentor Meeting] |  |  |  |
| 7. Rủi ro chính &amp; Cách xử lý |  |  |  |  |
| # | Rủi ro | Xác suất <br> (Cao/Trung bình/Thấp) | Tác động <br> (Cao/Trung bình/Thấp) | Cách phòng tránh / Xử lý |
| 1.0 | Đối tác không hợp tác hoặc phản hồi chậm | Trung bình | Cao | Xác định 2-3 đối tác dự phòng. Mentor hỗ trợ kết nối từ W1 |
| 2.0 | Phạm vi dự án bị mở rộng (scope creep) | Cao | Cao | Giữ đúng phạm vi đã chốt. Mọi thay đổi phải thảo luận với mentor trước |
| 3.0 | Thiếu hụt kỹ thuật (AI/ML/DevOps) | Trung bình | Trung bình | Học nhanh, dùng API thay tự build. Nhờ mentor hướng dẫn |
| 4.0 | Thành viên vắng mặt hoặc không hoàn thành việc | Thấp | Cao | Phân việc rõ ràng, check daily. Báo mentor ngay nếu có vấn đề |
| 5.0 | [Rủi ro khác của team] |  |  |  |
| 8. Tiêu chí thành công |  |  |  |  |
| Đánh giá cuối kỳ dựa trên 4 tiêu chí: |  |  |  |  |
| # | Tiêu chí | Trọng số | Cách đo lường |  |
| 1.0 | Sản phẩm V1 chạy được với dữ liệu thật | 40% | Sản phẩm live trên production, đối tác sử dụng được, không crash |  |
| 2.0 | Mức hài lòng của đối tác | 25% | Điểm đánh giá từ đối tác sau Demo 2 (thang 1-10) |  |
| 3.0 | Chất lượng code &amp; tài liệu | 20% | Code review, test coverage, README, architecture diagram |  |
| 4.0 | Làm việc nhóm &amp; Trách nhiệm | 15% | Standup đều đặn, báo cáo đúng hạn, phân việc rõ ràng |  |
| 9. Phê duyệt |  |  |  |  |
| Vai trò | Họ tên | Ngày | Chữ ký / Xác nhận |  |
| Team Lead | [Tên] | [DD/MM/YYYY] |  |  |
| Mentor phụ trách | [Tên mentor] | [DD/MM/YYYY] |  |  |
| Đối tác (nếu có) | [Tên] | [DD/MM/YYYY] |  |  |
| Lead Mentor (Lộc) | Lộc | [DD/MM/YYYY] |  |  |


---

## Sheet 5: Mẫu Daily Standup

| Mẫu Daily Standup — Báo cáo hàng ngày | Cột B | Cột C | Cột D |
| --- | --- | --- | --- |
| Gửi mỗi sáng trước 09:30 qua Discord #team-xxx-standup \| Hoặc báo cáo miệng trong call 15 phút |  |  |  |
| Thông tin |  |  |  |
| Team | [Alpha / Beta / Gamma / Delta] |  |  |
| Ngày | [DD/MM/YYYY] |  |  |
| Người báo cáo | [Tên thành viên] |  |  |
| Tuần | [W1-W6] |  |  |
| 3 câu hỏi bắt buộc |  |  |  |
| # | Câu hỏi | Trả lời |  |
| 1.0 | Hôm qua mình làm được gì? | [Liệt kê việc đã hoàn thành. Gắn link commit/PR nếu có] |  |
| 2.0 | Hôm nay mình dự định làm gì? | [Việc cần hoàn thành trong ngày. Rõ ràng, cụ thể] |  |
| 3.0 | Có gì đang kẹt không? | [Nếu có: mô tả vấn đề + cần ai giúp. Nếu không: ghi 'Không có'] |  |
| Template điền nhanh (copy cho mỗi thành viên) |  |  |  |
| Thành viên | Hôm qua | Hôm nay | Vướng mắc |
| [Tên 1] | [Việc đã làm] | [Việc sẽ làm] | [Blocker / Không có] |
| [Tên 2] | [Việc đã làm] | [Việc sẽ làm] | [Blocker / Không có] |
| [Tên 3] | [Việc đã làm] | [Việc sẽ làm] | [Blocker / Không có] |
| [Tên 4] | [Việc đã làm] | [Việc sẽ làm] | [Blocker / Không có] |
| Quy tắc Standup |  |  |  |
| Giờ | 09:00 mỗi sáng. Không trễ quá 09:15. |  |  |
| Thời lượng | Tối đa 15 phút. Không thảo luận chi tiết — việc đó để sau standup. |  |  |
| Format | Gửi text trên Discord TRƯỚC 09:30, hoặc báo trong call 15 phút. |  |  |
| Nội dung | Chỉ nói 3 thứ: đã làm gì / sẽ làm gì / có gì kẹt. Không kể lể dài dòng. |  |  |
| Nếu vắng | Báo team lead trước 08:30. Gửi standup text dù không tham gia call. |  |  |
| Blocker | Nếu có blocker → ghi rõ cần ai giúp gì. Team lead quyết định xử lý hoặc escalation mentor. |  |  |
| Mentor | Team lead tổng hợp standup → gửi tóm tắt cho mentor (Discord hoặc email) trước 10:00. |  |  |
| Mẫu tin nhắn gửi Discord |  |  |  |
| Ví dụ format gửi trên Discord #team-xxx-standup: <br>  <br> 🟢 Standup [DD/MM] — [Tên] <br> ✅ Hôm qua: Hoàn thành API đăng nhập, push lên PR #12 <br> 📅 Hôm nay: Làm trang dashboard, kết nối với API <br> 🚫 Kẹt: Không có <br>  <br> Hoặc nếu có blocker: <br> 🔴 Standup [DD/MM] — [Tên] <br> ✅ Hôm qua: Thiết kế UI trang chủ <br> 📅 Hôm nay: Code frontend dashboard <br> ⚠️ Kẹt: Cần BE API /dashboard nhưng anh A chưa xong. Nhờ team lead hỗ trợ đẩy nhanh. |  |  |  |


---

## Sheet 6: Đề xuất Hỗ Trợ Teams

| Đề xuất hỗ trợ — Server, GPU, công cụ, domain | Cột B | Cột C | Cột D | Cột E | Cột F | Cột G |
| --- | --- | --- | --- | --- | --- | --- |
| Teams chủ động sử dụng free tier trước |  |  |  |  |  |  |
| 1. Tổng quan hạ tầng |  |  |  |  |  |  |
| Loại tài nguyên | Mô tả | Gói miễn phí (Tự lo) | Gói trả phí | Ghi chú |  |  |
| Server / Hosting | VPS hoặc cloud hosting cho FE + BE + DB | Render (free), Railway ($5 credit), Vercel (free FE), Supabase (free DB) | VPS riêng (Ramnode, Hetzner ~$5-10/tháng) hoặc VinUni server | Ưu tiên free tier. Nâng cấp khi có real users. |  |  |
| GPU / AI Compute | Chạy inference LLM, embedding, fine-tune | Google Colab (free GPU), Hugging Face Spaces (free), Groq free tier | GPU VPS (RunPod ~$0.4/h) hoặc VinUni GPU cluster | Dùng API (OpenAI, Anthropic) thay self-host |  |  |
| AI API Keys | LLM API cho chatbot, summarization, etc. | Groq (free tier), Google Gemini (free tier), OpenRouter (free models) | OpenAI API ($5-20/tháng), Anthropic API ($5-20/tháng) | Chia sẻ 1 account/team. Track usage. |  |  |
| Claude Code | AI coding assistant cho development | Claude Free (hạn chế), GitHub Copilot Free | Claude Pro ($20/tháng/người) hoặc Claude Team | Đề xuất: 1 account Pro/team lead hoặc Max 20/tháng. |  |  |
| Domain / Sub-domain | Domain cho sản phẩm deployed | Sub-domain free: .vercel.app, .onrender.com, .railway.app, .up.railway.app | Domain riêng (~$10-15/năm) hoặc sub-domain vinuni.edu.vn | Liên hệ IT VinUni để xin sub-domain nếu cần. |  |  |
| Database | PostgreSQL, MongoDB, Redis cho app data | Supabase (free 500MB), MongoDB Atlas (free 512MB), Redis Cloud (free) | Managed DB trên VPS hoặc VinUni database | Free tier đủ cho MVP. Nâng cấp khi scale. |  |  |
| Storage / CDN | Lưu file, ảnh, static assets | Cloudflare R2 (free 10GB), AWS S3 free tier, Firebase Storage | Nâng cấp khi vượt free tier | Tối ưu file size trước khi upgrade. |  |  |
| Monitoring / Logging | Error tracking, performance, uptime | Sentry (free), UptimeRobot (free), Langfuse (free self-host) | Nâng cấp plan khi cần | Setup từ W2. Bắt buộc từ W3. |  |  |
| 2. Theo dõi yêu cầu hỗ trợ theo team |  |  |  |  |  |  |
| Team | Tài nguyên | Chi tiết yêu cầu | Chi phí dự kiến | Ưu tiên | Trạng thái | Người duyệt |
| Team Alpha | Server / Hosting | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Alpha | GPU / AI Compute | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Alpha | AI API Keys | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Alpha | Claude Code | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Alpha | Domain | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Beta | Server / Hosting | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Beta | GPU / AI Compute | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Beta | AI API Keys | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Beta | Claude Code | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Beta | Domain | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Gamma | Server / Hosting | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Gamma | GPU / AI Compute | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Gamma | AI API Keys | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Gamma | Claude Code | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Gamma | Domain | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Delta | Server / Hosting | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Delta | GPU / AI Compute | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Delta | AI API Keys | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Delta | Claude Code | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| Team Delta | Domain | [Điền yêu cầu cụ thể] | [$ / tháng] | P1 / P2 / P3 | Chưa gửi / Pending / Approved / Rejected |  |
| 3. Gợi ý tech stack (tự chọn) |  |  |  |  |  |  |
| Thành phần | Option A (Free) | Option B (Nâng cấp) | Khi nào dùng Option B |  |  |  |
| Frontend | React/Vue/Next.js + Vercel (free) | VPS + Nginx | Khi cần SSR hoặc custom domain |  |  |  |
| Backend API | FastAPI/Flask + Render free | VPS + Docker | Khi Render free tier quá chậm |  |  |  |
| Database | Supabase (PostgreSQL free) | Managed PostgreSQL trên VPS | Khi data &gt; 500MB |  |  |  |
| AI / LLM | Groq free + Gemini free + OpenRouter | OpenAI/Anthropic API | Khi cần chất lượng output cao hơn |  |  |  |
| Vector DB | ChromaDB local hoặc Pinecone free | Weaviate self-host trên VPS | Khi RAG data lớn |  |  |  |
| Embedding | HuggingFace Inference (free) | Self-host embedding model | Khi cần tốc độ inference nhanh hơn |  |  |  |
| Deployment | Render/Railway free tier | VPS + Docker Compose + Cloudflare | Khi cần uptime 99%+ và custom domain |  |  |  |
| Monitoring | Sentry free + Langfuse self-host | Datadog/New Relic | Khi cần giám sát chuyên sâu |  |  |  |
| 4. Quy trình yêu cầu hỗ trợ |  |  |  |  |  |  |
| Bước 1 | Team xác định nhu cầu tài nguyên trong W1 (Project Charter) |  |  |  |  |  |
| Bước 2 | Thử free tier trước (W2-W3). Đánh giá có đủ không. |  |  |  |  |  |
| Bước 3 | Nếu cần nâng cấp: điền vào bảng Section 2, trình trong Mentor Meeting T4 hoặc T7 |  |  |  |  |  |
| Bước 4 | Mentor review + approve (Lộc quyết định). Nếu cần funding → Lộc xin VinUni. |  |  |  |  |  |
| Bước 5 | Tài nguyên được cấp. Team setup + báo cáo hoàn tất trong File Quản Trị. |  |  |  |  |  |


---

