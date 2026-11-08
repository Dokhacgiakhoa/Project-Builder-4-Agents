# ADR 0014: ENGLISH AS PRIMARY LANGUAGE FOR TOKEN EFFICIENCY AND LLM NATIVE REASONING

* **Status**: Accepted
* **Date**: 2026-11-06
* **Builds on**: [ADR-0012](0012-agent-first-builder-and-health-check.md), [ADR-0013](0013-remote-knowledge-hub-and-zero-clone-bootstrap.md)

---

## 1. Context

* `Project-Builder-4-Agents` is exclusively designed for **AI coding agents** (Claude Code, Antigravity, Cursor, Windsurf, Codex) executing tasks for vibe coders.
* In modern LLM tokenizers (BPE / Byte-Pair Encoding used by OpenAI GPT, Claude, Gemini, Llama):
  1. Vietnamese and other languages with heavy diacritics and composite characters split each word/syllable into 2 to 4 tokens (rough illustration only, not measured: `khởi tạo dự án` ~ 8-10 tokens vs. `bootstrap project` ~ 2 tokens).
  2. English achieves an optimal density of ~1.3 tokens per word.
* Consequently, keeping system prompts, agent constitutions (`AGENTS.md`), decision docs, and curated skills in Vietnamese increases token consumption by **40% to 60%**, accelerating context window exhaustion and increasing API costs.
* Furthermore, LLMs possess native, highly-aligned reasoning capabilities in English, resulting in higher adherence to architectural constraints, zero ambiguity, and fewer hallucinations.
* Crucially, modern LLMs can effortlessly translate concepts into the vibe coder's native language (Vietnamese, Japanese, Spanish, etc.) during interactive dialogue without requiring the foundational knowledge hub to be written in that language.

---

## 2. Decision

1. **English as the Sole Primary Language for Agent Artifacts**:
   * All core architecture docs, decision profiles, playbooks, skill specifications (`SKILL.md`), MCP templates, and agent constitutions (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`) MUST be written in concise, technical English.
   * Internal instructions and system boundaries are written in English to maximize token efficiency and semantic fidelity.
2. **Dynamic Localization for Human Interaction**:
   * In `BOOTSTRAP.md` and `AGENTS.md` section 4 ("User Communication"), agents are instructed to **always converse with the human vibe coder in the user's preferred language** (defaulting to Vietnamese if prompted in Vietnamese).
   * The Agent acts as the bridge: internalizing the compact English operating system and communicating with the human in their native tongue.
3. **No Mixed-Language Bloat**:
   * Knowledge files and skills avoid bilingual repetition (e.g. repeating full paragraphs in both languages within the same file) to preserve token budget.

---

## 3. Consequences

> **Measurement note (2026-11-07)**: counted with a real Claude tokenizer (`claude -p`, differential) on 9 near-parallel docs (Vietnamese at 58e5df8 vs English now): English used 8,727 tokens vs 9,691 for Vietnamese, about **10% fewer** (per file 2-21% fewer). The 40-60% figure below is **contradicted** for this kit's markdown-heavy docs. Caveat: pairs are near-parallel, not exact translations, and the sample is small. Language choice may still matter for instruction-following, which was not measured.

* **Positive**:
  - Reduction in token consumption for equivalent text: about 10% measured on this kit's docs (the original 40-60% estimate was not supported).
  - Possible improvement in instruction-following across agent runtimes (hypothesis; no evaluation has been run, and Codex is unverified).
  - Broader readability for agents and international contributors.
  - Vibe coders converse with their agent in their own language (depends on the agent following AGENTS.md Section 4).
* **Trade-offs / Constraints**:
  - The repo maintainer and contributor documentation must maintain technical English fluency.
  - Existing Vietnamese documentation files in `core/` and `profiles/` will be systematically migrated to English while preserving intent routing in `INDEX.md`.
