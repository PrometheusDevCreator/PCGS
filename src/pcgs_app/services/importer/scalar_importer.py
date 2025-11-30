"""
Scalar Importer

Placeholder for importing course scalar structures from spreadsheets/legacy
sources. This module will supersede the Prometheus1 `import_course_structure`
excel routines while enforcing schema validation and audit logging.
"""

from typing import Any, List


def import_scalar_from_workbook(path: str) -> List[Any]:
    """
    Load scalar data from the provided workbook path.
    """

    # TODO: Re-implement `import_course_structure_from_excel` behaviour using a
    # streaming parser plus transform/validation hooks.
    raise NotImplementedError("Scalar importer not yet implemented.")


