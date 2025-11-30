"""
Streamlit Tab Renderers

Each module renders a specific tab/page in the UI shell. Keeping them isolated
prevents the mega-file problem seen in Prometheus1.
"""

from . import (
    tab_content,
    tab_create_course,
    tab_exports,
    tab_lessons,
    tab_planner,
    tab_scalar,
)  # noqa: F401

__all__ = [
    "tab_create_course",
    "tab_scalar",
    "tab_content",
    "tab_lessons",
    "tab_planner",
    "tab_exports",
]


