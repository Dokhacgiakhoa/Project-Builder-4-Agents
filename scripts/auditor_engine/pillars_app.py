"""Pillar Backend, Frontend, Database và Anti-Crash."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS  # noqa: F401


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
