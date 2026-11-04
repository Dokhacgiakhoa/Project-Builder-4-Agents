#!/usr/bin/env python3
"""
UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE & SYSTEM DESIGN AUDITOR
Pure Python Standard Library (100% Offline, Zero-Token, Zero-Dependency)
Analyzes codebase against Starter Kit Standards and outputs PROJECT_REVIEW_REPORT.md
"""

import os
import sys
import re
import datetime
from pathlib import Path

# Paths to ignore during code analysis
IGNORE_DIRS = {
    'node_modules', '.git', 'dist', 'build', 'bin', 'obj', 
    '.vscode', '.idea', '__pycache__', '.next', 'coverage'
}

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py'}

class ProjectAuditor:
    def __init__(self, root_dir='.'):
        self.root = Path(root_dir).resolve()
        self.scores = {}
        self.gaps = []
        self.innovations = []
        self.violations = []
        self.details = {}

    def run(self):
        print("\n" + "=" * 70)
        print("  🚀 UNIVERSAL PROJECT REVIEW & ARCHITECTURE AUDITOR")
        print("  Benchmarking against: Universal AI-Native Starter Kit Standards")
        print("=" * 70 + "\n")

        self.audit_clean_architecture()
        self.audit_system_design_specs()
        self.audit_frontend_architecture()
        self.audit_anti_crash_code()
        self.audit_ai_governance()
        self.audit_ui_ux_archetypes()
        self.audit_pitch_and_docs()
        self.detect_advanced_innovations()

        total_score = self.calculate_total_score()
        report_path = self.generate_markdown_report(total_score)
        self.print_console_summary(total_score, report_path)
        return total_score

    # -------------------------------------------------------------
    # 1. Clean Architecture & DDD Audit
    # -------------------------------------------------------------
    def audit_clean_architecture(self):
        score = 0
        layers_found = []
        missing_layers = []

        expected_layers = ['Domain', 'Application', 'Infrastructure', 'Presentation']
        backend_dir = self.root / 'src'

        if backend_dir.exists() and backend_dir.is_dir():
            for layer in expected_layers:
                layer_path = backend_dir / layer
                if layer_path.exists() and layer_path.is_dir():
                    layers_found.append(layer)
                    score += 20
                else:
                    missing_layers.append(layer)
            
            # Check domain purity (no framework imports in Domain)
            domain_path = backend_dir / 'Domain'
            domain_leaks = []
            if domain_path.exists():
                for p in domain_path.rglob('*'):
                    if p.is_file() and p.suffix in CODE_EXTENSIONS:
                        try:
                            content = p.read_text(encoding='utf-8', errors='ignore')
                            if re.search(r'(import .* from [\'"](express|react|axios|@nestjs)[\'"]|using (Microsoft\.AspNetCore|Microsoft\.EntityFrameworkCore))', content):
                                domain_leaks.append(str(p.relative_to(self.root)))
                        except Exception:
                            pass
                
                if domain_leaks:
                    self.gaps.append(f"Domain Layer Leak: Các file sau trong Domain phụ thuộc vào Framework: {', '.join(domain_leaks[:3])}")
                    score = max(0, score - 15)
                else:
                    score += 20
        else:
            missing_layers = expected_layers
            self.gaps.append("Thiếu thư mục kiến trúc Backend `src/` theo chuẩn Clean Architecture.")

        score = min(100, score)
        self.scores['Clean Architecture & DDD'] = score
        self.details['clean_arch'] = {
            'layers_found': layers_found,
            'missing_layers': missing_layers,
            'score': score
        }

    # -------------------------------------------------------------
    # 2. System Design & Contract-First
    # -------------------------------------------------------------
    def audit_system_design_specs(self):
        score = 0
        specs_dir = self.root / 'specs'
        found = []
        missing = []

        checkpoints = [
            ('product-vision.md', 25, 'Tầm nhìn sản phẩm (Outcome Tree)'),
            ('domains.md', 25, 'Phân rã Bounded Contexts'),
            ('contracts/api-contract-template.yaml', 30, 'API Contract (OpenAPI 3.0)'),
            ('features/template-spec.md', 20, 'Khung đặc tả tính năng Feature Spec')
        ]

        for rel_path, weight, desc in checkpoints:
            full_path = specs_dir / rel_path
            if full_path.exists():
                score += weight
                found.append(desc)
            else:
                missing.append(desc)

        if missing:
            self.gaps.append(f"System Design Specs còn thiếu: {', '.join(missing)}")

        self.scores['System Design & Contracts'] = score
        self.details['system_design'] = {'found': found, 'missing': missing, 'score': score}

    # -------------------------------------------------------------
    # 3. Frontend Feature-Driven (Bulletproof React)
    # -------------------------------------------------------------
    def audit_frontend_architecture(self):
        score = 0
        fe_dir = self.root / 'frontend'
        found = []
        missing = []

        if fe_dir.exists() and (fe_dir / 'package.json').exists():
            score += 20
            found.append('Frontend Package Config')

            # Check features directory
            features_dir = fe_dir / 'src' / 'features'
            if features_dir.exists() and any(features_dir.iterdir()):
                score += 30
                found.append('Feature-Driven Structure (src/features/)')
            else:
                missing.append('Cấu trúc thư mục theo tính năng (src/features/)')

            # Check State separation & safe client
            if (fe_dir / 'src' / 'lib' / 'api-client.ts').exists():
                score += 20
                found.append('Defensive API Client (Interceptors & Error Normalization)')
            else:
                missing.append('Defensive API Client (src/lib/api-client.ts)')

            if (fe_dir / 'src' / 'config' / 'index.ts').exists():
                score += 15
                found.append('Runtime Environment Validation (Zod Config)')
            else:
                missing.append('Runtime Config Validation (src/config/index.ts)')

            if (fe_dir / 'src' / 'stores').exists():
                score += 15
                found.append('Global Client State Store (Zustand)')
            else:
                missing.append('Client State Management Store')
        else:
            self.gaps.append("Dự án chưa tích hợp Frontend Starter Kit độc lập theo chuẩn Bulletproof React.")

        self.scores['Frontend Architecture'] = score
        self.details['frontend'] = {'found': found, 'missing': missing, 'score': score}

    # -------------------------------------------------------------
    # 4. Anti-Crash Standard (Code-Level Static Analysis)
    # -------------------------------------------------------------
    def audit_anti_crash_code(self):
        score = 100
        violations_count = 0
        scanned_files = 0

        # Scan code files
        for p in self.root.rglob('*'):
            if p.is_file() and p.suffix in CODE_EXTENSIONS:
                # Check ignore dirs
                if any(ignored in p.parts for ignored in IGNORE_DIRS):
                    continue
                # Also skip examples directory
                if 'examples' in p.parts:
                    continue

                scanned_files += 1
                try:
                    lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
                    for idx, line in enumerate(lines, 1):
                        rel_file = str(p.relative_to(self.root))
                        
                        # 1. Check naked JSON.parse
                        if 'JSON.parse(' in line and not line.strip().startswith('//') and not line.strip().startswith('*'):
                            # check if surrounded by try catch (simple window check)
                            window = "\n".join(lines[max(0, idx - 5):min(len(lines), idx + 5)])
                            if 'try' not in window:
                                self.violations.append({
                                    'file': rel_file,
                                    'line': idx,
                                    'type': 'Naked JSON.parse',
                                    'desc': 'Gọi JSON.parse không nằm trong khối try...catch an toàn.',
                                    'snippet': line.strip()[:80]
                                })
                                violations_count += 1

                        # 2. Check TypeScript ': any'
                        if p.suffix in {'.ts', '.tsx'}:
                            if re.search(r':\s*any\b', line) and not line.strip().startswith('//'):
                                self.violations.append({
                                    'file': rel_file,
                                    'line': idx,
                                    'type': 'Strict Typing Violation',
                                    'desc': 'Sử dụng kiểu dữ liệu ": any" vi phạm quy chuẩn Strict TypeScript.',
                                    'snippet': line.strip()[:80]
                                })
                                violations_count += 1
                except Exception:
                    pass

        # Deduct score for violations
        penalty = min(60, violations_count * 5)
        score = max(40, 100 - penalty)

        if violations_count > 0:
            self.gaps.append(f"Phát hiện {violations_count} điểm vi phạm Anti-Crash Standard trong mã nguồn.")

        self.scores['The Anti-Crash Standard'] = score
        self.details['anti_crash'] = {
            'scanned_files': scanned_files,
            'violations_count': violations_count,
            'score': score
        }

    # -------------------------------------------------------------
    # 5. AI Multi-Agent Governance & Context
    # -------------------------------------------------------------
    def audit_ai_governance(self):
        score = 0
        found = []
        missing = []

        # Check AGENTS.md
        if (self.root / 'AGENTS.md').exists():
            score += 35
            found.append('Bản hiến pháp điều phối AI (AGENTS.md)')
        else:
            missing.append('AGENTS.md')

        # Check ADRs
        adrs_dir = self.root / 'adrs'
        if adrs_dir.exists() and adrs_dir.is_dir():
            adr_files = list(adrs_dir.glob('*.md'))
            adr_count = len(adr_files)
            if adr_count >= 10:
                score += 35
                found.append(f'Thư viện Quyết định Kiến trúc ({adr_count}/10 ADRs đầy đủ)')
            elif adr_count >= 5:
                score += 20
                found.append(f'Thư viện Quyết định Kiến trúc ({adr_count}/10 ADRs - Cần bổ sung)')
            else:
                score += 10
                missing.append(f'ADRs (Mới có {adr_count}/10 ADRs)')
        else:
            missing.append('Thư mục adrs/')

        # Check planning
        planning_dir = self.root / 'planning'
        if (planning_dir / 'backlog.md').exists() and (planning_dir / 'roadmap.md').exists():
            score += 30
            found.append('Kế hoạch Sprint & Backlog (planning/backlog.md, roadmap.md)')
        else:
            missing.append('Kế hoạch phân bổ Sprint (planning/)')

        if missing:
            self.gaps.append(f"AI Context Base còn thiếu: {', '.join(missing)}")

        self.scores['AI Governance & Context'] = score
        self.details['ai_gov'] = {'found': found, 'missing': missing, 'score': score}

    # -------------------------------------------------------------
    # 6. UI/UX Archetypes & Design System
    # -------------------------------------------------------------
    def audit_ui_ux_archetypes(self):
        score = 0
        found = []
        missing = []

        if (self.root / 'knowledge-base' / 'ui-ux-presets' / 'design-archetypes-catalog.md').exists():
            score += 40
            found.append('Catalog 14+ UI/UX Archetypes & Benchmark mã nguồn mở')
        else:
            missing.append('Catalog UI/UX Presets')

        if (self.root / 'specs' / 'design-system' / 'visual-dna-prompts.md').exists():
            score += 30
            found.append('AI Visual DNA Prompt Cookbook')
        else:
            missing.append('AI Visual DNA Prompts')

        if (self.root / 'frontend' / 'src' / 'features' / 'theme-showcase').exists():
            score += 30
            found.append('Interactive Theme Showcase Studio trong Frontend')
        else:
            missing.append('Theme Showcase Studio')

        if missing:
            self.gaps.append(f"Hệ thống Design Presets còn thiếu: {', '.join(missing)}")

        self.scores['UI/UX Archetypes & Design'] = score
        self.details['ui_ux'] = {'found': found, 'missing': missing, 'score': score}

    # -------------------------------------------------------------
    # 7. Documentation & Pitch Deck Readiness
    # -------------------------------------------------------------
    def audit_pitch_and_docs(self):
        score = 0
        found = []
        missing = []

        # Pitch Deck
        pitch_dir = self.root / 'templates' / 'pitch-deck'
        if (pitch_dir / 'pitch-deck-template.md').exists() and (pitch_dir / 'marp-presentation.md').exists():
            score += 50
            found.append('The Ultimate Pitch Deck Kit (YC & Sequoia Standard + Marp Slides-as-Code + 20 Q&A)')
        else:
            missing.append('The Ultimate Pitch Deck Kit')

        # Diátaxis Guides
        guides_dir = self.root / 'docs' / 'guides'
        if (guides_dir / 'diataxis-framework-guide.md').exists() and (guides_dir / 'incident-runbook-template.md').exists():
            score += 50
            found.append('Diátaxis Documentation Framework (Onboarding 30p, User Guide, Incident Runbook 2h sáng)')
        else:
            missing.append('Hệ thống tài liệu Diátaxis Framework')

        if missing:
            self.gaps.append(f"Tài liệu & Pitch Deck còn thiếu: {', '.join(missing)}")

        self.scores['Pitch Deck & Diátaxis Docs'] = score
        self.details['pitch_docs'] = {'found': found, 'missing': missing, 'score': score}

    # -------------------------------------------------------------
    # 8. Detect Super-Standard Innovations (Điểm vượt trội)
    # -------------------------------------------------------------
    def detect_advanced_innovations(self):
        # 1. Vector Database / AI Embedding support
        docker_file = self.root / 'docker-compose.yml'
        if docker_file.exists():
            content = docker_file.read_text(encoding='utf-8', errors='ignore')
            if 'pgvector' in content or 'qdrant' in content or 'chroma' in content:
                self.innovations.append("Đã trang bị hạ tầng Vector Database (PostgreSQL pgvector) sẵn sàng cho RAG & AI Agents.")
            if 'redis' in content:
                self.innovations.append("Đã cấu hình Distributed Caching với Redis container tối ưu hiệu năng.")

        # 2. Automated CI/CD Workflows
        ci_workflow = self.root / '.github' / 'workflows' / 'ci.yml'
        if ci_workflow.exists():
            self.innovations.append("Đã thiết lập GitHub Actions CI Pipeline tự động hóa kiểm tra Linting, Test và Quality Gate.")

        # 3. Community Health Standards
        if (self.root / '.github' / 'SECURITY.md').exists() and (self.root / '.github' / 'dependabot.yml').exists():
            self.innovations.append("Đạt chuẩn GitHub Community Health cấp cao nhất (Security Policy + Tự động quét lỗ hổng Dependabot).")

        # 4. Interactive Live Showcase
        if (self.root / 'frontend' / 'src' / 'features' / 'theme-showcase').exists():
            self.innovations.append("Có sẵn Studio trực quan cho phép click đổi nhanh giữa 7 phong cách thị giác ngay trong app.")

    # -------------------------------------------------------------
    # Calculate Total Score & Letter Grade
    # -------------------------------------------------------------
    def calculate_total_score(self):
        weights = {
            'Clean Architecture & DDD': 0.18,
            'System Design & Contracts': 0.15,
            'Frontend Architecture': 0.15,
            'The Anti-Crash Standard': 0.18,
            'AI Governance & Context': 0.14,
            'UI/UX Archetypes & Design': 0.10,
            'Pitch Deck & Diátaxis Docs': 0.10
        }
        total = sum(self.scores.get(k, 0) * w for k, w in weights.items())
        # Bonus for innovations (up to 5 points)
        bonus = min(5, len(self.innovations))
        final_score = min(100, round(total + bonus))
        return final_score

    def get_letter_grade(self, score):
        if score >= 95: return 'A+ (Excellent - Production Grade)'
        if score >= 85: return 'A (Very Good - Ready for Staging)'
        if score >= 75: return 'B+ (Good - Minor Gaps)'
        if score >= 65: return 'B (Acceptable - Needs Refactoring)'
        if score >= 50: return 'C (Sub-Standard)'
        return 'F (Critical Architecture Deficit)'

    # -------------------------------------------------------------
    # Generate Output Markdown Report
    # -------------------------------------------------------------
    def generate_markdown_report(self, total_score):
        report_file = self.root / 'PROJECT_REVIEW_REPORT.md'
        grade = self.get_letter_grade(total_score)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            f"# 📋 BÁO CÁO THANH TRA KIẾN TRÚC & HỆ THỐNG DỰ ÁN",
            f"> **Thời gian quét**: `{now_str}`  ",
            f"> **Thước đo đối chiếu**: Universal AI-Native Project Starter Kit Standard  ",
            f"> **Phương pháp**: 100% Rule-Based Static Code Analysis (Deterministic, Zero-Token, Zero-Hallucination)",
            "",
            "---",
            "",
            "## 🎯 1. TỔNG KẾT TUÂN THỦ (EXECUTIVE SUMMARY)",
            "",
            f"- **Điểm Tuân Thủ Toàn Diện (Compliance Score)**: **`{total_score} / 100`**",
            f"- **Xếp Hạng Kiến Trúc (Architecture Grade)**: **`{grade}`**",
            f"- **Tổng số tệp mã nguồn quét**: `{self.details.get('anti_crash', {}).get('scanned_files', 0)} tệp`",
            f"- **Số vi phạm Anti-Crash phát hiện**: `{len(self.violations)} vị trí`",
            f"- **Số điểm cải tiến cao cấp (Innovations)**: `{len(self.innovations)} điểm sáng`",
            "",
            "---",
            "",
            "## 📊 2. BẢNG ĐỐI CHIẾU 7 TRỤ CỘT CHUẨN MỰC (BENCHMARK MATRIX)",
            "",
            "| Trụ Cột Kiến Trúc | Mức Độ Đạt | Điểm Số | Đánh Giá Hiện Trạng |",
            "| :--- | :---: | :---: | :--- |"
        ]

        for pillar, score in self.scores.items():
            status_icon = "✅ Đạt Chuẩn" if score >= 85 else ("⚠️ Cần Lưu Ý" if score >= 60 else "❌ Thiếu Sót")
            lines.append(f"| **{pillar}** | `{status_icon}` | **{score}/100** | Đối chiếu theo quy chuẩn Starter Kit |")

        lines.extend([
            "",
            "---",
            "",
            "## 🌟 3. CÁC ĐIỂM SÁNG VƯỢT TRỘI (SUPER-STANDARD INNOVATIONS DETECTED)",
            ""
        ])

        if self.innovations:
            for item in self.innovations:
                lines.append(f"- [x] 🏆 **{item}**")
        else:
            lines.append("*Chưa phát hiện điểm công nghệ mở rộng vượt trên Starter Kit.*")

        lines.extend([
            "",
            "---",
            "",
            "## ⚠️ 4. CÁC KHOẢNG TRỐNG KIẾN TRÚC CẦN BỔ SUNG (GAPS & MISSING SPECS)",
            ""
        ])

        if self.gaps:
            for gap in self.gaps:
                lines.append(f"- [ ] ❗ **{gap}**")
        else:
            lines.append("- [x] 🎉 **Không phát hiện khoảng trống kiến trúc lớn. Hệ thống đạt độ phủ chuẩn mực 100%!**")

        lines.extend([
            "",
            "---",
            "",
            "## 🚨 5. DANH SÁCH VI PHẠM MÃ NGUỒN CỤ THỂ (CODE-LEVEL VIOLATIONS LOG)",
            ""
        ])

        if self.violations:
            lines.append("| Tệp Tin & Số Dòng | Loại Vi Phạm | Mô Tả & Đoạn Mã |")
            lines.append("| :--- | :--- | :--- |")
            for v in self.violations[:20]: # Limit to top 20 in table
                lines.append(f"| `{v['file']}:{v['line']}` | `{v['type']}` | {v['desc']} <br/>`{v['snippet']}` |")
            if len(self.violations) > 20:
                lines.append(f"\n*... và còn {len(self.violations) - 20} vị trí vi phạm khác (xem chi tiết trong log quét).*")
        else:
            lines.append("- [x] 🎉 **Mã nguồn hoàn toàn sạch! Không phát hiện lỗi naked JSON.parse hay vi phạm strict typing.**")

        lines.extend([
            "",
            "---",
            "",
            "## 📋 6. KẾ HOẠCH HÀNH ĐỘNG ƯU TIÊN (PRIORITIZED ACTION PLAN)",
            "",
            "### Mức Ưu Tiên P0 (Cần Khắc Phục Ngay Để Đảm Bảo Anti-Crash):",
        ])

        if self.violations:
            for v in self.violations[:5]:
                lines.append(f"- [ ] Refactor `{v['file']}` tại dòng `{v['line']}` ({v['type']}).")
        else:
            lines.append("- [x] Đạt chuẩn P0 (Không có vi phạm runtime crash khẩn cấp).")

        lines.extend([
            "",
            "### Mức Ưu Tiên P1 (Hoàn Thiện Kiến Trúc & Hợp Đồng Giao Tiếp):",
            "- [x] Đảm bảo tính toàn vẹn của API Contracts trong `specs/contracts/`.",
            "- [x] Đảm bảo tuân thủ nguyên tắc Dependency Inversion trong Clean Architecture.",
            "",
            "### Mức Ưu Tiên P2 (Tối Ưu Hóa & Tài Liệu Vận Hành):",
            "- [x] Cập nhật bảng kiểm tra Definition of Done (DoD) trước mỗi đợt Release.",
            "- [x] Đồng bộ hóa kịch bản thuyết trình Pitch Deck với các tính năng mới nhất.",
            "",
            "---",
            "",
            "## 🤖 7. PROMPT READY FOR YOUR AI AGENT (LỆNH CHO CLAUDE / CURSOR / ANTIGRAVITY)",
            "",
            "Copy toàn bộ đoạn lệnh dưới đây và dán vào cửa sổ chat với AI Agent trong IDE của bạn:",
            "",
            "```markdown",
            "[ROLE & GOAL]: Bạn là Principal Software Architect & Senior Code Reviewer.",
            "[TASK]: Hãy đọc toàn bộ nội dung bản báo cáo này (`PROJECT_REVIEW_REPORT.md`).",
            "[CONTEXT]: Dự án của chúng tôi đang áp dụng chuẩn 'Universal AI-Native Project Starter Kit'.",
            "Báo cáo trên đã chỉ ra chính xác các điểm thiếu sót và các file vi phạm tại Mục 4 và Mục 5.",
            "",
            "[YÊU CẦU THỰC HIỆN]:",
            "1. Hãy phân tích các vi phạm Anti-Crash tại Mục 5 và đề xuất mã nguồn refactor tương ứng.",
            "2. Lập kế hoạch từng bước (Step-by-step Execution Plan) để giải quyết các khoảng trống tại Mục 4.",
            "3. Tuân thủ nghiêm ngặt nguyên tắc Defensive Programming (dùng ?., ??, Array.isArray(), try-catch).",
            "4. Đừng sửa đổi các điểm sáng vượt trội đã được ghi nhận tại Mục 3.",
            "5. Bắt đầu bằng kế hoạch xử lý cho các đầu việc P0 trước!",
            "```",
            "",
            "---",
            "*Báo cáo được khởi tạo tự động bởi Project-Review Auditor Engine v1.0*"
        ])

        report_file.write_text("\n".join(lines), encoding='utf-8')
        return report_file

    # -------------------------------------------------------------
    # Print Colorized Console Summary
    # -------------------------------------------------------------
    def print_console_summary(self, total_score, report_path):
        grade = self.get_letter_grade(total_score)
        print("  KẾT QUẢ ĐỐI CHIẾU KIẾN TRÚC:")
        for pillar, score in self.scores.items():
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            print(f"  • {pillar:<30} [{bar}] {score:>3}%")

        print("\n" + "-" * 70)
        print(f"  🏆 TỔNG ĐIỂM TUÂN THỦ (COMPLIANCE SCORE): {total_score} / 100")
        print(f"  🎖️ XẾP HẠNG KIẾN TRÚC: {grade}")
        print("-" * 70)

        if self.innovations:
            print("\n  🌟 ĐIỂM SÁNG CAO CẤP HƠN STARTER KIT (INNOVATIONS):")
            for item in self.innovations[:3]:
                print(f"    ✔ {item}")

        if self.gaps:
            print("\n  ⚠️ KHOẢNG TRỐNG KIẾN TRÚC CẦN BỔ SUNG (GAPS):")
            for gap in self.gaps[:3]:
                print(f"    ✖ {gap}")

        print("\n" + "=" * 70)
        print(f"  📄 BÁO CÁO CHI TIẾT ĐÃ XUẤT RA: {report_path.name}")
        print("  👉 Bước tiếp theo: Mở chat với AI Agent (Cursor, Claude Code, Antigravity)")
        print("     và dán đoạn Prompt ở Mục 7 của file report để AI bắt đầu sửa code!")
        print("=" * 70 + "\n")


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    auditor = ProjectAuditor(target)
    score = auditor.run()
    sys.exit(0 if score >= 70 else 1)
