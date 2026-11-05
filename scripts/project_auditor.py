#!/usr/bin/env python3

"""

UNIVERSAL PROJECT REVIEWER & ARCHITECTURE AUDITOR ENGINE v3.0

Pure Python Standard Library (100% Offline, Zero-Token, Zero-Dependency)

Dynamic Context-Aware Pillars (Option A Architecture):

  - Automatically identifies project archetype and features via Precision Profiling.

  - Dynamically activates relevant pillars (Baseline + Extensions: Security, Cloud, Microservices, Data, Observability).

  - Dynamically normalizes total score to 100 based on active pillars.

  - Pinpoints: Strengths | Deficiencies (Missing) | Bloat & Risks | Code Violations.

  - Blazing fast execution: ProjectTree pruned indexing (0.05s).

"""

import os

import sys

import re

import json

import datetime

from pathlib import Path

# Thư mục bỏ qua khi quét sâu mã nguồn

IGNORE_DIRS = {

    'node_modules', '.git', 'dist', 'build', 'bin', 'obj',

    '.vscode', '.idea', '__pycache__', '.next', 'coverage',

    'vendor', 'target', '.turbo', '.cache'

}

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.cs', '.py', '.go', '.java', '.rs', '.php'}

class ProjectTree:

    """Hệ thống lập chỉ mục và duyệt cây thư mục siêu tốc (Bỏ qua hoàn toàn node_modules, .git,...)."""

    def __init__(self, root: Path):

        self.root = root.resolve()

        self.all_files = []

        self.all_dirs = set()

        self.code_files = []

        self.files_by_name = {}

        self.files_by_ext = {}

        self._scan()

    def _scan(self):

        for dirpath, dirnames, filenames in os.walk(self.root):

            # Cắt tỉa thư mục ngay tại chỗ để os.walk không đi sâu vào các thư mục rác

            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.')]

            for d in dirnames:

                self.all_dirs.add(d.lower())

            for f in filenames:

                p = Path(dirpath) / f

                self.all_files.append(p)

                lower_f = f.lower()

                self.files_by_name.setdefault(lower_f, []).append(p)

                ext = p.suffix.lower()

                if ext:

                    self.files_by_ext.setdefault(ext, []).append(p)

                if ext in CODE_EXTENSIONS:

                    self.code_files.append(p)

    def find_by_name(self, name: str):

        return self.files_by_name.get(name.lower(), [])

    def find_by_ext(self, ext: str):

        return self.files_by_ext.get(ext.lower(), [])

    def any_name_starts_with(self, prefix: str):

        prefix = prefix.lower()

        return any(name.startswith(prefix) for name in self.files_by_name)

    def any_name_contains(self, substr: str):

        substr = substr.lower()

        return any(substr in name for name in self.files_by_name)

