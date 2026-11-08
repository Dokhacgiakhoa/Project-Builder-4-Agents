# ADR-0021: Safety Scan Pre-Gating, Unicode Normalization, and Context-Aware Directive Matching

- Status: Accepted (2026-11-07)
- Builds on: ADR-0017 (Offline Hygiene and Supply Chain Checks)

## Context
Full-text prompt injection scanning (`safety.py`) previously executed a suite of heavyweight regex patterns over every line of every scanned file. On medium-to-large repositories (e.g., P-062 with 5,470 files, LiteLLM with 15,227 files), this caused extreme scan latencies (P-062 taking ~28.9s, LiteLLM taking ~69.0s).
Simultaneously, adversarial prompt evasion techniques (such as Turkish dotless/dotted `İ`/`ı` case mappings, decomposed Unicode accents NFD vs NFC, and CSS-hidden containers) revealed detection gaps.

## Decision
We introduce a three-tiered optimization and hardening strategy for prompt injection detection:

1. **Literal Fast Pre-Gating (`_DIRECTIVE_GATE_LITERALS`)**:
   - Every complex regex pattern is guarded by a fast sub-string containment check (`any(lit in line_lower for lit in _DIRECTIVE_GATE_LITERALS)`).
   - *Soundness Verification*: The pre-gate literals are strictly verified by `_DIRECTIVE_GATE_PATTERN_COUNT` and automated differential equivalence checks against baseline corpora (`evals/results/raw/009-equivalence.json`). Lines that do not contain core directive anchor words bypass full regex compilation entirely.
2. **Unicode & Case Folding Normalization**:
   - Explicit handling for Turkish dotted capital `İ` (`\u0130` $\rightarrow$ `i`) and dotless `ı` before case folding.
   - NFC normalization (`unicodedata.normalize('NFC', line)`) applied to all non-ASCII lines, preventing NFD decomposition evasion (e.g., Vietnamese "bỏ qua" composed vs decomposed).
3. **Context-Aware Rules (`SAFE-002`, `SAFE-003`)**:
   - `SAFE-002` evaluates file context: directive phrases embedded inside markdown quotes, code blocks, or test assertion strings are evaluated contextually, reducing false alarms on security research documents.
   - `SAFE-003` specifically targets hidden directive payloads (zero-font, CSS `display:none`, HTML comments `<!-- ... -->`, or invisible elements). Plain text without a target noun that would otherwise be benign in visible prose is flagged as `SAFE-003` when concealed within hidden markup.
4. **Measured Empirical Speedups**:
   - P-062 mean scan time decreased from **28.9s $\rightarrow$ 5.9s (4.88x speedup)** (`evals/results/raw/010-ab-benchmark.json`).
   - LiteLLM mean scan time decreased from **69.0s $\rightarrow$ 35.4s (~2.0x speedup)** (`evals/results/raw/010-ab-benchmark.json`).
   - Finding identity across 23 repositories remained **100% invariant** (`evals/results/raw/011-nonsafe-identity.txt`).

## Consequences
- Significant reduction in CPU time spent in regex execution across all project archetypes.
- Hardened resilience against Unicode normalization bypasses.
- Semantic limitation: context-aware evaluation relies on static heuristics; adversarial nested obfuscation (e.g., base64 or rot13 encoded within markdown) requires dedicated decoding layers.

## What is Not Covered
- Runtime evaluation of dynamically loaded prompt templates in client applications.
- Multi-token obfuscation across line breaks (pre-gating operates on a line-by-line basis).
