"""Project analysis model (Project Model): languages, stack, dependency graph, architecture inferred from imports.

Pure logic, standard library only, no network/model calls (ADR-0018). Every conclusion comes with evidence.
Known limit: static analysis cannot see dynamic imports/reflection; confidence is reported alongside.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path

LANG_BY_EXT = {
    '.py': 'Python', '.js': 'JavaScript', '.jsx': 'JavaScript', '.mjs': 'JavaScript', '.cjs': 'JavaScript',
    '.ts': 'TypeScript', '.tsx': 'TypeScript', '.vue': 'Vue', '.svelte': 'Svelte',
    '.cs': 'C#', '.go': 'Go', '.java': 'Java', '.kt': 'Kotlin', '.rs': 'Rust', '.php': 'PHP',
    '.rb': 'Ruby', '.swift': 'Swift', '.dart': 'Dart', '.scala': 'Scala', '.c': 'C', '.h': 'C/C++',
    '.cpp': 'C++', '.ps1': 'PowerShell', '.sh': 'Shell',
}
DOC_EXT = {'.md', '.mdx', '.rst', '.txt'}
MAX_FILE_BYTES = 1_500_000
MAX_FILES = 6000

# A folder that is only a "container": the real components sit one level deeper.
CONTAINER_DIRS = {'src', 'source', 'app', 'apps', 'lib', 'libs', 'packages', 'services', 'internal', 'pkg', 'cmd',
                  'scripts', 'tools', 'features', 'modules', 'slices', 'domains', 'contexts'}

LAYER_NAMES = {
    'domain': {'domain', 'entities', 'entity', 'core', 'models', 'model'},
    'application': {'application', 'usecases', 'usecase', 'interactors', 'services', 'service'},
    'infrastructure': {'infrastructure', 'infra', 'adapters', 'repositories', 'persistence', 'data', 'db', 'dal'},
    'presentation': {'presentation', 'controllers', 'routes', 'api', 'endpoints', 'handlers', 'web', 'ui', 'pages',
                     'views', 'components'},
}

# root import name (lower case) -> (display name, group)
KNOWN_PACKAGES = {
    'fastapi': ('FastAPI', 'web-backend'), 'flask': ('Flask', 'web-backend'), 'django': ('Django', 'web-backend'),
    'starlette': ('Starlette', 'web-backend'), 'aiohttp': ('aiohttp', 'web-backend'), 'uvicorn': ('Uvicorn', 'web-backend'),
    'sqlalchemy': ('SQLAlchemy', 'database'), 'psycopg2': ('PostgreSQL driver', 'database'),
    'pymongo': ('MongoDB driver', 'database'), 'redis': ('Redis client', 'database'), 'peewee': ('Peewee', 'database'),
    'pydantic': ('Pydantic', 'validation'), 'celery': ('Celery', 'queue'),
    'pytest': ('pytest', 'testing'), 'pil': ('Pillow', 'imaging'), 'unittest': ('unittest', 'testing'), 'jest': ('Jest', 'testing'),
    'vitest': ('Vitest', 'testing'), 'xunit': ('xUnit', 'testing'), 'nunit': ('NUnit', 'testing'),
    'numpy': ('NumPy', 'data-ml'), 'pandas': ('pandas', 'data-ml'), 'torch': ('PyTorch', 'data-ml'),
    'tensorflow': ('TensorFlow', 'data-ml'), 'sklearn': ('scikit-learn', 'data-ml'),
    'langchain': ('LangChain', 'ai'), 'openai': ('OpenAI SDK', 'ai'), 'anthropic': ('Anthropic SDK', 'ai'),
    'google.generativeai': ('Gemini SDK', 'ai'), 'llama_index': ('LlamaIndex', 'ai'),
    'click': ('Click', 'cli'), 'typer': ('Typer', 'cli'), 'argparse': ('argparse', 'cli'),
    'requests': ('requests', 'http-client'), 'httpx': ('httpx', 'http-client'), 'axios': ('axios', 'http-client'),
    'pyinstaller': ('PyInstaller', 'build'), 'tkinter': ('Tkinter', 'desktop'), 'pyqt5': ('PyQt', 'desktop'),
    'pyside6': ('PySide', 'desktop'), 'webview': ('pywebview', 'desktop'),
    'react': ('React', 'web-frontend'), 'react-dom': ('React', 'web-frontend'), 'next': ('Next.js', 'web-fullstack'),
    'vue': ('Vue', 'web-frontend'), 'nuxt': ('Nuxt', 'web-fullstack'), 'svelte': ('Svelte', 'web-frontend'),
    '@angular/core': ('Angular', 'web-frontend'), 'vite': ('Vite', 'build'), 'tailwindcss': ('Tailwind CSS', 'web-frontend'),
    'express': ('Express', 'web-backend'), '@nestjs/core': ('NestJS', 'web-backend'), 'fastify': ('Fastify', 'web-backend'),
    'koa': ('Koa', 'web-backend'), 'prisma': ('Prisma', 'database'), '@prisma/client': ('Prisma', 'database'),
    'mongoose': ('Mongoose', 'database'), 'typeorm': ('TypeORM', 'database'), 'drizzle-orm': ('Drizzle', 'database'),
    'electron': ('Electron', 'desktop'), 'redux': ('Redux', 'web-frontend'), 'zustand': ('Zustand', 'web-frontend'),
    '@tanstack/react-query': ('TanStack Query', 'web-frontend'), 'zod': ('Zod', 'validation'),
    'microsoft.aspnetcore': ('ASP.NET Core', 'web-backend'), 'microsoft.entityframeworkcore': ('EF Core', 'database'),
    'system.windows.forms': ('WinForms', 'desktop'), 'system.windows': ('WPF', 'desktop'),
    'microsoft.web.webview2': ('WebView2', 'desktop'), 'microsoft.extensions': ('.NET Extensions', 'framework'),
    'org.springframework': ('Spring', 'web-backend'), 'javax.persistence': ('JPA', 'database'),
    'github.com/gin-gonic/gin': ('Gin', 'web-backend'), 'github.com/labstack/echo': ('Echo', 'web-backend'),
    'github.com/gofiber/fiber': ('Fiber', 'web-backend'), 'gorm.io/gorm': ('GORM', 'database'),
}

TEST_DIR_NAMES = {'test', 'tests', '__tests__', 'spec', 'specs', 'e2e'}


def _is_test_path(rel: Path) -> bool:
    name = rel.name.lower()
    if any(part.lower() in TEST_DIR_NAMES for part in rel.parts[:-1]):
        return True
    return (name.startswith('test_') or name.endswith(('_test.py', '_test.go', 'tests.cs', 'test.cs', 'test.java'))
            or '.test.' in name or '.spec.' in name)


def _read(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return None


def _loc(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def _component_of(rel: Path) -> str:
    parts = rel.parts[:-1]
    if not parts:
        return '(root)'
    if parts[0].lower() in CONTAINER_DIRS and len(parts) > 1:
        return f'{parts[0]}/{parts[1]}'
    return parts[0]


def _layer_of(component: str) -> str | None:
    leaf = component.split('/')[-1].lower()
    for layer, names in LAYER_NAMES.items():
        if leaf in names:
            return layer
    return None


class ProjectAnalyzer:
    """Scan a ProjectTree already filtered of sample/vendor zones and build the Project Model."""

    def __init__(self, root: Path, tree, progress_callback=None):
        self.root = Path(root)
        self.tree = tree
        self.files: list[dict] = []          # {rel, lang, loc, test, comp, text?}
        self.lang_loc = Counter()
        self.lang_files = Counter()
        self.doc_loc = 0
        self.test_loc = 0
        self.code_loc = 0
        self.edges = Counter()               # (comp_from, comp_to) -> import count
        self.externals = Counter()           # external package name -> occurrences
        self.ext_lang: dict[str, set[str]] = defaultdict(set)   # package name -> languages importing it
        self.entrypoints: list[str] = []
        self.declared: dict[str, set[str]] = defaultdict(set)   # ecosystem -> declared deps
        self._py_pkg: dict[str, str] = {}
        self._ns_comp: dict[str, str] = {}
        self._truncated = False
        self.progress_callback = progress_callback

    # ------------------------------------------------------------------ step 1: inventory
    def _inventory(self):
        stdlib = getattr(sys, 'stdlib_module_names', set())
        self._stdlib = set(stdlib)
        for p in self.tree.all_files[:MAX_FILES * 3]:
            try:
                rel = self.tree.rel_path(p)
            except ValueError:
                continue
            ext = p.suffix.lower()
            if ext in DOC_EXT:
                text = _read(p)
                if text is not None:
                    self.doc_loc += _loc(text)
                continue
            lang = LANG_BY_EXT.get(ext)
            if not lang:
                continue
            if len(self.files) >= MAX_FILES:
                self._truncated = True
                break
            text = _read(p)
            if text is None:
                continue
            loc = _loc(text)
            is_test = _is_test_path(rel)
            self.files.append({'rel': rel, 'lang': lang, 'loc': loc, 'test': is_test,
                               'comp': _component_of(rel), 'ext': ext, 'text': text})
            self.lang_loc[lang] += loc
            self.lang_files[lang] += 1
            self.code_loc += loc
            if is_test:
                self.test_loc += loc

    # ------------------------------------------------------------------ step 2: name index
    def _build_indexes(self):
        for f in self.files:
            comp, rel, ext = f['comp'], f['rel'], f['ext']
            if ext == '.py':
                if rel.parent.parts:
                    self._py_pkg.setdefault(rel.parent.parts[-1], comp)
                self._py_pkg.setdefault(rel.stem, comp)
            elif ext in ('.cs', '.java', '.kt'):
                m = re.search(r'^\s*(?:namespace|package)\s+([\w.]+)', f['text'], re.M)
                if m:
                    self._ns_comp.setdefault(m.group(1), comp)

    # ------------------------------------------------------------------ step 3: imports
    def _add_edge(self, src: str, dst: str):
        if dst and dst != src:
            self.edges[(src, dst)] += 1

    def _comp_for_path(self, path: Path) -> str:
        try:
            rel = path.relative_to(self.root)
        except ValueError:
            return ''
        return _component_of(rel) if rel.parts else '(root)'

    def _python_imports(self, f):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tree = ast.parse(f['text'])
        except (SyntaxError, ValueError, RecursionError):
            return
        comp, rel = f['comp'], f['rel']
        blocks = [tree.body]
        while blocks:
            for stmt in blocks.pop():
                st = type(stmt)
                if st is ast.Import:
                    for a in stmt.names:
                        self._python_target(comp, a.name)
                elif st is ast.ImportFrom:
                    if stmt.level:
                        base = self.root / rel
                        for _ in range(stmt.level):
                            base = base.parent
                        self._add_edge(comp, self._comp_for_path(base / 'x'))
                    elif stmt.module:
                        self._python_target(comp, stmt.module)
                elif st is ast.If:
                    t = stmt.test
                    if (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == '__name__'):
                        self.entrypoints.append(rel.as_posix())
                    blocks.append(stmt.body)
                    if stmt.orelse:
                        blocks.append(stmt.orelse)
                elif st in (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.With, ast.AsyncWith):
                    blocks.append(stmt.body)
                elif st in (ast.For, ast.AsyncFor, ast.While):
                    blocks.append(stmt.body)
                    if stmt.orelse:
                        blocks.append(stmt.orelse)
                elif st is ast.Try or (hasattr(ast, 'TryStar') and st is getattr(ast, 'TryStar')):
                    blocks.append(stmt.body)
                    if stmt.orelse:
                        blocks.append(stmt.orelse)
                    if stmt.finalbody:
                        blocks.append(stmt.finalbody)
                    for h in stmt.handlers:
                        blocks.append(h.body)
                elif hasattr(ast, 'Match') and st is ast.Match:
                    for case in stmt.cases:
                        blocks.append(case.body)

    def _python_target(self, comp: str, dotted: str):
        top = dotted.split('.')[0]
        if top in self._py_pkg:
            self._add_edge(comp, self._py_pkg[top])
        elif top not in self._stdlib:
            key = (dotted if dotted.startswith('google.generativeai') else top).lower()
            self.externals[key] += 1
            self.ext_lang[key].add('Python')

    _JS_IMPORT = re.compile(r'''(?:import\s+(?:[^'";]*?\s+from\s+)?|require\(\s*|import\(\s*)['"]([^'"]+)['"]''')

    def _js_imports(self, f):
        comp, rel = f['comp'], f['rel']
        for spec in self._JS_IMPORT.findall(f['text']):
            if spec.startswith('.'):
                target = (self.root / rel.parent / spec)
                try:
                    norm = Path(*[p for p in target.resolve().relative_to(self.root.resolve()).parts])
                except (ValueError, OSError):
                    continue
                self._add_edge(comp, _component_of(norm / 'x'))
            elif spec.startswith(('@/', '~/')):
                continue
            else:
                parts = spec.split('/')
                name = '/'.join(parts[:2]) if spec.startswith('@') else parts[0]
                if not name.startswith('node:'):
                    self.externals[name.lower()] += 1
                    self.ext_lang[name.lower()].add(f['lang'])

    def _ns_imports(self, f):
        pattern = (r'^\s*using\s+(?:static\s+)?([\w.]+)\s*;' if f['ext'] == '.cs'
                   else r'^\s*import\s+(?:static\s+)?([\w.]+)')
        for ns in re.findall(pattern, f['text'], re.M):
            best, best_len = None, 0
            for known, comp in self._ns_comp.items():
                if (ns == known or ns.startswith(known + '.') or known.startswith(ns + '.')) and len(known) > best_len:
                    best, best_len = comp, len(known)
            if best:
                self._add_edge(f['comp'], best)
            else:
                parts = ns.split('.')
                if parts[0] == 'System' and not ns.startswith('System.Windows'):
                    continue
                key = '.'.join(parts[:3] if parts[0] == 'Microsoft' else parts[:2]).lower()
                self.externals[key] += 1
                self.ext_lang[key].add(f['lang'])

    _GO_IMPORT = re.compile(r'"([\w.\-/]+)"')

    def _go_imports(self, f):
        for block in re.findall(r'import\s*\(([^)]*)\)|import\s+("[^"]+")', f['text']):
            for spec in self._GO_IMPORT.findall(block[0] or block[1]):
                if '.' in spec.split('/')[0]:
                    key = '/'.join(spec.split('/')[:3]).lower()
                    self.externals[key] += 1
                    self.ext_lang[key].add('Go')

    def _imports(self):
        py_files = [f for f in self.files if f['ext'] == '.py']
        py_total = len(py_files)
        py_count = 0
        for f in self.files:
            ext = f['ext']
            if ext == '.py':
                self._python_imports(f)
                py_count += 1
                if self.progress_callback and (py_count % 200 == 0 or py_count == py_total):
                    self.progress_callback(py_count, py_total)
            elif ext in ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.vue', '.svelte'):
                self._js_imports(f)
            elif ext in ('.cs', '.java', '.kt'):
                self._ns_imports(f)
            elif ext == '.go':
                self._go_imports(f)

    # ------------------------------------------------------------------ step 4: declared dependencies
    def _manifests(self):
        for p in self.tree.find_by_name('package.json'):
            try:
                data = json.loads(p.read_text(encoding='utf-8', errors='ignore'))
            except (OSError, ValueError):
                continue
            for key in ('dependencies', 'devDependencies'):
                self.declared['npm'] |= {k.lower() for k in (data.get(key) or {})}
        for p in self.tree.all_files:
            n = p.name.lower()
            if n.startswith('requirements') and n.endswith('.txt'):
                text = _read(p) or ''
                for line in text.splitlines():
                    m = re.match(r'\s*([A-Za-z0-9_.\-]+)', line)
                    if m and not line.lstrip().startswith(('#', '-')):
                        self.declared['pip'].add(m.group(1).lower().replace('-', '_'))
            elif n == 'pyproject.toml':
                text = _read(p) or ''
                for m in re.finditer(r'["\']([A-Za-z0-9_.\-]+)\s*(?:[<>=!~\[;].*?)?["\']', text):
                    pass
            elif n.endswith('.csproj'):
                text = _read(p) or ''
                self.declared['nuget'] |= {m.lower() for m in re.findall(r'PackageReference\s+Include="([^"]+)"', text)}
                for tfm in re.findall(r'<Use(WindowsForms|WPF)>\s*true', text):
                    self.externals['system.windows.forms' if tfm == 'WindowsForms' else 'system.windows'] += 1

    # ------------------------------------------------------------------ step 5: aggregation
    def _stack(self) -> list[dict]:
        found: dict[str, dict] = {}
        names = Counter(self.externals)
        for eco in self.declared.values():
            for d in eco:
                names[d] += 0
        for raw, cnt in names.items():
            for key, (display, cat) in KNOWN_PACKAGES.items():
                if raw == key or raw.startswith(key + '.') or raw.startswith(key + '/'):
                    entry = found.setdefault(display, {'name': display, 'category': cat, 'imports': 0, 'declared': False,
                                                       'languages': set()})
                    entry['imports'] += cnt
                    entry['languages'] |= self.ext_lang.get(raw, set())
                    break
        for eco in self.declared.values():
            for d in eco:
                for key, (display, cat) in KNOWN_PACKAGES.items():
                    if d == key or d.startswith(key + '.'):
                        found.setdefault(display, {'name': display, 'category': cat, 'imports': 0, 'declared': False,
                                                   'languages': set()})
                        found[display]['declared'] = True
        for e in found.values():
            e['languages'] = sorted(e['languages'])
        return sorted(found.values(), key=lambda e: (-e['imports'], e['name']))

    def _cycles(self, comps: set[str]) -> list[list[str]]:
        graph = defaultdict(set)
        for (a, b) in self.edges:
            graph[a].add(b)
        index, low, on, stack, out, counter = {}, {}, set(), [], [], [0]

        def strong(v):
            index[v] = low[v] = counter[0]
            counter[0] += 1
            stack.append(v)
            on.add(v)
            for w in graph[v]:
                if w not in index:
                    strong(w)
                    low[v] = min(low[v], low[w])
                elif w in on:
                    low[v] = min(low[v], index[w])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    out.append(sorted(comp))

        old = sys.getrecursionlimit()
        sys.setrecursionlimit(max(old, 5000))
        try:
            for v in sorted(comps):
                if v not in index:
                    strong(v)
        finally:
            sys.setrecursionlimit(old)
        return out

    def _components(self) -> list[dict]:
        by = defaultdict(lambda: {'loc': 0, 'files': 0, 'langs': Counter(), 'test': 0})
        for f in self.files:
            c = by[f['comp']]
            c['loc'] += f['loc']
            c['files'] += 1
            c['langs'][f['lang']] += f['loc']
            c['test'] += f['loc'] if f['test'] else 0
        fan_in, fan_out = Counter(), Counter()
        for (a, b), n in self.edges.items():
            fan_out[a] += 1
            fan_in[b] += 1
        comps = []
        for name, c in by.items():
            test_only = c['loc'] > 0 and c['test'] / c['loc'] > 0.8
            comps.append({
                'name': name, 'loc': c['loc'], 'files': c['files'],
                'language': c['langs'].most_common(1)[0][0], 'layer': _layer_of(name),
                'role': 'test' if test_only else 'code', 'fan_in': fan_in[name], 'fan_out': fan_out[name],
            })
        return sorted(comps, key=lambda c: -c['loc'])

    def _architecture(self, comps, cycles) -> dict:
        code = [c for c in comps if c['role'] == 'code']
        names = {c['name'].split('/')[-1].lower() for c in code}
        layers = {c['layer'] for c in code if c['layer']}
        evidence, violations = [], []
        # dependency-direction violations between layers
        layer_of = {c['name']: c['layer'] for c in code if c['layer']}
        forbidden = {('domain', 'infrastructure'), ('domain', 'presentation'), ('domain', 'application'),
                     ('application', 'presentation')}
        for (a, b), n in self.edges.items():
            la, lb = layer_of.get(a), layer_of.get(b)
            if la and lb and (la, lb) in forbidden:
                violations.append(f'{a} ({la}) depends on {b} ({lb}) — {n} imports')
        modular = [c for c in code if c['name'].split('/')[0].lower() in {'features', 'modules', 'slices', 'domains', 'contexts'}]
        total_loc = sum(c['loc'] for c in code) or 1
        if {'domain', 'infrastructure'} <= layers and ('application' in layers or 'presentation' in layers):
            style, label = 'clean-architecture', 'Clean / Hexagonal Layered Architecture'
            evidence.append('Has domain, infrastructure and application/presentation layers.')
            conf = 'high' if not violations else 'medium'
        elif len(modular) >= 3:
            cross = sum(n for (a, b), n in self.edges.items()
                        if a in {m['name'] for m in modular} and b in {m['name'] for m in modular})
            style = 'modular-monolith' if cross else 'vertical-slice'
            label = 'Monolith theo module' if cross else 'Vertical Slice (Feature-driven)'
            evidence.append(f'{len(modular)} modules/features; {cross} cross-imports between them.')
            conf = 'medium'
        elif len(layers & {'presentation', 'application', 'domain', 'infrastructure'}) >= 2:
            style, label = 'simple-layered', 'Simple Layered (presentation → service → data)'
            evidence.append('Found layer folders:' + ', '.join(sorted(layers)))
            conf = 'medium'
        elif len(code) <= 2:
            style, label = 'flat', 'Flat structure (minimal components)'
            evidence.append(f'Only {len(code)} source components.')
            conf = 'high'
        else:
            style, label = 'component-based', 'Component-based without explicit layering'
            evidence.append(f'{len(code)} components, matching no layer/module pattern yet.')
            conf = 'low'
        if cycles:
            evidence.append(f'{len(cycles)} circular dependency groups between components.')
        if names and total_loc < 800:
            evidence.append(f'Small codebase ({total_loc} lines of code).')
        return {'style': style, 'label': label, 'confidence': conf, 'evidence': evidence, 'violations': violations}

    def _kind(self, stack, comps) -> dict:
        total = sum(self.lang_loc.values()) or 1
        significant = {n for n, l in self.lang_loc.items() if l / total >= 0.2}
        # A stack group decides the project type only when it comes from a significant language (or is declared explicitly)
        cats = {s['category'] for s in stack if s['declared'] and not s['languages']
                or set(s['languages']) & significant}
        all_cats = {s['category'] for s in stack}
        evidence, secondary = [], []
        code = self.code_loc
        if code == 0 or self.doc_loc >= code:
            primary = ('docs-knowledge', 'Documentation / Knowledge base' + (' with tools' if code else ''))
            evidence.append(f'{self.doc_loc} documentation lines vs {code} lines of code.')
        elif 'web-fullstack' in cats or ({'web-backend', 'web-frontend'} <= cats):
            primary = ('web-fullstack', 'Full-stack web application')
        elif 'web-backend' in cats:
            primary = ('web-backend', 'Backend / API service')
        elif 'web-frontend' in cats:
            primary = ('web-frontend', 'Web frontend application')
        elif 'desktop' in cats:
            primary = ('desktop-app', 'Desktop application')
        elif 'data-ml' in cats or 'ai' in cats:
            primary = ('data-ml', 'Data / AI project')
        elif self.entrypoints or 'cli' in cats:
            primary = ('cli-tool', 'Command-line tool / script')
            evidence.append(f'{len(self.entrypoints)} files with a `__main__` entry point.')
        else:
            primary = ('library', 'Library / unspecified entrypoint')
        for cat, label in (('desktop', 'has a desktop component'), ('cli', 'has a CLI'), ('ai', 'integrates AI/LLM'),
                           ('database', 'has a data layer'), ('web-backend', 'has a web backend component'),
                           ('web-frontend', 'has a web frontend component')):
            if cat in all_cats and primary[0] not in (cat,):
                secondary.append(label)
        if self.entrypoints and primary[0] != 'cli-tool':
            secondary.append('has directly runnable scripts')
        return {'id': primary[0], 'label': primary[1], 'secondary': secondary, 'evidence': evidence}

    def analyze(self) -> dict:
        self._inventory()
        self._build_indexes()
        self._imports()
        self._manifests()
        stack = self._stack()
        comps = self._components()
        cycles = self._cycles({c['name'] for c in comps})
        arch = self._architecture(comps, cycles)
        kind = self._kind(stack, comps)
        total = sum(self.lang_loc.values()) or 1
        languages = [{'name': n, 'loc': l, 'files': self.lang_files[n], 'share': round(l / total * 100, 1)}
                     for n, l in self.lang_loc.most_common()]
        big = sorted(self.files, key=lambda f: -f['loc'])[:8]
        non_test_code = max(self.code_loc - self.test_loc, 1)
        return {
            'languages': languages,
            'primary_language': languages[0]['name'] if languages else None,
            'code_loc': self.code_loc, 'test_loc': self.test_loc, 'doc_loc': self.doc_loc,
            'test_ratio': round(self.test_loc / non_test_code, 2),
            'files_analyzed': len(self.files), 'truncated': self._truncated,
            'kind': kind, 'stack': stack, 'architecture': arch,
            'components': comps[:40],
            'edges': [{'from': a, 'to': b, 'count': n} for (a, b), n in self.edges.most_common(60)],
            'cycles': cycles,
            'entrypoints': sorted(set(self.entrypoints))[:12],
            'externals': [{'name': n, 'count': c} for n, c in self.externals.most_common(15)],
            'hotspots': {
                'large_files': [{'file': f['rel'].as_posix(), 'loc': f['loc']} for f in big if f['loc'] >= 350],
                'central_components': [c['name'] for c in sorted(comps, key=lambda c: -c['fan_in'])[:3] if c['fan_in'] >= 2],
            },
        }


def analyze_project(root: Path, tree, progress_callback=None) -> dict:
    return ProjectAnalyzer(root, tree, progress_callback=progress_callback).analyze()