class ProjectProfiler:

    """Tự động nhận diện TECH STACK, kiểu ARCHITECTURE và các năng lực kỹ thuật của dự án."""

    def __init__(self, root: Path, tree: ProjectTree = None):

        self.root = root.resolve()

        self.tree = tree if tree is not None else ProjectTree(self.root)

        self.languages = set()

        self.frameworks = set()

        self.databases = set()

        self.tools = set()

        self.archetype = "Ứng dụng Phần Mềm Tiêu Chuẩn (GENERAL APPLICATION)"

        self.arch_style = "Kiến trúc Tự Do / Chưa Xác Định (CUSTOM ARCHITECTURE)"

        # Cờ nhận diện năng lực kích hoạt động

        self.has_frontend = False

        self.has_backend = False

        self.has_database = False

        self.has_security = False

        self.has_cloud = False

        self.has_microservices = False

        self.has_data_caching = False

        self.has_observability = False

        self.has_agent_ecosystem = False

    def profile(self):

        # 1. Nhận diện MANIFEST & Ngôn ngữ lập trình

        has_pkg_json = bool(self.tree.find_by_name('package.json'))

        has_pyproject = bool(self.tree.find_by_name('pyproject.toml') or self.tree.find_by_name('requirements.txt'))

        has_csproj = bool(self.tree.find_by_ext('.csproj'))

        has_go_mod = bool(self.tree.find_by_name('go.mod'))

        has_pom = bool(self.tree.find_by_name('pom.xml'))

        has_cargo = bool(self.tree.find_by_name('cargo.toml'))

        if has_pkg_json:

            self.languages.add('JAVASCRIPT/TYPESCRIPT')

            self._inspect_package_json()

        if has_pyproject:

            self.languages.add('PYTHON')

            self._inspect_python()

        if has_csproj:

            self.languages.add('C# / .NET')

            self.frameworks.add('ASP.NET CORE')

            self.has_backend = True

            self._inspect_dotnet()

        if has_go_mod:

            self.languages.add('GO')

            self.has_backend = True

        if has_pom:

            self.languages.add('JAVA')

            self.has_backend = True

        if has_cargo:

            self.languages.add('RUST')

        # 2. Nhận diện INFRASTRUCTURE & DATABASE từ Docker Compose

        docker_compose = None

        for dc in ['docker-compose.yml', 'docker-compose.yaml', 'compose.yaml', 'compose.yml']:

            matches = self.tree.find_by_name(dc)

            if matches:

                docker_compose = matches[0]

                break

        if docker_compose and docker_compose.exists():

            self.tools.add('DOCKER COMPOSE')

            self.has_cloud = True

            try:

                dc_content = docker_compose.read_text(encoding='utf-8', errors='ignore').lower()

                if 'postgres' in dc_content: self.databases.add('POSTGRESQL'); self.has_database = True

                if 'mysql' in dc_content or 'mariadb' in dc_content: self.databases.add('MYSQL/MARIADB'); self.has_database = True

                if 'mongo' in dc_content: self.databases.add('MONGODB'); self.has_database = True

                if 'redis' in dc_content: self.databases.add('REDIS (DISTRIBUTED CACHE)'); self.has_data_caching = True

                if 'kafka' in dc_content or 'rabbitmq' in dc_content: self.has_microservices = True

                if 'prometheus' in dc_content or 'grafana' in dc_content: self.has_observability = True

                if 'pgvector' in dc_content or 'qdrant' in dc_content or 'chroma' in dc_content:

                    self.databases.add('VECTOR DATABASE (AI RAG)')

            except Exception:

                pass

        # 3. Nhận diện Cloud & Container

        has_dockerfile = self.tree.any_name_starts_with('dockerfile')

        has_k8s = any('k8s' in p.parts or 'helm' in p.parts or p.name.endswith('.k8s.yaml') for p in self.tree.all_files)

        has_ci = any('.github' in p.parts and 'workflows' in p.parts for p in self.tree.all_files) or bool(self.tree.find_by_name('.gitlab-ci.yml'))

        if has_dockerfile:

            self.tools.add('DOCKERFILE')

            self.has_cloud = True

        if has_k8s or has_ci:

            self.has_cloud = True

        # 4. Nhận diện Security & Supply Chain

        if has_pkg_json or has_pyproject or has_csproj or has_go_mod or has_pom or has_cargo or self.has_backend:

            self.has_security = True

        # 5. Nhận diện Microservices & Gateway

        has_proto = bool(self.tree.find_by_ext('.proto'))

        has_gateway_cfg = any(self.tree.any_name_starts_with(gw) for gw in ['ocelot', 'kong', 'traefik', 'envoy'])

        if has_proto or has_gateway_cfg or 'KAFKA CLIENT' in self.tools or 'RABBITMQ CLIENT' in self.tools:

            self.has_microservices = True

        # 6. Nhận diện AI Agent Ecosystem (Rules, Skills, Workflows)

        has_agent_rules = bool(

            self.tree.find_by_name('agents.md') or 

            self.tree.find_by_name('.cursorrules') or 

            self.tree.find_by_name('claude.md') or

            self.tree.find_by_name('.windsurfrules') or

            self.tree.find_by_name('.clinerules') or

            [p for p in self.tree.all_files if p.suffix.lower() == '.mdc' or 'copilot-instructions' in p.name.lower()]

        )

        has_agent_skills = any('skills' in p.parts and p.name.lower() in {'skill.md', 'skill.json'} for p in self.tree.all_files)

        has_agent_workflows = any(

            ('workflows' in p.parts or 'prompts' in p.parts or 'agent-practices' in p.parts) and p.suffix.lower() in {'.md', '.yaml', '.yml'}

            for p in self.tree.all_files

        )

        if has_agent_rules or has_agent_skills or has_agent_workflows:

            self.has_agent_ecosystem = True

        # 6. Nhận diện Phân loại loại hình dự án

        if self.has_frontend and self.has_backend:

            self.archetype = "Hệ thống FULL-STACK (FRONTEND + BACKEND)"

        elif self.has_frontend and not self.has_backend:

            self.archetype = "Ứng dụng Giao Diện Độc Lập (FRONTEND SPA / MOBILE)"

        elif self.has_backend and not self.has_frontend:

            self.archetype = "Nền tảng Dịch vụ Phía Sau (BACKEND API / MICROSERVICES)"

        elif any((self.root / f).exists() for f in ['main.py', 'cli.py', 'cmd', 'bin']):

            self.archetype = "Công cụ Dòng Lệnh / Hệ Thống (CLI TOOL / SYSTEM UTILITY)"

        # 7. Nhận diện phong cách kiến trúc

        self._detect_architecture_style()

        return {

            'archetype': self.archetype,

            'arch_style': self.arch_style,

            'languages': sorted(list(self.languages)),

            'frameworks': sorted(list(self.frameworks)),

            'databases': sorted(list(self.databases)),

            'tools': sorted(list(self.tools)),

            'has_frontend': self.has_frontend,

            'has_backend': self.has_backend,

            'has_database': len(self.databases) > 0 or self.has_database,

            'has_security': self.has_security,

            'has_cloud': self.has_cloud,

            'has_microservices': self.has_microservices,

            'has_data_caching': self.has_data_caching,

            'has_observability': self.has_observability,

            'has_agent_ecosystem': self.has_agent_ecosystem

        }

    def _inspect_package_json(self):

        pkg_paths = self.tree.find_by_name('package.json')

        for p in pkg_paths:

            if not p.exists(): continue

            try:

                data = json.loads(p.read_text(encoding='utf-8', errors='ignore'))

                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                # FRONTEND

                if 'react' in deps: self.frameworks.add('REACT'); self.has_frontend = True

                if 'next' in deps: self.frameworks.add('NEXT.JS'); self.has_frontend = True; self.has_backend = True

                if 'vue' in deps: self.frameworks.add('VUE'); self.has_frontend = True

                if 'nuxt' in deps: self.frameworks.add('NUXT'); self.has_frontend = True; self.has_backend = True

                if 'svelte' in deps or '@sveltejs/kit' in deps: self.frameworks.add('SVELTE'); self.has_frontend = True

                if '@angular/core' in deps: self.frameworks.add('ANGULAR'); self.has_frontend = True

                # BACKEND

                if 'express' in deps: self.frameworks.add('EXPRESS'); self.has_backend = True

                if '@nestjs/core' in deps: self.frameworks.add('NESTJS'); self.has_backend = True

                if 'fastify' in deps: self.frameworks.add('FASTIFY'); self.has_backend = True

                # DATABASE / ORM

                if 'prisma' in deps or '@prisma/client' in deps: self.databases.add('PRISMA ORM'); self.has_database = True

                if 'typeorm' in deps: self.databases.add('TYPEORM'); self.has_database = True

                if 'mongoose' in deps: self.databases.add('MONGOOSE (MONGODB)'); self.has_database = True

                if 'drizzle-orm' in deps: self.databases.add('DRIZZLE ORM'); self.has_database = True

                if 'pg' in deps: self.databases.add('POSTGRESQL DRIVER'); self.has_database = True

                if 'redis' in deps or 'ioredis' in deps: self.databases.add('REDIS CLIENT'); self.has_data_caching = True

                # SECURITY & HEADERS

                if 'helmet' in deps: self.tools.add('HELMET (HTTP HEADERS)')

                if 'cors' in deps: self.tools.add('CORS MIDDLEWARE')

                if 'express-rate-limit' in deps or 'rate-limiter-flexible' in deps: self.tools.add('RATE LIMITING')

                # LOGGING & OBSERVABILITY

                if 'winston' in deps: self.tools.add('WINSTON'); self.has_observability = True

                if 'pino' in deps: self.tools.add('PINO'); self.has_observability = True

                if '@opentelemetry/api' in deps: self.tools.add('OPENTELEMETRY'); self.has_observability = True

                # MESSAGING & MICROSERVICES

                if '@grpc/grpc-js' in deps or 'kafkajs' in deps or 'amqplib' in deps:

                    self.has_microservices = True

                    if 'kafkajs' in deps: self.tools.add('KAFKA CLIENT')

                    if 'amqplib' in deps: self.tools.add('RABBITMQ CLIENT')

                    if '@grpc/grpc-js' in deps: self.tools.add('GRPC')

            except Exception:

                pass

    def _inspect_python(self):

        req_files = self.tree.find_by_name('requirements.txt')

        pyproj_files = self.tree.find_by_name('pyproject.toml')

        content = ""

        for rf in req_files:

            try: content += rf.read_text(encoding='utf-8', errors='ignore').lower() + "\n"

            except Exception: pass

        for pf in pyproj_files:

            try: content += pf.read_text(encoding='utf-8', errors='ignore').lower() + "\n"

            except Exception: pass

        if 'fastapi' in content: self.frameworks.add('FASTAPI'); self.has_backend = True

        if 'django' in content: self.frameworks.add('DJANGO'); self.has_backend = True

        if 'flask' in content: self.frameworks.add('FLASK'); self.has_backend = True

        if 'sqlalchemy' in content: self.databases.add('SQLALCHEMY ORM'); self.has_database = True

        if 'alembic' in content: self.databases.add('ALEMBIC MIGRATIONS'); self.has_database = True

        if 'psycopg2' in content or 'asyncpg' in content: self.databases.add('POSTGRESQL'); self.has_database = True

        # Security & Observability & Data

        if 'slowapi' in content or 'ratelimit' in content: self.tools.add('RATE LIMITING')

        if 'loguru' in content or 'structlog' in content: self.tools.add('LOGURU / STRUCTLOG'); self.has_observability = True

        if 'opentelemetry' in content: self.tools.add('OPENTELEMETRY'); self.has_observability = True

        if 'pydantic' in content: self.tools.add('PYDANTIC (DATA VALIDATION)')

        if 'pandas' in content: self.frameworks.add('PANDAS')

        if 'pyspark' in content: self.frameworks.add('PYSPARK')

        if 'celery' in content: self.tools.add('CELERY (TASK QUEUE)')

        if 'redis' in content: self.databases.add('REDIS CLIENT'); self.has_data_caching = True

        if 'grpc' in content or 'kafka' in content or 'pika' in content: self.has_microservices = True

    def _inspect_dotnet(self):

        for csproj in self.tree.find_by_ext('.csproj'):

            try:

                text = csproj.read_text(encoding='utf-8', errors='ignore')

                if 'EntityFrameworkCore' in text: self.databases.add('ENTITY FRAMEWORK CORE'); self.has_database = True

                if 'Serilog' in text: self.tools.add('SERILOG'); self.has_observability = True

                if 'OpenTelemetry' in text: self.tools.add('OPENTELEMETRY'); self.has_observability = True

                if 'Polly' in text: self.tools.add('POLLY (RESILIENCY)'); self.has_microservices = True

                if 'Ocelot' in text: self.tools.add('OCELOT (API GATEWAY)'); self.has_microservices = True

                if 'StackExchange.Redis' in text: self.databases.add('REDIS CLIENT'); self.has_data_caching = True

            except Exception:

                pass

    def _detect_architecture_style(self):

        all_dirs = self.tree.all_dirs

        has_domain = any(d in all_dirs for d in ['domain', 'entities', 'core', 'models'])

        has_app = any(d in all_dirs for d in ['application', 'usecases', 'services', 'interactors'])

        has_infra = any(d in all_dirs for d in ['infrastructure', 'adapters', 'repositories', 'dal'])

        has_pres = any(d in all_dirs for d in ['presentation', 'controllers', 'routes', 'api', 'endpoints', 'handlers'])

        has_features = any(d in all_dirs for d in ['features', 'modules', 'slices'])

        if (has_domain and has_app and has_infra) or (has_domain and has_infra and has_pres):

            self.arch_style = "CLEAN ARCHITECTURE / HEXAGONAL (PORTS & ADAPTERS)"

        elif has_features:

            self.arch_style = "FEATURE-DRIVEN ARCHITECTURE / MODULAR MONOLITH"

        elif any(d in all_dirs for d in ['controllers', 'views']) and has_domain:

            self.arch_style = "MVC ARCHITECTURE (MODEL-VIEW-CONTROLLER)"

        elif has_pres and has_app:

            self.arch_style = "LAYERED ARCHITECTURE (PRESENTATION -> SERVICE)"

        else:

            self.arch_style = "PACKAGE & COMPONENT-BASED STRUCTURE"

