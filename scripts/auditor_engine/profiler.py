"""Nhận diện tech stack, kiến trúc và năng lực kỹ thuật của dự án."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .tree import ProjectTree


class ProjectProfiler:

    """Tự động nhận diện TECH STACK, kiểu ARCHITECTURE và các năng lực kỹ thuật của dự án."""

    def __init__(self, root: Path, tree: ProjectTree = None):
        self.read_errors = []  # lỗi đọc tệp không nghiêm trọng (được ghi lại thay vì nuốt im lặng)

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

        # Bằng chứng thô cho pillar Cloud/DevOps; has_cloud được chốt ở cuối profile() (ADR-0024)
        self._container_intent = False
        self._has_ci = False

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

            self._inspect_dotnet()

            # Chỉ coi là backend khi csproj thật sự là dự án web (không phải app desktop/console/thư viện)
            if any(re.search(r'Microsoft\.NET\.Sdk\.Web|Microsoft\.AspNetCore', self._read_text(c))
                   for c in self.tree.find_by_ext('.csproj')):

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

        # 2. Nhận diện INFRASTRUCTURE & DATABASE từ Docker Compose

        docker_compose = None

        for dc in ['docker-compose.yml', 'docker-compose.yaml', 'compose.yaml', 'compose.yml']:

            matches = self.tree.find_by_name(dc)

            if matches:

                docker_compose = matches[0]

                break

        if docker_compose and docker_compose.exists():

            self.tools.add('DOCKER COMPOSE')

            self._container_intent = True

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

            self._container_intent = True

        if has_k8s:

            self._container_intent = True

        if has_ci:

            self._has_ci = True

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

        # ADR-0024: pillar Cloud/DevOps chỉ áp dụng khi dự án có ý định đóng gói/triển khai
        # (Dockerfile, compose, k8s/helm) hoặc có CI kèm một dịch vụ triển khai được.
        # CI đơn thuần trên kho tri thức/thư viện/CLI không kích hoạt tiêu chí Docker.
        deployable = self.has_backend or self.has_frontend or self.has_microservices
        self.has_cloud = self._container_intent or (self._has_ci and deployable)

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

            try:
                content += rf.read_text(encoding='utf-8', errors='ignore').lower() + "\n"
            except OSError as e:
                self.read_errors.append(f"{rf}: {e}")

        for pf in pyproj_files:

            try:
                content += pf.read_text(encoding='utf-8', errors='ignore').lower() + "\n"
            except OSError as e:
                self.read_errors.append(f"{pf}: {e}")

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

    @staticmethod
    def _read_text(path):

        try:

            return path.read_text(encoding='utf-8', errors='ignore')

        except OSError:

            return ''

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
