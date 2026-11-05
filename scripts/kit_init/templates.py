"""Nội dung các tệp được sinh mới (không copy nguyên bản) cho dự án khởi tạo."""

README = """# {name}

> Dự án được khởi tạo từ **Universal AI-Native Project Starter Kit**. Con người nắm thẩm quyền,
> AI Agent (Claude Code, Antigravity, Cursor, Codex) thực thi theo Hiến pháp `AGENTS.md`.

## Bắt đầu

1. Điền tầm nhìn sản phẩm: `specs/product-vision.md`, ranh giới nghiệp vụ: `specs/domains.md`.
2. Chốt công nghệ: `adrs/0002-tech-stack.md` (mọi thay đổi kiến trúc đi qua một ADR mới).
3. Viết đặc tả tính năng từ `specs/features/template-spec.md` và API Contract trong `specs/contracts/`
   **trước khi** viết code.
4. Giao việc cho AI bằng `tasks/templates/task-spec.md`.

```bash
make setup   # tạo .env từ .env.example
make test    # chạy kiểm thử
make lint    # chạy linter
```

## Cấu trúc

| Thư mục | Vai trò |
| :--- | :--- |
| `AGENTS.md` | Hiến pháp hành vi cho AI Agent |
| `adrs/` | Architecture Decision Records |
| `specs/` | Tầm nhìn, domain, API contract, feature spec |
| `planning/` | Roadmap, backlog, sprint |
| `tasks/` | Mẫu nhiệm vụ giao cho AI |
| `docs/` | Tài liệu theo khung Diátaxis |
| `src/` | Mã nguồn (Clean Architecture: Domain → Application → Infrastructure → Presentation) |
| `tests/` | Kiểm thử tự động |

## Kiểm tra kiến trúc

Dùng `Project-Review.exe` (hoặc `python <starter-kit>/scripts/project_auditor.py .`) từ Starter Kit
để chấm điểm dự án này bất cứ lúc nào.
"""

MAKEFILE = """.PHONY: help setup up down test lint clean

help: ## Hiển thị danh mục lệnh
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {{FS = ":.*?## "}}; {{printf "  %-12s %s\\n", $$1, $$2}}'

setup: ## Tạo .env từ .env.example
\t@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env"; fi

up: ## Khởi chạy hạ tầng local (cần docker-compose.yml, tạo bằng --docker)
\tdocker compose up -d

down: ## Dừng hạ tầng local
\tdocker compose down

test: ## Chạy kiểm thử (TODO: thay bằng lệnh của stack: pytest / npm test / dotnet test)
\t@echo "TODO: cấu hình lệnh test"

lint: ## Chạy linter (TODO: thay bằng lệnh của stack)
\t@echo "TODO: cấu hình lệnh lint"

clean: ## Dọn cache tạm
\tfind . -type d -name "__pycache__" -exec rm -rf {{}} + 2>/dev/null || true
"""

CI = """name: Continuous Integration (CI)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  quality-gate:
    name: Code Quality & Test Gate
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Verify Context Files Integrity
        run: |
          test -f AGENTS.md || (echo "Missing AGENTS.md" && exit 1)
          test -d specs || (echo "Missing specs directory" && exit 1)
          test -d adrs || (echo "Missing adrs directory" && exit 1)

      # TODO: thay bằng bước lint/test thật của tech stack đã chọn trong adrs/0002-tech-stack.md
      # (DoD yêu cầu CI xanh; đừng để các bước giả lập `echo` tồn tại lâu).
"""
