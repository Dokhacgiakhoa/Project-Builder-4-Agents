---
id: A-003
type: reference
when: "Cần sơ đồ thư mục Clean Architecture theo .NET/Python/TypeScript"
---
# CẤU TRÚC PHÂN TẦNG CLEAN ARCHITECTURE (LAYERED BLUEPRINT)

Thư mục `src/` được tổ chức theo chuẩn **Clean Architecture & Domain-Driven Design (DDD)**. Bất kể bạn sử dụng tech stack nào (.NET, Python, TypeScript/Node, Go), mã nguồn nên được ánh xạ theo 4 tầng đồng tâm dưới đây:

---

## 🏛️ 1. CÁC TẦNG KIẾN TRÚC

```text
src/
├── Domain/                 # 1. Enterprise Core & Entities (Độc lập 100%)
│   ├── Entities/           # Thực thể chứa định danh và nghiệp vụ (Rich Models)
│   ├── ValueObjects/       # Đối tượng giá trị bất biến (Email, Money, Address)
│   ├── Events/             # Domain Events (UserRegisteredEvent)
│   └── Repositories/       # Giao diện (Interfaces) lưu trữ (IUserRepository)
│
├── Application/            # 2. Use Cases & Orchestration Logic
│   ├── Commands/           # CQRS Commands (CreateUserCommand + Handler)
│   ├── Queries/            # CQRS Queries (GetUserByIdQuery + Handler)
│   ├── DTOs/               # Data Transfer Objects
│   └── Interfaces/         # Giao diện dịch vụ (IEmailService, ICacheService)
│
├── Infrastructure/         # 3. External Implementations & Data Access
│   ├── Persistence/        # DB Context, Migration, Repository Implementations
│   ├── ExternalServices/   # Tích hợp third-party (Stripe, OpenAI, Supabase)
│   └── Caching/            # Redis Cache implementation
│
└── Presentation/           # 4. Entry Points & User Interface
    ├── Controllers/        # REST API Controllers / Route Handlers
    ├── Middlewares/        # Error Handling, Auth Token Validation, Rate Limiter
    └── Entrypoint/         # Program.cs / main.py / server.ts (Composition Root / DI)
```

---

## 🗺️ 2. BẢNG ÁNH XẠ TECH STACK (STACK MAPPING)

| Tầng Kiến Trúc | .NET / C# | Python (FastAPI) | TypeScript / Node (NestJS) |
| :--- | :--- | :--- | :--- |
| **Domain** | Class Entities, Record ValueObjects, `IRepository` | Pydantic / Dataclasses, Protocol Interfaces | Domain Entities, Type Interfaces |
| **Application** | MediatR Handlers, AutoMapper, FluentValidation | Use Case Services, Pydantic Schemas | Use Case Services, CQRS Handlers |
| **Infrastructure** | Entity Framework Core, Dapper, HttpClient | SQLAlchemy, Tortoise ORM, HTTPX | Prisma, TypeORM, Axios |
| **Presentation** | ASP.NET Core Controllers, Minimal APIs | FastAPI Routers, Dependency Injection | NestJS Controllers, Express Routes |
