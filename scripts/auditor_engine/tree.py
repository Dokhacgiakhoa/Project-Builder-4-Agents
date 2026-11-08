"""Project folder tree index (pruned indexing)."""

import fnmatch
import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS, SKIP_REASONS, SKIP_REL_PATTERNS, ALLOWED_DOT_DIRS  # noqa: F401


class ProjectTree:

    """Very fast folder tree indexing and traversal system (completely skips node_modules, .git, ...)."""

    def __init__(self, root: Path):

        self.root = root.resolve()

        self.all_files = []

        self.all_dirs = set()

        self.code_files = []

        self.files_by_name = {}

        self.files_by_ext = {}

        # (relative path, reason) of the skipped folders, to report to the Agent

        self.skipped = []

        self.rel_posix_map = {}
        self.file_ext_map = {}
        self.file_parts_lower = {}
        self._text_cache = {}
        self._cache_bytes = 0
        self._max_cache_bytes = 100 * 1024 * 1024
        self._read_calls = 0
        self._cache_hits = 0

        self._scan()

    def _scan(self):
        root_str = str(self.root)
        root_len = len(root_str)

        for dirpath, dirnames, filenames in os.walk(self.root):
            rel_dir = dirpath[root_len:].lstrip('\\/').replace('\\', '/')

            # Prune folders in place so os.walk does not descend into junk folders
            for d in dirnames:
                if d in IGNORE_DIRS:
                    rel = f'{rel_dir}/{d}' if rel_dir else d
                    self.skipped.append((rel, SKIP_REASONS.get(d, '')))

            rel_skip = set()
            for d in dirnames:
                if d in IGNORE_DIRS:
                    continue
                rel = f'{rel_dir}/{d}' if rel_dir else d
                for pat, reason in SKIP_REL_PATTERNS.items():
                    if fnmatch.fnmatchcase(rel, pat):
                        self.skipped.append((rel, reason))
                        rel_skip.add(d)

            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and d not in rel_skip and (not d.startswith('.') or d in ALLOWED_DOT_DIRS)]

            for d in dirnames:
                self.all_dirs.add(d.lower())

            dir_parts = tuple(part.lower() for part in rel_dir.split('/')) if rel_dir else ()
            for f in filenames:
                p = Path(dirpath) / f
                rel_str = f'{rel_dir}/{f}' if rel_dir else f
                self.rel_posix_map[p] = rel_str
                self.file_parts_lower[p] = dir_parts
                self.all_files.append(p)
                lower_f = f.lower()
                self.files_by_name.setdefault(lower_f, []).append(p)
                ext = p.suffix.lower()
                self.file_ext_map[p] = ext
                if ext:
                    self.files_by_ext.setdefault(ext, []).append(p)
                if ext in CODE_EXTENSIONS:
                    self.code_files.append(p)

    def rel_posix(self, p: Path) -> str:
        cached = self.rel_posix_map.get(p)
        if cached is not None:
            return cached
        return p.relative_to(self.root).as_posix()

    def rel_path(self, p: Path) -> Path:
        cached = self.rel_posix_map.get(p)
        if cached is not None:
            return Path(cached)
        return p.relative_to(self.root)

    def ext(self, p: Path) -> str:
        cached = self.file_ext_map.get(p)
        if cached is not None:
            return cached
        return p.suffix.lower()

    def parts_lower(self, p: Path) -> tuple[str, ...]:
        cached = self.file_parts_lower.get(p)
        if cached is not None:
            return cached
        return tuple(part.lower() for part in p.parts)

    def read_text(self, p: Path, limit: int = 1024 * 1024) -> str:
        self._read_calls += 1
        cached = self._text_cache.get(p)
        if cached is not None:
            self._cache_hits += 1
            return cached
        try:
            if p.stat().st_size > limit:
                return ''
            content = p.read_text(encoding='utf-8', errors='ignore')
            content_len = len(content)
            if self._cache_bytes + content_len < self._max_cache_bytes:
                self._text_cache[p] = content
                self._cache_bytes += content_len
            return content
        except OSError:
            return ''

    def clear_cache(self):
        self._text_cache.clear()
        self._cache_bytes = 0

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
