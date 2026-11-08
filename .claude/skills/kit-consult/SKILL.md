---
name: kit-consult
description: Use when needing guidance on architecture, design patterns, UI/UX systems, test strategies, CI, or resolving findings in project-review.md. Proactively fetches Project-Builder-4-Agents by intent rather than guessing conventions.
---

# Project-Builder-4-Agents Consultation

1. Read `.builder/kit.json` to identify kit remote coordinates (`kit_repo`, `kit_ref`) and the active profile.
2. Fetch `INDEX.md` from the remote kit (raw URL: `https://raw.githubusercontent.com/<owner>/<repo>/<kit_ref>/INDEX.md`).
3. Match entries where "When to use" matches the current task (max 2–3 docs). Prioritize docs from the active architecture profile.
4. Read matching docs, apply architectural constraints, and record significant architectural decisions in `adrs/`.
5. Never clone the entire kit repository. Do not apply conventions from conflicting profiles without an explicit ADR.
