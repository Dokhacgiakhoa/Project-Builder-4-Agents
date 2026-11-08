---
title: "Docker & CI/CD"
description: "Docker packaging and GitHub Actions CI pipelines"
weight: 1
---

## Docker

### Multi-stage Dockerfile

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Commands

```bash
docker build -t ai20k-app .
docker compose up -d
docker compose logs -f backend
docker compose down
```

## CI/CD (GitHub Actions)

CI executes automatically on GitHub pushes:

1. **Lint** — `ruff check` enforces formatting and style
2. **Test** — `pytest` runs the test suite
3. Pass → mergeable. Fail → fix issues before merge.

### Setup CI

Configured in `.github/workflows/ci.yml`.

### Minimum Requirements

- ✅ CI pipeline must execute cleanly
- ✅ Ruff lint pass
- ✅ All tests must pass

## Environment Variables

```bash
# .env.example — safe to commit (template)
# .env — NEVER COMMIT (contains real secrets)
```

## Git Workflow

```
main (production)
  └── develop (daily work)
       ├── feature/agent-flow
       ├── feature/api-routes
       └── feature/ui
```

### Commit Messages

```
feat: add agent graph with analyze and respond nodes
fix: resolve CORS blocked error on frontend
docs: update architecture diagram
test: add test cases for chat endpoint
refactor: extract analyze node into separate module
```
