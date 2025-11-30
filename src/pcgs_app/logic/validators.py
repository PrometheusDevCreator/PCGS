"""
Validation Helpers

Placeholder module for reusable validation rules (course metadata, scalar
structure, timetable constraints, etc.). This will supersede inline validation
logic in the legacy UI forms.
"""

from typing import Any, Dict


def validate_course_metadata(data: Dict[str, Any]) -> bool:
    """
    Validate the basic fields required to define a course.
    """

    # TODO: Port legacy per-field checks (course code format, duration bounds)
    # and extend with structured error reporting.
    return True