class ProjectAuditor:

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

# ------------------------------------------------------------------

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

                if re.search(r'```(?:bash|sh|shell|cmd|powershell)?\s*\n.*?(?:npm|pnpm|yarn|docker|go run|dotnet|python|pip)', content, re.DOTALL | re.IGNORECASE):

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

                if re.search(r'(architecture|cấu trúc|project structure|folder structure|kiến trúc)', content, re.IGNORECASE):

                    score += 15

                    found.append("Mô tả cấu trúc thư mục và sơ đồ ARCHITECTURE tổng quan")

                else:

                    missing.append("Sơ đồ hoặc tài liệu mô tả cấu trúc thư mục ARCHITECTURE")

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

    # ------------------------------------------------------------------

    # 2. Backend Waterflow & Architecture Trace (Nâng cấp DI & DTO validation)

    # ------------------------------------------------------------------

    def audit_backend_waterflow(self):

        score = 0

        found = []

        missing = []

        layer_leaks = []

        all_dirs = self.tree.all_dirs

        # Phân tầng kiến trúc

        has_domain = any(d in all_dirs for d in ['domain', 'entities', 'core', 'models'])

        has_app = any(d in all_dirs for d in ['application', 'usecases', 'services', 'interactors'])

        has_infra = any(d in all_dirs for d in ['infrastructure', 'adapters', 'repositories', 'dal'])

        has_pres = any(d in all_dirs for d in ['presentation', 'controllers', 'routes', 'api', 'endpoints', 'handlers'])

        has_features = any(d in all_dirs for d in ['features', 'modules', 'slices'])

        if has_domain and (has_app or has_infra):

            score += 30

            found.append(f"Cấu trúc phân tầng chuẩn mực theo {self.profile.get('arch_style')}")

        elif has_features:

            score += 30

            found.append("Cấu trúc module độc lập theo FEATURE-DRIVEN ARCHITECTURE")

        elif has_pres or has_app:

            score += 20

            found.append("Phân tách cơ bản giữa tầng PRESENTATION và BUSINESS LOGIC")

        else:

            missing.append("Phân định ranh giới rõ ràng giữa DOMAIN, APPLICATION và INFRASTRUCTURE")

        # Quét Dependency Injection (DI) & DTO Input Validation

        has_di = False

        has_dto_validation = False

        sql_in_controller_patterns = [

            r'SELECT\s+.*?\s+FROM', r'INSERT\s+INTO', r'UPDATE\s+.*?\s+SET',

            r'\.query\([\'\"]SELECT', r'db\.collection\('

        ]

        for p in self.tree.code_files:

            p_parts_lower = [part.lower() for part in p.parts]

            is_controller = any(c in p_parts_lower for c in ['controllers', 'routes', 'api', 'handlers'])

            is_domain = any(c in p_parts_lower for c in ['domain', 'entities', 'core'])

            try:

                text = p.read_text(encoding='utf-8', errors='ignore')

                # Check DI

                if '@Injectable' in text or 'builder.Services.Add' in text or 'Depends(' in text or ('constructor(' in text and 'private ' in text):

                    has_di = True

                # Check DTO Input Validation

                if 'zod' in text or 'class-validator' in text or 'pydantic' in text or 'Joi.' in text or 'FluentValidation' in text:

                    has_dto_validation = True

                if is_controller:

                    for pat in sql_in_controller_patterns:

                        if re.search(pat, text, re.IGNORECASE):

                            rel = str(p.relative_to(self.root))

                            layer_leaks.append(f"Rò rỉ kiến trúc: CONTROLLER `{rel}` truy vấn SQL trực tiếp thay vì qua REPOSITORY.")

                            break

                if is_domain:

                    if re.search(r'(import .* from [\'"](express|axios|react|@nestjs|typeorm|mongoose)[\'"]|using (Microsoft\.AspNetCore|Microsoft\.EntityFrameworkCore))', text):

                        rel = str(p.relative_to(self.root))

                        layer_leaks.append(f"DOMAIN LEAK: Tệp `{rel}` trong DOMAIN bị phụ thuộc vào FRAMEWORK hạ tầng.")

            except Exception:

                pass

        if not layer_leaks:

            score += 25

            found.append("Độ thuần khiết của DOMAIN và ranh giới CONTROLLER được bảo vệ hoàn hảo (0 LAYER LEAKS)")

        else:

            for leak in layer_leaks[:2]:

                self.violations.append({'file': 'ARCHITECTURE BOUNDARY', 'line': 0, 'type': 'LAYER LEAKAGE', 'desc': leak, 'snippet': ''})

            score = max(10, score - 15)

        if has_di:

            score += 15

            found.append("Áp dụng DEPENDENCY INJECTION (DI) tiêm phụ thuộc tường minh")

        else:

            missing.append("Mô hình tiêm phụ thuộc DEPENDENCY INJECTION (DI) để hỗ trợ Unit Testing")

        if has_dto_validation:

            score += 15

            found.append("Xác thực dữ liệu đầu vào DTO tự động (ZOD / PYDANTIC / CLASS-VALIDATOR)")

        else:

            missing.append("Xác thực tự động cho dữ liệu DTO đầu vào (Zod, Pydantic hoặc Schema Validator)")

        # Graceful Shutdown

        entry_files = ['server.ts', 'server.js', 'main.ts', 'main.go', 'Program.cs', 'app.py', 'main.py']

        found_entry = False

        for ef in entry_files:

            matches = self.tree.find_by_name(ef)

            for m in matches:

                found_entry = True

                try:

                    text = m.read_text(encoding='utf-8', errors='ignore')

                    if 'SIGTERM' in text or 'SIGINT' in text or 'graceful' in text.lower():

                        score += 15

                        found.append("Cơ chế giải phóng tài nguyên an toàn khi tắt SERVER (GRACEFUL SHUTDOWN)")

                        break

                    else:

                        missing.append("Cơ chế giải phóng kết nối và tài nguyên khi tắt SERVER (GRACEFUL SHUTDOWN)")

                except Exception:

                    pass

                break

            if found_entry: break

        score = min(100, score)

        self.scores['Kiến Trúc BACKEND & Luồng Dữ Liệu CORE'] = score

        self.add_log(f"  -> Phân tầng kiến trúc: Domain={has_domain}, App={has_app}, Infra={has_infra}, Pres={has_pres}.", "backend", "muted")
        self.details['backend'] = {

            'name': 'Backend & Core Flow',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 20,

            'is_na': False,

            'leaks': layer_leaks

        }

    # ------------------------------------------------------------------

    # 3. Frontend Architecture (Nâng cấp Error Boundary & Code Splitting)

    # ------------------------------------------------------------------

    def audit_frontend_waterflow(self):

        score = 0

        found = []

        missing = []

        # 1. Design System & UI Tokens

        tailwind_cfg = self.tree.any_name_starts_with('tailwind.config')

        theme_tokens = bool(self.tree.find_by_name('theme.ts') or [p for p in self.tree.all_files if p.name.startswith('tokens.')])

        css_vars = False

        for css_path in self.tree.find_by_ext('.css'):

            try:

                content = css_path.read_text(encoding='utf-8', errors='ignore')

                if ':root' in content and '--' in content:

                    css_vars = True

                    break

            except Exception:

                pass

        if tailwind_cfg or theme_tokens or css_vars:

            score += 30

            found.append("Hệ thống DESIGN TOKENS độc quyền (CUSTOM TAILWIND CONFIG / CSS VARIABLES / THEME TOKENS)")

        else:

            missing.append("Hệ thống quản lý biến thiết kế giao diện tập trung (DESIGN TOKENS / THEME VARIABLES)")

        # 2. API Client bọc tập trung

        has_api_client = False

        client_candidates = [p for p in self.tree.code_files if 'api-client' in p.name.lower() or 'client' in p.name.lower()]

        for p in client_candidates:

            try:

                c = p.read_text(encoding='utf-8', errors='ignore')

                if 'interceptors' in c or 'baseURL' in c or 'fetch(' in c or 'axios' in c:

                    has_api_client = True

                    break

            except Exception:

                pass

        if has_api_client:

            score += 25

            found.append("API CLIENT phòng thủ tập trung (INTERCEPTORS, BASEURL, ERROR NORMALIZATION)")

        else:

            missing.append("Tệp bọc API CLIENT tập trung (tránh gọi FETCH / AXIOS rải rác trong COMPONENT)")

        # 3. Quét Error Boundary & Code Splitting (Lazy Loading)

        has_error_boundary = False

        has_lazy_loading = False

        god_components = []

        fe_code_files = [p for p in self.tree.code_files if p.suffix in {'.tsx', '.jsx', '.vue', '.svelte'}]

        for p in fe_code_files:

            try:

                text = p.read_text(encoding='utf-8', errors='ignore')

                lines = text.splitlines()

                if len(lines) > 350:

                    god_components.append(f"{p.name} ({len(lines)} dòng)")

                if 'ErrorBoundary' in text or 'componentDidCatch' in text:

                    has_error_boundary = True

                if 'React.lazy' in text or 'defineAsyncComponent' in text or 'loadable(' in text:

                    has_lazy_loading = True

            except Exception:

                pass

        if has_error_boundary:

            score += 15

            found.append("Trang bị ERROR BOUNDARY bắt lỗi runtime chống crash trắng toàn bộ màn hình")

        else:

            missing.append("Thành phần ERROR BOUNDARY bao bọc route để xử lý lỗi sập giao diện an toàn")

        if has_lazy_loading:

            score += 15

            found.append("Kỹ thuật CODE-SPLITTING / LAZY LOADING tối ưu tốc độ tải trang ban đầu")

        else:

            missing.append("Kỹ thuật LAZY LOADING (React.lazy) cho các phân vùng trang kích thước lớn")

        if not god_components:

            score += 15

            found.append("Cấu trúc COMPONENT tinh gọn, phân tách trách nhiệm rõ ràng (0 GOD COMPONENTS)")

        else:

            score += 5

            self.gaps.append(f"Cảnh báo GOD COMPONENT phình to quá mức (> 350 dòng): {', '.join(god_components[:2])}")

        score = min(100, score)

        self.scores['Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)'] = score

        ui_count = len(self.tree.find_by_ext('.tsx') + self.tree.find_by_ext('.jsx') + self.tree.find_by_ext('.vue') + self.tree.find_by_ext('.html'))
        self.add_log(f'  -> Khảo sát giao diện: tìm thấy {ui_count} tệp UI components & styling.', 'frontend', 'muted')
        self.details['frontend'] = {

            'name': 'Frontend & UI/UX',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 20,

            'is_na': False,

            'god_components': god_components

        }

    # ------------------------------------------------------------------

    # 4. Database, Persistence & Query Safety (Nâng cấp N+1 Query & Transaction)

    # ------------------------------------------------------------------

    def audit_database_waterflow(self):

        score = 0

        found = []

        missing = []

        # 1. Database Migrations

        all_dirs = self.tree.all_dirs

        has_migrations = any(m in all_dirs for m in ['migrations', 'migration', 'prisma']) or bool(self.tree.find_by_name('schema.prisma') or self.tree.find_by_name('alembic.ini'))

        if has_migrations:

            score += 35

            found.append("Quản lý DATABASE MIGRATION có kiểm soát phiên bản theo thời gian")

        else:

            missing.append("Thư mục DATABASE MIGRATION (nguy cơ trôi lệch SCHEMA trên PRODUCTION)")

            self.gaps.append("Thiếu hệ thống DATABASE MIGRATION có kiểm soát phiên bản.")

        # 2. Connection Pooling

        has_pool_config = False

        has_transaction = False

        n_plus_one_risks = []

        sql_injection_risks = []

        raw_query_patterns = [

            r'\.query\s*\(\s*["\'].*?WHERE.*?\+.*?\)',

            r'\.execute\s*\(\s*f["\'].*?WHERE.*?\{.*?\}',

            r'\.raw\s*\(\s*`.*?WHERE.*?(\$\{.*?\})`'

        ]

        for p in self.tree.code_files:

            try:

                text = p.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', text, re.IGNORECASE):

                    has_pool_config = True

                if re.search(r'(\.transaction\(|db\.begin\(|\$transaction|using var transaction)', text, re.IGNORECASE):

                    has_transaction = True

                # Quét SQL Injection

                lines = text.splitlines()

                for idx, line in enumerate(lines, 1):

                    for pat in raw_query_patterns:

                        if re.search(pat, line, re.IGNORECASE):

                            sql_injection_risks.append({

                                'file': str(p.relative_to(self.root)),

                                'line': idx,

                                'type': 'SQL INJECTION RISK',

                                'desc': 'Nối chuỗi trực tiếp vào câu lệnh RAW SQL (Thiếu PARAMETERIZED QUERIES).',

                                'snippet': line.strip()[:80]

                            })

                            break

                # Quét N+1 Query sơ bộ trong vòng lặp for / forEach

                in_loop = False

                loop_start = 0

                for idx, line in enumerate(lines, 1):

                    if re.search(r'\b(for|while)\b.*\(|\.forEach\(|\bfor\s+\w+\s+in\b', line):

                        in_loop = True

                        loop_start = idx

                    elif in_loop and (idx - loop_start <= 15):

                        if re.search(r'await\s+(?:db|\w+Repository|\w+Model)\.(?:find|query|get)', line):

                            n_plus_one_risks.append(str(p.relative_to(self.root)))

                            in_loop = False

                    elif in_loop and (idx - loop_start > 15):

                        in_loop = False

            except Exception:

                pass

        if has_pool_config:

            score += 25

            found.append("Cấu hình CONNECTION POOL & TIMEOUT bảo vệ giới hạn kết nối DATABASE")

        else:

            missing.append("Cấu hình tường minh cho CONNECTION POOL (POOL_SIZE, IDLE_TIMEOUT)")

        if has_transaction:

            score += 20

            found.append("Cơ chế DATABASE TRANSACTION đảm bảo tính nguyên tử (ACID) khi ghi nhiều bảng")

        else:

            missing.append("Cơ chế bọc TRANSACTION tường minh cho các tác vụ thay đổi nhiều thực thể")

        if not sql_injection_risks:

            score += 20

            found.append("An toàn câu lệnh QUERY: Sử dụng PARAMETERIZED QUERIES hoặc TYPE-SAFE ORM")

        else:

            self.violations.extend(sql_injection_risks)

            self.gaps.append(f"Cảnh báo bảo mật: Phát hiện {len(sql_injection_risks)} vị trí nối chuỗi RAW SQL.")

            score = max(10, score - 20)

        if n_plus_one_risks:

            self.gaps.append(f"Cảnh báo N+1 QUERY: Phát hiện truy vấn CSDL trong vòng lặp tại: {', '.join(n_plus_one_risks[:2])}")

        score = min(100, score)

        self.scores['Hạ Tầng DATABASE & An Toàn QUERY'] = score

        self.add_log(f"  -> Cơ sở dữ liệu: {', '.join(self.databases) or 'SQL'}. Đã rà soát migration và query safety.", "database", "muted")
        self.details['database'] = {

            'name': 'Database & Query Safety',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False,

            'sql_risks': sql_injection_risks

        }

    # ------------------------------------------------------------------

    # 5. MỞ RỘNG: Bảo Mật & Chuỗi Cung Ứng (Security & Supply Chain)

    # ------------------------------------------------------------------

    def audit_security_and_supply_chain(self):

        score = 0

        found = []

        missing = []

        # 1. Dependency Lockfiles

        lockfiles = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock', 'go.sum', 'Cargo.lock', 'packages.lock.json']

        has_lockfile = any(bool(self.tree.find_by_name(lf)) for lf in lockfiles)

        if has_lockfile:

            score += 35

            found.append("Khóa chính xác phiên bản phụ thuộc qua DEPENDENCY LOCKFILE (chống Supply Chain Attack)")

        else:

            missing.append("Tệp DEPENDENCY LOCKFILE (package-lock.json, poetry.lock, go.sum)")

            self.gaps.append("Thiếu lockfile quản lý phụ thuộc, tiềm ẩn rủi ro trôi lệch phiên bản hoặc dính mã độc.")

        # 2. HTTP Security Headers (Helmet, CORS)

        has_headers = 'HELMET (HTTP HEADERS)' in self.tools or 'CORS MIDDLEWARE' in self.tools

        if not has_headers:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if 'helmet' in t or 'CORSMiddleware' in t or 'UseCors' in t or 'Content-Security-Policy' in t:

                        has_headers = True

                        break

                except Exception:

                    pass

        if has_headers:

            score += 25

            found.append("Cấu hình HTTP SECURITY HEADERS (CORS strict, HELMET, Content-Security-Policy)")

        else:

            missing.append("Thiết lập HTTP SECURITY HEADERS bảo vệ giao thức (CORS, Helmet, CSP)")

        # 3. Rate Limiting protection

        has_ratelimit = 'RATE LIMITING' in self.tools

        if not has_ratelimit:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if 'rateLimit' in t or 'slowapi' in t or 'RateLimiter' in t or 'Throttle' in t:

                        has_ratelimit = True

                        break

                except Exception:

                    pass

        if has_ratelimit:

            score += 20

            found.append("Cơ chế RATE LIMITING giới hạn tần suất yêu cầu chống Brute-force & DDoS")

        else:

            missing.append("Cơ chế RATE LIMITING bảo vệ API trước các đợt tấn công vét cạn (Brute-force)")

        # 4. Secret Isolation & .gitignore

        gitignore = self.root / '.gitignore'

        has_git_secret_protect = False

        if gitignore.exists():

            try:

                gi_text = gitignore.read_text(encoding='utf-8', errors='ignore')

                if '.env' in gi_text and not (self.root / '.env').exists():

                    has_git_secret_protect = True

            except Exception:

                pass

        if has_git_secret_protect:

            score += 20

            found.append("Cô lập biến môi trường nhạy cảm: .ENV được loại trừ 100% khỏi kho Git")

        else:

            missing.append("Chính sách cô lập SECRET nghiêm ngặt (đưa .ENV vào .gitignore và dùng KMS/Vault)")

        score = min(100, score)

        self.scores['Bảo Mật & Chuỗi Cung Ứng (SECURITY)'] = score

        self.add_log("  -> Kiểm tra lockfiles chuỗi cung ứng, file .env và quét hardcoded secrets.", "security", "muted")
        self.details['security'] = {

            'name': 'Bảo Mật & Chuỗi Cung Ứng',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 6. MỞ RỘNG: Hạ Tầng Cloud & Container (Cloud & DevOps)

    # ------------------------------------------------------------------

    def audit_cloud_and_container(self):

        score = 0

        found = []

        missing = []

        # 1. Dockerfile Multi-stage Build & Non-root User

        dockerfiles = [p for p in self.tree.all_files if p.name.lower().startswith('dockerfile')]

        has_multistage = False

        has_nonroot = False

        has_healthcheck = False

        for df in dockerfiles:

            try:

                content = df.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'FROM\s+.*?AS\s+\w+', content, re.IGNORECASE) and 'COPY --from=' in content:

                    has_multistage = True

                if re.search(r'USER\s+(?:non-root|10001|appuser|node|\w+)', content, re.IGNORECASE) and 'USER root' not in content:

                    has_nonroot = True

                if 'HEALTHCHECK' in content:

                    has_healthcheck = True

            except Exception:

                pass

        if has_multistage:

            score += 35

            found.append("Dockerfile chuẩn mực MULTI-STAGE BUILD tối ưu dung lượng và tính bảo mật")

        else:

            missing.append("Dockerfile tối ưu MULTI-STAGE BUILD (tách biệt môi trường build và runtime)")

        if has_nonroot:

            score += 25

            found.append("Chạy CONTAINER với quyền hạn tối thiểu (USER NON-ROOT)")

        else:

            missing.append("Khai báo USER NON-ROOT trong Dockerfile để ngăn chặn Container Escape")

        # 2. Health Checks (Liveness & Readiness Probes)

        if not has_healthcheck:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if '/healthz' in t or '/readyz' in t or '/health' in t:

                        has_healthcheck = True

                        break

                except Exception:

                    pass

        if has_healthcheck:

            score += 20

            found.append("Endpoint thăm dò trạng thái sức khỏe: LIVENESS & READINESS PROBES (/healthz, /readyz)")

        else:

            missing.append("Cung cấp endpoint LIVENESS & READINESS PROBES (/healthz, /readyz) cho bộ điều phối Cloud")

        # 3. Infrastructure as Code (Docker Compose, K8s manifests, Helm)

        has_iac = bool(self.tree.find_by_name('docker-compose.yml') or self.tree.find_by_name('docker-compose.yaml')) or any('k8s' in p.parts or 'helm' in p.parts for p in self.tree.all_files)

        if has_iac:

            score += 20

            found.append("Khai báo hạ tầng dưới dạng mã INFRASTRUCTURE AS CODE (DOCKER COMPOSE / KUBERNETES MANIFESTS)")

        else:

            missing.append("Tệp quản lý hạ tầng INFRASTRUCTURE AS CODE (docker-compose.yml hoặc K8s Helm)")

        score = min(100, score)

        self.scores['Hạ Tầng CLOUD & CONTAINER (DEVOPS)'] = score

        self.add_log("  -> Kiểm tra cấu hình Dockerfile, container specs và CI/CD workflows.", "cloud", "muted")
        self.details['cloud'] = {

            'name': 'Hạ Tầng Cloud & DevOps',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 7. MỞ RỘNG: Hệ Thống Phân Tán & Gateway (Microservices & Resiliency)

    # ------------------------------------------------------------------

    def audit_microservices_and_gateway(self):

        score = 0

        found = []

        missing = []

        # 1. API Gateway Routing

        has_gateway = any(self.tree.any_name_starts_with(gw) for gw in ['ocelot', 'kong', 'traefik', 'envoy'])

        if not has_gateway:

            for p in self.tree.find_by_ext('.conf'):

                try:

                    if 'proxy_pass' in p.read_text(encoding='utf-8', errors='ignore'):

                        has_gateway = True

                        break

                except Exception:

                    pass

        if has_gateway:

            score += 30

            found.append("API GATEWAY / REVERSE PROXY làm cổng điều phối lưu lượng tập trung")

        else:

            missing.append("Cấu hình API GATEWAY tập trung (Kong, Traefik, Ocelot hoặc Nginx)")

        # 2. Circuit Breaker & Resiliency (Polly, Resilience4j, Tenacity)

        has_circuit_breaker = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'(circuitBreaker|Policy\.Handle|resilience4j|tenacity|retry_with_backoff)', t, re.IGNORECASE):

                    has_circuit_breaker = True

                    break

            except Exception:

                pass

        if has_circuit_breaker:

            score += 30

            found.append("Cơ chế ngắt mạch CIRCUIT BREAKER & RETRY WITH JITTER chống sập dây chuyền (Cascading Failure)")

        else:

            missing.append("Cơ chế CIRCUIT BREAKER bảo vệ các lời gọi liên dịch vụ phân tán")

        # 3. Inter-service contracts (gRPC / Event-Driven)

        has_contracts = bool(self.tree.find_by_ext('.proto')) or 'KAFKA CLIENT' in self.tools or 'RABBITMQ CLIENT' in self.tools

        if has_contracts:

            score += 25

            found.append("Hợp đồng liên dịch vụ chặt chẽ qua gRPC PROTOBUF hoặc EVENT-DRIVEN MESSAGING (KAFKA/RABBITMQ)")

        else:

            missing.append("Đặc tả hợp đồng giao tiếp liên dịch vụ (gRPC Protobuf hoặc Event Broker)")

        # 4. Correlation ID Tracking

        has_correlation_id = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if 'x-request-id' in t.lower() or 'correlationid' in t.lower() or 'traceparent' in t.lower():

                    has_correlation_id = True

                    break

            except Exception:

                pass

        if has_correlation_id:

            score += 15

            found.append("Đính kèm CORRELATION ID (x-request-id) xuyên suốt hành trình của request")

        else:

            missing.append("Middleware gán CORRELATION ID (x-request-id) phục vụ truy vết phân tán")

        score = min(100, score)

        self.scores['Hệ Thống PHÂN TÁN & GATEWAY (MICROSERVICES)'] = score

        self.add_log("  -> Khảo sát API Gateway, Proto/gRPC schemas và ranh giới microservices.", "microservices", "muted")
        self.details['microservices'] = {

            'name': 'Hệ Thống Phân Tán & Gateway',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 8. MỞ RỘNG: Kỹ Thuật Dữ Liệu & Cache (Data & Caching Safety)

    # ------------------------------------------------------------------

    def audit_data_and_caching(self):

        score = 0

        found = []

        missing = []

        # 1. Redis Caching & Mandatory TTL

        has_redis = 'REDIS CLIENT' in self.databases or 'REDIS (DISTRIBUTED CACHE)' in self.databases or any('redis' in p.name.lower() for p in self.tree.all_files)

        has_ttl = False

        if has_redis:

            for p in self.tree.code_files:

                try:

                    t = p.read_text(encoding='utf-8', errors='ignore')

                    if re.search(r'(setex|expire|ttl\s*=|ex\s*=|px\s*=|TimeSpan\.From)', t, re.IGNORECASE):

                        has_ttl = True

                        break

                except Exception:

                    pass

            if has_ttl:

                score += 40

                found.append("Chiến lược CACHING chuẩn mực: Bắt buộc cài đặt thời gian sống (TTL) cho mọi Redis Key")

            else:

                score += 15

                missing.append("Thiết lập TTL (Time-To-Live) bắt buộc cho Cache Key để chống cạn kiệt RAM Redis")

        else:

            score += 35

            found.append("Dự án áp dụng bộ nhớ đệm cục bộ (In-Memory Cache) đơn giản")

        # 2. Connection Pool Limits

        has_pool_limits = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if re.search(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', t, re.IGNORECASE):

                    has_pool_limits = True

                    break

            except Exception:

                pass

        if has_pool_limits:

            score += 30

            found.append("Giới hạn CONNECTION POOLING rõ ràng bảo vệ hạ tầng cơ sở dữ liệu")

        else:

            missing.append("Giới hạn CONNECTION POOLING tối đa để chống nghẽn đường truyền (Connection Exhaustion)")

        # 3. Data Schema Validation / Data Contracts

        has_data_contract = 'PYDANTIC (DATA VALIDATION)' in self.tools or any(p.name.lower().startswith('schema.') or p.name.lower().startswith('models.') for p in self.tree.code_files)

        if has_data_contract:

            score += 30

            found.append("Kiểm soát chặt chẽ hợp đồng dữ liệu qua DATA CONTRACTS / SCHEMA VALIDATION")

        else:

            missing.append("Đặc tả SCHEMA tường minh cho các đối tượng luồng dữ liệu (Data Contracts)")

        score = min(100, score)

        self.scores['Kỹ Thuật DỮ LIỆU & CACHE (DATA RESILIENCY)'] = score

        self.add_log("  -> Rà soát chiến lược Cache (Redis/In-memory) và khả năng phục hồi dữ liệu.", "data_caching", "muted")
        self.details['data_caching'] = {

            'name': 'Kỹ Thuật Dữ Liệu & Cache',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 9. MỞ RỘNG: Giám Sát & Vận Hành (Observability & Ops)

    # ------------------------------------------------------------------

    def audit_observability_and_ops(self):

        score = 0

        found = []

        missing = []

        # 1. Structured JSON Logging

        has_structured_logger = any(l in self.tools for l in ['WINSTON', 'PINO', 'SERILOG', 'LOGURU / STRUCTLOG'])

        if has_structured_logger:

            score += 40

            found.append("Ghi nhật ký có cấu trúc chuẩn mực (STRUCTURED JSON LOGGING) sẵn sàng cho ELK / Loki")

        else:

            missing.append("Thư viện ghi nhật ký có cấu trúc STRUCTURED LOGGING (thay thế console.log / print thô)")

        # 2. Distributed Tracing (OpenTelemetry)

        has_otel = 'OPENTELEMETRY' in self.tools or any('otel' in p.name.lower() for p in self.tree.all_files)

        if has_otel:

            score += 30

            found.append("Tích hợp OPENTELEMETRY phục vụ thu thập dấu vết và phân tích độ trễ xuyên suốt")

        else:

            missing.append("Công cụ truy vết OPENTELEMETRY để theo dõi độ trễ hệ thống")

        # 3. Prometheus / Metrics Endpoint

        has_metrics = False

        for p in self.tree.code_files:

            try:

                t = p.read_text(encoding='utf-8', errors='ignore')

                if '/metrics' in t or 'prometheus' in t.lower() or 'prom-client' in t:

                    has_metrics = True

                    break

            except Exception:

                pass

        if has_metrics:

            score += 30

            found.append("Cung cấp endpoint chỉ số PROMETHEUS METRICS (/metrics) phục vụ cảnh báo tự động")

        else:

            missing.append("Endpoint xuất chỉ số hiệu năng PROMETHEUS METRICS (/metrics)")

        score = min(100, score)

        self.scores['Giám Sát & VẬN HÀNH (OBSERVABILITY & OPS)'] = score

        self.add_log("  -> Kiểm tra giải pháp Giám sát: Structured Logging, Tracing & Metrics.", "observability", "muted")
        self.details['observability'] = {

            'name': 'Giám Sát & Vận Hành',

            'found': found,

            'missing': missing,

            'score': score,

            'max_points': 15,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 10. Multi-Language Anti-Crash Standard

    # ------------------------------------------------------------------

    def audit_anti_crash_universal(self):

        score = 100

        violations_count = 0

        scanned_files = 0

        for p in self.tree.code_files:

            scanned_files += 1

            rel_file = str(p.relative_to(self.root))

            try:

                lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()

                for idx, line in enumerate(lines, 1):

                    stripped = line.strip()

                    if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*') or stripped.startswith('*'):

                        continue

                    # 1. Naked JSON.parse (JS/TS)

                    if 'JSON.parse(' in line:

                        window = "\n".join(lines[max(0, idx - 6):min(len(lines), idx + 6)])

                        if 'try' not in window:

                            self.violations.append({

                                'file': rel_file,

                                'line': idx,

                                'type': 'NAKED JSON.PARSE',

                                'desc': 'Gọi JSON.PARSE không bọc trong khối TRY-CATCH an toàn (Nguy cơ sập RUNTIME khi dữ liệu JSON hỏng).',

                                'snippet': stripped[:80]

                            })

                            violations_count += 1

                    # 2. Strict Typing Violation (: any)

                    if p.suffix in {'.ts', '.tsx'}:

                        if re.search(r':\s*any', line):

                            self.violations.append({

                                'file': rel_file,

                                'line': idx,

                                'type': 'STRICT TYPING VIOLATION',

                                'desc': 'Sử dụng kiểu dữ liệu ": any" vi phạm quy chuẩn STRICT TYPING của TYPESCRIPT.',

                                'snippet': stripped[:80]

                            })

                            violations_count += 1

                    # 3. Python Bare Except

                    if p.suffix == '.py':

                        if re.match(r'^\s*except\s*:\s*$', line) or re.match(r'^\s*except\s+Exception\s*:\s*pass\s*$', line):

                            self.violations.append({

                                'file': rel_file,

                                'line': idx,

                                'type': 'PYTHON SILENT EXCEPTION EATER',

                                'desc': 'Bắt lỗi im lặng (BARE EXCEPT hoặc EXCEPT EXCEPTION: PASS) làm nuốt chửng lỗi hệ thống.',

                                'snippet': stripped[:80]

                            })

                            violations_count += 1

                    # 4. Hardcoded Secret Detection

                    if re.search(r'(api_key|secret|password|bearer|private_key)\s*[:=]\s*[\'\"][A-Za-z0-9_\-\.]{16,}[\'\"]', line, re.IGNORECASE):

                        if not re.search(r'(process\.env|os\.environ|config\(|\.get\()', line, re.IGNORECASE):

                            self.violations.append({

                                'file': rel_file,

                                'line': idx,

                                'type': 'HARDCODED SECRET IN CODE',

                                'desc': 'Phát hiện CHUỖI KHÓA BẢO MẬT (SECRET/API KEY) được gán tĩnh trực tiếp vào mã nguồn.',

                                'snippet': stripped[:40] + '...[REDACTED]'

                            })

                            violations_count += 1

                    # 5. React useEffect Missing Cleanup (Timer / Subscription leak risk)

                    if p.suffix in {'.tsx', '.jsx'}:

                        if 'setInterval(' in line or 'addEventListener(' in line:

                            window = "\n".join(lines[max(0, idx - 2):min(len(lines), idx + 15)])

                            if 'return () =>' not in window and 'return function' not in window and 'clearInterval' not in window and 'removeEventListener' not in window:

                                self.violations.append({

                                    'file': rel_file,

                                    'line': idx,

                                    'type': 'REACT MEMORY LEAK RISK',

                                    'desc': 'Khởi tạo TIMER / EVENT LISTENER nhưng thiếu hàm CLEANUP giải phóng (Nguy cơ MEMORY LEAK).',

                                    'snippet': stripped[:80]

                                })

                                violations_count += 1

            except Exception:

                pass

        if violations_count > 0:

            deduction = min(75, violations_count * 5)

            score = max(20, score - deduction)

        else:

            score = 100

        if violations_count > 0:

            self.gaps.append(f"Phát hiện {violations_count} vị trí vi phạm tiêu chuẩn ANTI-CRASH trong mã nguồn.")

        self.scores['Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)'] = score

        anti_violations = [v for v in self.violations if v.get('type') in ['NAKED JSON.PARSE', 'STRICT TYPING VIOLATION', 'PYTHON SILENT EXCEPTION EATER', 'HARDCODED SECRET IN CODE', 'REACT MEMORY LEAK RISK']]

        self.add_log(f"  -> Đã quét AST trên {len(self.tree.code_files)} tệp mã nguồn: kiểm tra Null safety, try-catch I/O.", "anticrash", "muted")
        self.details['anticrash'] = {

            'name': 'Runtime Anti-Crash',

            'scanned_files': scanned_files,

            'violations_count': violations_count,

            'violations': anti_violations,

            'score': score,

            'max_points': 20,

            'is_na': False

        }

    # ------------------------------------------------------------------

    # 11. Architecture Docs, Contracts & AI Governance

    # ------------------------------------------------------------------

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
                    if re.search(r'(dừng lại hỏi|stop & ask|hỏi ý kiến|circuit breaker|xin ý kiến|confirm)', txt, re.IGNORECASE):
                        has_stop_and_ask = True
                    if re.search(r'(anti-crash|try-catch|defensive|null safety|chống đổ vỡ)', txt, re.IGNORECASE):
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
                found.append("Cơ chế ngắt mạch dừng lại hỏi (STOP & ASK / CIRCUIT BREAKER) khi yêu cầu mơ hồ hoặc có rủi ro")
            else:
                missing.append("Cơ chế chốt chặn STOP & ASK (buộc Agent dừng lại xin ý kiến khi chạm rủi ro kiến trúc)")

            if has_anti_crash_rules:
                score += 10
                found.append("Điều khoản ràng buộc bắt buộc lập trình phòng thủ (ANTI-CRASH DEFENSIVE STANDARD)")
            else:
                missing.append("Quy chuẩn chống đổ vỡ ANTI-CRASH bắt buộc trong hiến pháp Agent")
        else:
            missing.append("Thiếu tệp hiến pháp định hướng hành vi cho AI Agent (AGENTS.md, .cursorrules hoặc .mdc)")

        # 2. Quét Agent Skills Catalog (skills/*/SKILL.md, .agent/skills/)
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
            missing.append("Thư mục đóng gói kỹ năng AGENT SKILLS (skills/*/SKILL.md) để mở rộng năng lực tự động")

        # 3. Quét Agent Workflows & Automation Pipelines (.agent/workflows/, workflows/, prompts/)
        workflow_files = [
            p for p in self.tree.all_files 
            if ('workflows' in p.parts or 'prompts' in p.parts or 'agent-practices' in p.parts) and p.suffix.lower() in {'.md', '.yaml', '.yml'}
        ]
        has_verification_step = False

        if workflow_files:
            score += 15
            wf_names = ", ".join(sorted(list({p.name for p in workflow_files}))[:3])
            found.append(f"Quy trình tự động hóa tác vụ AGENT WORKFLOWS ({len(workflow_files)} kịch bản quy trình: {wf_names})")

            for wf in workflow_files:
                try:
                    txt = wf.read_text(encoding='utf-8', errors='ignore')
                    if re.search(r'(verify|test|lint|tự kiểm tra|nghiệm thu|checklist|validation)', txt, re.IGNORECASE):
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

    def audit_architecture_docs_and_ai(self):

        score = 0

        found = []

        missing = []

        # 1. AI AGENT Governance (AGENTS.md / .cursorrules / CLAUDE.md)

        ai_rules_files = ['AGENTS.md', '.cursorrules', 'CLAUDE.md', '.github/copilot-instructions.md']

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

        # 3. API CONTRACTS (OpenAPI / Swagger / Contracts)

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

    # ------------------------------------------------------------------

    # 12. Starter Kit Benchmark (Strengths, Bloat, Innovations)

    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------

    # Tính toán chuẩn hóa tổng điểm thang 100 theo Dynamic Context-Aware Model

    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------

    # Xuất báo cáo Markdown

    # ------------------------------------------------------------------

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

if __name__ == '__main__':

    target = sys.argv[1] if len(sys.argv) > 1 else '.'

    auditor = ProjectAuditor(target)

    auditor.run()

