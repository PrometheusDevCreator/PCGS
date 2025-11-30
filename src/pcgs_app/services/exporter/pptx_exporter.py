"""
PPTX Exporter Stub

This module will encapsulate the PowerPoint export logic, replacing the legacy
`export_course_ppt` routines that mixed template manipulation with UI state.
"""

from typing import Any


def export_course_ppt(course: Any, template_name: str) -> str:
    """
    Generate a PPTX export for the given course and return the file path.
    """

    # TODO: Rebuild the python-pptx workflow from Prometheus1 with a cleaner
    # template token system and theme integration.
    raise NotImplementedError("PPTX exporter not yet implemented.")


