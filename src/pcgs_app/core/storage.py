"""
Storage Facade

Exposes storage interfaces via `pcgs_app.core.storage` so higher layers can
depend on a stable contract even as the underlying persistence strategy in
`pcgs_core.storage` evolves (local JSON, SQLite, Postgres, etc.).
"""

from pcgs_core.storage import list_courses, load_course, save_course  # noqa: F401

__all__ = ["save_course", "load_course", "list_courses"]


