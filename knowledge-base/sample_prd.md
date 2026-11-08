# Sample PRD — Knowledge Retrieval Assistant for Accounting Teams

**Version:** 0.2 · **Status:** Draft for user validation · **Primary Persona:** Enterprise Accountant

> The product assists accountants in finding and cross-referencing information within enterprise-approved documents. It supports discovery and citation, not operational approval or formal tax advisory.

## 1. Problem Statement

When auditing an expense, invoice, or bookkeeping treatment, accountants must manually search across fragmented sources: internal financial regulations, payment procedures, accounting guidelines, laws, decrees, circulars, and official letters. Documents are dispersed, lengthy, multi-versioned, and phrase concepts differently, making search slow, risking reliance on obsolete regulations, or yielding unsubstantiated answers.

**Baseline Hypothesis to Validate:** Each accountant executes 5–10 lookups/week, spending 15–30 minutes/lookup; during closing periods or tax declarations, frequency and error risks escalate. Prior to PRD sign-off, interview 3–5 accountants, observe ≥ 5 live retrieval sessions, and collect 5–10 representative sample files.

### Prioritized Pain Points

| Pain Point | Current Workflow → Failure | Impact | Root Cause |
|---|---|---|---|
| Revenue/Expense Regulation Lookups | Open policy PDFs, templates, and ask seniors → slow, conflicting answers | Delays payment approvals; risk of missing documentation or exceeding authority | Dispersed docs, keyword search, lack of single approved source |
| Applying Tax Policies | Search laws/decrees/circulars across multiple portals → hard to verify validity dates | Risk of incorrect tax declarations or non-deductible expense treatments | Frequent legal revisions, cross-references, missing version history |
| Document Cross-Checking & Bookkeeping | Match invoices/vouchers with internal accounting policies → easy to miss conditions | Time lost in reviews; repeated back-and-forth revisions | Rules scattered across chapters, tables, and annexes |
| Audit Handover & Inquiries | Retrieve justification for auditors, executives, or onboarded staff → depends on individual memory | Time wasted, knowledge lost when staff departs | Knowledge trapped in employee heads and fragmented folders |

## 2. Goals & Metrics

During a 4-week pilot with 5 accountants and a benchmark query suite approved by the Chief Accountant:

- Reduce median retrieval time to verified answers to **≤ 3 minutes/session** (at least a **70% reduction vs. week 1 baseline**).
- At least **90% answer acceptance rate** by the Chief Accountant with zero critical errors across the 30 benchmark queries.
- **100% of affirmative operational statements** cite exact document title, version, and location.
- **100% of queries with insufficient grounds or out of scope** clearly declare lack of information without hallucinating.

## 3. Persona

**Primary — Enterprise Accountant:** Works on laptop; utilizes accounting software, Excel, email, and shared drive storage; performs lookups under tight closing and payment deadlines; deep domain understanding but varying technical/AI literacy. Primary goal is fast, verifiable citations before executing transactions.

**Peripheral Roles:** Chief Accountant (approves knowledge sources and answers to sensitive queries); Knowledge Admin (manages document uploads and RBAC permissions).

## 4. Input

| Dimension | MVP Scope |
|---|---|
| File Types | Searchable text PDF and DOCX: financial regulations, payment protocols, accounting manuals, legal circulars |
| Size Limits | ≤ 50 MB/file, ≤ 200 pages/file, max 20 files per batch |
| Language | English and Vietnamese; allows financial tables and industry terms |
| Document Quality | Machine-readable text with titles/versioning; scanned images and handwriting are out of scope for MVP |
| Pilot Volume | ≤ 1,000 documents, 5 pilot users |
| Sources | Only documents uploaded by Knowledge Admin and marked **Approved** by Chief Accountant; metadata: title, category, reference number, effective/expiry dates, version, department, access level |

## 5. Scope & Priority

| Priority | Feature | Business Value |
|---|---|---|
| **Must** | Approved Document Repository Management | Single source of truth with explicit versioning and validity states |
| **Must** | Q&A with Strict Grounded Citations | Answers directly linked to verifiable source passages |
| **Must** | Role-Based Access Control (2 roles) | Restricts access to sensitive departmental documents |
| **Should** | Structured Document Summarization | Rapid synthesis of scope, key mandates, obligations, and deadlines |
| **Could** | Side-by-side Version Comparison | Highlights revisions between legal or internal policy versions |
| **Won't** | Automated ledger booking, payment approvals, tax filing, direct bank integration, legal advice, OCR scans | Keeps MVP focused strictly on safe, verifiable knowledge retrieval |

## 6. Features & Acceptance Criteria

### F1 — Approved Document Repository Management (Must)
**Addressed Pain Point:** Dispersed documentation, lack of canonical versioning, unclear validity status.

**User Stories**
1. As a Knowledge Admin, I want to upload files with structured metadata so the repository is well-organized.
2. As a Chief Accountant, I want to approve documents so only vetted policies are used for generation.
3. As an Accountant, I want visibility into validity dates and revisions to avoid applying outdated policies.

