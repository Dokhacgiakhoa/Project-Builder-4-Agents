# Phương pháp xây dựng sản phẩm AI — ghi ý từ slide mentor

> Nguồn: 3 slide buổi duty của mentor G19 (gốc ở `cohort-4/mentor-g19/raw/`). Đây là phần **phương pháp dùng lại được**. Lịch, mốc và chỉ dẫn riêng cho đội ở `cohort-4/mentor-g19/lich-mentor.md`.
> Mentor là nguồn tham khảo, trọng số cao ở mảng kỹ thuật.

## 1. Kỹ sư AI & quy trình sản phẩm
- 3 trụ: Backend (gateway, service, queue, DB, cache) · AI (LLM, RAG, agent, finetune, eval) · Ops (K8s, CI/CD, GPU, serving, monitoring). AI = hệ thống (LLM + planning + tool + memory + RAG), không chỉ model.
- Ops: DevOps (hệ thống sống) · MLOps (model sống) · LLMOps (gateway, prompt versioning, tracing, eval production).
- Scrum: PO (cái gì) · Scrum Master (quy trình) · Dev team (cách làm). Sau coding agent: team nhỏ lại, engineer chuyển sang review + điều phối, QA dồn về engineer, giá trị dịch lên requirement và design.
- SDLC là vòng lặp mỗi sprint: Problem → Plan → Design → Dev + AI → Review → Test → Deploy → Monitor. Requirement đổi giữa sprint là bình thường. Tech design 1–2 trang. Hotfix đi tắt phải có postmortem.
- Môi trường Dev → Test → Staging (UAT) → Production, càng lên cao quyền deploy càng chặt.

## 2. Từ ý tưởng đến yêu cầu (PO)
- Bắt đầu từ user và nỗi đau. 5 câu: ai là user · đau ở đâu (đo được) · đang xử lý thế nào · tốt hơn bao nhiêu · có đáng làm trước (impact × effort).
- **Persona** = nhóm user + bối cảnh + hành vi/tool hiện tại + mục tiêu + trình độ công nghệ + các vai xung quanh. MVP chọn 1 primary persona. Phỏng vấn 3–5 user thật.
- **Pain point** = [Actor] khi làm [task] phải [quy trình] → gặp [failure] → tốn [cost × frequency] + evidence + root cause. Hợp lệ khi tái hiện được, có số, có root cause, tần suất đủ, evidence thật.
- **Input là requirement**, xét 6 chiều: format · kích thước · ngôn ngữ · chất lượng · khối lượng · nguồn. PO ghi thực tế → TL xác nhận khả thi → chốt thành AC. Xin file mẫu thật.
- **Mini-PRD** (what & why, không có how): problem · goals SMART · non-goals · persona · user story + AC · non-functional · scope MoSCoW (Must = MVP) · open questions có owner + deadline.
- PRD done: complete · unambiguous · measurable · testable · feasible · prioritized · aligned. Kiểm bằng explain-back test và test-case test. Red flags: tính từ không số, có giải pháp kỹ thuật, thiếu non-goals.
- Cắt scope theo độ sâu, không cắt bước: 3–5 feature Must, mỗi feature 4–6 AC, có unhappy path. Capacity: feature × estimate ≤ sức team × ngày còn lại.
- User story "Là…, tôi muốn…, để…" · AC Given/When/Then · INVEST · story > 3–4 ngày thì tách (SPIDR) · truy vết 2 chiều · CRUD check · 3 Amigos.

