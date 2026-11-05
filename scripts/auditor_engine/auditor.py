"""Điều phối thẩm định, chấm điểm và xuất báo cáo."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .tree import ProjectTree
from .profiler import ProjectProfiler
from .pillars_docs import DocsPillarsMixin
from .pillars_app import AppPillarsMixin
from .pillars_infra import InfraPillarsMixin


class ProjectAuditor(DocsPillarsMixin, AppPillarsMixin, InfraPillarsMixin):
    """Hệ thống thẩm định kiến trúc mã nguồn thích ứng (Dynamic Context-Aware Auditor)."""

    def __init__(self, root_dir='.'):

        self.root = Path(root_dir).resolve()

        self.tree = ProjectTree(self.root)

        self.profiler = ProjectProfiler(self.root, self.tree)

        self.profile = {}

        self.tools = set()

        self.databases = set()

        self.scores = {}

        self.gaps = []

        self.bloat = []

        self.innovations = []

        self.violations = []

        self.details = {}

        self.active_pillars = []

        self.all_pillars = []

        self.scan_logs = []

        self.report_path = None

    def add_log(self, text, stage='general', log_type='info'):
        import datetime
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.scan_logs.append({
            'time': timestamp,
            'stage': stage,
            'text': f'[{timestamp}] {text}',
            'type': log_type
        })

    def run(self, progress_callback=None):
        import time

        def cb(pct, msg):
            if progress_callback:
                progress_callback(pct, msg)
                time.sleep(0.01)

        self.add_log("Khởi động bộ máy đo kiểm Universal Project Auditor...", "init", "info")
        self.add_log(f"Khảo sát thư mục dự án: {self.root}", "init", "muted")

        cb(5, "Đang phân tích TECH STACK & nhận diện bản sắc dự án...")
        self.profile = self.profiler.profile()
        self.tools = set(self.profile.get('tools', []))
        self.databases = set(self.profile.get('databases', []))

        total_files = len(self.tree.all_files)
        code_files = len(self.tree.code_files)
        self.add_log(f"Lập chỉ mục ProjectTree siêu tốc: Đã duyệt {total_files} tệp tin ({code_files} tệp mã nguồn).", "indexing", "info")
        self.add_log(f"Nhận diện Archetype: {self.profile.get('archetype')}", "profiling", "info")
        if self.profile.get('languages'):
            langs = ", ".join(self.profile.get('languages'))
            fws = ", ".join(self.profile.get('frameworks', [])) or "None"
            self.add_log(f"Tech Stack nhận diện: Ngôn ngữ [{langs}] | Frameworks [{fws}]", "profiling", "muted")

        # Danh sách các bước thẩm định thích ứng theo đúng bản sắc đã phát hiện
        steps = [
            ("Readme & Onboarding", 15, self.audit_readme_and_onboarding, "readme", "Khảo sát tài liệu dự án (README & ONBOARDING)"),
        ]

        if self.profile.get('has_backend') or not self.profile.get('has_frontend'):
            steps.append(("Backend & Core Flow", 28, self.audit_backend_waterflow, "backend", "Thẩm định kiến trúc BACKEND & luồng dữ liệu CORE"))

        if self.profile.get('has_frontend'):
            steps.append(("Frontend & UI/UX", 42, self.audit_frontend_waterflow, "frontend", "Thẩm định kiến trúc FRONTEND & DESIGN SYSTEM (UI/UX)"))

        if self.profile.get('has_database'):
            steps.append(("Database & Query Safety", 55, self.audit_database_waterflow, "database", "Thẩm định DATABASE, MIGRATION & an toàn QUERY"))

        if self.profile.get('has_security'):
            steps.append(("Bảo Mật & Chuỗi Cung Ứng", 65, self.audit_security_and_supply_chain, "security", "Thẩm định BẢO MẬT & CHUỖI CUNG ỨNG (SECURITY)"))

        if self.profile.get('has_cloud'):
            steps.append(("Hạ Tầng Cloud & DevOps", 75, self.audit_cloud_and_container, "cloud", "Thẩm định HẠ TẦNG CLOUD & CONTAINER (DEVOPS)"))

        if self.profile.get('has_microservices'):
            steps.append(("Hệ Thống Phân Tán & Gateway", 82, self.audit_microservices_and_gateway, "microservices", "Thẩm định HỆ THỐNG PHÂN TÁN & GATEWAY (MICROSERVICES)"))

        if self.profile.get('has_data_caching'):
            steps.append(("Kỹ Thuật Dữ Liệu & Cache", 88, self.audit_data_and_caching, "data_caching", "Thẩm định KỸ THUẬT DỮ LIỆU & CACHE (DATA RESILIENCY)"))

        if self.profile.get('has_observability'):
            steps.append(("Giám Sát & Vận Hành", 92, self.audit_observability_and_ops, "observability", "Thẩm định GIÁM SÁT & VẬN HÀNH (OBSERVABILITY & OPS)"))

        steps.append(("Runtime Anti-Crash", 95, self.audit_anti_crash_universal, "anticrash", "Kiểm tra an toàn RUNTIME & tiêu chuẩn ANTI-CRASH"))

        if self.profile.get('has_agent_ecosystem'):
            steps.append(("Hệ Sinh Thái AI Agent", 96, self.audit_agent_ecosystem, "agent_ecosystem", "Thẩm định HỆ SINH THÁI AI AGENT (RULES, SKILLS & WORKFLOWS)"))

        steps.append(("Hồ Sơ Kiến Trúc & Hợp Đồng API", 98, self.audit_architecture_docs_and_ai, "contracts", "Rà soát HỒ SƠ KIẾN TRÚC & HỢP ĐỒNG API"))
        steps.append(("Gap Analysis", 99, self.benchmark_starter_kit, "starter_kit", "Phân tích khoảng cách (GAP ANALYSIS) so với STARTER KIT"))

        total_scan_steps = len(steps)
        for idx, (short_name, pct, fn, pillar_key, desc) in enumerate(steps, 1):
            cb(pct, f"Đang thẩm định [{idx}/{total_scan_steps}]: {desc}...")
            self.add_log(f"[{idx}/{total_scan_steps}] {desc}...", pillar_key, "info")
            try:
                fn()
            except Exception as e:
                print(f"[AUDIT ERROR in {desc}]: {e}", file=sys.stderr)
                self.add_log(f"  -> [LỖI]: {str(e)}", pillar_key, "error")

        total_score = self.calculate_total_score()
        self.report_path = self.generate_markdown_report(total_score)
        grade = self.get_letter_grade(total_score)

        self.add_log("----------------------------------------------------------------", "finish", "muted")
        self.add_log(f"✓ HOÀN THÀNH ĐO KIỂM TOÀN DIỆN! TỔNG ĐIỂM: {total_score}/100 [HẠNG: {grade}]", "finish", "success")
        self.add_log(f"Tệp báo cáo lưu tại: {self.report_path}", "finish", "info")
        self.add_log("✓ Quá trình quét hoàn tất thành công. Bạn có thể nhấn 'Xem Kết Quả Tổng Quan' hoặc chọn hạng mục bên trái để xem chi tiết.", "finish", "info")

        cb(100, f"Đã hoàn thành thẩm định! Báo cáo: {self.report_path.name}")
        return total_score

    def benchmark_starter_kit(self):

        # 1. Nhận diện Ưu điểm vượt trội (Strengths / Innovations)

        if 'VECTOR DATABASE (AI RAG)' in self.profile.get('databases', []):

            self.innovations.append("Trang bị hạ tầng VECTOR DATABASE sẵn sàng cho AI RAG & SEMANTIC SEARCH.")

        if 'REDIS (DISTRIBUTED CACHE)' in self.profile.get('databases', []):

            self.innovations.append("Cấu hình DISTRIBUTED CACHE với REDIS tối ưu tốc độ phản hồi.")

        if any('.github' in p.parts and 'workflows' in p.parts for p in self.tree.all_files):

            self.innovations.append("Tự động hóa QUALITY GATE & CI/CD PIPELINE với GITHUB ACTIONS.")

        if bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')):

            self.innovations.append("Chuẩn hóa môi trường phát triển nhất quán với DOCKER COMPOSE.")

        if self.details.get('frontend', {}).get('found'):

            if any('DESIGN TOKENS' in f for f in self.details['frontend']['found']):

                self.innovations.append("Hệ thống DESIGN SYSTEM & UI TOKENS độc quyền được thiết kế bài bản.")

        if self.details.get('security', {}).get('found'):

            if any('DEPENDENCY LOCKFILE' in f for f in self.details['security']['found']):

                self.innovations.append("Bảo vệ chuỗi cung ứng mã nguồn chặt chẽ qua DEPENDENCY LOCKFILE.")
        if self.details.get('agent_ecosystem', {}).get('found'):
            self.innovations.append("Chuẩn hóa hệ sinh thái AI AGENT (HIẾN PHÁP AGENTS.MD, SKILLS & WORKFLOWS) đón đầu kỷ nguyên Agentic AI.")

        # 2. Nhận diện Thừa / Rác / Rủi ro (Bloat & Redundancies)

        env_files = self.tree.find_by_name('.env')

        for ef in env_files:

            self.bloat.append(f"Tệp cấu hình nhạy cảm (.ENV) đang bị Git theo dõi: `{ef.relative_to(self.root)}` (Nguy cơ rò rỉ thông tin bảo mật).")

        if not (self.root / '.gitignore').exists():

            self.bloat.append("Dự án chưa có tệp `.gitignore` để loại trừ các tệp tạm và artifacts BUILD.")

        for junk_dir in ['dist', 'build', 'bin', 'obj', '.next', '__pycache__']:

            if (self.root / junk_dir).exists() and not (self.root / '.gitignore').exists():

                self.bloat.append(f"Thư mục cache BUILD `{junk_dir}/` có nguy cơ bị đưa lên remote git.")

    def calculate_total_score(self):
        total_earned = 0
        total_max = 0
        self.active_pillars = []
        self.all_pillars = []

        # 12 Hạng mục tiêu chuẩn toàn diện theo chuẩn Architecture
        candidate_pillars = [
            ('readme', 'Readme & Onboarding', 15),
            ('backend', 'Backend & Core Flow', 20),
            ('frontend', 'Frontend & UI/UX', 20),
            ('database', 'Database & Query Safety', 15),
            ('security', 'Bảo Mật & Chuỗi Cung Ứng', 15),
            ('cloud', 'Hạ Tầng Cloud & DevOps', 15),
            ('microservices', 'Hệ Thống Phân Tán & Gateway', 15),
            ('data_caching', 'Kỹ Thuật Dữ Liệu & Cache', 15),
            ('observability', 'Giám Sát & Vận Hành', 15),
            ('anticrash', 'Runtime Anti-Crash', 20),
            ('agent_ecosystem', 'Hệ Sinh Thái AI Agent', 15),
            ('contracts', 'Hồ Sơ Kiến Trúc & Hợp Đồng API', 10),
        ]

        for key, default_name, default_max in candidate_pillars:
            detail = self.details.get(key)
            if detail and not detail.get('is_na'):
                raw_score = detail.get('score', 0)
                max_pts = detail.get('max_points', default_max)
                earned = round((raw_score / 100.0) * max_pts)
                detail['points_earned'] = earned
                detail['max_points'] = max_pts
                total_earned += earned
                total_max += max_pts

                pillar_obj = {
                    'key': key,
                    'name': detail.get('name', default_name),
                    'score': earned,
                    'max': max_pts,
                    'raw_score': raw_score,
                    'ratio': (raw_score / 100.0) if max_pts > 0 else 0,
                    'found': detail.get('found', []),
                    'missing': detail.get('missing', []),
                    'is_na': False
                }
                self.active_pillars.append(pillar_obj)
                self.all_pillars.append(pillar_obj)
            else:
                pillar_obj = {
                    'key': key,
                    'name': default_name,
                    'score': 0,
                    'max': default_max,
                    'raw_score': 0,
                    'ratio': 0,
                    'found': [],
                    'missing': ['Hạng mục này không áp dụng cho cấu trúc dự án hiện tại'],
                    'is_na': True
                }
                self.all_pillars.append(pillar_obj)

        if total_max > 0:
            normalized_score = round((total_earned / total_max) * 100)
        else:
            normalized_score = 0

        bonus = min(5, len(self.innovations))
        final_score = min(100, normalized_score + bonus)
        return final_score

    def get_letter_grade(self, score):

        if score >= 95: return 'A+ (XUẤT SẮC - SẴN SÀNG PRODUCTION)'

        if score >= 85: return 'A (RẤT TỐT - SẴN SÀNG STAGING)'

        if score >= 75: return 'B+ (TỐT - CÒN MỘT SỐ TECHNICAL DEBT NHỎ)'

        if score >= 65: return 'B (CHẤP NHẬN ĐƯỢC - CẦN REFACTOR)'

        if score >= 50: return 'C (DƯỚI CHUẨN TIÊU CHÍ)'

        return 'F (CẦN TÁI CẤU TRÚC KIẾN TRÚC TOÀN DIỆN)'

    def get_ai_prompt(self):

        return (

            "[ROLE & GOAL]: Bạn là PRINCIPAL SOFTWARE ARCHITECT & SENIOR CODE REVIEWER.\n"

            f"[TASK]: Hãy đọc toàn bộ nội dung bản báo cáo này (`{self.report_path.name if self.report_path else 'PROJECT_REVIEW_REPORT.md'}`).\n"

            f"[CONTEXT DỰ ÁN]:\n"

            f"- Loại hình dự án: {self.profile.get('archetype')}\n"

            f"- TECH STACK nhận diện: {', '.join(self.profile.get('languages', []))} | {', '.join(self.profile.get('frameworks', []))}\n"

            f"- Phong cách ARCHITECTURE: {self.profile.get('arch_style')}\n\n"

            "[YÊU CẦU THỰC HIỆN]:\n"

            "1. Phân tích và refactor ngay các vị trí vi phạm ANTI-CRASH tại Mục 6 (P0 PRIORITY).\n"

            "2. Lên phương án xử lý các tiêu chí kiến trúc chưa đạt tại Mục 4 theo đúng bản sắc của dự án.\n"

            "3. Dọn dẹp các tệp cấu hình thừa hoặc rủi ro bảo mật chỉ ra tại Mục 5.\n"

            "4. Giữ nguyên và tối ưu hóa các điểm sáng công nghệ đã được ghi nhận tại Mục 3."

        )

    def generate_markdown_report(self, total_score):

        report_file = self.root / 'PROJECT_REVIEW_REPORT.md'

        grade = self.get_letter_grade(total_score)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [

            f"# 📋 BÁO CÁO BENCHMARK KIẾN TRÚC & ĐỐI CHIẾU CHUẨN MỰC DỰ ÁN",

            f"> **Thời gian benchmark**: `{now_str}`  ",

            f"> **Loại hình dự án**: `{self.profile.get('archetype')}`  ",

            f"> **Phương pháp**: 100% RULE-BASED DEEP WATERFLOW TRAVERSAL (ZERO-TOKEN, ZERO-HALLUCINATION)",

            "",

            "---",

            "",

            "## 🎯 1. HỒ SƠ DỰ ÁN & TỔNG KẾT BENCHMARK (PROJECT PROFILE & EXECUTIVE SUMMARY)",

            "",

            f"- **Điểm Benchmark Toàn Diện (BENCHMARK SCORE)**: **`{total_score} / 100`**",

            f"- **Xếp Hạng Kiến Trúc (ARCHITECTURE GRADE)**: **`{grade}`**",

            f"- **TECH STACK Nhận Diện**: {', '.join(self.profile.get('languages', ['UNKNOWN']))} ({', '.join(self.profile.get('frameworks', ['STANDARD']))})",

            f"- **DATABASE & Hạ Tầng**: {', '.join(self.profile.get('databases', ['NONE']))} | {', '.join(self.profile.get('tools', ['LOCAL']))}",

            f"- **Phong Cách Kiến Trúc**: **{self.profile.get('arch_style')}**",

            f"- **Tổng số tệp mã nguồn quét sâu**: `{self.details.get('anticrash', {}).get('scanned_files', 0)} tệp`",

            "",

            "---",

            "",

            "## 📊 2. BẢNG ĐỐI CHIẾU CÁC HẠNG MỤC BENCHMARK (BENCHMARK MATRIX)",

            "",

            "| Hạng Mục Benchmark | Trạng Thái | Điểm Hệ Số | Trọng Số Tối Đa | Đánh Giá Chi Tiết |",

            "| :--- | :---: | :---: | :---: | :--- |"

        ]

        for p in self.active_pillars:

            score_val = p.get('score', 0)

            max_val = p.get('max', 20)

            ratio = p.get('ratio', 0)

            status_icon = "✅ ĐẠT CHUẨN" if ratio >= 0.8 else ("⚠️ CẦN LƯU Ý" if ratio >= 0.5 else "❌ NGUY CƠ CAO")

            pts_str = f"**{score_val} ĐIỂM**"

            max_str = f"{max_val} Điểm"

            eval_str = f"Hoàn thành {len(p.get('found', []))} tiêu chí / Thiếu {len(p.get('missing', []))} tiêu chí"

            lines.append(f"| **{p.get('name')}** | `{status_icon}` | {pts_str} | {max_str} | {eval_str} |")

        lines.extend([

            "",

            "---",

            "",

            "## 🌟 3. DỰ ÁN CÓ ƯU ĐIỂM GÌ? (STRENGTHS & INNOVATIONS)",

            ""

        ])

        if self.innovations:

            for item in self.innovations:

                lines.append(f"- [x] 🏆 **{item}**")

        else:

            lines.append("*Dự án đang vận hành ở mức cơ bản, chưa phát hiện cấu hình công nghệ mở rộng.*")

        lines.extend([

            "",

            "---",

            "",

            "## ⚠️ 4. DỰ ÁN ĐANG THIẾU GÌ? (MISSING GAPS)",

            ""

        ])

        if self.gaps:

            for gap in self.gaps:

                lines.append(f"- [ ] ❗ **{gap}**")

        else:

            lines.append("- [x] 🎉 **Không phát hiện thiếu sót kiến trúc lớn. Hệ thống đạt độ phủ chuẩn mực!**")

        lines.extend([

            "",

            "---",

            "",

            "## 🧹 5. DỰ ÁN ĐANG THỪA / RÁC GÌ? (BLOAT & RISKS)",

            ""

        ])

        if self.bloat:

            for b in self.bloat:

                lines.append(f"- [ ] 🗑️ **{b}**")

        else:

            lines.append("- [x] 🍃 **Mã nguồn sạch sẽ, không có tệp thừa hoặc rác build lọt vào Git.**")

        lines.extend([

            "",

            "---",

            "",

            "## 🚨 6. CHI TIẾT VI PHẠM MÃ NGUỒN CỤ THỂ (ANTI-CRASH VIOLATIONS)",

            ""

        ])

        if self.violations:

            for v in self.violations:

                lines.append(f"- **`{v.get('type')}`** tại `{v.get('file')}:{v.get('line')}`: {v.get('desc')}")

                if v.get('snippet'):

                    lines.append(f"  ```\n  {v.get('snippet')}\n  ```")

        else:

            lines.append("- [x] 🛡️ **0 phát hiện vi phạm quy tắc Anti-Crash trên toàn bộ cây thư mục.**")

        report_file.write_text("\n".join(lines), encoding='utf-8')

        return report_file
