"""
Core Models Facade

Provides a stable import path (`pcgs_app.core.models`) for upper layers while
delegating the actual dataclass implementations to `pcgs_core.models`.
This makes it easier to introduce compatibility shims or extended metadata in
the future without rewriting existing modules.
"""

from pcgs_core.models import Course, Lesson, Timetable, User  # noqa: F401

__all__ = ["Course", "Lesson", "Timetable", "User"]


