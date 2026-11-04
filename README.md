# 🚀 UNIVERSAL AI-NATIVE PROJECT STARTER KIT
### *Khung Khởi Tạo & Quản Trị Dự Án Phần Mềm Chuẩn Hóa Với AI (Human + Multi-Agent Collaboration)*

[![CI Quality Gate](https://github.com/Dokhacgiakhoa/Project-Starter-Kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Dokhacgiakhoa/Project-Starter-Kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Architecture: Modular Monolith](https://img.shields.io/badge/Architecture-Modular%20Monolith-orange.svg)](#)
[![Standards: Anti--Crash](https://img.shields.io/badge/Standard-Anti--Crash-success.svg)](#)

---

## 📖 1. GIỚI THIỆU TỔNG QUAN

**Universal AI-Native Project Starter Kit** là bộ khung tiêu chuẩn, tổng quát hóa dùng để khởi tạo, tổ chức và vận hành bất kỳ dự án phần mềm nào (Full-stack Web/Mobile App, Hệ thống AI Agentic, Nền tảng SaaS, Microservices...) trong kỷ nguyên AI.

Bộ Starter Kit giải quyết bài toán lớn nhất khi lập trình cùng AI: **"AI tăng tốc độ sinh mã nhưng không có context tổng thể; nếu thiếu quy trình và kiến trúc chuẩn mực, AI sẽ giúp phá vỡ hệ thống nhanh gấp 10 lần."**

Bằng việc kết hợp hài hòa giữa **Thẩm quyền lãnh đạo của Con người (Human Leadership & Accountability)** và **Năng lực thực thi vượt trội của Hệ thống Trợ lý AI (Multi-Agent Execution: Claude Code, Antigravity, Cursor, Codex...)**, bộ khung này biến Git repository thành **Một Nguồn Sự Thật Duy Nhất (Single Source of Truth)**.

---

## 🏛️ 2. TRIẾT LÝ CỐT LÕI (CORE PHILOSOPHY)

```mermaid
graph LR
    A["1. Context-Driven<br/>Ngữ cảnh rõ ràng = AI code đúng"] --> B["2. Spec-Driven & Contract-First<br/>Khóa API Contract trước khi code"]
    B --> C["3. Outcome over Output<br/>Đo lường bằng giá trị thực tế"]
    C --> D["4. Anti-Crash Standard<br/>Defensive programming & Robust error handling"]
```

1. **Context-Driven (Ngữ Cảnh Là Nền Tảng)**: AI chỉ sinh mã chính xác khi được nạp đầy đủ bối cảnh từ Specs, ADRs, và Coding Rules. Toàn bộ context được phiên bản hóa trực tiếp trong Git.
2. **Spec-Driven & Contract-First**: Không bao giờ viết code trước khi có Feature Spec và API Contract. Frontend và Backend làm việc song song dựa trên hợp đồng giao tiếp độc lập.
3. **Outcome over Output**: Thành công của dự án không đo bằng số lượng dòng code (Output), mà đo bằng sự giải quyết triệt để bài toán người dùng và chỉ số tăng trưởng bền vững (Outcome).
4. **The Anti-Crash Standard**: Quy chuẩn kỹ thuật phòng vệ triệt để (Optional Chaining `?.`, Safe Fallbacks, `try...catch` bất đồng bộ, Input validation) ngăn chặn hoàn toàn lỗi sập ứng dụng hoặc màn hình trắng.

---

## 👥 3. PHÂN ĐỊNH TRÁCH NHIỆM (HUMAN VS. AI AGENTS)

> **Nguyên tắc**: *AI là cấp số nhân thực thi; Con người nắm giữ thẩm quyền, trách nhiệm giải trình và phê duyệt cuối cùng.*

```mermaid
flowchart TD
    subgraph Human [ĐỘI NGŨ CON NGƯỜI (Accountability & Quality Gate)]
        PO["Product Owner (PO)<br/>Bảo vệ GIÁ TRỊ & Nghiệp vụ"]
        PM["Project Manager (PM)<br/>Bảo vệ THỜI GIAN & Kỷ luật Sprint"]
        TL["Tech Lead / Architect<br/>Bảo vệ KỸ THUẬT & Phê duyệt PR"]
    end

    subgraph Agents [HỆ THỐNG TRỢ LÝ AI (Execution & Automation)]
        ArchAgent["Architect Agent (Antigravity/Claude)<br/>Quét Context, Soạn ADRs & Specs"]
        CodingAgent["Coding Agent (Claude Code/Cursor/Codex)<br/>TDD, Phân rã Subtasks, Sinh mã"]
        ReviewAgent["Reviewer Agent (CI / Quality Gate)<br/>Linting, Security Scan, Kiểm tra DoD"]
    end

    PO -->|Định nghĩa Problem & Outcome Tree| ArchAgent
    TL -->|Thiết lập Boundary & Constraints| ArchAgent
    ArchAgent -->|Soạn thảo Specs & API Contracts| TL
    PM -->|Giao Task lớn theo Sprint Backlog| CodingAgent
    CodingAgent -->|TDD Implementation & Self-Test| ReviewAgent
    ReviewAgent -->|Báo cáo vi phạm DoD & Lint Errors| TL
    TL -->|Code Review & Merge Main| PM
```

### Bảng phân định RACI Matrix

| Hạng Mục Hoạt Động | Human PO | Human PM | Human Tech Lead | AI Architect | AI Coder | AI Reviewer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Xác định Vấn đề & Khung Outcome** | **A / R** | C | C | C | I | I |
| **Soạn thảo Specs & API Contracts** | C | I | **A** | **R** | I | I |
| **Ban hành Quyết định Kiến trúc (ADR)** | I | I | **A** | **R** | I | I |
| **Phân bổ Sprint Backlog & Milestones**| C | **A / R** | C | C | I | I |
| **Phân rã Subtasks & TDD Code** | I | I | I | C | **A / R** | I |
| **Kiểm tra Kỷ luật DoD & Linting** | I | C | C | I | C | **R** |
| **Code Review & Phê duyệt Pull Request**| I | I | **A / R** | C | I | C |
| **Deploy Staging / Production** | I | **A** | **R** | I | I | C |

*(**R**: Responsible - Người thực hiện | **A**: Accountable - Người chịu trách nhiệm | **C**: Consulted - Tham vấn | **I**: Informed - Nhận thông báo)*

---

## 📂 4. CẤU TRÚC REPOSITORY CHUẨN (CONTEXT WORKSPACE)

```
├── .github/                        # Tự động hóa CI/CD & Mẫu cộng tác
│   ├── workflows/ci.yml            # CI Pipeline: Linting -> Test -> Quality Gate
│   ├── ISSUE_TEMPLATE/             # Form tạo Issue có cấu trúc (Bug, Feature, Task)
│   ├── PULL_REQUEST_TEMPLATE.md    # Khung mở PR đối chiếu checklist DoD
│   ├── CONTRIBUTING.md             # Hướng dẫn đóng góp mã nguồn chuẩn
│   ├── CODE_OF_CONDUCT.md          # Quy chuẩn hành vi Contributor Covenant
│   ├── SECURITY.md                 # Chính sách & báo cáo lỗ hổng bảo mật
│   └── dependabot.yml              # Quét & cập nhật bảo mật dependencies tự động
├── AGENTS.md                       # "Bản hiến pháp" điều phối hành vi cho AI Agents
├── specs/                          # Không gian đặc tả nghiệp vụ (Spec-driven)
│   ├── product-vision.md           # Tầm nhìn sản phẩm, Outcome Tree, Khung Who-What-How
│   ├── domains.md                  # Bản đồ phân rã Bounded Contexts
│   ├── user-roles.md               # Ma trận vai trò và phân quyền người dùng
│   ├── contracts/                  # API Contracts (OpenAPI 3.0 / JSON Schemas)
│   │   └── api-contract-template.yaml
│   ├── design-system/              # AI Visual DNA & Design Prompts
│   │   └── visual-dna-prompts.md   # Prompt Cookbook chuẩn hóa cho AI Coding
│   └── features/                   # Chi tiết từng Feature (Motivation - Design - Plan)
│       └── template-spec.md
├── adrs/                           # Architecture Decision Records (Quyết định kiến trúc)
│   ├── 0001-architecture-style.md # Kiểu kiến trúc (Modular Monolith)
│   ├── 0002-tech-stack.md          # Công nghệ & Chiến lược Cloud Free-Tier
│   ├── 0003-coding-conventions.md  # Chuẩn đặt tên & The Anti-Crash Standard
│   ├── 0004-test-strategy.md       # Chiến lược kiểm thử tự động TDD đa tầng
│   ├── 0005-definition-of-done.md  # Tiêu chuẩn hoàn thành nghiệm thu (DoD)
│   ├── 0006-clean-architecture-and-ddd.md # Phân tầng Clean Architecture & CQRS
│   ├── 0007-agentic-patterns-and-evals.md # Agentic AI Patterns & RAG Evals
│   ├── 0008-frontend-architecture.md     # Feature-Driven Architecture (Bulletproof React)
│   └── 0009-ui-ux-archetypes-and-design-presets.md # Quy chuẩn 7 Vũ trụ UI/UX & Theme Engine
├── planning/                       # Kế hoạch & Quản trị tiến độ
│   ├── roadmap.md                  # Lộ trình tổng thể & các Checkpoints
│   ├── backlog.md                  # Danh mục User Stories (US-xxx) và Tasks (T-xxx)
│   ├── sprints/                    # Kế hoạch theo từng Sprint
│   │   └── sprint-01.md
│   └── retrospective-template.md   # Mẫu họp cải tiến quy trình (Sad - Mad - Glad)
├── tasks/                          # Hồ sơ nhiệm vụ thực thi cho AI
│   └── templates/task-spec.md      # Khung mô tả task lớn để AI tự chia nhỏ
├── templates/                      # Biểu mẫu quản trị dự án
│   └── project-management/         # File Excel quản trị tập trung & Project Charter
├── knowledge-base/                 # Thư viện tri thức kỹ thuật & tài liệu hướng dẫn
│   ├── ui-ux-presets/              # 14+ UI/UX Archetypes Catalog & Mã nguồn mở
│   │   └── design-archetypes-catalog.md
│   ├── technical-book/             # 15 chương cẩm nang kỹ thuật phần mềm AI
│   ├── quan-tri-du-an/             # Cẩm nang quản trị dự án thực chiến
│   └── tu-duy/                     # Tư duy Product & AI-Native Engineering
├── docs/                           # Tài liệu thiết kế & triển khai
│   ├── system-architecture.md      # Sơ đồ kiến trúc tổng thể (C4 Container Diagram)
│   ├── deployment-guide.md         # Hướng dẫn deploy Local, Staging & Production
│   └── reference-slides/           # Các bài giảng & slide tham khảo
├── frontend/                       # FRONTEND STARTER KIT (Bulletproof React)
│   ├── src/app/                    # Application Providers & Router
│   ├── src/components/             # UI Components dùng chung (Buttons, Cards, Layouts)
│   ├── src/features/               # Modules nghiệp vụ độc lập (Auth, Dashboard, AI Chat)
│   │   ├── dashboard/              # Màn hình điều khiển số liệu
│   │   ├── ai-chat/                # Trợ lý giao tiếp AI Agent
│   │   └── theme-showcase/         # Studio chuyển đổi trực quan 7 UI/UX Archetypes
│   ├── src/lib/api-client.ts       # Axios client có interceptors & error normalization
│   ├── src/stores/                 # Quản lý Global Client State qua Zustand
│   └── README.md                   # Hướng dẫn chi tiết kiến trúc Frontend
├── src/                            # BACKEND & DOMAIN (Clean Architecture Blueprint)
│   ├── Domain/                     # Enterprise Core & Entities (Độc lập 100%)
│   ├── Application/                # Use Cases, CQRS Commands/Queries, DTOs
│   ├── Infrastructure/             # DB Persistence, External Services, Caching
│   ├── Presentation/               # REST API Controllers, Middlewares, DI Wiring
│   └── README.md                   # Hướng dẫn ánh xạ Clean Architecture đa ngôn ngữ
├── docker-compose.yml              # Khởi chạy hạ tầng local (Postgres+pgvector, Redis)
├── Makefile                        # Bộ lệnh dev chuẩn hóa (make up, test, lint, clean)
├── .editorconfig                   # Chuẩn hóa format code đa nền tảng IDE
├── tests/                          # Automated Test Suite (Unit, Integration, E2E)
├── .env.example                    # Mẫu cấu hình biến môi trường bảo mật
├── .gitignore                      # Quy chuẩn loại trừ file rác & secrets
├── PLAN.md                         # Kế hoạch chi tiết của Starter Kit
└── LICENSE                         # Giấy phép mã nguồn mở (MIT)
```

---

## 🔄 5. QUY TRÌNH THỰC THI 5 BƯỚC (END-TO-END WORKFLOW)

```mermaid
sequenceDiagram
    autonumber
    actor TechLead as Human Tech Lead / PM
    participant Context as Context Base (/specs, /adrs)
    participant Agent as AI Coding Agent
    participant Git as Git Repo / CI Quality Gate

    Note over TechLead,Context: BƯỚC 1: XÁC LẬP BỐI CẢNH (Context Ingestion)
    TechLead->>Context: Ban hành Feature Spec & Đóng băng API Contract
    TechLead->>Context: Ban hành các ADRs liên quan
    
    Note over TechLead,Agent: BƯỚC 2: GIAO VIỆC & PHÂN TÍCH (Task Assignment)
    TechLead->>Agent: Giao Task lớn (Mã US-xxx / T-xxx)
    Agent->>Context: Đọc toàn bộ Specs + ADRs + AGENTS.md
    Agent->>Agent: Tự động phân rã thành Subtasks & Lập Kế hoạch
    
    Note over Agent: BƯỚC 3: PHÁT TRIỂN THEO TDD (Test-Driven Development)
    Agent->>Agent: Viết Test Cases trước (Happy Path + 2 Edge Cases)
    Agent->>Agent: Viết Code logic để pass tests
    Agent->>Agent: Tự chạy Unit Test, Linting, Formatter
    
    Note over Agent,Git: BƯỚC 4: TẠO PR & KIỂM TRA ĐỘC LẬP
    Agent->>Git: Tạo Pull Request (PR < 400 lines) theo template
    Git->>Git: CI Pipeline tự động kiểm tra cú pháp & tests
    
    Note over Git,TechLead: BƯỚC 5: CON NGƯỜI PHÊ DUYỆT & RELEASE
    TechLead->>Git: Review PR đối chiếu Definition of Done (DoD)
    TechLead->>Git: Approve & Merge vào nhánh main
    Git->>TechLead: Tự động triển khai lên môi trường đích
```

---

## ⚡ 6. HƯỚNG DẪN BẮT ĐẦU NHANH (QUICK START)

### Bước 1: Khởi tạo từ Template
1. Nhấn nút **Use this template** trên GitHub hoặc clone về máy:
   ```bash
   git clone https://github.com/<your-org>/<your-repo>.git
   cd <your-repo>
   ```
2. Sao chép file cấu hình môi trường:
   ```bash
   cp .env.example .env
   ```

### Bước 2: Thiết lập Ngữ cảnh Dự án (Context Ingestion)
1. Chỉnh sửa `specs/product-vision.md`: Xác định rõ nhóm người dùng mục tiêu (Who) và nỗi đau lớn nhất cần giải quyết (What).
2. Kiểm tra `adrs/0002-tech-stack.md`: Lựa chọn ngôn ngữ/framework phù hợp với bài toán của nhóm bạn.
3. Cập nhật `planning/backlog.md`: Đưa các User Story đầu tiên vào Sprint 1.

### Bước 3: Làm việc cùng AI Coding Agent
Khi mở IDE (Antigravity, Cursor, Claude Code...), chỉ cần nhắc Agent:
> *"Hãy đọc file `AGENTS.md`, các ADR trong `adrs/` và kiểm tra task `T-001` trong `planning/backlog.md` để bắt đầu lập kế hoạch triển khai."*

---

## 🛡️ 7. TIÊU CHUẨN HOÀN THÀNH (DEFINITION OF DONE)

Một tính năng chỉ được xem là hoàn tất khi:
* [x] Triển khai bám sát `specs/features/` và không làm vỡ API Contract.
* [x] Tuân thủ 100% Anti-Crash Standard (Optional Chaining, Error Handling).
* [x] Bổ sung Unit / Integration Tests và đạt 100% test pass.
* [x] CI Pipeline trên GitHub Actions chạy màu xanh (PASS).
* [x] Được ít nhất 1 Human Reviewer phê duyệt trước khi merge vào nhánh `main`.

---

## 📄 GIẤY PHÉP (LICENSE)
Dự án được phân phối dưới giấy phép mã nguồn mở [MIT License](LICENSE). Mọi cá nhân, nhóm phát triển và tổ chức đều có thể tự do sử dụng, tùy biến và triển khai cho các sản phẩm thương mại hoặc phi thương mại.
