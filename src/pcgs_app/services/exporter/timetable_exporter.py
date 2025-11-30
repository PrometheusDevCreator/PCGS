"""
Timetable Exporter Stub

Responsible for generating timetable spreadsheets (XLSX/CSV) that align with
the Rabdan-style day structure. Legacy implementations lived in Streamlit
callbacks; here we isolate them for testing and reuse.
"""

from typing import Any


def export_timetable(course: Any, template_name: str) -> str:
    """
    Build the timetable file for the provided course and return the path.
    """

    # TODO: Re-implement the timetable XLSX writer, factoring in multi-session
    # layouts and theme tokens.
    raise NotImplementedError("Timetable exporter not yet implemented.")


