"""Pillar tài liệu, onboarding và hệ sinh thái AI Agent."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401


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

            found.append("Tệp README.md chuẩn xác tại thư mục gốc")

            try:

                content = readme_file.read_text(encoding='utf-8', errors='ignore')

                lines_count = len(content.splitlines())
                self.add_log(f"  -> Đã tìm thấy {readme_file.name} ({lines_count} dòng).", "readme", "muted")

                # Tiêu đề & Bài toán (Product Vision)

                if re.search(r'^#\s+.+', content, re.MULTILINE) and lines_count >= 15:

                    score += 20

                    found.append("Mô tả bài toán, mục tiêu và định vị giá trị sản phẩm rõ ràng")

                else:

                    missing.append("Đoạn giới thiệu mục tiêu bài toán và giá trị sản phẩm (PRODUCT VISION)")

                # Hướng dẫn khởi chạy (Quick Start)

                if re.search(r'```(?:bash|sh|shell|cmd|powershell)?\s*\n.*?(?:npm|pnpm|yarn|docker|go run|dotnet|python|pip|make)', content, re.DOTALL | re.IGNORECASE):

                    score += 25

                    found.append("Khối lệnh QUICK START hướng dẫn cài đặt và khởi chạy dự án cục bộ")

                else:

                    missing.append("Khối lệnh QUICK START hướng dẫn thiết lập môi trường và chạy mã nguồn")

                # Biến môi trường (.ENV)

                if re.search(r'(\.env|environment variable|biến môi trường)', content, re.IGNORECASE):

                    score += 15

                    found.append("Tài liệu hướng dẫn cấu hình biến môi trường (.ENV)")

                else:

                    missing.append("Tài liệu hướng dẫn cấu hình biến môi trường (.ENV)")

                # Cấu trúc kiến trúc / Thư mục

                if re.search(r'(architecture|cấu trúc|project structure|folder structure|kiến trúc|what\'s inside|tiers)', content, re.IGNORECASE):

                    score += 15

                    found.append("Mô tả cấu trúc thư mục và sơ đồ ARCHITECTURE tổng quan")

                else:

                    missing.append("Sơ đồ hoặc tài liệu mô tả cấu trúc thư mục ARCHITECTURE")

                # Living Documentation & Auto-Sync Pipeline (S-007)
                has_sync_script = (self.root / 'scripts' / 'sync_docs.py').is_file() or bool(self.tree.find_by_name('sync_docs.py'))
                has_auto_gen_stats = '<!-- AUTO-GEN:STATS -->' in content
                has_pre_commit = (self.root / '.githooks' / 'pre-commit').is_file()
                if has_sync_script or has_auto_gen_stats or has_pre_commit:
                    found.append("Cơ chế Tài liệu sống & Đồng bộ tự động 4 lớp (LIVING DOCUMENTATION AUTO-SYNC PIPELINE)")

            except Exception:

                pass

        else:

            missing.append("Dự án chưa có tệp README.md giới thiệu")

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

            if (self.root / af).exists() or bool(self.tree.find_by_name(af)):

                has_ai_rules = True

                score += 35

                found.append(f"Tệp quy chuẩn chỉ dẫn dành cho AI AGENT ({af})")

                break

        if not has_ai_rules:

            missing.append("Tệp quy chuẩn chỉ dẫn cho AI AGENT (AGENTS.md hoặc .CURSORRULES)")

        # 2. ARCHITECTURE DECISION RECORDS (ADRs)

        adrs = [p for p in self.tree.all_files if ('adrs' in p.parts or 'adr' in p.parts) and p.suffix == '.md']

        if len(adrs) >= 5:

            score += 35

            found.append(f"Kho lưu trữ hồ sơ quyết định kiến trúc ({len(adrs)} tệp ADR)")

        elif len(adrs) >= 1:

            score += 20

            found.append(f"Kho lưu trữ hồ sơ quyết định kiến trúc ({len(adrs)} tệp ADR - Cần bổ sung)")

        else:

            missing.append("Hồ sơ ARCHITECTURE DECISION RECORDS (ADRS)")

        # 3. API CONTRACTS (OpenAPI / Swagger / Contracts / MANIFEST.json)

        api_contracts = [p for p in self.tree.all_files if any(k in p.name.lower() for k in ['openapi', 'swagger', 'contract']) and p.suffix in {'.yaml', '.yml', '.json'}]

        if api_contracts:

            score += 30

            found.append(f"Chuẩn hóa tài liệu API CONTRACT ({api_contracts[0].name})")

        else:

            missing.append("Tài liệu đặc tả hợp đồng API CONTRACT (OPENAPI / SWAGGER)")

        score = min(100, score)

        self.scores['Quản Trị API CONTRACT & Cấu Hình AI AGENT'] = score

        self.add_log("  -> Đối soát Architecture Decision Records (ADRs), OpenAPI specs và Product Vision.", "contracts", "muted")
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
            found.append(f"Tệp quy chuẩn chỉ dẫn AI AGENT chuẩn mực ({names_str})")

            for rf in rule_files:
                try:
                    txt = rf.read_text(encoding='utf-8', errors='ignore')
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
                found.append("Quy tắc ràng buộc phủ định (NEGATIVE CONSTRAINTS) ngăn chặn Agent tự ý sửa đổi bừa bãi")
            else:
                missing.append("Quy tắc điều khoản cấm (NEGATIVE CONSTRAINTS: hành động nào Agent tuyệt đối KHÔNG được làm)")

            if has_stop_and_ask:
                score += 10
                found.append("Cơ chế ngắt mạch dừng lại hỏi (STOP & ASK / 2-ATTEMPT CIRCUIT BREAKER) chống vòng lặp Doom Loop")
            else:
                missing.append("Cơ chế chốt chặn STOP & ASK / CIRCUIT BREAKER (buộc Agent dừng lại xin ý kiến khi chạm rủi ro kiến trúc)")

            if has_anti_crash_rules:
                score += 10
                found.append("Điều khoản ràng buộc bắt buộc lập trình phòng thủ (ANTI-CRASH DEFENSIVE STANDARD)")
            else:
                missing.append("Quy chuẩn chống đổ vỡ ANTI-CRASH bắt buộc trong hiến pháp Agent")
        else:
            missing.append("Thiếu tệp hiến pháp định hướng hành vi cho AI Agent (AGENTS.md, .cursorrules hoặc .mdc)")

        # 2. Quét Agent Skills Catalog (.agents/skills/*/SKILL.md, .claude/skills/*/SKILL.md, skills/*/SKILL.md)
        skill_files = [p for p in self.tree.all_files if 'skills' in p.parts and p.name.lower() in {'skill.md', 'skill.json'}]
        valid_skills_count = 0
        has_yaml_frontmatter = False

        if skill_files:
            for sf in skill_files:
                try:
                    txt = sf.read_text(encoding='utf-8', errors='ignore')
                    if txt.startswith('---') and 'name:' in txt and 'description:' in txt:
                        has_yaml_frontmatter = True
                        valid_skills_count += 1
                    elif 'name' in txt and ('description' in txt or 'prompt' in txt):
                        valid_skills_count += 1
                except Exception:
                    pass

            score += 25
            found.append(f"Kho kỹ năng đóng gói AGENT SKILLS ({len(skill_files)} kỹ năng được phát hiện)")

            if has_yaml_frontmatter:
                score += 10
                found.append("Cấu trúc SKILL.md chuẩn hóa với YAML FRONTMATTER (name, description, instructions)")
            else:
                missing.append("Chuẩn hóa YAML FRONTMATTER (name, description) cho các tệp SKILL.md")
        else:
            missing.append("Thư mục đóng gói kỹ năng AGENT SKILLS (.agents/skills/*/SKILL.md) để mở rộng năng lực tự động")

        # 3. Quét Agent Workflows, Playbooks & Automation Pipelines (.agent/workflows/, workflows/, playbooks/, prompts/)
        workflow_files = [
            p for p in self.tree.all_files
            if ('workflows' in p.parts or 'playbooks' in p.parts or 'prompts' in p.parts or 'agent-practices' in p.parts) and p.suffix.lower() in {'.md', '.yaml', '.yml'}
        ]
        has_verification_step = False

        if workflow_files:
            score += 15
            wf_names = ", ".join(sorted(list({p.name for p in workflow_files}))[:3])
            found.append(f"Quy trình tự động hóa tác vụ AGENT WORKFLOWS & PLAYBOOKS ({len(workflow_files)} kịch bản: {wf_names})")

            for wf in workflow_files:
                try:
                    txt = wf.read_text(encoding='utf-8', errors='ignore')
                    if re.search(r'(verify|test|lint|tự kiểm tra|nghiệm thu|checklist|validation|sync_docs)', txt, re.IGNORECASE):
                        has_verification_step = True
                        break
                except Exception:
                    pass

            if has_verification_step:
                score += 10
                found.append("Quy trình tác vụ tích hợp chặng tự kiểm chứng (SELF-VERIFICATION / TDD FIRST)")
            else:
                missing.append("Chặng tự kiểm thử và nghiệm thu (SELF-VERIFICATION) trong kịch bản Workflow")
        else:
            missing.append("Quy trình kịch bản tác vụ nhiều bước (AGENT WORKFLOWS) hỗ trợ cộng tác tự động")

        # Ghi nhận thêm nếu repo có MANIFEST.json / llms.txt (Zero-Clone Remote Hub)
        if (self.root / 'MANIFEST.json').is_file() or (self.root / 'llms.txt').is_file():
            found.append("Hạ tầng chỉ mục máy đọc ZERO-CLONE REMOTE HUB (MANIFEST.json / llms.txt)")

        score = min(100, score)
        self.scores['Hệ Sinh Thái AI AGENT (RULES, SKILLS & WORKFLOWS)'] = score
        self.add_log("  -> Rà soát Agent Rules, SKILL.md specs, Workflows và tiêu chuẩn Circuit Breaker.", "agent_ecosystem", "muted")
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
