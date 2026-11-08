---
id: O-001
type: reference
when: "Authoring user and operational documentation via Diátaxis framework and incident runbooks"
---
# ADR 0010: DOCUMENTATION FRAMEWORK (DIÁTAXIS) AND PITCH DECK STANDARDS

* **Status**: Approved (Accepted)
* **Decision date**: 2026-11-04
* **Decided by**: Principal Architect & Documentation Lead

---

## 1. CONTEXT

In most technology projects, the following two components are often neglected or done in a patchwork way:
1. **Pitch Deck (Presenting & Defending the project)**: Engineering teams usually focus only on code and lack a standard business and presentation package (Problem, TAM/SAM/SOM, Unit Economics, GTM), which makes fundraising, hackathons or defending in front of leadership very hard.
2. **Documentation system (Documentation)**: Project documents are often written messily, mixing guidance for newcomers (Tutorials), solutions to specific problems (How-To), technical specifications (Reference) and architecture philosophy (Explanation), so the documents quickly go stale (Stale documentation) and cannot be applied in practice.

---

## 2. DECISION

We decided to fully standardize these two components in `Project-Builder-4-Agents`:

1. **Standardize the Pitch Deck after Y Combinator & Sequoia Capital**:
   - Stored at `templates/pitch-deck/pitch-deck-template.md`.
   - Supports the **Slides-as-Code** format through Marp (`templates/pitch-deck/marp-presentation.md`) so the team can manage slides with Git and export PDF/HTML automatically.
   - Provides 3-minute / 5-minute presentation scripts and a handbook for answering the investors'/judges' **20 tough challenge questions** (`templates/pitch-deck/pitch-scripts-and-qa-guide.md`).
   - Provides the **AI Pitch Generator Prompts** (`templates/pitch-deck/ai-pitch-generator-prompts.md`) so an AI Agent can analyze the codebase and fill in the slide content automatically.

2. **Apply the Diátaxis Documentation Framework**:
   - All technical guidance documents are structured in the 4 quadrants of Diátaxis (`profiles/documentation/guides/diataxis-framework-guide.md`):
     - **Tutorials**: a 10-15 minute start for newcomers.
     - **How-To Guides**: solve a specific real situation.
     - **Reference**: look up technical specifications and API contracts.
     - **Explanation**: explain the architecture and the ADR decisions.
   - Ready-made:
     - `profiles/documentation/guides/developer-onboarding-guide.md`: guides a new engineer to a first commit in 30 minutes.
     - `profiles/documentation/guides/user-guide-template.md`: an end-user guide template with no technical jargon.
     - `profiles/documentation/guides/incident-runbook-template.md`: an on-call handbook and the P1/P2 incident response process at 2 a.m.

---

## 3. CONSEQUENCES

* **Pros**:
  - Raises the project's success rate from convincing the board (Pitching) to real operation (Production Operations).
  - Cuts new-developer onboarding time from days to under 30 minutes.
  - Production incidents are handled by a precise standard process, minimizing system downtime (MTTR).
* **Cons**:
  - Requires team members to keep the discipline of updating documents and slides when the product changes significantly.
* **System Impact**:
  - Does not affect the performance or runtime of the application source code.
