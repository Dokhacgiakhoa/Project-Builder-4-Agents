---
id: D-001
type: reference
when: "Building scalable React frontend with feature-based modular structure"
---
# ADR 0008: FRONTEND FEATURE-DRIVEN ARCHITECTURE (BULLETPROOF REACT)

* **Status**: Approved (Accepted)
* **Decision date**: 2026-11-04
* **Decided by**: Frontend Architect & Tech Lead

---

## 1. CONTEXT
In software projects with complex user interfaces, organizing folders the traditional technical-classification way (all components in one folder, all hooks in another) quickly leads to a "spaghetti" structure that is hard to maintain and prone to git conflicts when many developers or AI Coding Agents work at the same time.

---

## 2. DECISION
We adopt the **Feature-Driven Architecture** (based on the **Bulletproof React** model):

1. **Tech Stack**:
   - **Framework**: React 18+ combined with Vite (a high-speed build tool).
   - **Language**: TypeScript in strict checking mode (`strict: true`).
   - **Styling**: Tailwind CSS.
   - **Server State**: TanStack React Query (handles caching, API synchronization).
   - **Client State**: Zustand (lightweight state management, no boilerplate).
   - **Schema Validation**: Zod (real-time data type checking).

2. **Module Boundary Rules**:
   - All business logic is divided into independent Feature Modules inside `src/features/{feature-name}/`.
   - A Feature **MUST NOT** import another Feature's internal files directly. If sharing is needed, go through the public `index.ts` file or move it up to the shared `src/components/` layer.
   - Unidirectional Dependency Flow: `Features` depend on `Shared Layers` (`components/`, `lib/`, `stores/`), never the other way around.

---

## 3. CONSEQUENCES
* **Pros**:
  - Highly modular; a feature can be removed or replaced easily without affecting the rest of the app.
  - Extremely friendly to AI Coding Agents: the Agent only needs to focus its context on exactly one feature folder to finish a task.
  - Fully decoupled from the Backend: connected through an independent API Contract.
* **Cons**:
  - Requires the team to keep the discipline of exporting through `index.ts`.
