# CONTRIBUTING GUIDELINES

Thank you for your interest in contributing to the project! To maintain high code quality and seamless collaboration between human engineers and autonomous AI coding agents, please adhere to the guidelines below.

---

## 🚦 1. Core Principles
1. **Spec-Driven**: Any non-trivial architectural change, feature addition, or refactor must be accompanied by an Issue or Feature Spec under `specs/` before implementation.
2. **Context Integrity**: Thoroughly review `AGENTS.md` and active architectural decision records in `adrs/` before making changes.
3. **The Anti-Crash Standard**: Strictly enforce defensive programming (optional chaining, explicit error handling, safe fallback values).

---

## 🌿 2. Git Branching Strategy
- `main`: Production-ready branch. Direct pushes to `main` are restricted.
- Feature branches: `feature/{issue-id}-{short-name}` (e.g., `feature/US-004-auth-flow`).
- Bugfix branches: `bugfix/{bug-id}-{short-name}` (e.g., `bugfix/BUG-012-null-pointer`).
- Urgent hotfixes: `hotfix/{short-name}`.

---

## 📝 3. Commit Conventions (Conventional Commits)
All commit messages must be in English, written in the imperative mood, following standard prefixes:
- `feat`: New feature or capability (e.g., `feat: add semantic routing for agent supervisor`).
- `fix`: Bug fix (e.g., `fix: handle empty payload in project controller`).
- `docs`: Documentation updates (e.g., `docs: update deployment guide for docker`).
- `refactor`: Code refactoring without changing behavior (e.g., `refactor: extract repository interface in domain layer`).
- `test`: Adding or updating test cases (e.g., `test: add unit tests for token validation`).
- `chore`: Maintenance, dependencies, or CI/CD adjustments (e.g., `chore: update dependencies`).

---

## 🔍 4. Pull Request Process
1. Open a Pull Request targeting `main` (or `develop`).
2. Fill out all sections of `.github/PULL_REQUEST_TEMPLATE.md`.
3. Keep PR size compact (ideally under **400 lines of diff**) for thorough review.
4. Ensure 100% of CI checks pass.
5. Require at least one human maintainer review before merging.
