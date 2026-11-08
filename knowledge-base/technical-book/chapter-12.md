---
title: "DevOps and Deployment"
weight: 12
---

## 12.1 Docker — Application Containerization

Docker is a platform that allows you to package an application along with all of its dependencies (libraries, configuration, environment variables) into a single unit called a **container**. Containers ensure that an application runs identically across any environment — from your personal laptop to production servers. In AI20K, 100% of judging panels grade DevOps criteria, and Docker is the foundational tool required to achieve a high score.

Before Docker, developers often faced the classic "Friday night problem" — an application worked perfectly on local machines but failed when deployed to the server. The root causes were discrepancies in Python versions, system libraries, and environment configurations. Docker resolves this by packaging the entire runtime environment into an immutable image. You build once and run anywhere.

**Image vs Container** are two core concepts that must be distinguished:

- **Image**: An immutable blueprint containing the OS, runtime, application code, and dependencies. Images are built from a `Dockerfile` and stored in a registry (Docker Hub, GitHub Container Registry).
- **Container**: A running instance of an image. You can launch multiple isolated containers from the same image, each maintaining its own runtime state.

A basic Docker lifecycle workflow:

```bash
# Build image from Dockerfile
docker build -t my-agent-api:latest .

# Run container from image
docker run -d -p 8000:8000 --name my-api my-agent-api:latest

# View container logs
docker logs my-api

# Stop container
docker stop my-api

# Remove container
docker rm my-api

# Remove image
docker rmi my-agent-api:latest
```

The complete lifecycle: write a `Dockerfile` → build the image → run the container → push the image to a registry → pull it to the server → run in production.

> 💡 **TIP:** Always tag images with a specific semantic version (for example, `my-agent-api:1.0.3`) rather than relying solely on `latest`. The `latest` tag creates ambiguity during rollbacks and fails to guarantee reproducibility.

Essential Docker commands for everyday workflows:

```bash
# List all running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Monitor resource usage
docker stats

# Open an interactive shell inside a running container for debugging
docker exec -it my-api /bin/bash

# Inspect image details (layers, size)
docker images
docker history my-agent-api:latest
```

When building AI Agent applications, Docker becomes particularly vital because these applications depend on a complex stack: LangChain, LangGraph, embedding models, vector store clients, and LLM API keys. Docker ensures that every component is consistently configured across development, testing, and production environments.

> ⚠️ **NOTE:** Never store secrets (API keys, passwords, database credentials) inside a Docker image. Use runtime environment variables or Docker secrets to inject sensitive information safely.

