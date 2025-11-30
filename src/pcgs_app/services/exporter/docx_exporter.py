"""
DOCX Exporter Stub

Prepares learner handbooks, course summaries, and other narrative documents.
Legacy Prometheus logic relied on python-docx helpers embedded in notebooks;
this module will encapsulate that behaviour.
"""

from typing import Any


def export_course_doc(course: Any, template_name: str) -> str:
    """
    Build a DOCX-based course document and return the output path.
    """

    # TODO: Implement placeholder/merge field replacement similar to the legacy
    # project, but driven by theme tokens and structured metadata.
    raise NotImplementedError("DOCX exporter not yet implemented.")


