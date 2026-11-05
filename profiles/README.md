# PROFILES — CẤU HÌNH SÂU, CHỌN THEO TỪNG DỰ ÁN

> Dành cho Agent. `core/` là phần **bắt buộc** cho mọi repo. Thư mục này là phần **tùy biến**: mỗi dự án chọn một profile kiến trúc, một stack, và các profile bổ sung phù hợp sau bước phỏng vấn (`../core/discovery.md`). Kết quả chọn ghi vào `.builder/kit.json` và ADR của dự án.

## Cách chọn nhanh

| Dự án | Profile kiến trúc | Tài liệu |
| :-- | :-- | :-- |
| Demo, đồ án, MVP một người làm, ít nghiệp vụ | **Layered đơn giản** | [architecture/simple-layered.md](architecture/simple-layered.md) |
| Nghiệp vụ phức tạp, sống lâu, cần test và thay thế hạ tầng dễ | **Clean Architecture** (+DDD) | [architecture/clean-architecture.md](architecture/clean-architecture.md), bản đồ thư mục: [clean-architecture-layout.md](architecture/clean-architecture-layout.md) |
| Nhiều tính năng độc lập, nhóm nhỏ, muốn thêm tính năng không đụng nhau | **Vertical Slice** | [architecture/vertical-slice.md](architecture/vertical-slice.md) |
| Một hệ thống lớn dần, muốn ranh giới module rõ nhưng chưa tách dịch vụ | **Modular Monolith** | [architecture/modular-monolith.md](architecture/modular-monolith.md) |

Không chắc: chọn **Layered đơn giản** cho dự án nhỏ, **Clean Architecture** cho dự án có nghiệp vụ thật. Ghi lý do vào ADR; có thể đổi sau bằng ADR mới.

## Profile bổ sung (kết hợp với profile kiến trúc)

| Khi dự án có... | Profile | Tài liệu |
| :-- | :-- | :-- |
| Giao diện web React | Frontend | [frontend/bulletproof-react.md](frontend/bulletproof-react.md), mã khởi đầu: [frontend/starter](frontend/starter/README.md) |
| Cần diện mạo UI rõ ràng, theme sáng/tối | Design system | [design/ui-ux-archetypes-and-presets.md](design/ui-ux-archetypes-and-presets.md), [design/design-archetypes-catalog.md](design/design-archetypes-catalog.md), [design/visual-dna-prompts.md](design/visual-dna-prompts.md) |
| LLM, Agent, RAG bên trong sản phẩm | Ứng dụng AI | [ai-apps/agentic-patterns-and-evals.md](ai-apps/agentic-patterns-and-evals.md) |
| Cần chọn/đối chiếu design pattern | Patterns | [patterns/design-patterns-catalog.md](patterns/design-patterns-catalog.md) |
| Ngân sách bằng 0 | Stack free tier | [stacks/cloud-free-tier-stack.md](stacks/cloud-free-tier-stack.md), hạ tầng cục bộ: [stacks/postgres-redis.docker-compose.yml](stacks/postgres-redis.docker-compose.yml) |
| Cần tài liệu người dùng, runbook, onboarding | Tài liệu | [documentation/documentation-and-pitch-standards.md](documentation/documentation-and-pitch-standards.md) |

## Mỗi profile kiến trúc cam kết gì
Mỗi tài liệu profile phải trả lời được 5 câu để Agent làm đúng mà không phải đoán:
1. **Khi nào chọn / khi nào không**.
2. **Sơ đồ thư mục** mục tiêu (kèm ví dụ theo ngôn ngữ).
3. **Quy tắc phụ thuộc** (cái gì được phép gọi cái gì).
4. **Cách thêm một tính năng mới** từng bước.
5. **Lỗi thường gặp** mà Health Check sẽ bắt.

## Thêm profile mới
Tạo tài liệu theo 5 mục trên, thêm dòng vào bảng trên và vào `../INDEX.md` (chạy `python scripts/check_links.py`). Stack cụ thể (ví dụ `stacks/dotnet-clean.md`) được bổ sung dần theo nhu cầu thực tế.