**AC**
- Given an in-scope file, when uploaded, then the system displays processing status and requires mandatory metadata.
- Documents are only queried after status transitions to **Approved**.
- Superseded versions remain auditable but clearly flagged as expired/replaced.
- Corrupted files, missing metadata, or size breaches are rejected with clear diagnostic reasons.

### F2 — Grounded Q&A with Source Citations (Must)
**Addressed Pain Point:** Slow regulation lookups; hallucinated or conflicting answers.

**User Stories**
1. As an Accountant, I want to ask questions in natural language to avoid manual search across dozens of files.
2. As an Accountant, I want 1-click links to exact source passages to verify accuracy before applying rules.
3. As an Accountant, I want the system to decline answering when evidence is lacking to prevent compliance errors.

**AC**
- Answers are synthesized strictly from **Approved** documents the user has permission to read.
- Every operational statement includes document title, version, and page/section number; users can open the exact highlighted passage.
- **Definition of "Sufficient Grounds":** Each conclusion must tie directly to at least one verbatim excerpt from an Approved document. Speculative synthesis combining disconnected fragments is classified as **Insufficient Grounds**.
- When queries are out of scope or lack evidence, the system replies "Insufficient evidence in approved documents" and specifies what information is missing.
- When sources conflict, the system surfaces the discrepancy and requests Chief Accountant review rather than picking one arbitrarily.
- Zero fabricated citations; 100% valid citation rate on the 30 benchmark queries.
- p95 response latency ≤ 10s during pilot (excluding initial document indexing time).

### F3 — Access Control & Audit Trails (Must)
**Addressed Pain Point:** Sensitive financial documents in shared folders; lack of access accountability.

**User Stories**
1. As an Accountant, I only want access to documents permitted for my role to avoid compliance breaches.
2. As a Knowledge Admin, I want to assign role-based permissions to govern repository access.
3. As a Chief Accountant, I want audit logs to trace who uploaded, approved, or queried documents.

**AC**
- Accountants can only query/view authorized documents; Knowledge Admins manage repository assets.
- Unauthorized users cannot view restricted document titles, excerpts, or presence in search results.
- All uploads, status mutations, queries, and citation view events are logged with user ID and timestamp.

### F4 — Structured Document Summarization (Should)
**Addressed Pain Point:** Long legal and policy texts take hours to parse for operational impact.

**User Stories**
1. As an Accountant, I want structured summaries to quickly grasp document scope and mandates.
2. As an Accountant, I want key obligations, conditions, and deadlines highlighted.
3. As an Accountant, I want each point linked to source paragraphs.

**AC**
- Output structure: Scope of Application, Core Directives, Mandatory Obligations/Deadlines, Related Documents, Points Requiring Clarification.
- Every section includes citations; absent points are explicitly marked "Not Mentioned".

## 7. Non-Functional Requirements
- **Security:** User authentication, RBAC enforced on search and citations; no internal enterprise data used for third-party model training without explicit consent.
- **Reliability:** Refuse answering when context is insufficient; immutable version history and audit trails. **All affirmative outputs include a mandatory disclaimer: "Subject to verification by authorized personnel before operational application."**
- **Performance:** p95 query latency ≤ 10 seconds within pilot workload scope.
- **AI Evaluation:** 30 benchmark queries (12 happy path, 6 missing sources, 6 conflicting sources, 6 out-of-scope); Chief Accountant grades correctness and groundedness.
- **Usability:** Upload and processing errors must surface actionable diagnostic messages.

## 8. Definition of Done
MVP is done when 5 pilot accountants complete the end-to-end journey: **Sign in → Ask question → Read grounded response → Inspect source citation → Confirm/reject answer**, all **Must features (F1–F3) satisfy feature-level ACs in Section 6**, and metrics in Section 2 pass across the 30 benchmark queries.

## 9. Open Questions
| Question | Owner | Deadline |
|---|---|---|
| Empirical baseline: lookup count, duration, and top errors? | PO | Prior to Sprint 1 |
| 5–10 initial sample files and metadata templates? | Chief Accountant | Prior to F1 grooming |
| Approval authority for document types & conflict resolution policy? | Chief Accountant | Prior to F2 grooming |
| Threshold defining "critical error" in eval suite? | PO + Chief Accountant | Prior to Sprint 1 |
| Benchmark ground-truth answers for 30 eval queries? | Chief Accountant | Prior to UAT |

## 10. Sign-off
| Role | Verification Scope | Assignee | Date | Status |
|---|---|---|---|---|
| PO | Business requirements, MoSCoW priorities, KPI targets | — | — | ☐ Pending Sign-off |
| Tech Lead | Technical feasibility within team capacity (p95 ≤ 10s on ≤ 1,000 docs) | — | — | ☐ Pending Sign-off |
| Chief Accountant | Domain correctness, 30 eval questions, definition of sufficient grounds | — | — | ☐ Pending Sign-off |
