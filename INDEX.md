# INDEX — BẢNG ĐỊNH TUYẾN Ý ĐỊNH → TÀI LIỆU (DÀNH CHO AGENT)

> Người dùng **không biết** repo có tài liệu nào. Hãy đọc cột **"Khi nào dùng"**, khớp với việc người dùng đang nói/làm, rồi mở đúng tài liệu. Đọc tối đa 2–3 tài liệu mỗi lần. Địa chỉ thô: `https://raw.githubusercontent.com/Dokhacgiakhoa/Project-Builder-Kit/<ref>/<đường dẫn>`.
> Tầng: **C** = Core (bắt buộc mọi dự án) · **P** = Profile (chọn theo dự án) · **L** = Library (tham khảo/tùy chọn).

## 1. Khởi tạo và vòng đời
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| K-001 | C | Người dùng muốn **bắt đầu dự án mới** hoặc "dựng khung/setup chuẩn" cho dự án đang có | [BOOTSTRAP.md](BOOTSTRAP.md) |
| K-002 | C | Cần **hỏi người dùng** để hiểu dự án, chốt luồng, stack | [core/discovery.md](core/discovery.md) |
| K-003 | C | Cần biết **thế nào là đạt chuẩn tối thiểu** cho mọi repo dùng Agent | [core/README.md](core/README.md) |
| K-004 | C | Cần **chọn kiểu kiến trúc / profile** phù hợp dự án | [profiles/README.md](profiles/README.md) |
| K-005 | C | Hỏi "dự án đang bị gì", trước khi mở PR, hoặc có `project-review.md` | [scripts/README.md](scripts/README.md) |

## 2. Chuẩn làm việc (Core)
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| S-001 | C | Viết code: đặt tên, xử lý lỗi, phòng vệ crash, không hardcode | [core/standards/coding-conventions.md](core/standards/coding-conventions.md) |
| S-002 | C | Viết test, thiếu test, chọn mức test (unit/integration/e2e) | [core/standards/test-strategy.md](core/standards/test-strategy.md) |
| S-003 | C | Trước khi báo "xong" / mở PR | [core/standards/definition-of-done.md](core/standards/definition-of-done.md) |
| S-004 | C | Sửa cùng lỗi nhiều lần, "vá víu", code ngày càng rối | [knowledge-base/tu-duy/anti-patching-architectural-thinking.md](knowledge-base/tu-duy/anti-patching-architectural-thinking.md) |
| S-005 | L | Tránh lỗi phổ biến khi làm việc với Agent | [knowledge-base/technical-book/anti-patterns/common-mistakes.md](knowledge-base/technical-book/anti-patterns/common-mistakes.md) |

## 3. Kiến trúc (Profile)
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| A-001 | P | Demo, đồ án, MVP nhỏ, CRUD đơn giản | [profiles/architecture/simple-layered.md](profiles/architecture/simple-layered.md) |
| A-002 | P | Nghiệp vụ phức tạp, test độc lập framework, đổi hạ tầng | [profiles/architecture/clean-architecture.md](profiles/architecture/clean-architecture.md) |
| A-003 | P | Cần sơ đồ thư mục Clean Architecture theo .NET/Python/TypeScript | [profiles/architecture/clean-architecture-layout.md](profiles/architecture/clean-architecture-layout.md) |
| A-004 | P | Nhiều tính năng độc lập, làm song song | [profiles/architecture/vertical-slice.md](profiles/architecture/vertical-slice.md) |
| A-005 | P | Hệ thống lớn dần, cần ranh giới module | [profiles/architecture/modular-monolith.md](profiles/architecture/modular-monolith.md) |
| A-006 | P | Chọn/đối chiếu design pattern, refactor theo pattern | [profiles/patterns/design-patterns-catalog.md](profiles/patterns/design-patterns-catalog.md) |
| A-007 | L | Thiết kế hệ thống tổng thể, sơ đồ C4 | [knowledge-base/technical-book/architecture/system-design.md](knowledge-base/technical-book/architecture/system-design.md) |

