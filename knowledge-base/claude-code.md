# Using Claude Code Effectively — Notes from Phan Minh Tam & Bui Viet Hoang

Source: `claude-code-g19.html` (27 slides). Key takeaways applicable to any AI coding agent.

## 5 Core Principles
1. Context is a budget, not a buffer. Spend tokens only on items directly relevant to the current task.
2. Proactively steer after every turn: Continue · Rewind · Clear · Compact · Subagent.
3. Decouple lifecycle phases: Explore → Plan → Implement → Verify, always bounded by deterministic pass/fail signals.
4. Keep `CLAUDE.md` as lean as possible. If deleting a rule does not cause regressions, delete it.
5. Large tasks require spec-first alignment in repository files before execution. Good specs make `/clear` cheap.

## Context Management
- **Context Rot:** As context fills up, attention dilutes. Responses remain superficially confident but drift away from intent without warnings. Mentor heuristic: keep active conversations within ~1/3 of the context window. Monitor with `/context`.
- **Worth keeping:** Target files, architectural constraints, settled decisions, verification evidence.
- **Noise to discard:** Failed debug loops, outdated exploratory branches, verbose one-off tool outputs, unrelated tasks.

## Choosing Actions After Each Turn (In Priority Order)
- Next task does not depend on prior conversational context → **Clear**.
- Agent took a wrong turn → **Rewind** (`Esc Esc` or `/rewind`). Retains file discovery while stripping dead-end branches. Before rewinding, ask the agent for a 3-line diagnostic of why it failed. (Checkpoints do not track external bash modifications; git remains authoritative).
- Only need a final verdict/summary → **Subagent** (isolated context, "cleanroom"): trace execution flows, review diffs against spec, draft docs, investigate edge cases.
- Conversation history is long but mostly needed → **Compact** early with explicit instructions on what to keep and drop. If writing a fresh brief takes < 2 minutes, choose **Clear** instead.
- Otherwise → **Continue**.
- **Two-strike rule:** If correcting an agent twice on the same mistake fails → **Clear** context and rewrite the prompt.
- **Specialized sessions:** Separate implementation, review, and investigation into independent sessions. Reviewers in clean contexts catch subtleties much more reliably.

## Working Protocol
- Skip planning only when the diff can be summarized in a single sentence. If touching multiple files, implicit dependencies, or unfamiliar modules → mandate a Plan.
- Always provide automated self-verification: unit test, build command, linter, test script, or visual comparison. Require proof rather than asking "are you done?".
- Prompt specifics: target files/directories · hard constraints · existing patterns to mirror · observable symptoms.
- `CLAUDE.md`: reserve for custom build/test commands, repo-specific code style deviations, branch/PR conventions, and core architectural invariants. Avoid verbose explanations, generic advice, external API documentation, or volatile status info.
- **Spec-first:** Let the agent interview you → generate `SPEC.md` → launch a fresh session for implementation. Spec tools like GitHub Spec Kit (`specify` → `clarify` → `plan` → `tasks` → `analyze` → `implement`) are optional structures. Specs never replace verification.

## 5 Failure Patterns
Kitchen sink sessions · Endless circular patching · Bloated CLAUDE.md · Unverified trust ("hallucinated completion") · Unbounded exploratory rabbit holes.
