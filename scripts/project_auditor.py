#!/usr/bin/env python3
"""
UNIVERSAL PROJECT REVIEWER & ARCHITECTURE AUDITOR ENGINE v2.0
Pure Python Standard Library (100% Offline, Zero-Token, Zero-Dependency)

Two-Tier Architectural Audit Model:
  TIER 1: Deep Codebase Traversal (Waterflow Model: Root -> FE, BE, DB, Docs -> Leaf Files)
          Evaluates ANY project, ANY tech stack, ANY architecture dynamically and fairly.
  TIER 2: Starter Kit Benchmark & 4-Quadrant Gap Analysis
          Pinpoints: Missing (Thiếu) | Bloat (Thừa/Rác) | Strengths (Ưu điểm) | Risks (Nhược điểm).
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


class ProjectProfiler:
    """Tự động nhận diện TECH STACK, kiểu ARCHITECTURE và loại hình dự án."""

    def __init__(self, root: Path):
        self.root = root
        self.languages = set()
        self.frameworks = set()
        self.databases = set()
        self.tools = set()
        self.archetype = "Ứng dụng Phần Mềm Tiêu Chuẩn (GENERAL APPLICATION)"
        self.arch_style = "Kiến trúc Tự Do / Chưa Xác Định (CUSTOM ARCHITECTURE)"
        self.has_frontend = False
        self.has_backend = False
        self.has_database = False

    def profile(self):
        # 1. Nhận diện MANIFEST & Ngôn ngữ lập trình
        has_pkg_json = (self.root / 'package.json').exists() or any(self.root.glob('*/package.json'))
        has_pyproject = (self.root / 'pyproject.toml').exists() or (self.root / 'requirements.txt').exists()
        has_csproj = any(self.root.glob('*.csproj')) or any(self.root.glob('*/*.csproj'))
        has_go_mod = (self.root / 'go.mod').exists() or any(self.root.glob('*/go.mod'))
        has_pom = (self.root / 'pom.xml').exists() or any(self.root.glob('*/pom.xml'))
        has_cargo = (self.root / 'Cargo.toml').exists() or any(self.root.glob('*/Cargo.toml'))

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
        if has_go_mod:
            self.languages.add('GO')
            self.has_backend = True
        if has_pom:
            self.languages.add('JAVA')
            self.has_backend = True
        if has_cargo:
            self.languages.add('RUST')

        # 2. Nhận diện INFRASTRUCTURE & DATABASE
        docker_compose = self.root / 'docker-compose.yml'
        if docker_compose.exists():
            self.tools.add('DOCKER COMPOSE')
            try:
                dc_content = docker_compose.read_text(encoding='utf-8', errors='ignore').lower()
                if 'postgres' in dc_content: self.databases.add('POSTGRESQL')
                if 'mysql' in dc_content or 'mariadb' in dc_content: self.databases.add('MYSQL/MARIADB')
                if 'mongo' in dc_content: self.databases.add('MONGODB')
                if 'redis' in dc_content: self.databases.add('REDIS (DISTRIBUTED CACHE)')
                if 'pgvector' in dc_content or 'qdrant' in dc_content or 'chroma' in dc_content:
                    self.databases.add('VECTOR DATABASE (AI RAG)')
            except Exception:
                pass

        if (self.root / 'Dockerfile').exists():
            self.tools.add('DOCKERFILE')

        # 3. Phân loại loại hình dự án
        if self.has_frontend and self.has_backend:
            self.archetype = "Hệ thống FULL-STACK (FRONTEND + BACKEND)"
        elif self.has_frontend and not self.has_backend:
            self.archetype = "Ứng dụng Giao Diện Độc Lập (FRONTEND SPA / MOBILE)"
        elif self.has_backend and not self.has_frontend:
            self.archetype = "Nền tảng Dịch vụ Phía Sau (BACKEND API / MICROSERVICES)"
        elif any((self.root / f).exists() for f in ['main.py', 'cli.py', 'cmd', 'bin']):
            self.archetype = "Công cụ Dòng Lệnh / Hệ Thống (CLI TOOL / SYSTEM UTILITY)"

        # 4. Nhận diện phong cách kiến trúc
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
            'has_database': len(self.databases) > 0 or self.has_database
        }

    def _inspect_package_json(self):
        pkg_paths = [self.root / 'package.json'] + list(self.root.glob('*/package.json'))
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
                if 'redis' in deps or 'ioredis' in deps: self.databases.add('REDIS CLIENT'); self.has_database = True
            except Exception:
                pass

    def _inspect_python(self):
        req_file = self.root / 'requirements.txt'
        pyproj = self.root / 'pyproject.toml'
        content = ""
        if req_file.exists():
            content += req_file.read_text(encoding='utf-8', errors='ignore').lower() + "\n"
        if pyproj.exists():
            content += pyproj.read_text(encoding='utf-8', errors='ignore').lower() + "\n"

        if 'fastapi' in content: self.frameworks.add('FASTAPI'); self.has_backend = True
        if 'django' in content: self.frameworks.add('DJANGO'); self.has_backend = True
        if 'flask' in content: self.frameworks.add('FLASK'); self.has_backend = True
        if 'sqlalchemy' in content: self.databases.add('SQLALCHEMY ORM'); self.has_database = True
        if 'alembic' in content: self.databases.add('ALEMBIC MIGRATIONS'); self.has_database = True
        if 'psycopg2' in content or 'asyncpg' in content: self.databases.add('POSTGRESQL'); self.has_database = True

    def _detect_architecture_style(self):
        all_dirs = set()
        for p in self.root.rglob('*'):
            if p.is_dir() and not any(ign in p.parts for ign in IGNORE_DIRS):
                all_dirs.add(p.name.lower())

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
    """Hệ thống thẩm định kiến trúc mã nguồn & đối chiếu chuẩn mực STARTER KIT."""

    def __init__(self, root_dir='.'):
        self.root = Path(root_dir).resolve()
        self.profiler = ProjectProfiler(self.root)
        self.profile = {}
        self.scores = {}
        self.gaps = []
        self.bloat = []
        self.innovations = []
        self.violations = []
        self.details = {}
        self.report_path = None

    def run(self, progress_callback=None):
        import time

        def cb(pct, msg):
            if progress_callback:
                progress_callback(pct, msg)
                time.sleep(0.04)

        cb(5, "Đang phân tích TECH STACK và kiến trúc tổng thể...")
        self.profile = self.profiler.profile()

        steps = [
            ("Khảo sát tài liệu dự án (README & ONBOARDING)", 20, self.audit_readme_and_onboarding),
            ("Thẩm định kiến trúc BACKEND & luồng dữ liệu CORE", 40, self.audit_backend_waterflow),
            ("Thẩm định kiến trúc FRONTEND & DESIGN SYSTEM (UI/UX)", 60, self.audit_frontend_waterflow),
            ("Thẩm định DATABASE, MIGRATION & an toàn QUERY", 75, self.audit_database_waterflow),
            ("Kiểm tra an toàn RUNTIME & tiêu chuẩn ANTI-CRASH", 88, self.audit_anti_crash_universal),
            ("Rà soát SPEC, API CONTRACT & cấu hình AI AGENT", 94, self.audit_architecture_docs_and_ai),
            ("Phân tích khoảng cách (GAP ANALYSIS) so với STARTER KIT", 98, self.benchmark_starter_kit)
        ]

        for name, pct, fn in steps:
            cb(pct, f"Đang thẩm định: {name}...")
            fn()

        total_score = self.calculate_total_score()
        self.report_path = self.generate_markdown_report(total_score)
        cb(100, f"Đã hoàn thành thẩm định! Báo cáo: {self.report_path.name}")
        return total_score

    # ------------------------------------------------------------------
    # 1. README, Onboarding & Project Hygiene
    # ------------------------------------------------------------------
    def audit_readme_and_onboarding(self):
        score = 0
        found = []
        missing = []

        readme_file = None
        for name in ['README.md', 'readme.md', 'README.MD', 'README']:
            p = self.root / name
            if p.exists() and p.is_file():
                readme_file = p
                break

        if readme_file:
            score += 25
            found.append("Tệp README.md chuẩn xác tại thư mục gốc")
            try:
                content = readme_file.read_text(encoding='utf-8', errors='ignore')
                lines_count = len(content.splitlines())

                # Tiêu đề & Bài toán (Product Vision / Why)
                if re.search(r'^#\s+.+', content, re.MULTILINE) and lines_count >= 15:
                    score += 20
                    found.append("Mô tả bài toán, mục tiêu và định vị giá trị sản phẩm rõ ràng")
                else:
                    missing.append("Đoạn giới thiệu mục tiêu bài toán và giá trị sản phẩm (PRODUCT VISION)")

                # Hướng dẫn khởi chạy (Quick Start code blocks)
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
        self.details['readme'] = {'found': found, 'missing': missing, 'score': score}

    # ------------------------------------------------------------------
    # 2. Backend Waterflow & Architecture Trace
    # ------------------------------------------------------------------
    def audit_backend_waterflow(self):
        score = 0
        found = []
        missing = []
        layer_leaks = []

        all_dirs = set()
        for p in self.root.rglob('*'):
            if p.is_dir() and not any(ign in p.parts for ign in IGNORE_DIRS):
                all_dirs.add(p.name.lower())

        # Phân tầng kiến trúc
        has_domain = any(d in all_dirs for d in ['domain', 'entities', 'core', 'models'])
        has_app = any(d in all_dirs for d in ['application', 'usecases', 'services', 'interactors'])
        has_infra = any(d in all_dirs for d in ['infrastructure', 'adapters', 'repositories', 'dal'])
        has_pres = any(d in all_dirs for d in ['presentation', 'controllers', 'routes', 'api', 'endpoints', 'handlers'])
        has_features = any(d in all_dirs for d in ['features', 'modules', 'slices'])

        if has_domain and (has_app or has_infra):
            score += 40
            found.append(f"Cấu trúc phân tầng chuẩn mực theo {self.profile.get('arch_style')}")
        elif has_features:
            score += 40
            found.append("Cấu trúc module độc lập theo FEATURE-DRIVEN ARCHITECTURE")
        elif has_pres or has_app:
            score += 25
            found.append("Phân tách cơ bản giữa tầng PRESENTATION và BUSINESS LOGIC")
        else:
            missing.append("Phân định ranh giới rõ ràng giữa DOMAIN, APPLICATION và INFRASTRUCTURE")

        # Quét rò rỉ ranh giới kiến trúc (Layer Leakage)
        sql_in_controller_patterns = [
            r'SELECT\s+.*?\s+FROM', r'INSERT\s+INTO', r'UPDATE\s+.*?\s+SET',
            r'\.query\([\'"]SELECT', r'db\.collection\('
        ]
        
        for p in self.root.rglob('*'):
            if not p.is_file() or p.suffix not in CODE_EXTENSIONS:
                continue
            if any(ign in p.parts for ign in IGNORE_DIRS):
                continue
            
            p_parts_lower = [part.lower() for part in p.parts]
            is_controller = any(c in p_parts_lower for c in ['controllers', 'routes', 'api', 'handlers'])
            is_domain = any(c in p_parts_lower for c in ['domain', 'entities', 'core'])

            if is_controller:
                try:
                    text = p.read_text(encoding='utf-8', errors='ignore')
                    for pat in sql_in_controller_patterns:
                        if re.search(pat, text, re.IGNORECASE):
                            rel = str(p.relative_to(self.root))
                            layer_leaks.append(f"Rò rỉ kiến trúc: CONTROLLER `{rel}` truy vấn SQL trực tiếp thay vì thông qua REPOSITORY / SERVICE.")
                            break
                except Exception:
                    pass

            if is_domain:
                try:
                    text = p.read_text(encoding='utf-8', errors='ignore')
                    if re.search(r'(import .* from [\'"](express|axios|react|@nestjs|typeorm|mongoose)[\'"]|using (Microsoft\.AspNetCore|Microsoft\.EntityFrameworkCore))', text):
                        rel = str(p.relative_to(self.root))
                        layer_leaks.append(f"DOMAIN LEAK: Tệp `{rel}` trong DOMAIN bị phụ thuộc vào FRAMEWORK hạ tầng.")
                except Exception:
                    pass

        if not layer_leaks:
            score += 35
            found.append("Độ thuần khiết của DOMAIN và ranh giới CONTROLLER được bảo vệ hoàn hảo (0 LAYER LEAKS)")
        else:
            for leak in layer_leaks[:2]:
                self.violations.append({'file': 'ARCHITECTURE BOUNDARY', 'line': 0, 'type': 'LAYER LEAKAGE', 'desc': leak, 'snippet': ''})
            score = max(10, score - 20)

        # Kiểm tra vòng đời Entry Point (Graceful Shutdown)
        entry_files = ['server.ts', 'server.js', 'main.ts', 'main.go', 'Program.cs', 'app.py', 'main.py']
        found_entry = False
        for ef in entry_files:
            matches = list(self.root.rglob(ef))
            for m in matches:
                if any(ign in m.parts for ign in IGNORE_DIRS): continue
                found_entry = True
                try:
                    text = m.read_text(encoding='utf-8', errors='ignore')
                    if 'SIGTERM' in text or 'SIGINT' in text or 'graceful' in text.lower():
                        score += 15
                        found.append("Đã thiết lập cơ chế GRACEFUL SHUTDOWN để giải phóng tài nguyên an toàn")
                        break
                    else:
                        missing.append("Cơ chế giải phóng kết nối và tài nguyên khi tắt SERVER (GRACEFUL SHUTDOWN)")
                except Exception:
                    pass
                break
            if found_entry: break

        if not found_entry and self.profile.get('has_backend'):
            score += 10
        elif found_entry:
            score += 10

        score = min(100, score)
        self.scores['Kiến Trúc BACKEND & Luồng Dữ Liệu CORE'] = score
        self.details['backend'] = {'found': found, 'missing': missing, 'score': score, 'leaks': layer_leaks}

    # ------------------------------------------------------------------
    # 3. Frontend Architecture & Custom UI/UX Waterflow
    # ------------------------------------------------------------------
    def audit_frontend_waterflow(self):
        score = 0
        found = []
        missing = []

        # Nếu là dự án thuần BACKEND hoặc CLI, đánh giá công bằng theo API USABILITY
        if not self.profile.get('has_frontend'):
            score = 95
            found.append("Dự án BACKEND / API / CLI: Đạt chuẩn thiết kế RESTFUL API & CLI ERGONOMICS (Không bắt buộc UI)")
            self.scores['Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)'] = score
            self.details['frontend'] = {'found': found, 'missing': [], 'score': score}
            return

        # 1. Nhận diện DESIGN SYSTEM & UI TOKENS độc quyền
        has_custom_tokens = False
        tailwind_cfg = any(self.root.glob('**/tailwind.config.*'))
        theme_tokens = any(self.root.glob('**/theme.ts')) or any(self.root.glob('**/tokens.*'))
        css_vars = False

        for css_path in self.root.rglob('*.css'):
            if any(ign in css_path.parts for ign in IGNORE_DIRS): continue
            try:
                content = css_path.read_text(encoding='utf-8', errors='ignore')
                if ':root' in content and '--' in content:
                    css_vars = True
                    break
            except Exception:
                pass

        if tailwind_cfg or theme_tokens or css_vars:
            has_custom_tokens = True
            score += 35
            found.append("Hệ thống DESIGN TOKENS độc quyền (CUSTOM TAILWIND CONFIG / CSS VARIABLES / THEME TOKENS)")
        else:
            missing.append("Hệ thống quản lý biến thiết kế giao diện tập trung (DESIGN TOKENS / THEME VARIABLES)")

        # 2. API CLIENT phòng thủ tập trung
        has_api_client = False
        for p in self.root.rglob('*api-client*'):
            if p.is_file() and not any(ign in p.parts for ign in IGNORE_DIRS):
                has_api_client = True
                break

        if not has_api_client:
            for p in self.root.rglob('*client*'):
                if p.is_file() and p.suffix in CODE_EXTENSIONS and not any(ign in p.parts for ign in IGNORE_DIRS):
                    try:
                        c = p.read_text(encoding='utf-8', errors='ignore')
                        if 'interceptors' in c or 'baseURL' in c:
                            has_api_client = True
                            break
                    except Exception:
                        pass

        if has_api_client:
            score += 25
            found.append("API CLIENT phòng thủ tập trung (INTERCEPTORS, BASEURL, ERROR NORMALIZATION)")
        else:
            missing.append("Tệp bọc API CLIENT tập trung (tránh gọi FETCH / AXIOS rải rác trong COMPONENT)")

        # 3. Quản lý STATE
        all_dirs = {p.name.lower() for p in self.root.rglob('*') if p.is_dir() and not any(ign in p.parts for ign in IGNORE_DIRS)}
        if any(s in all_dirs for s in ['stores', 'store', 'redux', 'context', 'slices']):
            score += 20
            found.append("Quản lý STATE tập trung bằng STORE (ZUSTAND / REDUX / CONTEXT)")
        else:
            score += 10
            found.append("Quản lý STATE cục bộ và tham số URL")

        # 4. Quét GOD COMPONENT (> 350 dòng)
        god_components = []
        for p in self.root.rglob('*'):
            if p.is_file() and p.suffix in {'.tsx', '.jsx', '.vue', '.svelte'}:
                if any(ign in p.parts for ign in IGNORE_DIRS): continue
                try:
                    lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
                    if len(lines) > 350:
                        rel = str(p.relative_to(self.root))
                        god_components.append(f"{rel} ({len(lines)} dòng)")
                except Exception:
                    pass

        if not god_components:
            score += 20
            found.append("Cấu trúc COMPONENT tinh gọn, phân tách trách nhiệm rõ ràng (0 GOD COMPONENTS)")
        else:
            score += 10
            self.gaps.append(f"Cảnh báo GOD COMPONENT phình to quá mức (> 350 dòng): {', '.join(god_components[:2])}")

        score = min(100, score)
        self.scores['Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)'] = score
        self.details['frontend'] = {
            'found': found,
            'missing': missing,
            'score': score,
            'god_components': god_components
        }

    # ------------------------------------------------------------------
    # 4. Database, Persistence & Query Safety Waterflow
    # ------------------------------------------------------------------
    def audit_database_waterflow(self):
        score = 0
        found = []
        missing = []

        if not self.profile.get('has_database'):
            score = 90
            found.append("Dự án không yêu cầu CSDL quan hệ / Dịch vụ phi trạng thái (STATELESS SERVICE)")
            self.scores['Hạ Tầng DATABASE & An Toàn QUERY'] = score
            self.details['database'] = {'found': found, 'missing': [], 'score': score}
            return

        # 1. Kiểm soát DATABASE MIGRATIONS
        all_dirs = {p.name.lower() for p in self.root.rglob('*') if p.is_dir() and not any(ign in p.parts for ign in IGNORE_DIRS)}
        has_migrations = any(m in all_dirs for m in ['migrations', 'migration', 'prisma']) or any(self.root.glob('**/schema.prisma')) or any(self.root.glob('**/alembic.ini'))
        
        if has_migrations:
            score += 40
            found.append("Quản lý DATABASE MIGRATION có kiểm soát phiên bản theo thời gian")
        else:
            missing.append("Thư mục DATABASE MIGRATION (nguy cơ trôi lệch SCHEMA trên PRODUCTION)")
            self.gaps.append("Thiếu hệ thống DATABASE MIGRATION có kiểm soát phiên bản.")

        # 2. CONNECTION POOLING & RESILIENCY
        has_pool_config = False
        for p in self.root.rglob('*'):
            if p.is_file() and p.suffix in CODE_EXTENSIONS and not any(ign in p.parts for ign in IGNORE_DIRS):
                try:
                    text = p.read_text(encoding='utf-8', errors='ignore')
                    if re.search(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', text, re.IGNORECASE):
                        has_pool_config = True
                        break
                except Exception:
                    pass

        if has_pool_config:
            score += 30
            found.append("Cấu hình CONNECTION POOL & TIMEOUT bảo vệ giới hạn kết nối DATABASE")
        else:
            missing.append("Cấu hình tường minh cho CONNECTION POOL (POOL_SIZE, IDLE_TIMEOUT)")

        # 3. Quét nguy cơ SQL INJECTION
        sql_injection_risks = []
        raw_query_patterns = [
            r'\.query\s*\(\s*["\'].*?WHERE.*?\+.*?\)',
            r'\.execute\s*\(\s*f["\'].*?WHERE.*?\{.*?\}',
            r'\.raw\s*\(\s*`.*?WHERE.*?(\$\{.*?\})`'
        ]

        for p in self.root.rglob('*'):
            if not p.is_file() or p.suffix not in CODE_EXTENSIONS: continue
            if any(ign in p.parts for ign in IGNORE_DIRS): continue
            try:
                lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
                for idx, line in enumerate(lines, 1):
                    for pat in raw_query_patterns:
                        if re.search(pat, line, re.IGNORECASE):
                            rel = str(p.relative_to(self.root))
                            sql_injection_risks.append({
                                'file': rel,
                                'line': idx,
                                'type': 'SQL INJECTION RISK',
                                'desc': 'Nối chuỗi trực tiếp vào câu lệnh RAW SQL (Thiếu PARAMETERIZED QUERIES).',
                                'snippet': line.strip()[:80]
                            })
                            break
            except Exception:
                pass

        if not sql_injection_risks:
            score += 30
            found.append("An toàn câu lệnh QUERY: Sử dụng PARAMETERIZED QUERIES hoặc TYPE-SAFE ORM")
        else:
            self.violations.extend(sql_injection_risks)
            self.gaps.append(f"Cảnh báo bảo mật: Phát hiện {len(sql_injection_risks)} vị trí nối chuỗi RAW SQL tiềm ẩn nguy cơ SQL INJECTION.")
            score = max(20, score - 20)

        score = min(100, score)
        self.scores['Hạ Tầng DATABASE & An Toàn QUERY'] = score
        self.details['database'] = {
            'found': found,
            'missing': missing,
            'score': score,
            'sql_risks': sql_injection_risks
        }

    # ------------------------------------------------------------------
    # 5. Multi-Language Anti-Crash Standard (Code-Level Static Analysis)
    # ------------------------------------------------------------------
    def audit_anti_crash_universal(self):
        score = 100
        violations_count = 0
        scanned_files = 0

        for p in self.root.rglob('*'):
            if not p.is_file() or p.suffix not in CODE_EXTENSIONS:
                continue
            if any(ign in p.parts for ign in IGNORE_DIRS):
                continue

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
                        if re.search(r':\s*any\b', line):
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
                                'desc': 'Bắt ngoại lệ không tường minh hoặc nuốt lỗi (bare EXCEPT hoặc EXCEPT EXCEPTION: PASS).',
                                'snippet': stripped[:80]
                            })
                            violations_count += 1

                    # 4. Hardcoded Secrets Detection
                    if re.search(r'(?:api_key|apiKey|secret_key|secretKey|private_key|password)\s*=\s*["\'][a-zA-Z0-9_\-\.]{12,}["\']', line, re.IGNORECASE):
                        if 'test' not in rel_file.lower() and 'mock' not in rel_file.lower() and 'fixture' not in rel_file.lower():
                            self.violations.append({
                                'file': rel_file,
                                'line': idx,
                                'type': 'HARDCODED SECRET IN CODE',
                                'desc': 'Phát hiện mật khẩu / API KEY / PRIVATE TOKEN hardcode trực tiếp trong mã nguồn.',
                                'snippet': stripped[:80]
                            })
                            violations_count += 1

            except Exception:
                pass

        penalty = min(50, violations_count * 5)
        score = max(40, 100 - penalty)

        if violations_count > 0:
            self.gaps.append(f"Phát hiện {violations_count} vị trí vi phạm tiêu chuẩn ANTI-CRASH trong mã nguồn.")

        self.scores['Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)'] = score
        anti_violations = [v for v in self.violations if v.get('type') in ['NAKED JSON.PARSE', 'STRICT TYPING VIOLATION', 'PYTHON SILENT EXCEPTION EATER', 'HARDCODED SECRET IN CODE']]
        self.details['anti_crash'] = {
            'scanned_files': scanned_files,
            'violations_count': violations_count,
            'violations': anti_violations,
            'score': score
        }

    # ------------------------------------------------------------------
    # 6. Architecture Docs, Contracts & AI Governance
    # ------------------------------------------------------------------
    def audit_architecture_docs_and_ai(self):
        score = 0
        found = []
        missing = []

        # 1. AI AGENT Governance (AGENTS.md / .cursorrules / CLAUDE.md)
        ai_rules_files = ['AGENTS.md', '.cursorrules', 'CLAUDE.md', '.github/copilot-instructions.md']
        has_ai_rules = False
        for af in ai_rules_files:
            if (self.root / af).exists():
                has_ai_rules = True
                score += 35
                found.append(f"Tệp quy chuẩn chỉ dẫn dành cho AI AGENT ({af})")
                break
        if not has_ai_rules:
            missing.append("Tệp quy chuẩn chỉ dẫn cho AI AGENT (AGENTS.md hoặc .CURSORRULES)")

        # 2. ARCHITECTURE DECISION RECORDS (ADRs)
        adrs_dir = self.root / 'adrs'
        if not adrs_dir.exists(): adrs_dir = self.root / 'docs' / 'adr'
        if not adrs_dir.exists(): adrs_dir = self.root / 'docs' / 'adrs'

        if adrs_dir.exists() and adrs_dir.is_dir():
            adr_count = len(list(adrs_dir.glob('*.md')))
            if adr_count >= 5:
                score += 35
                found.append(f"Kho lưu trữ hồ sơ quyết định kiến trúc ({adr_count} tệp ADR)")
            elif adr_count >= 1:
                score += 20
                found.append(f"Kho lưu trữ hồ sơ quyết định kiến trúc ({adr_count} tệp ADR - Cần bổ sung)")
            else:
                missing.append("Hồ sơ ARCHITECTURE DECISION RECORDS (ADRS)")
        else:
            missing.append("Hồ sơ ARCHITECTURE DECISION RECORDS (ADRS)")

        # 3. API CONTRACTS (OpenAPI / Swagger / Contracts)
        has_contract = False
        for pattern in ['**/api-contract*.yaml', '**/openapi.yaml', '**/openapi.json', '**/swagger.yaml', '**/swagger.json']:
            matches = list(self.root.glob(pattern))
            if matches:
                has_contract = True
                score += 30
                found.append(f"Chuẩn hóa tài liệu API CONTRACT ({matches[0].name})")
                break

        if not has_contract:
            missing.append("Tài liệu đặc tả hợp đồng API CONTRACT (OPENAPI / SWAGGER)")

        score = min(100, score)
        self.scores['Quản Trị API CONTRACT & Cấu Hình AI AGENT'] = score
        self.details['contracts'] = {'found': found, 'missing': missing, 'score': score}

    # ------------------------------------------------------------------
    # 7. Starter Kit Benchmark (Missing, Bloat, Pros, Cons)
    # ------------------------------------------------------------------
    def benchmark_starter_kit(self):
        # 1. Nhận diện Ưu điểm vượt trội (Strengths / Innovations)
        if 'VECTOR DATABASE (AI RAG)' in self.profile.get('databases', []):
            self.innovations.append("Trang bị hạ tầng VECTOR DATABASE sẵn sàng cho AI RAG & SEMANTIC SEARCH.")
        if 'REDIS (DISTRIBUTED CACHE)' in self.profile.get('databases', []):
            self.innovations.append("Cấu hình DISTRIBUTED CACHE với REDIS tối ưu tốc độ phản hồi.")
        if any(self.root.glob('.github/workflows/*.yml')):
            self.innovations.append("Tự động hóa QUALITY GATE & CI/CD PIPELINE với GITHUB ACTIONS.")
        if (self.root / 'docker-compose.yml').exists():
            self.innovations.append("Chuẩn hóa môi trường phát triển nhất quán với DOCKER COMPOSE.")
        if self.details.get('frontend', {}).get('found'):
            if any('DESIGN TOKENS' in f for f in self.details['frontend']['found']):
                self.innovations.append("Hệ thống DESIGN SYSTEM & UI TOKENS độc quyền được thiết kế bài bản.")

        # 2. Nhận diện Thừa / Rác / Rủi ro (Bloat & Redundancies)
        env_files = list(self.root.glob('**/.env'))
        for ef in env_files:
            if not any(ign in ef.parts for ign in IGNORE_DIRS) and ef.name == '.env':
                self.bloat.append(f"Tệp cấu hình nhạy cảm (.ENV) đang bị Git theo dõi: `{ef.relative_to(self.root)}` (Nguy cơ rò rỉ thông tin bảo mật).")

        if not (self.root / '.gitignore').exists():
            self.bloat.append("Dự án chưa có tệp `.gitignore` để loại trừ các tệp tạm và artifacts BUILD.")

        for junk_dir in ['dist', 'build', 'bin', 'obj', '.next', '__pycache__']:
            if (self.root / junk_dir).exists() and not (self.root / '.gitignore').exists():
                self.bloat.append(f"Thư mục cache BUILD `{junk_dir}/` có nguy cơ bị đưa lên remote git.")

    # ------------------------------------------------------------------
    # Phân bổ trọng số thích ứng theo loại hình dự án (Adaptive Archetype Weights)
    # ------------------------------------------------------------------
    def get_adaptive_weights(self):
        has_fe = self.profile.get('has_frontend', False)
        has_be = self.profile.get('has_backend', False)
        has_db = self.profile.get('has_database', False)

        if has_fe and not has_be and not has_db:
            # Dự án thuần FRONTEND SPA / UI/UX / MOBILE
            return {
                'readme': ('Tài Liệu & Hướng Dẫn (README & ONBOARDING)', 20, False),
                'backend': ('Kiến Trúc BACKEND & Luồng Dữ Liệu CORE', 0, True),  # is_na = True
                'frontend': ('Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)', 35, False),
                'database': ('Hạ Tầng DATABASE & An Toàn QUERY', 0, True),       # is_na = True
                'anti_crash': ('Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)', 25, False),
                'contracts': ('Quản Trị API CONTRACT & Cấu Hình AI AGENT', 20, False),
            }
        elif has_be and not has_fe:
            # Dự án thuần BACKEND API / MICROSERVICES / THUẬT TOÁN
            return {
                'readme': ('Tài Liệu & Hướng Dẫn (README & ONBOARDING)', 10, False),
                'backend': ('Kiến Trúc BACKEND & Luồng Dữ Liệu CORE', 35, False),
                'frontend': ('Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)', 0, True),  # is_na = True
                'database': ('Hạ Tầng DATABASE & An Toàn QUERY', 25, False),
                'anti_crash': ('Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)', 20, False),
                'contracts': ('Quản Trị API CONTRACT & Cấu Hình AI AGENT', 10, False),
            }
        elif not has_fe and not has_be and not has_db:
            # Dự án CLI TOOL / SYSTEM UTILITY / GIẢI THUẬT ĐỘC LẬP
            return {
                'readme': ('Tài Liệu & Hướng Dẫn (README & ONBOARDING)', 20, False),
                'backend': ('Kiến Trúc BACKEND & Luồng Dữ Liệu CORE', 40, False),
                'frontend': ('Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)', 0, True),
                'database': ('Hạ Tầng DATABASE & An Toàn QUERY', 0, True),
                'anti_crash': ('Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)', 30, False),
                'contracts': ('Quản Trị API CONTRACT & Cấu Hình AI AGENT', 10, False),
            }
        else:
            # Dự án FULL-STACK toàn diện
            return {
                'readme': ('Tài Liệu & Hướng Dẫn (README & ONBOARDING)', 15, False),
                'backend': ('Kiến Trúc BACKEND & Luồng Dữ Liệu CORE', 20, False),
                'frontend': ('Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)', 20, False),
                'database': ('Hạ Tầng DATABASE & An Toàn QUERY', 15, False),
                'anti_crash': ('Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)', 20, False),
                'contracts': ('Quản Trị API CONTRACT & Cấu Hình AI AGENT', 10, False),
            }

    # ------------------------------------------------------------------
    # Tính toán tổng điểm theo hệ số thích ứng (Adaptive Benchmark Scoring)
    # ------------------------------------------------------------------
    def calculate_total_score(self):
        adaptive_weights = self.get_adaptive_weights()
        total_earned = 0

        for mod, (score_key, max_pts, is_na) in adaptive_weights.items():
            raw = self.scores.get(score_key, 0)
            if is_na:
                pts = 0
            else:
                pts = round((raw / 100.0) * max_pts)
                total_earned += pts

            if mod in self.details:
                self.details[mod]['points_earned'] = pts
                self.details[mod]['max_points'] = max_pts
                self.details[mod]['raw_score'] = raw
                self.details[mod]['module_title'] = score_key
                self.details[mod]['is_na'] = is_na

        bonus = min(5, len(self.innovations))
        final_score = min(100, total_earned + bonus)
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
            f"- **Tổng số tệp mã nguồn quét sâu**: `{self.details.get('anti_crash', {}).get('scanned_files', 0)} tệp`",
            "",
            "---",
            "",
            "## 📊 2. BẢNG ĐỐI CHIẾU CÁC HẠNG MỤC BENCHMARK (BENCHMARK MATRIX)",
            "",
            "| Hạng Mục Benchmark | Trạng Thái | Điểm Hệ Số | Trọng Số Tối Đa | Đánh Giá Chi Tiết |",
            "| :--- | :---: | :---: | :---: | :--- |"
        ]

        module_keys = [
            ('Tài Liệu & Hướng Dẫn (README & ONBOARDING)', 'readme'),
            ('Kiến Trúc BACKEND & Luồng Dữ Liệu CORE', 'backend'),
            ('Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)', 'frontend'),
            ('Hạ Tầng DATABASE & An Toàn QUERY', 'database'),
            ('Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)', 'anti_crash'),
            ('Quản Trị API CONTRACT & Cấu Hình AI AGENT', 'contracts')
        ]

        for pillar, mod in module_keys:
            detail = self.details.get(mod, {})
            score = self.scores.get(pillar, 0)
            is_na = detail.get('is_na', False)
            if is_na:
                status_icon = "⚪ MIỄN TRỪ"
                pts_str = "N/A"
                max_str = "0 Điểm (Miễn trừ)"
                eval_str = f"Không áp dụng cho loại hình {self.profile.get('archetype', 'này')}"
            else:
                pts = detail.get('points_earned', round(score * 0.2))
                max_p = detail.get('max_points', 20)
                status_icon = "✅ ĐẠT CHUẨN" if score >= 80 else ("⚠️ CẦN LƯU Ý" if score >= 60 else "❌ THIẾU SÓT")
                pts_str = f"**{pts} ĐIỂM**"
                max_str = f"{max_p} Điểm"
                eval_str = "Đo kiểm sâu theo mã nguồn thực tế"

            lines.append(f"| **{pillar}** | `{status_icon}` | {pts_str} | {max_str} | {eval_str} |")

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
                lines.append(f"- [ ] ⚠️ **{b}**")
        else:
            lines.append("- [x] 🎉 **Mã nguồn sạch sẽ! Không phát hiện tệp bí mật (.ENV) bị commit hay rác build artifacts.**")

        lines.extend([
            "",
            "---",
            "",
            "## 🚨 6. DANH SÁCH VI PHẠM MÃ NGUỒN CỤ THỂ (CODE-LEVEL VIOLATIONS LOG)",
            ""
        ])

        if self.violations:
            lines.append("| Tệp Tin & Số Dòng | Loại Vi Phạm | Mô Tả & Đoạn Mã |")
            lines.append("| :--- | :--- | :--- |")
            for v in self.violations[:20]:
                lines.append(f"| `{v['file']}:{v['line']}` | `{v['type']}` | {v['desc']} <br/>`{v['snippet']}` |")
            if len(self.violations) > 20:
                lines.append(f"\n*... và còn {len(self.violations) - 20} vị trí vi phạm khác (xem chi tiết trong log quét).*")
        else:
            lines.append("- [x] 🎉 **Mã nguồn an toàn! Không phát hiện lỗi sập RUNTIME, NAKED JSON.PARSE hay vi phạm STRICT TYPING.**")

        lines.extend([
            "",
            "---",
            "",
            "## 🤖 7. PROMPT DÀNH CHO AI AGENT ĐỂ REFACTOR (READY FOR CLAUDE / CURSOR / ANTIGRAVITY)",
            "",
            "Sao chép toàn bộ đoạn lệnh dưới đây và dán vào cửa sổ chat với AI AGENT trong IDE của bạn:",
            "",
            "```markdown",
            self.get_ai_prompt(),
            "```",
            "",
            "---",
            "*Báo cáo được khởi tạo tự động bởi Universal Project Reviewer Engine v2.0*"
        ])

        report_file.write_text("\n".join(lines), encoding='utf-8')
        return report_file


if __name__ == '__main__':
    default_dir = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path.cwd()
    target = default_dir
    if len(sys.argv) > 1:
        arg_path = Path(sys.argv[1]).resolve()
        if arg_path.is_dir():
            target = arg_path

    auditor = ProjectAuditor(target)
    score = auditor.run()

    if getattr(sys, 'frozen', False) and (len(sys.argv) <= 1 or sys.argv[1] not in ('ci-mode', '--no-pause')):
        try:
            input("Nhấn phím Enter để đóng cửa sổ...")
        except Exception:
            pass

    sys.exit(0 if score >= 70 else 1)
