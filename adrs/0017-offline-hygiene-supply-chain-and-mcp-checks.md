# ADR 0017: OFFLINE HYGIENE, SUPPLY-CHAIN AND MCP CHECKS IN HEALTH CHECK

* **Status**: Accepted
* **Date**: 2026-11-07
* **Builds on**: [ADR-0012](0012-agent-first-builder-and-health-check.md), [ADR-0016](0016-work-log-standard-and-health-check.md)

---

## 1. Context

* A 2026-11-07 review found Health Check scans text files for prompt injection (`SAFE-`) and source for hardcoded secrets, but does not look at committed secrets/logs/binaries, install-time scripts, unpinned dependencies, MCP package names, or leftover spec markers.
* Constraints: Python standard library only, no network, no model calls, no changes to the score.

## 2. Decision

Add `scripts/auditor_engine/hygiene.py` (pure logic) emitting findings only, each with a remediation doc: `SEC-005`, `HYG-002`, `SUP-001..004`, `AGT-004`, `AGT-005`, `SPEC-001` (table in `scripts/README.md`).

* Files committed to git are listed with `git ls-files`. Without git or a `.git` directory these checks are skipped rather than guessed from `.gitignore`.
* Findings contain codes, counts and sanitized file names, never file contents.
* The MCP known-bad table is hardcoded from facts verified against npm/GitHub on 2026-11-07 and must be refreshed by hand.

## 3. Consequences

* Not covered, by design: CVE lookup (needs network), typosquat detection (needs a package list), malware scanning, and anything inside `node_modules` (pruned).
* Measured on two repositories only: a private project reported 30 tracked `.log` files; the kit reports its own committed `.exe` (`SUP-004`, planned for removal under TASKS A3). False-positive rate on a wider set is unmeasured.
* `SUP-004` and `HYG-002` may flag intentional files; the message says what to verify, not that the file is malicious.
