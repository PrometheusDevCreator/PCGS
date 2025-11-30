"""
Data Transformation Utilities

Responsible for reshaping data between layers (UI ↔ core models ↔ exports).
Legacy Prometheus logic often duplicated these conversions; centralising them
prevents drift and provides a single mapping source.
"""

from typing import Any, Dict


def course_form_to_model(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert UI form payloads into a structure accepted by pcgs_core workflows.
    """

    # TODO: Map form field names to dataclass fields, normalise values, and
    # attach metadata from lexicon tokens.
    return payload.copy()


