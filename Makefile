.PHONY: help review build-exe test lint check-links

help: ## Show command directory (for Project-Builder-4-Agents developers)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

review: ## Project Builder Analytics: make review [TARGET=path/to/target] -> project-review.md
	python scripts/project_auditor.py $(or $(TARGET),.)

build-exe: ## Package engine + standalone shell executable (requires PyInstaller and .NET 10 SDK)
	python scripts/build_exe.py

test: ## Run complete test suite (pytest + vitest for frontend starter)
	python -m pytest tests -q
	cd profiles/frontend/starter && npm test

lint: ## Verify Python syntax and run ESLint on frontend starter
	python -m compileall -q scripts
	cd profiles/frontend/starter && npm run lint

check-links: ## Verify document link integrity and INDEX.md routing constraints
	python scripts/check_links.py
