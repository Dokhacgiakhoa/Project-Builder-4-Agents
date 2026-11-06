"""Chỉ mục cây thư mục dự án (pruned indexing)."""

import os
import sys
import re
import json
import datetime
from pathlib import Path

from .constants import IGNORE_DIRS, CODE_EXTENSIONS, SKIP_REASONS, ALLOWED_DOT_DIRS  # noqa: F401


class ProjectTree:

    """Hệ thống lập chỉ mục và duyệt cây thư mục siêu tốc (Bỏ qua hoàn toàn node_modules, .git,...)."""

    def __init__(self, root: Path):

        self.root = root.resolve()

        self.all_files = []

        self.all_dirs = set()

        self.code_files = []

        self.files_by_name = {}

        self.files_by_ext = {}

        # (đường dẫn tương đối, lý do) của các thư mục bị bỏ qua, để báo cáo cho Agent

        self.skipped = []

        self._scan()

    def _scan(self):

        for dirpath, dirnames, filenames in os.walk(self.root):

            # Cắt tỉa thư mục ngay tại chỗ để os.walk không đi sâu vào các thư mục rác

            for d in dirnames:

                if d in IGNORE_DIRS:

                    rel = (Path(dirpath) / d).relative_to(self.root).as_posix()

                    self.skipped.append((rel, SKIP_REASONS.get(d, '')))

            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and (not d.startswith('.') or d in ALLOWED_DOT_DIRS)]

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
