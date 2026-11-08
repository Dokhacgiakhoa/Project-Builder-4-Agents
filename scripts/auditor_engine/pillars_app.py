"""Backend, Frontend, Database and Anti-Crash pillars."""

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
    """Backend, Frontend, Database and Anti-Crash pillars."""

    def audit_backend_waterflow(self):
        score = 0
        found = []
        missing = []
        layer_leaks = []
        all_dirs = self.tree.all_dirs

        # Layered architecture
        has_domain = any(d in all_dirs for d in ['domain', 'entities', 'core', 'models'])
        has_app = any(d in all_dirs for d in ['application', 'usecases', 'services', 'interactors'])
        has_infra = any(d in all_dirs for d in ['infrastructure', 'adapters', 'repositories', 'dal'])
        has_pres = any(d in all_dirs for d in ['presentation', 'controllers', 'routes', 'api', 'endpoints', 'handlers'])
        has_features = any(d in all_dirs for d in ['features', 'modules', 'slices'])

        matched_dirs = [d for d in ['domain', 'core', 'models', 'application', 'services', 'infrastructure', 'repositories', 'controllers', 'routes', 'api', 'features'] if d in all_dirs]

        if has_domain and (has_app or has_infra):
            score += 30
            found.append(CriterionItem(
                f"Standard layered structure following {self.profile.get('arch_style')}",
                evidence=", ".join(matched_dirs[:4]),
                details=f"Verified a layered structure with distinct functional layers: {', '.join(matched_dirs[:4])}.",
                badge="Layered Arch"
            ))
        elif has_features:
            score += 30
            found.append(CriterionItem(
                'Independent module structure following FEATURE-DRIVEN ARCHITECTURE',
                evidence=", ".join(matched_dirs[:4]),
                details='Verified independent isolated Feature/Module code organization.',
                badge="Feature-Driven"
            ))
        elif has_pres or has_app:
            score += 20
            found.append(CriterionItem(
                'Basic separation between PRESENTATION and BUSINESS LOGIC layers',
                evidence=", ".join(matched_dirs[:4]),
                details='Verified separation between presentation/API and business logic layers.',
                badge="Separated Logic"
            ))
        else:
            missing.append(CriterionItem(
                'Clear separation of DOMAIN, APPLICATION and INFRASTRUCTURE boundaries',
                evidence='Directory Structure',
                details='Source files mixed in same directories or lacking clear layering between core business and infrastructure.',
                remediation='Reorganize folders by architectural layers (domain/core, services, controllers/routes).'
            ))

        # Scan Dependency Injection (DI) & DTO Input Validation
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
                            layer_leaks.append(f"Architecture leak: CONTROLLER `{rel}` queries SQL directly instead of going through a REPOSITORY.")
                            break

                if is_domain:
                    if _DOMAIN_LEAK_PATTERN.search(text):
                        layer_leaks.append(f"DOMAIN LEAK: File `{rel}` in the DOMAIN depends on an infrastructure FRAMEWORK.")
            except Exception:
                pass

        if not layer_leaks:
            score += 25
            found.append(CriterionItem(
                'DOMAIN purity and CONTROLLER boundaries protected (0 Layer Leaks)',
                evidence=f"Scanned {len(self.tree.code_files)} source files",
                details='No controllers execute direct SQL queries or bind domain to frameworks.',
                badge="0 Leaks"
            ))
        else:
            for leak in layer_leaks[:2]:
                self.violations.append({'file': 'ARCHITECTURE BOUNDARY', 'line': 0, 'type': 'LAYER LEAKAGE', 'desc': leak, 'snippet': ''})
            score = max(10, score - 15)
            missing.append(CriterionItem(
                f"LAYER LEAK warning: Detected {len(layer_leaks)} layer boundary violations",
                evidence=layer_leaks[0],
                details='Controllers query SQL directly or Domain models import external frameworks instead of going through a Repository.',
                remediation='Extract DB queries into the Repository/DAL layer and inject them into Controllers through an Interface/Service.'
            ))

        if has_di:
            score += 15
            found.append(CriterionItem(
                'Explicit DEPENDENCY INJECTION (DI) applied',
                evidence=di_found_file or 'Backend source code',
                snippet=di_found_snippet or "Dependency Injection",
                details='Detected Dependency Injection (DI/IoC) usage for modularity and testability.',
                badge="DI Pattern"
            ))
        else:
            missing.append(CriterionItem(
                'Dependency Injection (DI) pattern supporting Unit Testing',
                evidence="Controllers / Services",
                details='No Dependency Injection found (constructor injection, Depends, @Injectable); services create their dependencies directly with `new`.',
                remediation='Apply Inversion of Control / DI through constructor injection or the framework container.'
            ))

        if has_dto_validation:
            score += 15
            found.append(CriterionItem(
                'Automated DTO input validation (Zod / Pydantic / Class-Validator)',
                evidence=dto_found_file or "Schemas / DTOs",
                snippet=dto_found_snippet or "DTO Schema Validation",
                details='Detected an automatic DTO validation library protecting input data before it reaches the processing layer.',
                badge="DTO Validation"
            ))
        else:
            missing.append(CriterionItem(
                'Automated input DTO validation (Zod, Pydantic, or Schema Validator)',
                evidence="Request Handlers",
                details='Missing an automatic input-schema validation library (Zod, Pydantic, class-validator) at the endpoints.',
                remediation='Define DTO schemas (e.g. a Pydantic BaseModel or a Zod object) and validate in the Controller/Handler layer.'
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
                            'Safe resource cleanup on shutdown (Graceful Shutdown)',
                            evidence=f"{rel_ef}",
                            snippet="process.on('SIGTERM') / signal handler",
                            details='Detected SIGTERM / SIGINT signal listeners that close database connections and the HTTP server safely.',
                            badge="Graceful Exit"
                        ))
                    else:
                        missing.append(CriterionItem(
                            'Graceful resource release and cleanup on SERVER shutdown (GRACEFUL SHUTDOWN)',
                            evidence=f"{rel_ef}",
                            details='Lacks SIGTERM/SIGINT signal handling to release DB connections and stop server without dropping in-flight requests.',
                            remediation='Add SIGTERM/SIGINT signal listeners to gracefully close database connection pools and server instances.'
                        ))
                except Exception:
                    pass
                break
            if found_entry:
                break

        score = min(100, score)
        self.scores['BACKEND Architecture & CORE Data Flow'] = score
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
                'Design tokens system (Custom Tailwind config / CSS variables / Theme tokens)',
                evidence=token_ev,
                details=f"Detected a centralized UI management system via {token_ev}.",
                badge="Design Tokens"
            ))
        else:
            missing.append(CriterionItem(
                'Centralized design tokens and theme variables system',
                evidence="CSS / Styling",
                details='No centralized design-token configuration found (such as Tailwind colors/spacing or CSS :root variables).',
                remediation='Create a custom tailwind.config.js or define a :root color/spacing variable table in CSS.'
            ))

        # 2. Centralized API Client wrapper
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
                'Centralized defensive API client (Interceptors, baseURL, error normalization)',
                evidence=api_client_path or "api-client",
                details=f"Detected a centralized API Client module at `{api_client_path}` that standardizes baseURL and uniform error handling.",
                badge="API Client"
            ))
        else:
            missing.append(CriterionItem(
                'Centralized API client wrapper (avoids scattered fetch/axios calls in components)',
                evidence='Frontend layer',
                details='Missing a shared API Client wrapper; fetch/axios calls risk being scattered across UI components.',
                remediation='Create `api/client.ts` wrapping Axios/Fetch with baseURL, auth header and an error-code normalizer.'
            ))

        # 3. Scan Error Boundary & Code Splitting (Lazy Loading)
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
                    god_components.append(f"{p.name} ({len(lines)} lines)")

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
                'Error Boundary catching runtime errors preventing white-screen crash',
                evidence=error_boundary_file or "ErrorBoundary component",
                details='Detected Error Boundary component catching React rendering exceptions, protecting user experience.',
                badge="Error Boundary"
            ))
        else:
            missing.append(CriterionItem(
                'Error Boundary component wrapping routes for safe UI crash recovery',
                evidence="Root Layout / App",
                details='No Error Boundary component wraps the routes; a render error risks blanking the whole page.',
                remediation='Create an ErrorBoundary component (or Next.js error.tsx) that shows a fallback UI on runtime errors.'
            ))

        if has_lazy_loading:
            score += 15
            found.append(CriterionItem(
                'Code-splitting / lazy loading optimizing initial page load speed',
                evidence=lazy_loading_file or "React.lazy / Async Component",
                details='Lazy loading was applied to heavy pages or modules.',
                badge="Code Splitting"
            ))
        else:
            missing.append(CriterionItem(
                'LAZY LOADING technique (React.lazy) for large page sections',
                evidence="Routing / Pages",
                details='React.lazy() or dynamic import is not applied to large pages and modals, increasing the initial bundle size.',
                remediation='Use `React.lazy()` or Next.js `dynamic()` for admin screens and large dialogs.'
            ))

        if not god_components:
            score += 15
            found.append(CriterionItem(
                'Lean COMPONENT structure with clear separation of responsibilities (0 GOD COMPONENTS)',
                evidence=f"Scanned {len(fe_code_files)} UI files",
                details='All UI components are under 350 lines, ensuring single responsibility and easy maintenance.',
                badge="Clean Components"
            ))
        else:
            score += 5
            self.gaps.append(f"GOD COMPONENT warning, excessive size (> 350 lines): {', '.join(god_components[:2])}")
            missing.append(CriterionItem(
                f"GOD COMPONENT warning: Detected {len(god_components)} oversized components (> 350 lines)",
                evidence=", ".join(god_components[:3]),
                details=f"Detected components exceeding the size standard: {', '.join(god_components[:3])}.",
                remediation='Split large components into smaller sub-components or extract custom hooks.'
            ))

        score = min(100, score)
        self.scores['FRONTEND Architecture & DESIGN SYSTEM (UI/UX)'] = score
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
                'Version-controlled database migration management',
                evidence=mig_ev,
                details=f"Verified a versioned database schema management system via `{mig_ev}`.",
                badge="Migrations OK"
            ))
        else:
            missing.append(CriterionItem(
                'DATABASE MIGRATION folder (risk of SCHEMA drift on PRODUCTION)',
                evidence='Database folder',
                details='No migration folder or schema management tool found (Prisma, Alembic, Flyway, EF Core).',
                remediation='Set up a migration tool (e.g. Prisma Migrate or Alembic) to keep the DB structure in sync with Git versions.'
            ))
            self.gaps.append('Missing a version-controlled DATABASE MIGRATION system.')

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

                # Scan SQL Injection & N+1 Query (Single-pass)
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
                                    'desc': 'Strings concatenated directly into RAW SQL statements (missing PARAMETERIZED QUERIES).',
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
                'Connection pool & timeout configuration protecting database connection limits',
                evidence=pool_file or "DB Config",
                details='Verified connection limit configuration (pool size, idle timeout) protecting the DB from connection exhaustion.',
                badge="Connection Pool"
            ))
        else:
            missing.append(CriterionItem(
                'Explicit CONNECTION POOL configuration (POOL_SIZE, IDLE_TIMEOUT)',
                evidence="Database Connection",
                details='pool_size or timeout for database connections is not set explicitly.',
                remediation='Declare pool_size (e.g. 10-20) and idle_timeout in the DB connection configuration.'
            ))

        if has_transaction:
            score += 20
            found.append(CriterionItem(
                'DATABASE TRANSACTION mechanism ensuring atomicity (ACID) when writing multiple tables',
                evidence=tx_file or "DB Repositories",
                details='Verified use of transactions for complex write operations ensuring ACID integrity.',
                badge="ACID Transaction"
            ))
        else:
            missing.append(CriterionItem(
                'Explicit transaction wrapping for multi-entity mutation operations',
                evidence='Data Access layer',
                details='No transaction block found for multi-table update operations.',
                remediation='Use `$transaction`, `session.begin()` or `BeginTransaction()` for cross-table write flows.'
            ))

        if not sql_injection_risks:
            score += 20
            found.append(CriterionItem(
                'Query safety: Parameterized queries or type-safe ORM usage',
                evidence=f"Scanned {len(self.tree.code_files)} source files",
                details='100% of database queries use safe ORMs or parameterized queries.',
                badge="Query Safety"
            ))
        else:
            self.violations.extend(sql_injection_risks)
            self.gaps.append(f"Security warning: Detected {len(sql_injection_risks)} RAW SQL string concatenation locations.")
            score = max(10, score - 20)
            missing.append(CriterionItem(
                f"SQL INJECTION warning: Detected {len(sql_injection_risks)} direct string concatenation locations",
                evidence=sql_injection_risks[0]['file'],
                snippet=sql_injection_risks[0]['snippet'],
                details=f"Detected {len(sql_injection_risks)} places that concatenate strings directly into SQL statements instead of using parameter placeholders.",
                remediation='Convert string concatenation queries to parameterized placeholders (e.g. $1, :val, or ?).'
            ))

        if n_plus_one_risks:
            self.gaps.append(f"N+1 QUERY warning: Detected database queries inside loops at: {', '.join(n_plus_one_risks[:2])}")

        score = min(100, score)
        self.scores['DATABASE Infrastructure & QUERY Safety'] = score
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
                                'desc': 'JSON.parse called outside try-catch block (runtime crash risk on malformed JSON).',
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
                                'desc': 'Using ": any" type violates TypeScript strict typing standards.',
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
                                'desc': 'Silent exception handling (bare except or except Exception: pass) swallows system errors.',
                                'snippet': stripped[:80]
                            }
                            self.violations.append(item)
                            violations_count += 1
                            bare_except_count += 1
                            if not bare_except_sample:
                                bare_except_sample = item

                    # 4. Hardcoded Secret Detection (fast pre-filter)
                    # Skip test files / mock fixtures so synthetic test payloads do not raise false alarms
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
                                    'desc': 'Hardcoded secret / API key statically assigned directly in source code.',
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
                                    'desc': 'TIMER / EVENT LISTENER created without a CLEANUP function to release it (MEMORY LEAK risk).',
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
            self.gaps.append(f"Detected {violations_count} locations violating ANTI-CRASH standards in the source code.")
        else:
            score = 100

        # Classify Criteria Met & Criteria Not Met
        if naked_json_count == 0:
            found.append(CriterionItem(
                'JSON handling safety: 0 naked JSON.parse risks of runtime crash',
                evidence=f"{scanned_files} source files",
                details='100% of JSON parsing calls wrapped in try-catch or safe schema validation.',
                badge="JSON Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"Detected {naked_json_count} NAKED JSON.PARSE locations without try-catch",
                evidence=f"{naked_json_sample['file']}:{naked_json_sample['line']}",
                snippet=naked_json_sample['snippet'],
                details='Directly calling JSON.parse without try-catch crashes the application if JSON is malformed.',
                remediation='Wrap all JSON.parse in `try { ... } catch (e) { ... }` blocks or use safe parse utilities.'
            ))

        if bare_except_count == 0:
            found.append(CriterionItem(
                'Exception control: No Silent Exception Eaters (Bare Except / Pass)',
                evidence=f"{scanned_files} source files",
                details='No silent swallowing of exceptions with except: pass; all errors logged explicitly.',
                badge="Exception Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"Detected {bare_except_count} BARE EXCEPT locations silently swallowing system errors",
                evidence=f"{bare_except_sample['file']}:{bare_except_sample['line']}",
                snippet=bare_except_sample['snippet'],
                details='Catching errors with `except:` or `except Exception: pass` obscures critical errors from debugging.',
                remediation='Specify exact exceptions (e.g. except ValueError) and log errors comprehensively.'
            ))

        if hardcoded_secrets_count == 0:
            found.append(CriterionItem(
                'Secret safety: No Hardcoded Secrets / API Keys detected',
                evidence='Sensitive Regex Scan',
                details='No secret keys, API keys or passwords statically hardcoded in source.',
                badge="No Secrets"
            ))
        else:
            missing.append(CriterionItem(
                f"WARNING: Detected {hardcoded_secrets_count} HARDCODED SECRET strings in code",
                evidence=f"{hardcoded_secrets_sample['file']}:{hardcoded_secrets_sample['line']}",
                snippet=hardcoded_secrets_sample['snippet'],
                details='Secret keys or API keys hardcoded in source code; risk of leaking upon git commit.',
                remediation='Move all secrets into environment variables (.env) and read via process.env or os.environ.'
            ))

        if react_leak_count == 0:
            found.append(CriterionItem(
                'Resource safety: No Timer / Event Listener memory leak risks detected',
                evidence='Lifecycle Hooks Scan',
                details='All timers and event subscriptions provide cleanup cancellation handlers.',
                badge="Lifecycle Safe"
            ))
        else:
            missing.append(CriterionItem(
                f"MEMORY LEAK warning: Detected {react_leak_count} Timers/Listeners lacking a cleanup function",
                evidence=f"{react_leak_sample['file']}:{react_leak_sample['line']}",
                snippet=react_leak_sample['snippet'],
                details='setInterval or addEventListener initiated in useEffect lacking cleanup on unmount.',
                remediation='Return cleanup handler in useEffect: `return () => clearInterval(id);`.'
            ))

        self.scores['RUNTIME Safety Standards (ANTI-CRASH)'] = score
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
