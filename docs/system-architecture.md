# KIẾN TRÚC TỔNG THỂ HỆ THỐNG (SYSTEM ARCHITECTURE)

---

## 🏛️ 1. SƠ ĐỒ KIẾN TRÚC TỔNG QUAN (C4 CONTAINER DIAGRAM)

```mermaid
graph TD
    Client[Web / Mobile Client<br/>Next.js / React]
    API[Backend API Gateway<br/>FastAPI / Modular Monolith]
    AI_Agent[AI Agentic Engine<br/>LangGraph / Multi-Agent Swarm]
    DB[(Primary Database<br/>PostgreSQL / Supabase)]
    VectorDB[(Vector Store<br/>pgvector / ChromaDB)]
    Monitor[Telemetry & Observability<br/>Langfuse Tracing]

    Client -->|HTTPS / REST API| API
    API -->|Workflow Trigger| AI_Agent
    API -->|SQL Queries| DB
    AI_Agent -->|Semantic Search| VectorDB
    AI_Agent -->|Log Traces| Monitor
    API -->|Log Traces| Monitor
```

---

## 🔄 2. LUỒNG DỮ LIỆU CHÍNH (KEY DATA FLOW)
1. Người dùng gửi yêu cầu từ giao diện Client.
2. Backend API xác thực quyền (`ROLE_USER`), kiểm tra Input Schema.
3. Kích hoạt AI Agent để thực hiện suy luận hoặc tìm kiếm ngữ nghĩa trên Vector DB.
4. Trả về kết quả phòng vệ (Defensive Payload) cho Client hiển thị.
