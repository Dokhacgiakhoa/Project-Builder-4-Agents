# DOMAIN BOUNDARIES & CONTEXT MAP (BOUNDED CONTEXTS)

> **Objective**: Partition the system into decoupled bounded contexts so developers and AI agents can execute in parallel without code collisions.

---

## 🗺️ 1. Domain Context Map

```mermaid
graph LR
    subgraph Core Domain [Core Business Domains]
        D1["Identity & Auth Domain"]
        D2[Core Business Logic Domain]
        D3["AI Intelligence / Agentic Domain"]
    end

    subgraph Supporting Domain [Supporting Domains]
        D4["Notification & Communication"]
        D5["Analytics & Observability"]
    end

    D1 -->|User Context| D2
    D2 -->|Prompts & Data| D3
    D2 -->|Events| D4
    D3 -->|Telemetry Traces| D5
```

---

## 📦 2. Boundary Conventions & Cross-Domain Communication

1. **Contract-Only Communication**:
   - Domain A MUST NOT directly access database tables or private internals of Domain B.
   - All inter-domain communication must traverse public API contracts (REST, RPC) or event buses.
2. **Context Isolation for AI Coding Agents**:
   - When assigning tasks in Domain A, feed only Domain A's context and related contracts into the agent to prevent token bloat and hallucination.
