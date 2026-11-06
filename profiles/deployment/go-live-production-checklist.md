---
id: T-005
type: playbook
when: "When preparing to **deploy product to real production (Go-Live / Production Deploy)**, beyond localhost"
---

# PLAYBOOK: PRODUCTION GO-LIVE CHECKLIST

> **For AI Agents**: Guide the Vibe Coder from `localhost` to live internet production (Go-Live). The objective is a stable, secure, zero-to-low cost deployment (prioritizing Cloud Free-Tiers) passing 100% of Project Health Check criteria with an A+ score.

---

## 1. Core Go-Live Tenets
1. **Zero Hardcoded Secrets**: All DB credentials, JWT secrets, and API keys must be configured on Cloud Provider Dashboards, never in Git.
2. **Explicit CORS & Domains**: Never leave `CORS: *` in production. Restrict API access strictly to your deployed frontend domain.
3. **Standardized Containerization**: Docker multi-stage builds, non-root user (`appuser`), minimal image foot-print.
4. **Health Check Endpoint**: Backend must expose `/healthz` or `/api/health` returning HTTP 200 for cloud liveness/readiness probes.

---

## 2. The 5 Go-Live Control Gates

### Gate 1: Build & Optimization Gate
* [ ] Run production `build` locally; resolve all compiler and TypeScript warnings.
* [ ] Code Splitting: Ensure heavy routes leverage dynamic imports (`React.lazy`), preventing single giant JS bundles > 1MB.
* [ ] Verify `.dockerignore` excludes `node_modules`, `.git`, `.env`, and build caches.

### Gate 2: Security & Network Gate
* [ ] **HTTP Security Headers**: Inject `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`.
* [ ] **Rate Limiting**: Enable rate limiting middleware (e.g., max 100 reqs/min/IP) to prevent abuse.
* [ ] **Error Sanitization**: Never leak raw database errors or stack traces to clients; return friendly messages with traceable error IDs.

### Gate 3: Database & Data Safety Gate
* [ ] Apply all pending database migrations cleanly to the production database.
* [ ] Enable Connection Pooling (e.g., Supabase Pooling port 6543 or PgBouncer) to prevent connection exhaustion.
* [ ] Verify automated database backups on the persistence platform.

### Gate 4: Zero-Cost Cloud Hosting Gate
* [ ] **Frontend**: Deploy to **Vercel** or **Cloudflare Pages** (connected to GitHub main branch).
* [ ] **Backend**: Deploy to **Railway** or **Render / Fly.io / Koyeb**.
* [ ] **Database**: Provision **Supabase** (PostgreSQL 500MB free tier) or **Turso / Neon**.
* [ ] **Environment Variables**: Configure all keys listed in `.env.example` in the cloud hosting provider's dashboard.

### Gate 5: Comprehensive Health Check Gate
* [ ] Execute Project Health Check:
  ```bash
  python scripts/project_auditor.py <target_project_dir>
  ```
* [ ] Achieve **Grade A or A+** (≥ 90/100 points).
* [ ] Resolve 100% of High and Medium severity findings before final announcement.

---

## 3. Incident Triage & Instant Rollback Protocol
* If deployment encounters 500 errors or crashes:
  1. Inspect runtime logs on Cloud Dashboard (check missing environment variables or DB connectivity).
  2. Click **Rollback** (or redeploy previous green commit) in Vercel/Railway dashboard for instant restoration.
  3. Activate local `anti-patching-debugger` to analyze root cause before attempting another deployment.
