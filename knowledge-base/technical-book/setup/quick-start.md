---
title: "Quick Start"
description: "Bootstrap your project in 5 minutes"
weight: 1
---

## Quick Start Guide

### Step 1: Clone Team Repository

Clone the project repository to your development machine:

```bash
git clone https://github.com/<COURSE-ORG>/<TEAM-ID>.git
cd <TEAM-ID>
```

### Step 2: Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux (or .venv\Scripts\Activate.ps1 on Windows)

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# → Open .env and populate required API keys
```

### Step 3: Verify Setup

```bash
# Launch development server
uvicorn src.main:app --reload

# Open browser: http://localhost:8000/docs
# → Confirm Swagger UI renders correctly
```

### Step 4: Git Setup

```bash
# Confirm remote repository mapping
git remote -v

# Create development branch
git checkout -b develop

# Initial push
git push -u origin develop
```

## Folder Structure

```
<TEAM-ID>/
├── src/                    ← Primary application source code
│   ├── agents/             ← LangGraph agents
│   │   ├── graph.py        ← Graph topology definition
│   │   ├── state.py        ← State schema
│   │   ├── nodes/          ← Graph processing nodes
│   │   └── tools/          ← Agent tool definitions
│   ├── api/                ← FastAPI routes
│   ├── models/             ← Pydantic schemas
│   ├── services/           ← Domain business logic
│   ├── config.py           ← Centralized configuration settings
│   └── main.py             ← Application entry point
├── tests/                  ← Automated test suite
├── docs/                   ← Project documentation
├── eval/                   ← Evaluation benchmarks & evidence
├── presentation/           ← Demo slides and recordings
├── Dockerfile              ← Multi-stage container build
├── docker-compose.yml      ← Local full-stack runtime
└── .github/workflows/      ← CI/CD pipeline definitions
```

## Code Organization Principles

1. **Single Responsibility per File** — `graph.py` builds graphs, `state.py` defines schemas.
2. **Modular Nodes in `nodes/`** — Isolate each graph node into its own module.
3. **Dedicated Tools in `tools/`** — Separate external integrations into discrete tool definitions.
4. **Decoupled API Routing** — Keep FastAPI endpoint routes isolated from `main.py`.
5. **Centralized Configuration** — Manage all environment settings through `config.py`.
