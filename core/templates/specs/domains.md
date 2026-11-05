# DOMAIN BOUNDARIES & CONTEXT MAP (BOUNDED CONTEXTS)

> **Mục tiêu**: Phân chia hệ thống thành các Domain rành mạch để AI và các thành viên có thể làm việc song song mà không xung đột mã nguồn.

---

## 🗺️ 1. BẢN ĐỒ CÁC DOMAIN (DOMAIN MAP)

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
> [📊 Mở sơ đồ trên Mermaid Live / AI Editor](https://mermaid.live/edit#pako:eNptUU1PAjEQ_StND54khq-LBxNkPZAQNYIn6qHsDkuT7XTTTokb4L87hcYA2tu89-bNvOlelq4C-Shk7XW7FfMPhYJfiOszMHUeROGsNihWp-I5BoMQQkbD17kjvaK_UnJWAZKhTtyJSaRtlil5qRvcWM1dbcqsvNQN2W8yEzMkaBpTA5YgHsSkThPKW2fASuHN-ovYts6Twfo3xB_oKsGIJ746MhtTajIOOcXUWRsx19c5xmk_1E3H6wSWvq0D-J1em4YP8N9iRV_0ek-HT5axL8f6pgOfI5ODE_nunW0p2RWaNNPDK_plx-kDw6MMD0_wEhqwQL4TS69LSIKxvBfSgueQVfrifWpQkrYsVAwoWcFGx4aUVHhMYh3JLTosmSQfgZHYVpqgMJrvaTN8_AHIirNR)

---

## 📦 2. QUY ƯỚC RANH GIỚI & GIAO TIẾP LIÊN DOMAIN

1. **Giao tiếp qua Hợp đồng (Contract-Only Communication)**:
   - Domain A KHÔNG được phép truy cập trực tiếp vào DB Table hoặc nội hàm private của Domain B.
   - Mọi tương tác phải qua API Contract (REST API, RPC) hoặc Event Bus công khai.
2. **Context Cô Lập Cho AI Coding Agent**:
   - Khi giao task thuộc Domain A, Agent chỉ cần nạp context của Domain A và các Contracts liên quan, tránh over-context dẫn đến ảo giác (hallucination).
