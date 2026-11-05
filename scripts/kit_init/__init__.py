"""Kit Init Engine: khởi tạo dự án mới từ Starter Kit (thuần logic, testable, headless)."""

from .core import InitError, Result, init_project

__all__ = ["InitError", "Result", "init_project"]
