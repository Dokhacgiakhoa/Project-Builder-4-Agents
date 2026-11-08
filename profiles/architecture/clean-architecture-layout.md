---
id: A-003
type: reference
when: "Target folder layout for Clean Architecture in .NET / Python / TypeScript"
---
# CLEAN ARCHITECTURE DIRECTORY LAYOUT (LAYERED BLUEPRINT)

The `src/` directory is organized according to **Clean Architecture & Domain-Driven Design (DDD)** principles. Regardless of tech stack (.NET, Python, TypeScript, Go), map source code across these four concentric layers:

---

## 🏛️ 1. Concentric Architectural Layers

```text
src/
├── Domain/                 # 1. Enterprise Core & Entities (100% Framework Independent)
│   ├── Entities/           # Rich models with identity and business invariants
│   ├── ValueObjects/       # Immutable value objects (Email, Money, Address)
│   ├── Events/             # Domain Events (UserRegisteredEvent)
│   └── Repositories/       # Storage interfaces (IUserRepository)
│
├── Application/            # 2. Use Cases & Orchestration Logic
│   ├── Commands/           # CQRS Commands (CreateUserCommand + Handler)
│   ├── Queries/            # CQRS Queries (GetUserByIdQuery + Handler)
│   ├── DTOs/               # Data Transfer Objects
│   └── Interfaces/         # Service interfaces (IEmailService, ICacheService)
│
├── Infrastructure/         # 3. External Implementations & Persistence
│   ├── Persistence/        # DB Context, Migrations, Repository Implementations
│   ├── ExternalServices/   # Third-party integrations (Stripe, OpenAI, Supabase)
│   └── Caching/            # Redis cache adapters
│
└── Presentation/           # 4. Entry Points & User Interface
    ├── Controllers/        # REST API Controllers / Route Handlers
    ├── Middlewares/        # Error Handling, Auth Token Validation, Rate Limiter
    └── Entrypoint/         # Program.cs / main.py / server.ts (Composition Root / DI)
```

---

## 🗺️ 2. Stack Mapping Reference

| Architectural Layer | .NET / C# | Python (FastAPI) | TypeScript / Node (NestJS/Express) |
| :--- | :--- | :--- | :--- |
| **Domain** | Class Entities, Record ValueObjects, `IRepository` | Pydantic / Dataclasses, Protocol Interfaces | Domain Entities, TypeScript Interfaces |
| **Application** | MediatR Handlers, AutoMapper, FluentValidation | Use Case Services, Pydantic Schemas | Use Case Services, CQRS Handlers |
| **Infrastructure** | Entity Framework Core, Dapper, HttpClient | SQLAlchemy, Tortoise ORM, HTTPX | Prisma, Drizzle, TypeORM, Axios |
| **Presentation** | ASP.NET Core Controllers, Minimal APIs | FastAPI Routers, Dependency Injection | NestJS Controllers, Express Routes |
