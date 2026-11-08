"""Pillar tài liệu, onboarding và hệ sinh thái AI Agent."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .models import CriterionItem


class DocsPillarsMixin:
    """Pillar tài liệu, onboarding và hệ sinh thái AI Agent."""

    def audit_readme_and_onboarding(self):
        score = 0
        found = []
        missing = []
        readme_file = None

        for name in ['README.md', 'readme.md', 'README.MD', 'README']:
            matches = self.tree.find_by_name(name)
            if matches:
                readme_file = matches[0]
                break

        if readme_file and readme_file.exists():
            score += 25
            try:
                content = readme_file.read_text(encoding='utf-8', errors='ignore')
                lines_count = len(content.splitlines())
                file_size_kb = len(content.encode('utf-8')) / 1024
                self.add_log(f"  -> Found {readme_file.name} ({lines_count} lines).", "readme", "muted")

                found.append(CriterionItem(
                    "Tệp README.md chuẩn xác tại thư mục gốc",
                    evidence=f"{readme_file.name} ({lines_count} dòng, {file_size_kb:.1f} KB)",
                    details=f"Đã phát hiện tệp tài liệu khởi đầu chính của dự án tại `{readme_file.name}` với {lines_count} dòng nội dung.",
                    badge=f"{lines_count} dòng"
                ))

                # Tiêu đề & Bài toán (Product Vision)
                title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                if title_match and lines_count >= 15:
                    score += 20
                    title_str = title_match.group(1).strip()
                    found.append(CriterionItem(
                        "Mô tả bài toán, mục tiêu và định vị giá trị sản phẩm rõ ràng",
                        evidence=f"{readme_file.name}:L1",
                        snippet=f"# {title_str[:80]}",
                        details=f"Phát hiện tiêu đề và định vị sản phẩm: '{title_str}' cùng phần mô tả mục tiêu bài toán nghiệp vụ.",
                        badge="Product Vision"
                    ))
                else:
                    missing.append(CriterionItem(
                        "Đoạn giới thiệu mục tiêu bài toán và giá trị sản phẩm (PRODUCT VISION)",
                        evidence=readme_file.name,
                        details="Tệp README thiếu tiêu đề cấp cao nhất (# Heading) hoặc quá ngắn (< 15 dòng) để mô tả bài toán và giá trị sản phẩm.",
                        remediation="Bổ sung mục giới thiệu: # Tên dự án, vấn đề giải quyết, đối tượng người dùng và giá trị cốt lõi."
                    ))

                # Hướng dẫn khởi chạy (Quick Start)
                in_block = False
                current_block = []
                current_lang = ''
                code_blocks = []
                for line in content.replace('\r\n', '\n').splitlines():
                    stripped = line.strip()
                    if stripped.startswith('```'):
                        if in_block:
                            code_blocks.append((current_lang, '\n'.join(current_block)))
                            in_block = False
                            current_block = []
                            current_lang = ''
                        else:
                            in_block = True
                            current_lang = stripped[3:].strip().lower()
                            current_block = []
                    elif in_block:
                        current_block.append(line)

                found_quickstart_cmd = None
                for lang, body in code_blocks:
                    if re.search(r'(?:npm|pnpm|yarn|docker|go run|dotnet|python|pip|make|uvicorn|cargo|audit|run)', body, re.IGNORECASE):
                        lines_cmd = [l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('<')]
                        if lines_cmd:
                            found_quickstart_cmd = '\n'.join(lines_cmd[:3])
                            break

                if found_quickstart_cmd:
                    score += 25
                    found.append(CriterionItem(
                        "Khối lệnh QUICK START hướng dẫn cài đặt và khởi chạy dự án cục bộ",
                        evidence=f"{readme_file.name}",
                        snippet=found_quickstart_cmd,
                        details="Đã phát hiện khối mã lệnh hướng dẫn khởi chạy dự án môi trường phát triển cục bộ.",
                        badge="Quick Start"
                    ))
                else:
                    missing.append(CriterionItem(
                        "Khối lệnh QUICK START hướng dẫn thiết lập môi trường và chạy mã nguồn",
                        evidence=readme_file.name,
                        details="Không tìm thấy khối mã (code block bash/shell) hướng dẫn cài đặt dependencies và chạy dev server cục bộ.",
                        remediation="Thêm khối lệnh Quick Start mẫu (ví dụ: npm install && npm run dev hoặc pip install -r requirements.txt)."
                    ))

                # Biến môi trường (.ENV)
                env_match = re.search(r'(\.env|environment variable|biến môi trường)', content, re.IGNORECASE)
                env_example = self.tree.find_by_name('.env.example') or self.tree.find_by_name('.env.sample') or self.tree.find_by_name('.env.template')
                if env_match or env_example:
                    score += 15
                    ev_name = env_example[0].name if env_example else readme_file.name
                    found.append(CriterionItem(
                        "Tài liệu hướng dẫn cấu hình biến môi trường (.ENV)",
                        evidence=ev_name,
                        snippet=f"Tệp {ev_name}" if env_example else "Mục .ENV trong README",
                        details="Đã xác minh tài liệu biến môi trường và tệp cấu hình mẫu an toàn.",
                        badge=".ENV Docs"
                    ))
                else:
                    missing.append(CriterionItem(
                        "Tài liệu hướng dẫn cấu hình biến môi trường (.ENV)",
                        evidence=readme_file.name,
                        details="Thiếu tài liệu hướng dẫn cấu hình biến môi trường và không tìm thấy tệp .env.example mẫu.",
                        remediation="Tạo tệp `.env.example` liệt kê các biến cấu hình cần thiết và ghi chú vào README.md."
                    ))

                # Cấu trúc kiến trúc / Thư mục
                if re.search(r'(architecture|cấu trúc|project structure|folder structure|kiến trúc|what\'s inside|tiers)', content, re.IGNORECASE):
                    score += 15
                    has_mermaid = 'mermaid' in content.lower()
                    badge_str = "Mermaid Diagram" if has_mermaid else "Directory Map"
                    found.append(CriterionItem(
                        "Mô tả cấu trúc thư mục và sơ đồ ARCHITECTURE tổng quan",
                        evidence=readme_file.name,
                        details=f"Đã phát hiện sơ đồ/mô tả cấu trúc kiến trúc dự án ({badge_str}).",
                        badge=badge_str
                    ))
                else:
                    missing.append(CriterionItem(
                        "Sơ đồ hoặc tài liệu mô tả cấu trúc thư mục ARCHITECTURE",
                        evidence=readme_file.name,
                        details="Không tìm thấy sơ đồ kiến trúc (Mermaid diagram) hoặc cây thư mục giải thích cấu trúc dự án trong README.",
                        remediation="Bổ sung sơ đồ kiến trúc tổng quan hoặc cây thư mục với chú thích vai trò của từng thư mục."
                    ))

                # Living Documentation & Auto-Sync Pipeline (S-007)
                has_sync_script = (self.root / 'scripts' / 'sync_docs.py').is_file() or bool(self.tree.find_by_name('sync_docs.py'))
                has_auto_gen_stats = bool(self.tree.find_by_name('MANIFEST.json')) or bool(self.tree.find_by_name('llms.txt'))
                has_pre_commit = (self.root / '.githooks' / 'pre-commit').is_file() or (self.root / '.pre-commit-config.yaml').is_file()

                if has_sync_script or has_auto_gen_stats or has_pre_commit:
                    tools_found = []
                    if has_sync_script:
                        tools_found.append("scripts/sync_docs.py")
                    if has_auto_gen_stats:
                        tools_found.append("MANIFEST.json / llms.txt")
                    if has_pre_commit:
                        tools_found.append("pre-commit hook")
                    found.append(CriterionItem(
                        "Cơ chế Tài liệu sống & Đồng bộ tự động 4 lớp (LIVING DOCUMENTATION AUTO-SYNC PIPELINE)",
                        evidence=", ".join(tools_found),
                        details=f"Đã phát hiện hệ thống chống trôi lệch tài liệu tự động: {', '.join(tools_found)}.",
                        badge="Living Docs"
                    ))

            except Exception:
                pass
        else:
            missing.append(CriterionItem(
                "Dự án chưa có tệp README.md giới thiệu",
                evidence="Thư mục gốc",
                details="Không tìm thấy tệp README.md (hoặc readme.md) tại thư mục gốc của dự án.",
                remediation="Khởi tạo tệp README.md trình bày mục tiêu sản phẩm, kiến trúc và lệnh khởi chạy."
            ))
            self.gaps.append("Thiếu tệp README.md hướng dẫn khởi chạy dự án và ONBOARDING cho thành viên mới.")

        score = min(100, score)
        self.scores['Tài Liệu & Hướng Dẫn (README & ONBOARDING)'] = score
        self.details['readme'] = {
            'name': 'Readme & Onboarding',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False
        }

    def audit_architecture_docs_and_ai(self):
        score = 0
        found = []
        missing = []

        # 1. AI AGENT Governance (AGENTS.md / .cursorrules / CLAUDE.md)
        ai_rules_files = ['AGENTS.md', '.cursorrules', 'CLAUDE.md', '.windsurfrules', '.github/copilot-instructions.md']
        has_ai_rules = False

        for af in ai_rules_files:
            matches = self.tree.find_by_name(af)
            if (self.root / af).exists() or matches:
                target_f = (self.root / af) if (self.root / af).exists() else matches[0]
                has_ai_rules = True
                score += 35
                try:
                    lines_cnt = len(target_f.read_text(encoding='utf-8', errors='ignore').splitlines())
                except Exception:
                    lines_cnt = 0
                found.append(CriterionItem(
                    f"Tệp quy chuẩn chỉ dẫn dành cho AI AGENT ({af})",
                    evidence=f"{af} ({lines_cnt} dòng)",
                    details=f"Đã phát hiện hiến pháp chỉ đạo Agent tại `{af}` với {lines_cnt} dòng định hướng hành vi.",
                    badge="Agent Governance"
                ))
                break

        if not has_ai_rules:
            missing.append(CriterionItem(
                "Tệp quy chuẩn chỉ dẫn cho AI AGENT (AGENTS.md hoặc .CURSORRULES)",
                evidence="Thư mục gốc",
                details="Chưa có tệp AGENTS.md, .cursorrules hoặc CLAUDE.md để định hướng hành vi của AI Agent.",
                remediation="Tạo tệp AGENTS.md tuân thủ chuẩn Project-Builder-4-Agents để giao tiếp hiệu quả với AI."
            ))

        # 2. ARCHITECTURE DECISION RECORDS (ADRs)
        adrs = [p for p in self.tree.all_files if ('adrs' in p.parts or 'adr' in p.parts) and p.suffix == '.md']
        if len(adrs) >= 5:
            score += 35
            adr_samples = ", ".join([p.name for p in adrs[:3]])
            found.append(CriterionItem(
                f"Kho lưu trữ hồ sơ quyết định kiến trúc ({len(adrs)} tệp ADR)",
                evidence=f"{len(adrs)} tệp ({adr_samples}...)",
                details=f"Phát hiện {len(adrs)} hồ sơ quyết định kiến trúc (ADR) ghi lại các quyết định kỹ thuật cốt lõi.",
                badge=f"{len(adrs)} ADRs"
            ))
        elif len(adrs) >= 1:
            score += 20
            adr_samples = ", ".join([p.name for p in adrs])
            found.append(CriterionItem(
                f"Kho lưu trữ hồ sơ quyết định kiến trúc ({len(adrs)} tệp ADR - Cần bổ sung)",
                evidence=f"{len(adrs)} tệp ({adr_samples})",
                details=f"Phát hiện {len(adrs)} ADR, khuyến nghị bổ sung thêm các quyết định quan trọng.",
                badge=f"{len(adrs)} ADRs"
            ))
        else:
            missing.append(CriterionItem(
                "Hồ sơ ARCHITECTURE DECISION RECORDS (ADRS)",
                evidence="docs/adr/ hoặc adrs/",
                details="Chưa phát hiện thư mục ADRs lưu trữ lịch sử các quyết định kiến trúc hệ thống.",
                remediation="Khởi tạo thư mục docs/adr/ hoặc adrs/ và viết ADR cho các quyết định công nghệ quan trọng."
            ))

        # 3. API CONTRACTS (OpenAPI / Swagger / Contracts / MANIFEST.json)
        api_contracts = [p for p in self.tree.all_files if any(k in p.name.lower() for k in ['openapi', 'swagger', 'contract']) and p.suffix in {'.yaml', '.yml', '.json'}]
        if api_contracts:
            score += 30
            rel_path = str(self.tree.rel_path(api_contracts[0])) if hasattr(self.tree, 'rel_path') else api_contracts[0].name
            found.append(CriterionItem(
                f"Chuẩn hóa tài liệu API CONTRACT ({api_contracts[0].name})",
                evidence=rel_path,
                details=f"Đã phát hiện đặc tả API hợp đồng tại `{rel_path}` phục vụ tích hợp chuẩn mực.",
                badge="API Contract"
            ))
        else:
            missing.append(CriterionItem(
                "Tài liệu đặc tả hợp đồng API CONTRACT (OPENAPI / SWAGGER)",
                evidence="openapi.yaml / swagger.json",
                details="Chưa phát hiện tài liệu đặc tả API chuẩn (OpenAPI 3.0, Swagger hoặc Proto schemas).",
                remediation="Bổ sung tài liệu OpenAPI (openapi.yaml) hoặc tích hợp thư viện auto-generate Swagger docs."
            ))

        score = min(100, score)
        self.scores['Quản Trị API CONTRACT & Cấu Hình AI AGENT'] = score
        self.add_log("  -> Verified Architecture Decision Records (ADRs), OpenAPI specs and Product Vision.", "contracts", "muted")
        self.details['contracts'] = {
            'name': 'Hồ Sơ Kiến Trúc & Hợp Đồng API',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 10,
            'is_na': False
        }

    def audit_agent_ecosystem(self):
        score = 0
        found = []
        missing = []

        # 1. Quét Agent Rules & Hiến pháp (AGENTS.md, .cursorrules, .cursor/rules/*.mdc, CLAUDE.md, .windsurfrules)
        rule_files = []
        rule_candidates = [
            'AGENTS.md', '.cursorrules', 'CLAUDE.md', '.windsurfrules',
            '.clinerules', '.github/copilot-instructions.md'
        ]
        for rc in rule_candidates:
            matches = self.tree.find_by_name(rc)
            for m in matches:
                rule_files.append(m)

        # Thêm các file .mdc (Cursor Rules)
        rule_files.extend([p for p in self.tree.all_files if p.suffix.lower() == '.mdc'])

        has_negative_constraints = False
        has_stop_and_ask = False
        has_anti_crash_rules = False

        if rule_files:
            score += 20
            names_str = ", ".join(sorted(list({p.name for p in rule_files}))[:4])
            found.append(CriterionItem(
                f"Tệp quy chuẩn chỉ dẫn AI AGENT chuẩn mực ({names_str})",
                evidence=names_str,
                details=f"Đã tìm thấy {len(rule_files)} tệp chỉ dẫn Agent trong dự án: {names_str}.",
                badge=f"{len(rule_files)} rules"
            ))

            for rf in rule_files:
                try:
                    txt = self.tree.read_text(rf)
                    if re.search(r'(cấm|không được|tuyệt đối không|never|prohibited|forbidden|do not)', txt, re.IGNORECASE):
                        has_negative_constraints = True
                    if re.search(r'(dừng lại hỏi|stop & ask|hỏi ý kiến|circuit breaker|xin ý kiến|confirm|2-attempt)', txt, re.IGNORECASE):
                        has_stop_and_ask = True
                    if re.search(r'(anti-crash|try-catch|defensive|null safety|chống đổ vỡ|zero-drift)', txt, re.IGNORECASE):
                        has_anti_crash_rules = True
                except Exception:
                    pass

            if has_negative_constraints:
                score += 10
                found.append(CriterionItem(
                    "Quy tắc ràng buộc phủ định (NEGATIVE CONSTRAINTS) ngăn chặn Agent tự ý sửa đổi bừa bãi",
                    evidence="AGENTS.md / rules",
                    details="Phát hiện các điều khoản cấm (never, do not, cấm) thiết lập ranh giới an toàn cho Agent.",
                    badge="Negative Constraints"
                ))
            else:
                missing.append(CriterionItem(
                    "Quy tắc điều khoản cấm (NEGATIVE CONSTRAINTS: hành động nào Agent tuyệt đối KHÔNG được làm)",
                    evidence="AGENTS.md",
                    details="Hiến pháp Agent chưa liệt kê các hành động bị cấm tuyệt đối (ví dụ: không xóa file, không đổi kiến trúc khi chưa hỏi).",
                    remediation="Bổ sung danh sách điều khoản cấm (Negative Constraints) vào AGENTS.md."
                ))

            if has_stop_and_ask:
                score += 10
                found.append(CriterionItem(
                    "Cơ chế ngắt mạch dừng lại hỏi (STOP & ASK / 2-ATTEMPT CIRCUIT BREAKER) chống vòng lặp Doom Loop",
                    evidence="AGENTS.md",
                    details="Phát hiện điều khoản ngắt mạch (stop & ask, 2-attempt circuit breaker) yêu cầu Agent dừng lại hỏi ý kiến.",
                    badge="Circuit Breaker"
                ))
            else:
                missing.append(CriterionItem(
                    "Cơ chế chốt chặn STOP & ASK / CIRCUIT BREAKER (buộc Agent dừng lại xin ý kiến khi chạm rủi ro kiến trúc)",
                    evidence="AGENTS.md",
                    details="Thiếu quy tắc ngắt mạch buộc Agent dừng lại xin ý kiến sau 2 lần thử thất bại hoặc khi có nguy cơ phá vỡ cấu trúc.",
                    remediation="Thêm nguyên tắc '2-Attempt Circuit Breaker: Stop and ask before breaking backwards compatibility' vào AGENTS.md."
                ))

            if has_anti_crash_rules:
                score += 10
                found.append(CriterionItem(
                    "Điều khoản ràng buộc bắt buộc lập trình phòng thủ (ANTI-CRASH DEFENSIVE STANDARD)",
                    evidence="AGENTS.md",
                    details="Phát hiện điều khoản quy định bắt buộc lập trình phòng thủ chống đổ vỡ runtime.",
                    badge="Defensive Standards"
                ))
            else:
                missing.append(CriterionItem(
                    "Quy chuẩn chống đổ vỡ ANTI-CRASH bắt buộc trong hiến pháp Agent",
                    evidence="AGENTS.md",
                    details="Thiếu yêu cầu bắt buộc Agent phải bọc try-catch, kiểm tra null safety và validate kiểu dữ liệu đầu vào.",
                    remediation="Bổ sung mục Defensive Programming Guidelines vào AGENTS.md."
                ))
        else:
            missing.append(CriterionItem(
                "Thiếu tệp hiến pháp định hướng hành vi cho AI Agent (AGENTS.md, .cursorrules hoặc .mdc)",
                evidence="Thư mục gốc",
                details="Không tìm thấy tệp hiến pháp nào định hướng hành vi cho AI Coding Agent.",
                remediation="Khởi tạo tệp AGENTS.md theo mẫu Project-Builder-4-Agents."
            ))

        # 2. Quét Agent Skills Catalog (.agents/skills/*/SKILL.md, .claude/skills/*/SKILL.md, skills/*/SKILL.md)
        skill_files = [p for p in self.tree.all_files if 'skills' in p.parts and p.name.lower() in {'skill.md', 'skill.json'}]
        valid_skills_count = 0
        has_yaml_frontmatter = False

        if skill_files:
            for sf in skill_files:
                try:
                    txt = self.tree.read_text(sf)
                    if txt.startswith('---') and 'name:' in txt and 'description:' in txt:
                        has_yaml_frontmatter = True
                        valid_skills_count += 1
                    elif 'name' in txt and ('description' in txt or 'prompt' in txt):
                        valid_skills_count += 1
                except Exception:
                    pass

            score += 25
            skill_names = [p.parent.name for p in skill_files[:4]]
            found.append(CriterionItem(
                f"Kho kỹ năng đóng gói AGENT SKILLS ({len(skill_files)} kỹ năng được phát hiện)",
                evidence=f"{len(skill_files)} skills ({', '.join(skill_names)})",
                details=f"Đã xác minh kho kỹ năng Agent đóng gói dạng SKILL.md: {', '.join(skill_names)}.",
                badge=f"{len(skill_files)} skills"
            ))

            if has_yaml_frontmatter:
                score += 10
                found.append(CriterionItem(
                    "Cấu trúc SKILL.md chuẩn hóa với YAML FRONTMATTER (name, description, instructions)",
                    evidence=f"{valid_skills_count} tệp SKILL.md",
                    details=f"Đã xác minh {valid_skills_count} tệp SKILL.md có YAML frontmatter đúng chuẩn Agent Skill Specification.",
                    badge="Frontmatter OK"
                ))
            else:
                missing.append(CriterionItem(
                    "Chuẩn hóa YAML FRONTMATTER (name, description) cho các tệp SKILL.md",
                    evidence=".agents/skills/*/SKILL.md",
                    details="Các tệp SKILL.md hiện tại thiếu khối YAML Frontmatter chuẩn (name, description).",
                    remediation="Bổ sung block YAML `--- name: ... description: ... ---` vào đầu mỗi tệp SKILL.md."
                ))
        else:
            missing.append(CriterionItem(
                "Thư mục đóng gói kỹ năng AGENT SKILLS (.agents/skills/*/SKILL.md) để mở rộng năng lực tự động",
                evidence=".agents/skills/",
                details="Chưa có thư mục đóng gói Agent Skills chuyên biệt để trao quyền cho Agent tự thực thi tác vụ chuyên sâu.",
                remediation="Tạo thư mục `.agents/skills/<skill-name>/SKILL.md` đóng gói các kỹ năng kiểm thử, review hoặc deploy."
            ))

        # 3. Quét Agent Workflows, Playbooks & Automation Pipelines (.agent/workflows/, workflows/, playbooks/, prompts/)
        workflow_files = [
            p for p in self.tree.all_files
            if ('workflows' in p.parts or 'playbooks' in p.parts or 'prompts' in p.parts or 'agent-practices' in p.parts) and p.suffix.lower() in {'.md', '.yaml', '.yml'}
        ]
        has_verification_step = False

        if workflow_files:
            score += 15
            wf_names = ", ".join(sorted(list({p.name for p in workflow_files}))[:3])
            found.append(CriterionItem(
                f"Quy trình tự động hóa tác vụ AGENT WORKFLOWS & PLAYBOOKS ({len(workflow_files)} kịch bản: {wf_names})",
                evidence=f"{len(workflow_files)} kịch bản ({wf_names})",
                details=f"Đã tìm thấy {len(workflow_files)} kịch bản quy trình nhiều bước hỗ trợ cộng tác: {wf_names}.",
                badge=f"{len(workflow_files)} workflows"
            ))

            for wf in workflow_files:
                try:
                    txt = self.tree.read_text(wf)
                    if re.search(r'(verify|test|lint|tự kiểm tra|nghiệm thu|checklist|validation|sync_docs)', txt, re.IGNORECASE):
                        has_verification_step = True
                        break
                except Exception:
                    pass

            if has_verification_step:
                score += 10
                found.append(CriterionItem(
                    "Quy trình tác vụ tích hợp chặng tự kiểm chứng (SELF-VERIFICATION / TDD FIRST)",
                    evidence="workflows / playbooks",
                    details="Kịch bản quy trình chứa bước kiểm chứng tự động (test, lint, verification) trước khi đóng task.",
                    badge="Verification Gate"
                ))
            else:
                missing.append(CriterionItem(
                    "Chặng tự kiểm thử và nghiệm thu (SELF-VERIFICATION) trong kịch bản Workflow",
                    evidence="workflows / playbooks",
                    details="Kịch bản workflow chưa có bước bắt buộc Agent tự chạy test / lint để kiểm chứng kết quả trước khi báo cáo hoàn thành.",
                    remediation="Bổ sung bước Self-Verification Gate vào các kịch bản workflow."
                ))
        else:
            missing.append(CriterionItem(
                "Quy trình kịch bản tác vụ nhiều bước (AGENT WORKFLOWS) hỗ trợ cộng tác tự động",
                evidence=".agents/workflows/ hoặc playbooks/",
                details="Chưa có kịch bản quy trình từng bước chuẩn hóa để phối hợp tác vụ phức tạp.",
                remediation="Tạo thư mục `.agents/workflows/` chứa các kịch bản chạy test, refactor hoặc phát hành phiên bản."
            ))

        # Ghi nhận thêm nếu repo có MANIFEST.json / llms.txt (Zero-Clone Remote Hub)
        if (self.root / 'MANIFEST.json').is_file() or (self.root / 'llms.txt').is_file():
            found.append(CriterionItem(
                "Hạ tầng chỉ mục máy đọc ZERO-CLONE REMOTE HUB (MANIFEST.json / llms.txt)",
                evidence="MANIFEST.json / llms.txt",
                details="Dự án trang bị chỉ mục máy đọc MANIFEST.json và llms.txt cho AI Agent tra cứu không cần clone toàn bộ repo.",
                badge="Zero-Clone Hub"
            ))

        score = min(100, score)
        self.scores['Hệ Sinh Thái AI AGENT (RULES, SKILLS & WORKFLOWS)'] = score
        self.add_log("  -> Audited Agent Rules, SKILL.md specs, Workflows and Circuit Breaker standards.", "agent_ecosystem", "muted")
        self.details['agent_ecosystem'] = {
            'name': 'Hệ Sinh Thái AI Agent',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False,
            'rule_files_count': len(rule_files),
            'skills_count': len(skill_files),
            'workflows_count': len(workflow_files)
        }
