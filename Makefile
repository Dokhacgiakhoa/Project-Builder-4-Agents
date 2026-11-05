.PHONY: help review build-exe test lint check-links

help: ## Hiển thị danh mục lệnh (dành cho người phát triển Project-Builder-4-Agents)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

review: ## Project Health Check: make review [TARGET=đường/dẫn] -> project-review.md
	python scripts/project_auditor.py $(or $(TARGET),.)

build-exe: ## Đóng gói engine + Project-Health-Check.exe (cần PyInstaller, .NET 10 SDK)
	python scripts/build_exe.py

test: ## Chạy toàn bộ kiểm thử (pytest + vitest cho frontend mẫu)
	python -m pytest tests -q
	cd profiles/frontend/starter && npm test

lint: ## Kiểm tra cú pháp Python và ESLint cho frontend mẫu
	python -m compileall -q scripts
	cd profiles/frontend/starter && npm run lint

check-links: ## Kiểm tra link tài liệu (INDEX.md không được dẫn Agent vào ngõ cụt)
	python scripts/check_links.py
