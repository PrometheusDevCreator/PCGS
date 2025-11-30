"""
Exports Tab

Provides placeholders for the courseware export center.
"""

import streamlit as st


def render_tab_exports() -> None:
    """Render the exports tab placeholder."""

    st.header("Generate Courseware")
    st.success("Export pipelines will orchestrate PPTX/DOCX/XLSX generation here.")
    # TODO: Surface exporter services, template selection, and batch actions.


