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
                    'Accurate README.md in root directory',
                    evidence=f"{readme_file.name} ({lines_count} lines, {file_size_kb:.1f} KB)",
                    details=f"Detected the main starter documentation file at `{readme_file.name}` with {lines_count} lines of content.",
                    badge=f"{lines_count} lines"
                ))

                # Tiêu đề & Bài toán (Product Vision)
                title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                if title_match and lines_count >= 15:
                    score += 20
                    title_str = title_match.group(1).strip()
                    found.append(CriterionItem(
                        'Clear product vision, problem description and value proposition',
                        evidence=f"{readme_file.name}:L1",
                        snippet=f"# {title_str[:80]}",
                        details=f"Detected the title and product positioning: '{title_str}' along with a description of the business problem and goals.",
                        badge="Product Vision"
                    ))
                else:
                    missing.append(CriterionItem(
                        'Product vision and problem value proposition section',
                        evidence=readme_file.name,
                        details='The README lacks a top-level heading (# Heading) or is too short (< 15 lines) to describe the problem and product value.',
                        remediation='Add an introduction: # Project name, the problem solved, target users and core value.'
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
                        'QUICK START command block guiding local setup and startup',
                        evidence=f"{readme_file.name}",
                        snippet=found_quickstart_cmd,
                        details='Detected command block instructing how to run the project in local development.',
                        badge="Quick Start"
                    ))
                else:
                    missing.append(CriterionItem(
                        'QUICK START block for environment setup and running code',
                        evidence=readme_file.name,
                        details='No code block (bash/shell) found with instructions to install dependencies and run the local dev server.',
                        remediation='Add a sample Quick Start command block (e.g. npm install && npm run dev or pip install -r requirements.txt).'
                    ))

                # Biến môi trường (.ENV)
                env_match = re.search(r'(\.env|environment variable|biến môi trường)', content, re.IGNORECASE)
                env_example = self.tree.find_by_name('.env.example') or self.tree.find_by_name('.env.sample') or self.tree.find_by_name('.env.template')
                if env_match or env_example:
                    score += 15
                    ev_name = env_example[0].name if env_example else readme_file.name
                    found.append(CriterionItem(
                        'Environment variables configuration documentation (.ENV)',
                        evidence=ev_name,
                        snippet=f"File {ev_name}" if env_example else '.ENV section in README',
                        details='Verified environment variable documentation and a safe sample configuration file.',
                        badge=".ENV Docs"
                    ))
                else:
                    missing.append(CriterionItem(
                        'Environment variables configuration documentation (.ENV)',
                        evidence=readme_file.name,
                        details='Missing documentation on configuring environment variables and no sample .env.example file found.',
                        remediation='Create a `.env.example` file listing the required configuration variables and note it in README.md.'
                    ))

                # Cấu trúc kiến trúc / Thư mục
                if re.search(r'(architecture|cấu trúc|project structure|folder structure|kiến trúc|what\'s inside|tiers)', content, re.IGNORECASE):
                    score += 15
                    has_mermaid = 'mermaid' in content.lower()
                    badge_str = "Mermaid Diagram" if has_mermaid else "Directory Map"
                    found.append(CriterionItem(
                        'Directory structure description and ARCHITECTURE overview diagram',
                        evidence=readme_file.name,
                        details=f"Detected an architecture structure diagram/description of the project ({badge_str}).",
                        badge=badge_str
                    ))
                else:
                    missing.append(CriterionItem(
                        'Diagram or document describing ARCHITECTURE directory layout',
                        evidence=readme_file.name,
                        details='No architecture diagram (Mermaid diagram) or folder tree explaining the project structure found in the README.',
                        remediation="Add an overview architecture diagram or a folder tree annotated with each folder's role."
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
                        '4-Layer Living Documentation auto-sync pipeline',
                        evidence=", ".join(tools_found),
                        details=f"Detected an automatic documentation-drift prevention system: {', '.join(tools_found)}.",
                        badge="Living Docs"
                    ))

            except Exception:
                pass
        else:
            missing.append(CriterionItem(
                'Project is missing introductory README.md file',
                evidence='Root folder',
                details='No README.md (or readme.md) found in the project root.',
                remediation='Create README.md covering the product goal, architecture and run commands.'
            ))
            self.gaps.append('Missing README.md with run instructions and ONBOARDING for new members.')

        score = min(100, score)
        self.scores['Documentation & Guides (README & ONBOARDING)'] = score
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
                    f"Standard instruction file for AI AGENTS ({af})",
                    evidence=f"{af} ({lines_cnt} lines)",
                    details=f"Detected the Agent constitution at `{af}` with {lines_cnt} lines of behavior guidance.",
                    badge="Agent Governance"
                ))
                break

        if not has_ai_rules:
            missing.append(CriterionItem(
                'AI Agent directive specification (AGENTS.md or .cursorrules)',
                evidence='Root folder',
                details="No AGENTS.md, .cursorrules or CLAUDE.md to steer the AI Agent's behavior.",
                remediation='Create an AGENTS.md following the Project-Builder-4-Agents standard to communicate effectively with AI.'
            ))

        # 2. ARCHITECTURE DECISION RECORDS (ADRs)
        adrs = [p for p in self.tree.all_files if ('adrs' in p.parts or 'adr' in p.parts) and p.suffix == '.md']
        if len(adrs) >= 5:
            score += 35
            adr_samples = ", ".join([p.name for p in adrs[:3]])
            found.append(CriterionItem(
                f"Architecture decision record repository ({len(adrs)} ADR files)",
                evidence=f"{len(adrs)} files ({adr_samples}...)",
                details=f"Detected {len(adrs)} architecture decision records (ADRs) documenting core technical decisions.",
                badge=f"{len(adrs)} ADRs"
            ))
        elif len(adrs) >= 1:
            score += 20
            adr_samples = ", ".join([p.name for p in adrs])
            found.append(CriterionItem(
                f"Architecture decision record repository ({len(adrs)} ADR files - needs more)",
                evidence=f"{len(adrs)} files ({adr_samples})",
                details=f"Detected {len(adrs)} ADRs; adding more important decisions is recommended.",
                badge=f"{len(adrs)} ADRs"
            ))
        else:
            missing.append(CriterionItem(
                'Architecture Decision Records (ADRs)',
                evidence='docs/adr/ or adrs/',
                details='No ADR folder found to store the history of system architecture decisions.',
                remediation='Create a docs/adr/ or adrs/ folder and write ADRs for important technology decisions.'
            ))

        # 3. API CONTRACTS (OpenAPI / Swagger / Contracts / MANIFEST.json)
        api_contracts = [p for p in self.tree.all_files if any(k in p.name.lower() for k in ['openapi', 'swagger', 'contract']) and p.suffix in {'.yaml', '.yml', '.json'}]
        if api_contracts:
            score += 30
            rel_path = str(self.tree.rel_path(api_contracts[0])) if hasattr(self.tree, 'rel_path') else api_contracts[0].name
            found.append(CriterionItem(
                f"Standardized API CONTRACT documentation ({api_contracts[0].name})",
                evidence=rel_path,
                details=f"Detected an API contract specification at `{rel_path}` supporting standard integration.",
                badge="API Contract"
            ))
        else:
            missing.append(CriterionItem(
                'API contract specification (OpenAPI / Swagger)',
                evidence="openapi.yaml / swagger.json",
                details='No standard API specification found (OpenAPI 3.0, Swagger or Proto schemas).',
                remediation='Add OpenAPI documentation (openapi.yaml) or integrate a Swagger auto-generation library.'
            ))

        score = min(100, score)
        self.scores['API CONTRACT Governance & AI AGENT Configuration'] = score
        self.add_log("  -> Verified Architecture Decision Records (ADRs), OpenAPI specs and Product Vision.", "contracts", "muted")
        self.details['contracts'] = {
            'name': 'Architecture Records & API Contracts',
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
                f"Standard AI AGENT instruction files ({names_str})",
                evidence=names_str,
                details=f"Found {len(rule_files)} Agent instruction files in the project: {names_str}.",
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
                    'Negative constraints preventing unintended modifications by Agent',
                    evidence="AGENTS.md / rules",
                    details='Detected prohibition clauses (never, do not, prohibited) that set safety boundaries for the Agent.',
                    badge="Negative Constraints"
                ))
            else:
                missing.append(CriterionItem(
                    'Prohibited actions (Negative constraints: what Agent must NEVER do)',
                    evidence="AGENTS.md",
                    details='The Agent constitution does not list absolutely forbidden actions (e.g. do not delete files, do not change the architecture without asking).',
                    remediation='Add a list of prohibition clauses (Negative Constraints) to AGENTS.md.'
                ))

            if has_stop_and_ask:
                score += 10
                found.append(CriterionItem(
                    'Stop & Ask / 2-Attempt Circuit Breaker preventing Doom Loops',
                    evidence="AGENTS.md",
                    details='Detected circuit-breaker clauses (stop & ask, 2-attempt circuit breaker) requiring the Agent to stop and ask.',
                    badge="Circuit Breaker"
                ))
            else:
                missing.append(CriterionItem(
                    'Stop & Ask / Circuit Breaker gate (forces Agent to seek confirmation on architectural risks)',
                    evidence="AGENTS.md",
                    details='Missing a circuit-breaker rule forcing the Agent to stop and ask after 2 failed attempts or when the structure is at risk of breaking.',
                    remediation="Add the principle '2-Attempt Circuit Breaker: Stop and ask before breaking backwards compatibility' to AGENTS.md."
                ))

            if has_anti_crash_rules:
                score += 10
                found.append(CriterionItem(
                    'Mandatory defensive programming clause (Anti-Crash standard)',
                    evidence="AGENTS.md",
                    details='Detected a clause mandating defensive programming against runtime breakage.',
                    badge="Defensive Standards"
                ))
            else:
                missing.append(CriterionItem(
                    'Mandatory anti-crash defensive rules in Agent constitution',
                    evidence="AGENTS.md",
                    details='Missing mandatory rule requiring Agent to wrap try-catch, check null safety, and validate input types.',
                    remediation='Add Defensive Programming Guidelines section to AGENTS.md.'
                ))
        else:
            missing.append(CriterionItem(
                'Missing behavioral constitution for AI Agents (AGENTS.md, .cursorrules or .mdc)',
                evidence='Root folder',
                details="No constitution file found to steer the AI Coding Agent's behavior.",
                remediation='Create an AGENTS.md from the Project-Builder-4-Agents template.'
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
                f"Packaged AGENT SKILLS repository ({len(skill_files)} skills detected)",
                evidence=f"{len(skill_files)} skills ({', '.join(skill_names)})",
                details=f"Verified a repository of Agent skills packaged as SKILL.md: {', '.join(skill_names)}.",
                badge=f"{len(skill_files)} skills"
            ))

            if has_yaml_frontmatter:
                score += 10
                found.append(CriterionItem(
                    'Standardized SKILL.md structure with YAML frontmatter (name, description, instructions)',
                    evidence=f"{valid_skills_count} SKILL.md files",
                    details=f"Verified {valid_skills_count} SKILL.md files with YAML frontmatter conforming to the Agent Skill Specification.",
                    badge="Frontmatter OK"
                ))
            else:
                missing.append(CriterionItem(
                    'Standardized YAML frontmatter (name, description) for SKILL.md files',
                    evidence=".agents/skills/*/SKILL.md",
                    details='The current SKILL.md files lack the standard YAML frontmatter block (name, description).',
                    remediation='Add the YAML block `--- name: ... description: ... ---` at the top of each SKILL.md.'
                ))
        else:
            missing.append(CriterionItem(
                'Packaged Agent skills directory (.agents/skills/*/SKILL.md) for automated capability expansion',
                evidence=".agents/skills/",
                details='No dedicated Agent Skills folder to empower the Agent to run specialized tasks on its own.',
                remediation='Create `.agents/skills/<skill-name>/SKILL.md` packaging testing, review or deploy skills.'
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
                f"AGENT WORKFLOWS & PLAYBOOKS task automation ({len(workflow_files)} scripts: {wf_names})",
                evidence=f"{len(workflow_files)} scripts ({wf_names})",
                details=f"Found {len(workflow_files)} multi-step workflow scripts supporting collaboration: {wf_names}.",
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
                    'Task workflow with integrated self-verification stage (Self-Verification / TDD first)',
                    evidence="workflows / playbooks",
                    details='The workflow scripts contain an automatic verification step (test, lint, verification) before closing a task.',
                    badge="Verification Gate"
                ))
            else:
                missing.append(CriterionItem(
                    'Self-testing and acceptance verification stage in Agent workflow',
                    evidence="workflows / playbooks",
                    details='The workflow scripts lack a mandatory step for the Agent to run tests / lint itself to verify results before reporting completion.',
                    remediation='Add a Self-Verification Gate step to the workflow scripts.'
                ))
        else:
            missing.append(CriterionItem(
                'Multi-step task workflow scripts (Agent Workflows) for autonomous collaboration',
                evidence='.agents/workflows/ or playbooks/',
                details='No standardized step-by-step workflow for coordinating complex tasks.',
                remediation='Create an `.agents/workflows/` folder containing scripts for running tests, refactoring or releasing versions.'
            ))

        # Ghi nhận thêm nếu repo có MANIFEST.json / llms.txt (Zero-Clone Remote Hub)
        if (self.root / 'MANIFEST.json').is_file() or (self.root / 'llms.txt').is_file():
            found.append(CriterionItem(
                'Zero-Clone machine-readable index infrastructure (MANIFEST.json / llms.txt)',
                evidence="MANIFEST.json / llms.txt",
                details='The project provides machine-readable indexes MANIFEST.json and llms.txt so AI Agents can look things up without cloning the whole repo.',
                badge="Zero-Clone Hub"
            ))

        score = min(100, score)
        self.scores['AI AGENT Ecosystem (RULES, SKILLS & WORKFLOWS)'] = score
        self.add_log("  -> Audited Agent Rules, SKILL.md specs, Workflows and Circuit Breaker standards.", "agent_ecosystem", "muted")
        self.details['agent_ecosystem'] = {
            'name': 'AI Agent Ecosystem',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False,
            'rule_files_count': len(rule_files),
            'skills_count': len(skill_files),
            'workflows_count': len(workflow_files)
        }
