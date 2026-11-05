# DISCOVERY — KỊCH BẢN PHỎNG VẤN DỰ ÁN (BƯỚC 2)

> Dành cho Agent. Mục tiêu: từ lời mô tả của người dùng, chốt được **bản tóm tắt dự án**, **stack** và **profile kiến trúc**, rồi ghi lại thành tài liệu. Người dùng có thể là fresher hoặc người vibe coding: dùng ngôn ngữ đời thường, giải thích thuật ngữ trong một câu, **đừng hỏi dồn**.

## Nguyên tắc hội thoại
* Hỏi **tối đa 3 câu mỗi lượt**, bắt đầu bằng câu về *người dùng và vấn đề*, không bắt đầu bằng công nghệ.
* Với mỗi câu kỹ thuật, **đưa sẵn gợi ý mặc định kèm lý do** để người dùng chỉ cần gật đầu ("Mình đề xuất X vì ... — bạn đồng ý không?").
* Người dùng nói "không biết": tự chọn mặc định an toàn, ghi rõ giả định vào `docs/project-brief.md` để xem lại sau.
* Không bắt người dùng nhắc tên tệp hay lệnh git. Bạn tự làm.
* Trả lời bằng **ngôn ngữ người dùng đang dùng**.

## Các nhóm thông tin cần thu thập (theo thứ tự)
1. **Who/What**: ai dùng, nỗi đau chính, "xong" nghĩa là gì (một câu).
2. **Luồng chính**: 3–5 việc người dùng làm trong sản phẩm, từ đầu đến cuối.
3. **Dữ liệu và tài khoản**: cần đăng nhập? lưu gì? có dữ liệu nhạy cảm?
4. **Loại ứng dụng**: web, API, di động, công cụ dòng lệnh, có LLM/Agent bên trong không?
5. **Ràng buộc**: ngân sách (free tier?), hạn chót, ngôn ngữ/công nghệ đã biết hoặc bắt buộc, nơi triển khai.
6. **Người làm**: một mình hay nhóm; mức quen thuộc với code (để chọn mức phức tạp phù hợp).
7. **Quy mô dự kiến**: demo/đồ án, sản phẩm nhỏ, hay sản phẩm sẽ lớn dần.

## Từ câu trả lời đến quyết định
| Tín hiệu | Gợi ý | Tài liệu |
| :-- | :-- | :-- |
| Demo, đồ án, một người làm, ít nghiệp vụ | Layered đơn giản | `../profiles/architecture/simple-layered.md` |
| Nghiệp vụ phức tạp, sống lâu, cần test sâu | Clean Architecture (+DDD khi cần) | `../profiles/architecture/clean-architecture.md` |
| Nhiều tính năng độc lập, nhóm nhỏ làm song song | Vertical Slice hoặc Modular Monolith | `../profiles/architecture/vertical-slice.md`, `../profiles/architecture/modular-monolith.md` |
| Có LLM/Agent/RAG bên trong | Thêm profile AI | `../profiles/ai-apps/agentic-patterns-and-evals.md` |
| Có giao diện web nhiều màn hình | Thêm profile frontend + design system | `../profiles/frontend/bulletproof-react.md`, `../profiles/design/ui-ux-archetypes-and-presets.md` |
| Ngân sách bằng 0 | Stack free tier | `../profiles/stacks/cloud-free-tier-stack.md` |

Chi tiết cách chọn: `../profiles/README.md`. Nếu không có profile phù hợp: dùng Technology Selection Gate trong `templates/AGENTS.md` mục 6.

## Đầu ra bắt buộc của bước 2
1. `docs/project-brief.md` điền đủ (kể cả **các giả định** đã tự chọn).
2. `adrs/0001-*.md`: quyết định **stack**; `adrs/0002-*.md`: quyết định **kiểu kiến trúc** (từ `templates/adrs/0000-template.md`).
3. `.builder/kit.json` cập nhật `profiles` đã chọn.
4. Tóm tắt cho người dùng bằng ngôn ngữ đơn giản: sẽ dựng gì, vì sao, và bước tiếp theo. **Chờ họ đồng ý** trước khi dựng khung code ở bước 3.
