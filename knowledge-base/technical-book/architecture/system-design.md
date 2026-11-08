---
title: "System Design"
description: "System architecture overview and component topologies"
weight: 1
---

## System Architecture

### Overview Diagram

```mermaid
graph TB
    User([User]) --> UI["Frontend<br/>React/Next.js"]
    UI -->|REST API| API[FastAPI Backend]
    API --> Agent[LangGraph Agent]
    Agent --> LLM["LLM Service<br/>GPT-4o / Gemini"]
    Agent --> Tools[Agent Tools]
    Tools --> DB[("Database")]
    Agent --> VS["Vector Store<br/>ChromaDB"]
```
> [📊 View diagram in Mermaid Live / AI Editor](https://mermaid.live/edit#pako:eNplUUFuwjAQ_IrlE0hNc-kJVUikKVGktEIkcIk5LM42SUts5DhVK-DvXZvQHurDeLyenR3ZJy51hXzGeG3g2LAiEorR2vRoJqXD3ZQFwZxt0lLwpdHKoqoe9yacrxGkDV_xy96_94LvxsbUyc_r57xgi1V6dlAuobe0swjkB7WPUldx1osalS0zUHXiM_jzTeO4V2XZCyUgZDmaz1aiD5GsiuBBs5Al2LWq_Y3x11dofejL69nzUeG5V8RRORE8Bgt76FHw6T-PbU6jtyitNiwnuM5-aozuII5oKL9jvEPTQVu5tzw5A8Ftgx35zYhW-AbDwQou1MWJYbA6_1aSLq0ZkCrDsQKLcQv0Ed1YvvwAV8iBEw==)

## Components

### 1. Frontend (React/Next.js)

- **Purpose:** User interface for end-users
- **Key Features:** Responsive, dark mode, realtime
- **State Management:** React hooks / Zustand

### 2. Backend (FastAPI)

- **Purpose:** API gateway handling business logic and routing
- **API Design:** RESTful endpoints
- **Auth:** JWT (when required)

### 3. AI Agent (LangGraph)

- **Agent Type:** ReAct / Plan-and-Execute / Custom
- **State:** TypedDict schema
- **Nodes:** Execute individual pipeline stages
- **Tools:** Search, calculate, API calls

### 4. Database

- **Type:** PostgreSQL (production) / SQLite (dev)
- **ORM:** SQLAlchemy (when relational mapping needed)
- **Migrations:** Alembic (schema migrations)

### 5. Vector Store

- **Type:** ChromaDB (local) / Pinecone (cloud)
- **Embeddings:** OpenAI embeddings
- **Purpose:** RAG / similarity search

## Data Flow

1. User submits request from Web Client
2. API endpoint validates payload schema via Pydantic
3. Agent processes request via LangGraph pipeline
4. LLM generate response
5. Tools execute external actions (when dispatched)
6. Output streams back to Web Client via API

## Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Framework | FastAPI | Async, auto-docs, type-safe |
| Agent | LangGraph | Flexible state machine |
| Database | SQLite → PostgreSQL | Lightweight local dev, robust in production |
| Frontend | Next.js | Full-stack ready |