```mermaid
flowchart LR
    PUSH[git push] --> CI[GitHub Actions]
    CI --> LINT[ruff check]
    LINT --> TEST[pytest + coverage]
    TEST --> BUILD[Docker build multi-stage]
    BUILD --> SCAN[Health check container]
    SCAN --> DEPLOY{branch?}
    DEPLOY -->|develop| STG["Staging: Render/Vercel preview"]
    DEPLOY -->|main| PROD[Production deploy]
```
> [📊 Open diagram on Mermaid Live / AI Editor](https://mermaid.live/edit#pako:eNplkMtuwjAQRX9l5G2Luu-iFSUIIkUQkVCpsrMw9iSxSOzIsUEI-Pc6D6mLennP8VzN3IkwEsk7kLIxV1Fz6yA5MA3hpcdsSyvloPN9XcBi8QGrmG6U2_oTLIVTRvfFpK7iESfxLqfWlyWIGsV5hkM64nyd5bS7OewdvIAwF7S8wtka4Gh9HeMkopERZ7Rw8qqR0PrGqUXv_uxRGvVstdzRLfLG1VNrGKwdVxrt7A7GqEbrNNn_3E-Wa1F_Pic6hQN_SLxgY7oHZPmGMpKFPqWrdziglmjfvtEKbKCzeFF4ZaT4N6ANtQ9ID_uIptZIP94IJHaNuRXkFUiLNjhyuPd9-M2Iq7FFFgJGJJY8LMoI089B5t6Z7KZFgM56DInvJHcYKV5Z3s7x8xexOI_z)

## 12.2 Multi-stage Dockerfile

Multi-stage builds are a Docker technique that allows you to define multiple stages within a single `Dockerfile`. The first stage (builder) installs compilation tools and project dependencies. The second stage (production) copies only the required build artifacts, omitting build tools entirely. Result: a production image that is 5 to 10 times smaller and significantly more secure since it lacks compilation toolchains.

Why are multi-stage builds important? A standard Python image often swells to 1–2 GB because it retains the pip cache, compilation toolchains (gcc, g++), and temporary build artifacts. Multi-stage builds reduce this size down to 200–400 MB, saving network bandwidth during deployments and shrinking the attack surface.

Here is a complete, production-ready `Dockerfile` for a LangGraph + FastAPI application:

```dockerfile
# ============================================
# Stage 1: Builder — install dependencies
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies required for compiling C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies into an isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Production — minimal runtime image
# ============================================
FROM python:3.11-slim AS production

# Configure environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

WORKDIR /app

# Create a non-root user for security hardening
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY . .

# Transfer file ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Health check — verify that the API is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Launch application using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Detailed breakdown of critical components:

**Layer caching:** Docker builds images layer by layer, corresponding to each instruction in the Dockerfile. When code changes occur, only layers from `COPY . .` downward need to be rebuilt. As long as `requirements.txt` remains unchanged, the `pip install` layer is retrieved directly from cache — saving 2–5 minutes per build. This explains why `COPY requirements.txt` must always precede `COPY . .`.

**Non-root user:** By default, Docker runs containers as `root`. If an attacker exploits a vulnerability in the application, they inherit root privileges inside the container. Creating and running as `appuser` enforces the principle of least privilege, isolating system resources.

**HEALTHCHECK directive:** Docker periodically checks the container's health every 30 seconds. If the health probe fails 3 consecutive times, the container is flagged as `unhealthy`, allowing orchestrators (Docker Compose, Kubernetes) to trigger automatic restarts. This guarantees high service availability for the API.

> 🔑 **KEY TAKEAWAY:** Always adopt multi-stage builds for production environments. Smaller images are faster to deploy and inherently more secure. Stage 1 compiles, Stage 2 executes — this standard pattern applies to any modern Python application.

Add a `.dockerignore` file to exclude unnecessary files from the build context:

```text
__pycache__/
*.pyc
*.pyo
.env
.git
.gitignore
.venv/
venv/
*.md
tests/
.dockerignore
Dockerfile
docker-compose.yml
```

The `.dockerignore` file functions like `.gitignore` — preventing superfluous files from entering the Docker build context, accelerating build times, and maintaining minimal image sizes.

## 12.3 Docker Compose — Multi-Service Management

Docker Compose is a tool for defining and running multi-container applications using a declarative YAML file. Instead of executing 5 to 6 cumbersome `docker run` commands manually, you define a single `docker-compose.yml` file and run `docker compose up` — automatically handling service provisioning, network interconnection, and container lifecycles.

In a typical AI Agent architecture, you need at least 3 to 4 collaborating services: an API server, a relational database (PostgreSQL), a vector store (Chroma/PGVector), and optionally Redis for caching and session state. Docker Compose orchestrates this entire stack effortlessly.

Below is a complete `docker-compose.yml` configuration tailored for an AI Agent project:

```yaml
version: "3.9"

services:
  # ============================================
  # API Server — FastAPI + LangGraph
  # ============================================
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: agent-api
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://agentuser:agentpass@db:5432/agentdb
      - REDIS_URL=redis://redis:6379/0
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - LANGSMITH_PROJECT=ai20k-agent
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    volumes:
      - ./app:/app/app  # Hot reload during development
    networks:
      - agent-network
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
        reservations:
          memory: 256M
          cpus: "0.25"
    restart: unless-stopped

  # ============================================
  # PostgreSQL — Primary Database
  # ============================================
  db:
    image: postgres:16-alpine
    container_name: agent-db
    environment:
      POSTGRES_USER: agentuser
      POSTGRES_PASSWORD: agentpass
      POSTGRES_DB: agentdb
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agentuser -d agentdb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - agent-network
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.25"
    restart: unless-stopped

  # ============================================
  # Redis — Cache & Session Store
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: agent-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - agent-network
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: "0.1"
    restart: unless-stopped

# ============================================
# Named Volumes — Data persistence
# ============================================
volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local

# ============================================
# Networks — Service isolation
# ============================================
networks:
  agent-network:
    driver: bridge
```

Key architectural concepts explained:

**depends_on with health conditions:** The `api` service waits until both `db` and `redis` report healthy status before spinning up. Without `condition: service_healthy`, the API container might launch before the database is ready to accept connections, causing startup connection errors.

**Named volumes:** `postgres-data` and `redis-data` persist data independently outside the container lifecycles. Running `docker compose down` destroys container instances while preserving stored state. Only `docker compose down -v` wipes volume data, guarding against accidental data loss.

**Resource limits:** The `deploy.resources.limits` directives cap memory and CPU usage per service. If the API suffers from a memory leak (common in Python stacks handling complex AI workflows), consumption is throttled to 512MB instead of exhausting server RAM and crashing sibling services.

> 💡 **TIP:** During active development, mount `./app:/app/app` under `volumes` to enable live hot-reloading — changes made locally will instantly take effect inside the container. Ensure this line is removed when deploying to production.

Essential Docker Compose commands:

```bash
# Launch all services in background (detached mode)
docker compose up -d

# Stream real-time logs across all services
docker compose logs -f

# Stream logs for a specific service
docker compose logs -f api

# Restart a specific service
docker compose restart api

# Stop all containers while preserving data volumes
docker compose down

# Stop all containers and remove volume data
docker compose down -v

# Rebuild images and restart services
docker compose up -d --build
```

> ⚠️ **NOTE:** Never commit a `docker-compose.yml` file containing production credentials into version control. Store secrets in a local `.env` file and verify that `.env` is listed in `.gitignore`. Docker Compose automatically reads environment files present in the working directory.

## 12.4 CI/CD with GitHub Actions

CI/CD stands for Continuous Integration and Continuous Deployment. CI ensures that every code push triggers automated test suites — detecting bugs and regressions before code merges into protected branches. CD automates deployment pipelines to servers once all tests pass successfully. Overlooking CI/CD is one of the most common pitfalls in hackathons and leads to severe score deductions under DevOps judging criteria.

GitHub Actions is an integrated CI/CD platform built directly into GitHub. Workflows are declared using YAML files located under `.github/workflows/`. Each workflow comprises one or more jobs, and each job executes a sequence of individual steps. Workflows are triggered by repository events such as pushes, pull requests, or manual triggers (`workflow_dispatch`).

Here is a comprehensive CI workflow:

```yaml
# .github/workflows/ci.yml
name: CI — Lint, Test, Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # ============================================
  # Job 1: Lint & Format Check
  # ============================================
  lint:
    name: Lint with Ruff
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Ruff
        run: pip install ruff

      - name: Run Ruff check
        run: ruff check . --output-format=github

      - name: Check formatting
        run: ruff format --check .

  # ============================================
  # Job 2: Run Tests
  # ============================================
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint  # Only run after linting passes
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov httpx

      - name: Run tests with coverage
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: coverage.xml

  # ============================================
  # Job 3: Build Docker Image
  # ============================================
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test  # Only run after tests pass
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: agent-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**Workflow structure explained:**

This pipeline sequences 3 jobs sequentially: lint → test → build. If linting fails, testing and building are cancelled immediately, conserving runner minutes. If unit tests fail, the build stage is halted, ensuring broken code is never packaged into an image.

**Linting with Ruff:** Ruff is an extremely fast Python linter and code formatter written in Rust, replacing Flake8, isort, and Black. It enforces code conventions, import order, detects unused variables, and flags common anti-patterns. Using `--output-format=github` outputs inline annotations directly onto pull request diffs for instant reviewer feedback.

**Caching pip dependencies:** The `actions/cache` action caches downloaded wheels and tarballs across workflow runs, avoiding redundant downloads of 100+ packages on every commit. The cache key tracks changes to `requirements.txt`, invalidating only when dependencies are modified.

> 🔑 **KEY TAKEAWAY:** Maintain at least linting and automated tests inside your CI pipeline. This constitutes one of the clearest signals of software engineering maturity to the evaluation committee. Many teams omit CI/CD entirely — having it running immediately sets your project apart.

Dedicated production **deployment workflow**:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # Enable manual triggering

jobs:
  deploy:
    name: Deploy to Render
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Trigger Render Deploy Hook
        run: |
          curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"

      - name: Notify deployment
        run: |
          echo "Deployed commit ${{ github.sha }} to production"
```

This workflow automates continuous delivery whenever code is merged into the `main` branch by invoking a Render Deploy Hook via HTTP POST, instructing Render to fetch the latest changes and initiate deployment.

## 12.5 Cloud Deployment

Once your Docker image and CI/CD pipelines are verified, the next step is hosting the application on cloud infrastructure for real user access. In AI20K, a functional Live URL is one of the 10 mandatory deliverables.

Several hosting options exist, but the following stack offers the optimal balance of simplicity and reliability for AI Agent projects:

### Backend — Render or Railway

**Render** (render.com) is a platform-as-a-service (PaaS) supporting containerized and Git-backed deployments. Highlights: generous free tier, automated SSL, native GitHub deployment webhooks, and seamless Dockerfile support.

**Railway** (railway.app) provides similar capabilities with intuitive UX and multi-database provisioning. Both options work smoothly for AI20K requirements.

Step-by-step deployment on Render:

1. Sign up on Render using your GitHub account.
2. Select "New Web Service" → "Build and deploy from a Docker image".
3. Connect your project's GitHub repository.
4. Configure environment variables: `OPENAI_API_KEY`, `DATABASE_URL`, `LANGSMITH_API_KEY`.
5. Select an instance tier: Free (512MB RAM) or Starter ($7/month).
6. Render builds the Docker image and provisions the public URL.

**Environment variables** manage dynamic configuration and secrets safely. On Render, set them under Dashboard → Environment:

```
OPENAI_API_KEY=sk-proj-xxxxx
DATABASE_URL=postgresql://user:pass@host:5432/db
LANGSMITH_API_KEY=lsv2_pt_xxxxx
LANGSMITH_PROJECT=ai20k-agent-production
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Frontend — Vercel

For web user interfaces (React, Next.js, Streamlit), deploy to **Vercel** (vercel.com). Vercel is optimized for frontend architectures, featuring a global CDN and generous free tier allowances.

```bash
# Deploy frontend to Vercel
npm install -g vercel
vercel --prod
```

### Custom Domains

Acquire a custom domain from Namecheap, Cloudflare, or GoDaddy (~$10/year) and configure DNS records toward Render/Vercel:

- Render: Configure custom domains under Settings → Custom Domains
- Vercel: Configure under Project Settings → Domains
- CNAME record: `your-subdomain.yourdomain.com` → `your-app.onrender.com`

> 💡 **TIP:** Consider purchasing a `.app` or `.dev` top-level domain — Google enforces built-in HTTPS on these TLDs, eliminating manual SSL configuration. A `.me` domain is also popular for portfolio demonstrations.

Post-deployment verification commands:

```bash
# Probe health endpoint
curl https://your-app.onrender.com/health

# Test primary chat API endpoint
curl https://your-app.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "thread_id": "test-123"}'

# Measure response latency
curl -o /dev/null -s -w "Time: %{time_total}s\n" \
  https://your-app.onrender.com/health
```

> ⚠️ **NOTE:** Render free tier instances enter sleep mode after 15 minutes of inactivity. Initial requests following sleep take 30 to 60 seconds to cold start. Set up an automated ping service (such as UptimeRobot) every 5 minutes to prevent cold starts, or upgrade to a paid tier during Demo Day.

## 12.6 Monitoring and Logging

Monitoring and structured logging form the pillars of production reliability. Without monitoring, identifying outages or degradation is impossible. Without logging, diagnosing bugs and edge cases becomes guesswork. Within AI20K DevOps grading, robust monitoring and logging represent the differentiator between an average score and top marks.

### Python Structured Logging Setup

While Python includes a built-in `logging` module, its default configuration lacks structure. Below is a production-grade structured logging setup:

```python
# app/core/logging_config.py
import logging
import sys
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format application logs into structured JSON records."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include custom context attributes if present
        if hasattr(record, "extra_data"):
            log_entry["data"] = record.extra_data

        # Capture exception tracebacks if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging(log_level: str = "INFO") -> None:
    """Initialize application logging configuration."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Output handler for stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # Suppress verbose loggers from external dependencies
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
```

**Structured logging** serializes log messages into structured JSON rather than unstructured text. Benefits: easily indexable, searchable, and natively compatible with monitoring backends such as Datadog, Grafana Loki, or ELK Stack.

```python
# Logging usage across application logic
import logging

logger = logging.getLogger(__name__)

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    logger.info(
        "Processing chat request",
        extra={
            "extra_data": {
                "thread_id": request.thread_id,
                "message_length": len(request.message),
            }
        },
    )
    try:
        response = await agent.arun(request.message)
        logger.info(
            "Chat request completed",
            extra={
                "extra_data": {
                    "thread_id": request.thread_id,
                    "response_length": len(response),
                }
            },
        )
        return {"response": response}
    except Exception as e:
        logger.error(
            "Chat request failed",
            exc_info=True,
            extra={
                "extra_data": {
                    "thread_id": request.thread_id,
                    "error_type": type(e).__name__,
                }
            },
        )
        raise
```

### LangSmith for AI Tracing

LangSmith provides deep observability tailored specifically for LLM, LangChain, and LangGraph architectures. It instruments every single agent step — from user input, model invocations, document retrievals, to generated outputs. AI Logs is frequently among the highest scoring deliverables when configured properly.

Configuring LangSmith requires only three environment variables:

```bash
export LANGSMITH_API_KEY="lsv2_pt_xxxxx"
export LANGSMITH_PROJECT="ai20k-agent"
export LANGCHAIN_TRACING_V2="true"
```

```python
# In the application, LangSmith tracing activates automatically via environment variables
# No custom instrumentation required — simply import langchain
import os

# Verify LangSmith configuration
assert os.getenv("LANGCHAIN_TRACING_V2") == "true", "LangSmith not configured"
```

The LangSmith dashboard offers granular visibility:
- Every execution represents a traceable session.
- Every state node in the graph is visualized as a child span.
- Token metrics, execution latencies, and dollar costs per model call.
- Inspection of prompt inputs and model completions at every node for effortless debugging.

### Health Check Endpoints

A health check endpoint provides a standardized probe for monitoring systems to verify application uptime and dependency status:

```python
# app/api/health.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    """
    Primary health check endpoint for monitoring probes.
    Verifies API availability, database connectivity, and downstream services.
    """
    checks = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
    }

    # Verify database connectivity
    try:
        # Example probe logic:
        # async with db.session() as session:
        #     await session.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        checks["database"] = "disconnected"
        checks["status"] = "degraded"

    # Verify downstream LLM service availability
    try:
        # Lightweight probe to LLM endpoint or verification of API credentials
        checks["llm_api"] = "reachable"
    except Exception as e:
        logger.error(f"LLM API health check failed: {e}")
        checks["llm_api"] = "unreachable"
        checks["status"] = "degraded"

    status_code = 200 if checks["status"] == "healthy" else 503
    return JSONResponse(content=checks, status_code=status_code)


@router.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe — verifies container process is alive."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_probe():
    """Kubernetes readiness probe — verifies service is ready to handle incoming traffic."""
    # Check all critical upstream and downstream dependencies
    return {"status": "ready"}
```

> 🔑 **KEY TAKEAWAY:** Three essential monitoring pillars: (1) Structured logging for application error tracing, (2) LangSmith for AI pipeline observability, and (3) Health check endpoints for infrastructure uptime monitoring. The evaluation panel places special emphasis on AI Logs as clear evidence of deterministic, reliable agent execution.

## Summary

This chapter explored the complete DevOps lifecycle for production-ready AI Agent applications:

- **Docker** encapsulates applications within portable containers, ensuring consistent runtime behavior across all target environments.
- **Multi-stage Dockerfile** minimizes production image sizes and enhances container hardening using non-root users and automated health checks.
- **Docker Compose** coordinates multi-service topologies (API, PostgreSQL, Redis) with health checks, restarts, and resource constraints.
- **GitHub Actions CI/CD** automates linting, test suites, and image builds on every push — demonstrating software engineering rigor.
- **Cloud Deployment** leverages Render for backend hosting and Vercel for frontend distribution quickly and reliably.
- **Monitoring and Logging** integrates structured JSON logging, LangSmith AI observability, and standardized health check probes.

DevOps constitutes an explicit scoring category in AI20K. While many teams overlook testing and CI/CD pipelines, establishing Docker + CI/CD + automated tests + health checks firmly establishes your project among top contenders.

## Review Questions

1. What is the fundamental difference between a Docker image and a Docker container?
2. Why do multi-stage builds yield significantly smaller images? Explain the mechanics of Docker layer caching.
3. How does `depends_on` with `condition: service_healthy` differ from a standard `depends_on` configuration?
4. If a GitHub Actions CI pipeline fails at the testing step, does the build job proceed? Why?
5. Why is it dangerous to embed API keys directly in a Docker image? What is the recommended best practice?
6. What advantages does structured JSON logging provide over standard plain text logging?
7. What telemetry does LangSmith capture, and why is this critical for AI Agent debugging?
8. What HTTP status code should a health check endpoint return when application dependencies are unhealthy or degraded?
