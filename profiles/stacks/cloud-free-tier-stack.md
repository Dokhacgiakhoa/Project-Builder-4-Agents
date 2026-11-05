# ADR 0002: TECHNOLOGY STACK & CLOUD FREE-TIER GUIDELINES

* **Trạng thái**: Đã phê duyệt (Accepted)
* **Ngày quyết định**: 2026-11-04

---

## 1. BỐI CẢNH (CONTEXT)
Dự án cần một Tech Stack hiện đại, mạnh mẽ, có hệ sinh thái thư viện phong phú và đặc biệt có thể vận hành ổn định trên các nền tảng Cloud Free-Tier phục vụ nghiên cứu và phát triển sản phẩm.

## 2. QUYẾT ĐỊNH (DECISION)
* **Backend Framework**: Ngôn ngữ bậc cao có type-checking (FastAPI / Node.js TypeScript / ASP.NET Core).
* **Database & Vector Search**: PostgreSQL (tích hợp extension `pgvector` qua Supabase Free Tier) kết hợp ChromaDB local cho vector embedding.
* **LLM Orchestration**: LangChain / LangGraph hoặc Native SDK.
* **LLM Engine Providers**:
  - Mistral AI (1 tỷ token/tháng free) & Google Gemini Flash (backup nhanh).
  - Groq LPU cho các kịch bản demo cần tốc độ phản hồi tức thì.
* **Frontend UI**: Next.js (React) deploy trên Vercel hoặc Streamlit cho dashboard nhanh.
* **CI/CD & Source Control**: GitHub Actions.
* **Observability**: Langfuse (Self-hosted hoặc Cloud Free Tier).

## 3. NGUYÊN TẮC HẠ TẦNG
* Ưu tiên 100% Free-Tier trong giai đoạn phát triển.
* Xử lý Cold Start bằng health check ping định kỳ.
* Toàn bộ Secrets / API Keys phải lưu trong `.env`, tuyệt đối không commit lên Git.
