---
id: T-001
type: reference
when: "Free-tier cloud infrastructure stack for small MVPs"
---
# ADR 0002: TECHNOLOGY STACK & CLOUD FREE-TIER GUIDELINES

* **Status**: Approved (Accepted)
* **Decision date**: 2026-11-04

---

## 1. CONTEXT
The project needs a modern, powerful Tech Stack with a rich library ecosystem that in particular can run stably on Cloud Free-Tier platforms for research and product development.

## 2. DECISION
* **Backend Framework**: A high-level language with type checking (FastAPI / Node.js TypeScript / ASP.NET Core).
* **Database & Vector Search**: PostgreSQL (with the `pgvector` extension through the Supabase Free Tier) combined with local ChromaDB for vector embeddings.
* **LLM Orchestration**: LangChain / LangGraph or the Native SDK.
* **LLM Engine Providers**:
  - Mistral AI (1 billion tokens/month free) & Google Gemini Flash (fast backup).
  - Groq LPU for demo scenarios that need instant response speed.
* **Frontend UI**: Next.js (React) deployed on Vercel, or Streamlit for a quick dashboard.
* **CI/CD & Source Control**: GitHub Actions.
* **Observability**: Langfuse (Self-hosted or Cloud Free Tier).

## 3. INFRASTRUCTURE PRINCIPLES
* Prioritize 100% Free-Tier during the development phase.
* Handle Cold Start with periodic health check pings.
* All Secrets / API Keys must be stored in `.env` and must never be committed to Git.
