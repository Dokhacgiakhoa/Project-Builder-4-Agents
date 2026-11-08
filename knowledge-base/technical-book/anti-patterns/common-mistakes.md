---
title: "Common Engineering Mistakes"
description: "Top code quality and architectural failure modes to avoid"
weight: 1
---

# Top 10 Engineering Mistakes

### 1. Bare Except Clauses

```python
# ❌ Masks critical errors and complicates debugging
try:
    result = await process(data)
except:
    pass

# ✅ Catch specific exceptions and log diagnostics
try:
    result = await process(data)
except ValueError as e:
    logger.error(f"Invalid payload format: {e}")
    return {"error": str(e)}
```

### 2. Hardcoded API Credentials

```python
# ❌ Secret committed directly to version control
client = OpenAI(api_key="sk-abc123...")

# ✅ Isolate credentials in .env and Pydantic settings
from src.config import get_settings
settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)
```

### 3. Missing Automated Tests

Ensure comprehensive unit and integration tests exist in `tests/` covering both API routes and agent workflows.

### 4. Absent CI/CD Pipelines

Automate linting, type checks, and tests via `.github/workflows/ci.yml` so every PR is validated before merging.

### 5. Bloated Monolithic Functions

Break functions exceeding 30 lines or 3 parameters into modular, single-purpose routines.

### 6. Missing System Architecture Diagrams

Document system components and data flows in `docs/architecture_diagram.md` using Mermaid syntax.

### 7. Incomplete README Documentation

Ensure `README.md` includes clear problem statements, architecture summaries, and exact onboarding runbooks.

### 8. Missing Evaluation Evidence

Record quantitative evaluation benchmarks and reproducibility scripts in `eval/`.

### 9. Monolithic Single-File Architectures

Deconstruct applications into dedicated layers: `agents/`, `api/`, `services/`, and `models/`.

### 10. Absent Type Hints

Enforce comprehensive type annotations across all function signatures to maintain code reliability.
