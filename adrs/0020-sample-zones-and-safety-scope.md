# ADR-0020: Sample Zones Segmentation and Safety Scan Scope

- Status: Accepted (2026-11-07)
- Builds on: ADR-0018 (Project Analysis and Knowledge Pack)

## Context
In early versions of the Health Check engine, file tree indexing applied a single monolithic ignore list across all audit subsystems. This caused two opposing failure modes:
1. **Sample pollution in architectural scoring**: Test fixtures, documentation starters, and template examples (e.g., `examples/`, `profiles/*/starter/`, `templates/`) polluted AST analysis and pillar scoring. For instance, scanning this kit repository falsely activated the Frontend pillar (20/20) and misclassified the architecture due to sample `.csproj` and React starter templates.
2. **Safety scanning blind spots**: Overzealous exclusion of directories (such as `fixtures/`, `evals/`, `samples/`) completely bypassed security analysis (`scan_safety`), allowing prompt injection payloads and untrusted directives hidden inside mock data or sample trees to escape detection.

## Decision
We decouple general architectural indexing from security scanning by establishing distinct directory boundary scopes:

1. **Architectural Indexing Exclusion**: Sample and template directories (`examples`, `templates`, `starter`, `samples`, `fixtures`, etc.) are ignored by `tree.py` for AST parsing, archetype detection, pillar evaluation, and anti-crash rule analysis.
2. **Dedicated Safety Scan Scope (`SAFETY_IGNORE_DIRS`)**: `safety.py` uses its own strict ignore set containing exactly 22 names (e.g., `.git`, `node_modules`, `venv`, `__pycache__`, `.pytest_cache`). Crucially, sample directories, documentation folders, and mock suites remain **fully scanned** for prompt injections and malicious directives.
3. **Git Hygiene Verification**: Cleanliness checks (`git_hygiene.py`) independently inspect uncommitted state and untracked artifacts across the entire repository boundary regardless of sample tags.

## Consequences
- **Kit self-audit score**: This kit repository (`Project-Builder-4-Agents`) accurately reflects its core tooling identity, scoring **90/100 (Grade A)** without false Frontend/Fullstack pillar inflations.
- **Corpus archetype impact**: Known projects with extensive mock fixtures (e.g., `flask` with tutorial apps, `cline` with extension fixtures) are no longer misled by sample code stacks.
- **Architectural gap exposed**: Standalone libraries and multi-language agent hubs currently map into generic archetypes due to the absence of a dedicated "Library/Framework" archetype model.

## What is Not Covered
- Fine-grained semantic tagging for user-defined multi-project monorepos (e.g., Nx/Lerna workspaces).
- A specialized "Library/Framework" archetype classification in `analysis.py` (remains an open roadmap item).
