.PHONY: help setup up down restart logs test lint clean

help: ## Hiển thị danh mục các lệnh hỗ trợ
	@echo "Universal Project Starter Kit - Developer Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Khởi tạo môi trường (Copy .env, tạo thư mục)
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example"; fi
	@echo "Setup completed successfully."

dev-frontend: ## Khởi chạy Frontend React (Vite dev server)
	cd frontend && npm run dev

build-frontend: ## Biên dịch production build cho Frontend
	cd frontend && npm run build

up: ## Khởi chạy toàn bộ hạ tầng local qua Docker Compose
	docker compose up -d

down: ## Dừng toàn bộ hạ tầng Docker Compose
	docker compose down

restart: down up ## Khởi động lại toàn bộ containers

logs: ## Xem logs thời gian thực của Docker containers
	docker compose logs -f

test: ## Chạy bộ kiểm thử tự động
	@echo "Running test suite..."
	# Tùy biến lệnh test: pytest / npm test / dotnet test

lint: ## Chạy kiểm tra định dạng và linter
	@echo "Running linter..."
	# Tùy biến lệnh lint: ruff check / npm run lint / dotnet format

clean: ## Dọn dẹp các tệp tạm, cache và build artifacts
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules/.cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "bin" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "obj" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean completed."