## 4. Giao diện và design system (Profile)
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| D-001 | P | Làm giao diện web React theo cấu trúc tính năng | [profiles/frontend/bulletproof-react.md](profiles/frontend/bulletproof-react.md) |
| D-002 | P | Cần mã khởi đầu frontend (Vite + React + TS + Tailwind) | [profiles/frontend/starter/README.md](profiles/frontend/starter/README.md) |
| D-003 | P | Chọn phong cách giao diện, theme sáng/tối, design system | [profiles/design/ui-ux-archetypes-and-presets.md](profiles/design/ui-ux-archetypes-and-presets.md) |
| D-004 | P | Xem danh mục phong cách UI (archetype) để chọn | [profiles/design/design-archetypes-catalog.md](profiles/design/design-archetypes-catalog.md) |
| D-005 | P | Cần prompt mô tả phong cách để Agent dựng giao diện đúng gu | [profiles/design/visual-dna-prompts.md](profiles/design/visual-dna-prompts.md) |

## 5. Ứng dụng có AI/LLM (Profile)
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| I-001 | P | Sản phẩm có Agent, tool calling, RAG, MCP; cần đánh giá chất lượng (evals) | [profiles/ai-apps/agentic-patterns-and-evals.md](profiles/ai-apps/agentic-patterns-and-evals.md) |
| I-002 | L | Mẫu RAG | [knowledge-base/technical-book/patterns/rag-pattern.md](knowledge-base/technical-book/patterns/rag-pattern.md) |

## 6. Cấu hình Agent: rule, skill, workflow
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| G-001 | C | Thêm rule/skill/workflow, cấu hình nhiều công cụ Agent (Claude Code, Codex, Antigravity...) | [knowledge-base/technical-book/agent-practices/multi-tool-config.md](knowledge-base/technical-book/agent-practices/multi-tool-config.md) |
| G-002 | L | Quản lý context của Agent, khi hội thoại dài, Agent "lạc đề" | [knowledge-base/technical-book/agent-practices/context-management.md](knowledge-base/technical-book/agent-practices/context-management.md) |
| G-003 | L | Guardrail, giới hạn quyền cho Agent | [knowledge-base/technical-book/agent-practices/guardrails.md](knowledge-base/technical-book/agent-practices/guardrails.md) |
| G-004 | L | Viết prompt/chỉ dẫn hiệu quả, dùng Claude Code hiệu quả | [knowledge-base/claude-code.md](knowledge-base/claude-code.md) |

## 7. Hạ tầng, tài liệu, quản trị (Library)
| ID | Tầng | Khi nào dùng | Tài liệu |
| :-- | :-: | :-- | :-- |
| T-001 | P | Stack miễn phí (free tier) cho dự án nhỏ | [profiles/stacks/cloud-free-tier-stack.md](profiles/stacks/cloud-free-tier-stack.md) |
| T-002 | P | Cần Postgres/Redis chạy cục bộ | [profiles/stacks/postgres-redis.docker-compose.yml](profiles/stacks/postgres-redis.docker-compose.yml) |
| T-003 | L | Docker, CI/CD | [knowledge-base/technical-book/devops/docker-cicd.md](knowledge-base/technical-book/devops/docker-cicd.md) |
| T-004 | L | Hướng dẫn triển khai | [profiles/documentation/deployment-guide.md](profiles/documentation/deployment-guide.md) |
| O-001 | P | Viết tài liệu người dùng/vận hành theo khung Diátaxis, runbook sự cố | [profiles/documentation/documentation-and-pitch-standards.md](profiles/documentation/documentation-and-pitch-standards.md) |
| O-002 | L | Làm pitch deck / thuyết trình gọi vốn | [templates/pitch-deck/pitch-deck-template.md](templates/pitch-deck/pitch-deck-template.md) |
| O-003 | L | Quản trị dự án, sprint, retrospective, báo cáo | [knowledge-base/quan-tri-du-an/README.md](knowledge-base/quan-tri-du-an/README.md) |
| O-004 | C | Lập roadmap/backlog/sprint cho dự án | [core/templates/planning/roadmap.md](core/templates/planning/roadmap.md) |
| O-005 | L | Gỡ lỗi môi trường, sự cố thường gặp | [knowledge-base/technical-book/troubleshooting.md](knowledge-base/technical-book/troubleshooting.md) |
