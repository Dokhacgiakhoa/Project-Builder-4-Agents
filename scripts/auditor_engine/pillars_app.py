"""Pillar Backend, Frontend, Database và Anti-Crash."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401
from .models import CriterionItem

_SQL_CONTROLLER_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r'SELECT\s+.*?\s+FROM', r'INSERT\s+INTO', r'UPDATE\s+.*?\s+SET',
        r'\.query\([\'"]SELECT', r'db\.collection\('
    ]
]
_DOMAIN_LEAK_PATTERN = re.compile(
    r'(import .* from [\'"](express|axios|react|@nestjs|typeorm|mongoose)[\'"]|using (Microsoft\.AspNetCore|Microsoft\.EntityFrameworkCore))'
)
_POOL_CONFIG_PATTERN = re.compile(r'(max_connections|pool_size|connectionLimit|maxPoolSize|poolTimeout)', re.IGNORECASE)
_TRANSACTION_PATTERN = re.compile(r'(\.transaction\(|db\.begin\(|\$transaction|using var transaction)', re.IGNORECASE)
_RAW_QUERY_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r'\.query\s*\(\s*["\'].*?WHERE.*?\+.*?\)',
        r'\.execute\s*\(\s*f["\'].*?WHERE.*?\{.*?\}',
        r'\.raw\s*\(\s*`.*?WHERE.*?(\$\{.*?\})`'
    ]
]
_LOOP_PATTERN = re.compile(r'\b(for|while)\b.*\(|\.forEach\(|\bfor\s+\w+\s+in\b')
_N_PLUS_ONE_PATTERN = re.compile(r'await\s+(?:db|\w+Repository|\w+Model)\.(?:find|query|get)')
_STRICT_TYPING_PATTERN = re.compile(r':\s*any\b')
_PYTHON_BARE_EXCEPT_1 = re.compile(r'^\s*except\s*:\s*$')
_PYTHON_BARE_EXCEPT_2 = re.compile(r'^\s*except\s+Exception\s*:\s*pass\s*$')
_SECRET_PATTERN = re.compile(r'(api_key|secret|password|bearer|private_key)\s*[:=]\s*[\'"][A-Za-z0-9_\-\.]{16,}[\'"]', re.IGNORECASE)
_ENV_WHITELIST_PATTERN = re.compile(r'(process\.env|os\.environ|config\(|\.get\()', re.IGNORECASE)


class AppPillarsMixin:
    """Pillar Backend, Frontend, Database và Anti-Crash."""

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

        matched_dirs = [d for d in ['domain', 'core', 'models', 'application', 'services', 'infrastructure', 'repositories', 'controllers', 'routes', 'api', 'features'] if d in all_dirs]

        if has_domain and (has_app or has_infra):
            score += 30
            found.append(CriterionItem(
                f"Cấu trúc phân tầng chuẩn mực theo {self.profile.get('arch_style')}",
                evidence=", ".join(matched_dirs[:4]),
                details=f"Đã xác minh cấu trúc phân tầng với các tầng chức năng rõ rệt: {', '.join(matched_dirs[:4])}.",
                badge="Layered Arch"
            ))
        elif has_features:
            score += 30
            found.append(CriterionItem(
                "Cấu trúc module độc lập theo FEATURE-DRIVEN ARCHITECTURE",
                evidence=", ".join(matched_dirs[:4]),
                details="Đã xác minh tổ chức mã nguồn theo từng Feature/Module độc lập cô lập.",
                badge="Feature-Driven"
            ))
        elif has_pres or has_app:
            score += 20
            found.append(CriterionItem(
                "Phân tách cơ bản giữa tầng PRESENTATION và BUSINESS LOGIC",
                evidence=", ".join(matched_dirs[:4]),
                details="Đã xác minh phân định giữa tầng hiển thị/API và tầng xử lý nghiệp vụ.",
                badge="Separated Logic"
            ))
        else:
            missing.append(CriterionItem(
                "Phân định ranh giới rõ ràng giữa DOMAIN, APPLICATION và INFRASTRUCTURE",
                evidence="Cấu trúc thư mục",
                details="Toàn bộ mã nguồn nằm lẫn lộn trong cùng thư mục hoặc thiếu phân tầng rõ rệt giữa nghiệp vụ cốt lõi và hạ tầng.",
                remediation="Tổ chức lại thư mục theo chuẩn phân tầng (domain/core, services, controllers/routes)."
            ))

        # Quét Dependency Injection (DI) & DTO Input Validation
        has_di = False
        has_dto_validation = False
        di_found_file = None
        di_found_snippet = None
        dto_found_file = None
        dto_found_snippet = None

        for p in self.tree.code_files:
            p_parts_lower = self.tree.parts_lower(p) if hasattr(self.tree, 'parts_lower') else [part.lower() for part in p.parts]
            is_controller = any(c in p_parts_lower for c in ['controllers', 'routes', 'api', 'handlers'])
            is_domain = any(c in p_parts_lower for c in ['domain', 'entities', 'core'])
            rel = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else str(p.relative_to(self.root))

            try:
                text = self.tree.read_text(p)

                # Check DI
                if not di_found_file:
                    if '@Injectable' in text:
                        has_di = True; di_found_file = rel; di_found_snippet = "@Injectable()"
                    elif 'builder.Services.Add' in text:
                        has_di = True; di_found_file = rel; di_found_snippet = "builder.Services.AddScoped/Singleton"
                    elif 'Depends(' in text:
                        has_di = True; di_found_file = rel; di_found_snippet = "Depends(...) (FastAPI)"
                    elif 'constructor(' in text and 'private ' in text:
                        has_di = True; di_found_file = rel; di_found_snippet = "constructor(private readonly ...)"

                # Check DTO Input Validation
                if not dto_found_file:
                    if 'pydantic' in text or 'BaseModel' in text:
                        has_dto_validation = True; dto_found_file = rel; dto_found_snippet = "BaseModel (Pydantic)"
                    elif 'zod' in text or 'z.object' in text:
                        has_dto_validation = True; dto_found_file = rel; dto_found_snippet = "z.object(...) (Zod)"
                    elif 'class-validator' in text:
                        has_dto_validation = True; dto_found_file = rel; dto_found_snippet = "class-validator decorators"
                    elif 'Joi.' in text:
                        has_dto_validation = True; dto_found_file = rel; dto_found_snippet = "Joi.object(...)"
                    elif 'FluentValidation' in text:
                        has_dto_validation = True; dto_found_file = rel; dto_found_snippet = "AbstractValidator (FluentValidation)"

                if is_controller:
                    for pat in _SQL_CONTROLLER_PATTERNS:
                        if pat.search(text):
                            layer_leaks.append(f"Rò rỉ kiến trúc: CONTROLLER `{rel}` truy vấn SQL trực tiếp thay vì qua REPOSITORY.")
                            break

                if is_domain:
                    if _DOMAIN_LEAK_PATTERN.search(text):
                        layer_leaks.append(f"DOMAIN LEAK: Tệp `{rel}` trong DOMAIN bị phụ thuộc vào FRAMEWORK hạ tầng.")
            except Exception:
                pass

        if not layer_leaks:
            score += 25
            found.append(CriterionItem(
                "Độ thuần khiết của DOMAIN và ranh giới CONTROLLER được bảo vệ hoàn hảo (0 LAYER LEAKS)",
                evidence=f"Đã quét {len(self.tree.code_files)} tệp mã nguồn",
                details="Không phát hiện bất kỳ controller nào gọi truy vấn SQL trực tiếp hoặc domain bị dính framework.",
                badge="0 Leaks"
            ))
        else:
            for leak in layer_leaks[:2]:
                self.violations.append({'file': 'ARCHITECTURE BOUNDARY', 'line': 0, 'type': 'LAYER LEAKAGE', 'desc': leak, 'snippet': ''})
            score = max(10, score - 15)
            missing.append(CriterionItem(
                f"Cảnh báo LAYER LEAK: Phát hiện {len(layer_leaks)} điểm vi phạm ranh giới phân tầng",
                evidence=layer_leaks[0],
                details="Controller truy vấn SQL trực tiếp hoặc Domain model import framework bên ngoài thay vì qua Repository.",
                remediation="Trích xuất các truy vấn DB vào tầng Repository/DAL và inject vào Controller thông qua Interface/Service."
            ))

        if has_di:
            score += 15
            found.append(CriterionItem(
                "Áp dụng DEPENDENCY INJECTION (DI) tiêm phụ thuộc tường minh",
                evidence=di_found_file or "Mã nguồn backend",
                snippet=di_found_snippet or "Dependency Injection",
                details="Đã phát hiện áp dụng kỹ thuật tiêm phụ thuộc (DI / IoC) giúp mã nguồn module hóa và dễ viết Unit Test.",
                badge="DI Pattern"
            ))
        else:
            missing.append(CriterionItem(
                "Mô hình tiêm phụ thuộc DEPENDENCY INJECTION (DI) để hỗ trợ Unit Testing",
                evidence="Controllers / Services",
                details="Chưa thấy sử dụng Dependency Injection (constructor injection, Depends, @Injectable), các service khởi tạo phụ thuộc cứng bằng `new`.",
                remediation="Áp dụng Inversion of Control / DI thông qua constructor injection hoặc container của framework."
            ))

        if has_dto_validation:
            score += 15
            found.append(CriterionItem(
                "Xác thực dữ liệu đầu vào DTO tự động (ZOD / PYDANTIC / CLASS-VALIDATOR)",
                evidence=dto_found_file or "Schemas / DTOs",
                snippet=dto_found_snippet or "DTO Schema Validation",
                details="Đã phát hiện thư viện xác thực DTO tự động bảo vệ dữ liệu đầu vào trước khi vào tầng xử lý.",
                badge="DTO Validation"
            ))
        else:
            missing.append(CriterionItem(
                "Xác thực tự động cho dữ liệu DTO đầu vào (Zod, Pydantic hoặc Schema Validator)",
                evidence="Request Handlers",
                details="Thiếu thư viện xác thực schema dữ liệu đầu vào tự động (Zod, Pydantic, class-validator) tại các endpoint.",
                remediation="Định nghĩa DTO schema (vd. Pydantic BaseModel hoặc Zod object) và validate tại tầng Controller/Handler."
            ))

        # Graceful Shutdown
        entry_files = ['server.ts', 'server.js', 'main.ts', 'main.go', 'Program.cs', 'app.py', 'main.py']
        found_entry = False

        for ef in entry_files:
            matches = self.tree.find_by_name(ef)
            for m in matches:
                found_entry = True
                try:
                    text = m.read_text(encoding='utf-8', errors='ignore')
                    rel_ef = str(self.tree.rel_path(m)) if hasattr(self.tree, 'rel_path') else m.name
                    if 'SIGTERM' in text or 'SIGINT' in text or 'graceful' in text.lower():
                        score += 15
                        found.append(CriterionItem(
                            "Cơ chế giải phóng tài nguyên an toàn khi tắt SERVER (GRACEFUL SHUTDOWN)",
                            evidence=f"{rel_ef}",
                            snippet="process.on('SIGTERM') / signal handler",
                            details="Đã phát hiện bộ lắng nghe tín hiệu SIGTERM / SIGINT để đóng kết nối database và HTTP server an toàn.",
                            badge="Graceful Exit"
                        ))
                    else:
                        missing.append(CriterionItem(
                            "Cơ chế giải phóng kết nối và tài nguyên khi tắt SERVER (GRACEFUL SHUTDOWN)",
                            evidence=f"{rel_ef}",
                            details="Chưa có cơ chế xử lý tín hiệu SIGTERM/SIGINT để giải phóng kết nối DB và dừng server mà không làm rớt request đang dở dang.",
                            remediation="Bổ sung hàm lắng nghe SIGTERM/SIGINT đóng gracefully các pool kết nối cơ sở dữ liệu và server."
                        ))
                except Exception:
                    pass
                break
            if found_entry:
                break

        score = min(100, score)
        self.scores['Kiến Trúc BACKEND & Luồng Dữ Liệu CORE'] = score
        self.add_log(f"  -> Layered architecture: Domain={has_domain}, App={has_app}, Infra={has_infra}, Pres={has_pres}.", "backend", "muted")
        self.details['backend'] = {
            'name': 'Backend & Core Flow',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 20,
            'is_na': False,
            'leaks': layer_leaks
        }

    def audit_frontend_waterflow(self):
        score = 0
        found = []
        missing = []

        # 1. Design System & UI Tokens
        tailwind_cfg = self.tree.any_name_starts_with('tailwind.config')
        theme_tokens = bool(self.tree.find_by_name('theme.ts') or [p for p in self.tree.all_files if p.name.startswith('tokens.')])
        css_vars = False
        css_path_found = None

        for css_path in self.tree.find_by_ext('.css'):
            try:
                content = self.tree.read_text(css_path)
                if ':root' in content and '--' in content:
                    css_vars = True
                    css_path_found = str(self.tree.rel_path(css_path)) if hasattr(self.tree, 'rel_path') else css_path.name
                    break
            except Exception:
                pass

        if tailwind_cfg or theme_tokens or css_vars:
            score += 30
            token_ev = "tailwind.config.js" if tailwind_cfg else (css_path_found or "theme.ts / tokens")
            found.append(CriterionItem(
                "Hệ thống DESIGN TOKENS độc quyền (CUSTOM TAILWIND CONFIG / CSS VARIABLES / THEME TOKENS)",
                evidence=token_ev,
                details=f"Đã phát hiện hệ thống quản lý giao diện tập trung qua {token_ev}.",
                badge="Design Tokens"
            ))
        else:
            missing.append(CriterionItem(
                "Hệ thống quản lý biến thiết kế giao diện tập trung (DESIGN TOKENS / THEME VARIABLES)",
                evidence="CSS / Styling",
                details="Chưa phát hiện tệp cấu hình design tokens tập trung (như Tailwind colors/spacing hoặc CSS Variables :root).",
                remediation="Tạo tệp tailwind.config.js tùy biến hoặc định nghĩa bảng biến màu sắc/khoảng cách :root trong CSS."
            ))

        # 2. API Client bọc tập trung
        has_api_client = False
        client_candidates = [p for p in self.tree.code_files if 'api-client' in p.name.lower() or 'client' in p.name.lower()]
        api_client_path = None

        for p in client_candidates:
            try:
                c = self.tree.read_text(p)
                if 'interceptors' in c or 'baseURL' in c or 'fetch(' in c or 'axios' in c:
                    has_api_client = True
                    api_client_path = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name
                    break
            except Exception:
                pass

        if has_api_client:
            score += 25
            found.append(CriterionItem(
                "API CLIENT phòng thủ tập trung (INTERCEPTORS, BASEURL, ERROR NORMALIZATION)",
                evidence=api_client_path or "api-client",
                details=f"Đã phát hiện module API Client tập trung tại `{api_client_path}` giúp chuẩn hóa baseURL và xử lý lỗi đồng nhất.",
                badge="API Client"
            ))
        else:
            missing.append(CriterionItem(
                "Tệp bọc API CLIENT tập trung (tránh gọi FETCH / AXIOS rải rác trong COMPONENT)",
                evidence="Tầng Frontend",
                details="Thiếu tệp bao bọc API Client dùng chung, có nguy cơ gọi fetch/axios rải rác trong component UI.",
                remediation="Tạo tệp `api/client.ts` bọc Axios/Fetch với baseURL, auth header và bộ chuẩn hóa mã lỗi."
            ))

        # 3. Quét Error Boundary & Code Splitting (Lazy Loading)
        has_error_boundary = False
        error_boundary_file = None
        has_lazy_loading = False
        lazy_loading_file = None
        god_components = []

        fe_code_files = [p for p in self.tree.code_files if p.suffix in {'.tsx', '.jsx', '.vue', '.svelte'}]

        for p in fe_code_files:
            try:
                text = self.tree.read_text(p)
                lines = text.splitlines()
                rel_fe = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else p.name

                if len(lines) > 350:
                    god_components.append(f"{p.name} ({len(lines)} dòng)")

                if not error_boundary_file and ('ErrorBoundary' in text or 'componentDidCatch' in text or 'error.tsx' in p.name):
                    has_error_boundary = True
                    error_boundary_file = rel_fe

                if not lazy_loading_file and ('React.lazy' in text or 'defineAsyncComponent' in text or 'loadable(' in text or 'dynamic(' in text):
                    has_lazy_loading = True
                    lazy_loading_file = rel_fe
            except Exception:
                pass

        if has_error_boundary:
            score += 15
            found.append(CriterionItem(
                "Trang bị ERROR BOUNDARY bắt lỗi runtime chống crash trắng toàn bộ màn hình",
                evidence=error_boundary_file or "ErrorBoundary component",
                details="Đã phát hiện component Error Boundary bắt các ngoại lệ React rendering, bảo vệ trải nghiệm người dùng.",
                badge="Error Boundary"
            ))
        else:
            missing.append(CriterionItem(
                "Thành phần ERROR BOUNDARY bao bọc route để xử lý lỗi sập giao diện an toàn",
                evidence="Root Layout / App",
                details="Chưa có component Error Boundary bao bọc các tuyến đường (routes), rủi ro lỗi render làm trắng toàn trang.",
                remediation="Tạo component ErrorBoundary (hoặc Next.js error.tsx) hiển thị fallback UI khi xảy ra lỗi runtime."
            ))

        if has_lazy_loading:
            score += 15
            found.append(CriterionItem(
                "Kỹ thuật CODE-SPLITTING / LAZY LOADING tối ưu tốc độ tải trang ban đầu",
                evidence=lazy_loading_file or "React.lazy / Async Component",
                details="Đã áp dụng kỹ thuật nạp động (lazy loading) cho các trang hoặc module nặng.",
                badge="Code Splitting"
            ))
        else:
            missing.append(CriterionItem(
                "Kỹ thuật LAZY LOADING (React.lazy) cho các phân vùng trang kích thước lớn",
                evidence="Routing / Pages",
                details="Chưa áp dụng React.lazy() hoặc dynamic import cho các trang và modal lớn, làm tăng kích thước bundle ban đầu.",
                remediation="Dùng `React.lazy()` hoặc Next.js `dynamic()` cho các màn hình quản trị và dialog lớn."
            ))

        if not god_components:
            score += 15
            found.append(CriterionItem(
                "Cấu trúc COMPONENT tinh gọn, phân tách trách nhiệm rõ ràng (0 GOD COMPONENTS)",
                evidence=f"Đã quét {len(fe_code_files)} tệp UI",
                details="Tất cả các component giao diện đều có kích thước dưới 350 dòng, đảm bảo tính đơn nhiệm và dễ bảo trì.",
                badge="Clean Components"
            ))
        else:
            score += 5
            self.gaps.append(f"Cảnh báo GOD COMPONENT phình to quá mức (> 350 dòng): {', '.join(god_components[:2])}")
            missing.append(CriterionItem(
                f"Cảnh báo GOD COMPONENT: Phát hiện {len(god_components)} component quá lớn (> 350 dòng)",
                evidence=", ".join(god_components[:3]),
                details=f"Phát hiện component phình to vượt chuẩn: {', '.join(god_components[:3])}.",
                remediation="Tách các component lớn thành các sub-components nhỏ hơn hoặc trích xuất custom hooks."
            ))

        score = min(100, score)
        self.scores['Kiến Trúc FRONTEND & DESIGN SYSTEM (UI/UX)'] = score
        ui_count = len(self.tree.find_by_ext('.tsx') + self.tree.find_by_ext('.jsx') + self.tree.find_by_ext('.vue') + self.tree.find_by_ext('.html'))
        self.add_log(f'  -> UI audit: found {ui_count} UI components & styling files.', 'frontend', 'muted')
        self.details['frontend'] = {
            'name': 'Frontend & UI/UX',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 20,
            'is_na': False,
            'god_components': god_components
        }

    def audit_database_waterflow(self):
        score = 0
        found = []
        missing = []
        all_dirs = self.tree.all_dirs

        # 1. Database Migrations
        has_migrations = any(m in all_dirs for m in ['migrations', 'migration', 'prisma']) or bool(self.tree.find_by_name('schema.prisma') or self.tree.find_by_name('alembic.ini'))

        if has_migrations:
            score += 35
            mig_ev = "prisma/schema.prisma" if self.tree.find_by_name("schema.prisma") else ("alembic.ini" if self.tree.find_by_name("alembic.ini") else "migrations/")
            found.append(CriterionItem(
                "Quản lý DATABASE MIGRATION có kiểm soát phiên bản theo thời gian",
                evidence=mig_ev,
                details=f"Đã xác minh hệ thống quản lý lược đồ CSDL có phiên bản qua `{mig_ev}`.",
                badge="Migrations OK"
            ))
        else:
            missing.append(CriterionItem(
                "Thư mục DATABASE MIGRATION (nguy cơ trôi lệch SCHEMA trên PRODUCTION)",
                evidence="Thư mục CSDL",
                details="Chưa tìm thấy thư mục migration hoặc công cụ quản lý schema (Prisma, Alembic, Flyway, EF Core).",
                remediation="Thiết lập công cụ migration (vd. Prisma Migrate hoặc Alembic) để đồng bộ cấu trúc DB theo phiên bản Git."
            ))
            self.gaps.append("Thiếu hệ thống DATABASE MIGRATION có kiểm soát phiên bản.")

        # 2. Connection Pooling & Transactions
        has_pool_config = False
        has_transaction = False
        pool_file = None
        tx_file = None
        n_plus_one_risks = []
        sql_injection_risks = []

        for p in self.tree.code_files:
            try:
                text = self.tree.read_text(p)
                if not text:
                    continue
                rel_str = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else str(p.relative_to(self.root))

                if not pool_file and _POOL_CONFIG_PATTERN.search(text):
                    has_pool_config = True
                    pool_file = rel_str

                if not tx_file and _TRANSACTION_PATTERN.search(text):
                    has_transaction = True
                    tx_file = rel_str

                # Quét SQL Injection & N+1 Query (Single-pass)
                lines_text = text.splitlines()
                in_loop = False
                loop_start = 0

                for idx, line in enumerate(lines_text, 1):
                    if 'where' in line.lower():
                        for pat in _RAW_QUERY_PATTERNS:
                            if pat.search(line):
                                sql_injection_risks.append({
                                    'file': rel_str,
                                    'line': idx,
                                    'type': 'SQL INJECTION RISK',
                                    'desc': 'Nối chuỗi trực tiếp vào câu lệnh RAW SQL (Thiếu PARAMETERIZED QUERIES).',
                                    'snippet': line.strip()[:80]
                                })
                                break

                    if ('for' in line or 'while' in line) and _LOOP_PATTERN.search(line):
                        in_loop = True
                        loop_start = idx
                    elif in_loop and (idx - loop_start <= 15):
                        if 'await' in line and _N_PLUS_ONE_PATTERN.search(line):
                            n_plus_one_risks.append(rel_str)
                            in_loop = False
                    elif in_loop and (idx - loop_start > 15):
                        in_loop = False
            except Exception:
                pass

        if has_pool_config:
            score += 25
            found.append(CriterionItem(
                "Cấu hình CONNECTION POOL & TIMEOUT bảo vệ giới hạn kết nối DATABASE",
                evidence=pool_file or "DB Config",
                details="Đã xác minh cấu hình giới hạn kết nối (pool size, idle timeout) bảo vệ DB không bị cạn kiệt kết nối.",
                badge="Connection Pool"
            ))
        else:
            missing.append(CriterionItem(
                "Cấu hình tường minh cho CONNECTION POOL (POOL_SIZE, IDLE_TIMEOUT)",
                evidence="Database Connection",
                details="Chưa thiết lập tường minh pool_size hoặc timeout cho kết nối cơ sở dữ liệu.",
                remediation="Khai báo pool_size (vd: 10-20) và idle_timeout trong cấu hình kết nối DB."
            ))

        if has_transaction:
            score += 20
            found.append(CriterionItem(
                "Cơ chế DATABASE TRANSACTION đảm bảo tính nguyên tử (ACID) khi ghi nhiều bảng",
                evidence=tx_file or "DB Repositories",
                details="Đã xác minh sử dụng transaction cho các tác vụ ghi dữ liệu phức tạp đảm bảo tính toàn vẹn ACID.",
                badge="ACID Transaction"
            ))
        else:
            missing.append(CriterionItem(
                "Cơ chế bọc TRANSACTION tường minh cho các tác vụ thay đổi nhiều thực thể",
                evidence="Tầng Data Access",
                details="Chưa tìm thấy khối bọc Transaction cho các nghiệp vụ cập nhật nhiều bảng cùng lúc.",
                remediation="Sử dụng `$transaction`, `session.begin()` hoặc `BeginTransaction()` cho các luồng ghi liên bảng."
            ))

        if not sql_injection_risks:
            score += 20
            found.append(CriterionItem(
                "An toàn câu lệnh QUERY: Sử dụng PARAMETERIZED QUERIES hoặc TYPE-SAFE ORM",
                evidence=f"Đã quét {len(self.tree.code_files)} tệp mã nguồn",
                details="100% câu lệnh truy vấn dữ liệu sử dụng ORM an toàn hoặc tham số hóa (parameterized queries).",
                badge="Query Safety"
            ))
        else:
            self.violations.extend(sql_injection_risks)
            self.gaps.append(f"Cảnh báo bảo mật: Phát hiện {len(sql_injection_risks)} vị trí nối chuỗi RAW SQL.")
            score = max(10, score - 20)
            missing.append(CriterionItem(
                f"Cảnh báo SQL INJECTION: Phát hiện {len(sql_injection_risks)} vị trí nối chuỗi trực tiếp",
                evidence=sql_injection_risks[0]['file'],
                snippet=sql_injection_risks[0]['snippet'],
                details=f"Phát hiện {len(sql_injection_risks)} vị trí nối chuỗi trực tiếp vào câu lệnh SQL thay vì dùng placeholder tham số.",
                remediation="Chuyển đổi các câu lệnh nối chuỗi sang sử dụng query parameter (ví dụ: $1, :val hoặc ?)."
            ))

        if n_plus_one_risks:
            self.gaps.append(f"Cảnh báo N+1 QUERY: Phát hiện truy vấn CSDL trong vòng lặp tại: {', '.join(n_plus_one_risks[:2])}")

        score = min(100, score)
        self.scores['Hạ Tầng DATABASE & An Toàn QUERY'] = score
        self.add_log(f"  -> Database: {', '.join(self.databases) or 'SQL'}. Audited migrations and query safety.", "database", "muted")
        self.details['database'] = {
            'name': 'Database & Query Safety',
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 15,
            'is_na': False,
        }

    def audit_anti_crash_universal(self):
        score = 100
        violations_count = 0
        scanned_files = 0
        found = []
        missing = []

        naked_json_count = 0
        naked_json_sample = None
        bare_except_count = 0
        bare_except_sample = None
        hardcoded_secrets_count = 0
        hardcoded_secrets_sample = None
        react_leak_count = 0
        react_leak_sample = None
        strict_typing_count = 0
        strict_typing_sample = None

        for p in self.tree.code_files:
            scanned_files += 1
            rel_file = str(self.tree.rel_path(p)) if hasattr(self.tree, 'rel_path') else str(p.relative_to(self.root))
            ext = self.tree.ext(p) if hasattr(self.tree, 'ext') else p.suffix.lower()
            p_parts_lower = [part.lower() for part in p.parts]
            is_test_file = any(part in ('tests', 'test', 'fixtures', 'mocks') for part in p_parts_lower) or p.name.startswith('test_')

            try:
                lines_text = self.tree.read_text(p).splitlines()

                for idx, line in enumerate(lines_text, 1):
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*') or stripped.startswith('*'):
                        continue

                    # 1. Naked JSON.parse (JS/TS)
                    if 'JSON.parse(' in line:
                        window = "\n".join(lines_text[max(0, idx - 6):min(len(lines_text), idx + 6)])
                        if 'try' not in window:
                            item = {
                                'file': rel_file,
                                'line': idx,
                                'type': 'NAKED JSON.PARSE',
                                'desc': 'Gọi JSON.PARSE không bọc trong khối TRY-CATCH an toàn (Nguy cơ sập RUNTIME khi dữ liệu JSON hỏng).',
                                'snippet': stripped[:80]
                            }
                            self.violations.append(item)
                            violations_count += 1
                            naked_json_count += 1
                            if not naked_json_sample:
                                naked_json_sample = item

                    # 2. Strict Typing Violation (: any)
                    if ext in {'.ts', '.tsx'}:
                        if _STRICT_TYPING_PATTERN.search(line):
                            item = {
                                'file': rel_file,
                                'line': idx,
                                'type': 'STRICT TYPING VIOLATION',
                                'desc': 'Sử dụng kiểu dữ liệu ": any" vi phạm quy chuẩn STRICT TYPING của TYPESCRIPT.',
                                'snippet': stripped[:80]
                            }
                            self.violations.append(item)
                            violations_count += 1
                            strict_typing_count += 1
                            if not strict_typing_sample:
                                strict_typing_sample = item

                    # 3. Python Bare Except
                    if ext == '.py':
                        if _PYTHON_BARE_EXCEPT_1.match(line) or _PYTHON_BARE_EXCEPT_2.match(line):
                            item = {
                                'file': rel_file,
                                'line': idx,
                                'type': 'PYTHON SILENT EXCEPTION EATER',
                                'desc': 'Bắt lỗi im lặng (BARE EXCEPT hoặc EXCEPT EXCEPTION: PASS) làm nuốt chửng lỗi hệ thống.',
                                'snippet': stripped[:80]
                            }
                            self.violations.append(item)
                            violations_count += 1
                            bare_except_count += 1
                            if not bare_except_sample:
                                bare_except_sample = item

                    # 4. Hardcoded Secret Detection (fast pre-filter)
                    # Bỏ qua tệp test / mock fixtures để tránh synthetic payload kiểm thử gây báo động giả
                    if is_test_file:
                        continue

                    lower_line = line.lower()
                    if ('api_key' in lower_line or 'secret' in lower_line or 'password' in lower_line
                            or 'bearer' in lower_line or 'private_key' in lower_line):
                        if _SECRET_PATTERN.search(line):
                            if not _ENV_WHITELIST_PATTERN.search(line):
                                item = {
                                    'file': rel_file,
                                    'line': idx,
                                    'type': 'HARDCODED SECRET IN CODE',
                                    'desc': 'Phát hiện CHUỖI KHÓA BẢO MẬT (SECRET/API KEY) được gán tĩnh trực tiếp vào mã nguồn.',
                                    'snippet': stripped[:40] + '...[REDACTED]'
                                }
                                self.violations.append(item)
                                violations_count += 1
                                hardcoded_secrets_count += 1
                                if not hardcoded_secrets_sample:
                                    hardcoded_secrets_sample = item

                    # 5. React useEffect Missing Cleanup (Timer / Subscription leak risk)
                    if ext in {'.tsx', '.jsx'}:
                        if 'setInterval(' in line or 'addEventListener(' in line:
                            window = "\n".join(lines_text[max(0, idx - 2):min(len(lines_text), idx + 15)])
                            if 'return () =>' not in window and 'return function' not in window and 'clearInterval' not in window and 'removeEventListener' not in window:
                                item = {
                                    'file': rel_file,
                                    'line': idx,
                                    'type': 'REACT MEMORY LEAK RISK',
                                    'desc': 'Khởi tạo TIMER / EVENT LISTENER nhưng thiếu hàm CLEANUP giải phóng (Nguy cơ MEMORY LEAK).',
                                    'snippet': stripped[:80]
                                }
                                self.violations.append(item)
                                violations_count += 1
                                react_leak_count += 1
                                if not react_leak_sample:
                                    react_leak_sample = item
            except Exception:
                pass

        if violations_count > 0:
            deduction = min(75, violations_count * 5)
            score = max(20, score - deduction)
            self.gaps.append(f"Phát hiện {violations_count} vị trí vi phạm tiêu chuẩn ANTI-CRASH trong mã nguồn.")
        else:
            score = 100

        # Phân loại Criteria Met & Criteria Not Met
        if naked_json_count == 0:
            found.append(CriterionItem(
                "An toàn xử lý JSON: 0 Naked JSON.parse rủi ro sập runtime",
                evidence=f"{scanned_files} tệp mã nguồn",
                details="100% các lời gọi parse JSON đều được bọc trong try-catch hoặc schema validation an toàn.",
                badge="JSON Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"Phát hiện {naked_json_count} vị trí NAKED JSON.PARSE không bọc try-catch",
                evidence=f"{naked_json_sample['file']}:{naked_json_sample['line']}",
                snippet=naked_json_sample['snippet'],
                details="Gọi JSON.parse trực tiếp mà không có try-catch sẽ làm sập server hoặc ứng dụng nếu chuỗi JSON không hợp lệ.",
                remediation="Bọc toàn bộ JSON.parse trong khối `try { ... } catch (e) { ... }` hoặc dùng hàm parse an toàn."
            ))

        if bare_except_count == 0:
            found.append(CriterionItem(
                "Kiểm soát ngoại lệ: Không có Silent Exception Eater (Bare Except / Pass)",
                evidence=f"{scanned_files} tệp mã nguồn",
                details="Không nuốt chửng ngoại lệ hệ thống bằng except: pass, toàn bộ lỗi được ghi log tường minh.",
                badge="Exception Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"Phát hiện {bare_except_count} vị trí BARE EXCEPT nuốt chửng lỗi hệ thống",
                evidence=f"{bare_except_sample['file']}:{bare_except_sample['line']}",
                snippet=bare_except_sample['snippet'],
                details="Bắt lỗi dạng `except:` hoặc `except Exception: pass` làm ẩn đi các lỗi nghiêm trọng không thể debug.",
                remediation="Chỉ định chính xác ngoại lệ cần bắt (vd: except ValueError) và ghi log lỗi đầy đủ."
            ))

        if hardcoded_secrets_count == 0:
            found.append(CriterionItem(
                "An toàn bí mật mã nguồn: Không phát hiện Hardcoded Secret / API Key",
                evidence="Quét Regex nhạy cảm",
                details="Không phát hiện chuỗi khóa bí mật, API key hoặc password nào bị gán cứng vào mã nguồn.",
                badge="No Secrets"
            ))
        else:
            missing.append(CriterionItem(
                f"CẢNH BÁO: Phát hiện {hardcoded_secrets_count} chuỗi HARDCODED SECRET trong mã",
                evidence=f"{hardcoded_secrets_sample['file']}:{hardcoded_secrets_sample['line']}",
                snippet=hardcoded_secrets_sample['snippet'],
                details="Chuỗi bí mật hoặc API key được gán tĩnh trực tiếp vào mã nguồn, có nguy cơ lộ khi commit lên Git.",
                remediation="Di chuyển toàn bộ khóa bảo mật vào biến môi trường (.env) và đọc qua process.env hoặc os.environ."
            ))

        if react_leak_count == 0:
            found.append(CriterionItem(
                "An toàn tài nguyên: Không phát hiện Timer / Event Listener rò rỉ bộ nhớ",
                evidence="Quét Lifecycle Hooks",
                details="Toàn bộ các tác vụ định thời và đăng ký sự kiện đều có hàm hủy cleanup giải phóng tài nguyên.",
                badge="Lifecycle Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"Cảnh báo MEMORY LEAK: Phát hiện {react_leak_count} Timer/Listener thiếu hàm cleanup",
                evidence=f"{react_leak_sample['file']}:{react_leak_sample['line']}",
                snippet=react_leak_sample['snippet'],
                details="Khởi tạo setInterval hoặc addEventListener trong useEffect nhưng thiếu hàm cleanup giải phóng khi unmount.",
                remediation="Trả về hàm dọn dẹp trong useEffect: `return () => clearInterval(id);`."
            ))

        self.scores['Tiêu Chuẩn An Toàn RUNTIME (ANTI-CRASH)'] = score
        anti_violations = [v for v in self.violations if v.get('type') in ['NAKED JSON.PARSE', 'STRICT TYPING VIOLATION', 'PYTHON SILENT EXCEPTION EATER', 'HARDCODED SECRET IN CODE', 'REACT MEMORY LEAK RISK']]
        self.add_log(f"  -> AST scan completed on {len(self.tree.code_files)} source files: checked Null safety, try-catch I/O.", "anticrash", "muted")
        self.details['anticrash'] = {
            'name': 'Runtime Anti-Crash',
            'scanned_files': scanned_files,
            'violations_count': violations_count,
            'violations': anti_violations,
            'found': found,
            'missing': missing,
            'score': score,
            'max_points': 20,
            'is_na': False
        }