## 3. Thiết kế (Tech Lead)
- Design trước khi code. 5 câu: đặc tính task · component nào, vì sao (kèm phương án đã loại) · contract giữa module · fail thì sao · timeline có kịp.
- Tech Design Doc 1–2 trang: context · diagram · lựa chọn component · interface · data model · đặc tính task · risks · open questions. Chưa được review = chưa design.
- Diagram: mỗi box 1 trách nhiệm, mũi tên có nhãn (protocol + data), phân biệt sync/async, vẽ rõ boundary.
- Chọn component: đúng đặc tính task (việc lâu → queue + worker; việc cần nhanh → cache, streaming) · thứ team đã biết · managed/API trước · mỗi component thêm = thêm thứ phải vận hành.
- Phân tích top-down: capability chung → component (phục vụ ≥ 2 feature) → verify bằng ma trận feature × component.
- Tránh over-engineering (microservices, Kafka, self-host LLM, multi-agent khi chưa cần). Leo thang prompt → RAG → finetune. YAGNI.
- Contract-first: `/v1`, format lỗi thống nhất, backward compatible, OpenAPI. FE mock từ spec, BE làm thật song song. Spec là prompt tốt nhất cho coding agent.
- Architecture review 5 câu: cover đủ PRD · đúng đặc tính task · có SPOF không · contract đủ rõ · effort khớp capacity. Sau khi chốt thì **design freeze**: muốn đổi phải có lý do + ảnh hưởng + chi phí.
- Feature depth: "follow the data", mỗi lần data đổi trạng thái là 1 tầng kỹ thuật. Hỏi: sync hay bg · fail thì sao · user thấy gì khi chờ · làm lại thì sao (idempotency).
- Pattern: Singleton, Factory, Repository, Hexagonal · AI: Adapter (đa LLM), Strategy (routing), Orchestrator–Worker, Circuit Breaker.

## 4. Chia việc
- 1 story = 1 role + 1 hành động + 1 kết quả quan sát được. Bước user không thấy là task, không phải story. 3 phép thử: viết được AC · demo được · subtask ≤ 1 ngày (không được thì spike 1 ngày).
- Task chia theo việc, không theo role. 2 task hay quên: **chốt contract** (đầu story) · **ghép + test tích hợp** (cuối story).
- DoD 3 cấp (không có "done 90%"): task (code + test pass, PR merge, không TODO tạm) · story (mọi AC pass thật, demo trên môi trường chung) · feature (mọi story Must done, eval đạt ngưỡng, người khác tự bấm thử được).
- Board là nguồn sự thật: 1 issue = 1 story · label = feature + MoSCoW · PR "Closes #n" · card đứng > 2 ngày thì daily phải hỏi.
- Daily 4 câu: đang làm · đã xong · vướng gì · root cause. Ownership: chủ động hỏi trước, backward planning từ ngày deploy.

## 5. Setup & build loop
- Repo khớp diagram. `.env.example` commit, key thật không commit. `docker compose up` dựng cả stack. CI lint + test mọi PR, đỏ không merge. README = runbook chạy trong 15 phút.
- DevOps: infra → component (HA) → runtime → pipeline. Dockerfile multi-stage làm template, image không chứa secret. `restart: always` + healthcheck. Nghiệm thu: tắt container bất kỳ, hệ tự dậy.
- CI/CD: merge → lint + test → build image tag = git sha → auto deploy dev → smoke `/health`. Không deploy tay.
- **Walking skeleton** sớm: 1 màn hình → 1 endpoint → 1 lượt agent → 1 dòng DB, chạy trên môi trường chung. Quá lâu không xong → cắt Must. Xong quá sớm → chọn 1 hướng khoan sâu.
- Nhịp task với coding agent: người viết interface + test → agent implement → người review + chạy test → PR nhỏ.
- Luật PR: < 400 dòng · 1 PR = 1 task · review trong ngày · CI đỏ không merge · mô tả có "Closes #n" + cách test. Review = chạy thử, hỏi "case nào làm code này gãy?". Người approve chịu trách nhiệm ngang người viết.
- Mock để song song: FE mock từ contract · mock LLM trong test (happy/refusal/timeout) · seed data chung có case xấu.

## 6. Test, eval, vận hành
- Mọi module mock được. Kịch bản: happy · edge · error · concurrent · security. Unit (nhiều nhất) → integration → manual E2E (người là chốt chặn cuối).
- Eval AI: output LLM · RAG (precision/recall, groundedness) · agent (task success, tool call đúng) · safety (injection). Golden set → chạy full pipeline → chấm auto + judge + người → regression mỗi lần đổi prompt/model.
- Ops: ≥ 2 replica, healthcheck, rollback bằng image tag, logs + traces + metrics, LLM observability (Langfuse/LangSmith).
