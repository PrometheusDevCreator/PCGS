"""
Form Widgets

Reusable form sections for metadata, scalar entries, etc.
"""

from typing import Any, Dict

import streamlit as st


def render_metadata_form(initial: Dict[str, Any]):
    """
    Render a minimal metadata form block.
    """

    # TODO: Expand with validation feedback + theming.
    return {
        "name": st.text_input("Name", value=initial.get("name", "")),
        "code": st.text_input("Code", value=initial.get("code", "")),
    }


