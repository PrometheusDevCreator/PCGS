"""
PCGS V2 Main Shell

This is the Streamlit entry point that wires up the V2 tab routing via
`app_root.get_app_tabs()`. It replaces the legacy `pcgs_ui_streamlit/main.py`
placeholder shell.

Run via:
    streamlit run src/pcgs_app/main_shell.py  (with PYTHONPATH=src)
or via the launcher:
    python app.py
"""

import os
import sys

# ---------------------------------------------------------------------------
# Bootstrap: ensure "src" is on sys.path so pcgs_app is importable.
# This allows running the shell directly with `streamlit run` as well as via
# the launcher (app.py), which also sets PYTHONPATH.
# ---------------------------------------------------------------------------
_this_file = os.path.abspath(__file__)
_src_dir = os.path.dirname(os.path.dirname(_this_file))  # src/pcgs_app -> src
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

import streamlit as st

from pcgs_app.app_root import get_app_tabs
from pcgs_app.ui.theme.streamlit_theme import apply_base_theme
from pcgs_app.ui.theme.tokens import get_default_tokens


def main() -> None:
    """
    Render the V2 Prometheus app shell with sidebar navigation and tab routing.
    """
    st.set_page_config(
        page_title="Prometheus Course Generation System 2.0",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply neon theme globally
    apply_base_theme(get_default_tokens())

    tabs = get_app_tabs()
    tab_labels = [t["label"] for t in tabs]
    tab_ids = [t["id"] for t in tabs]

    # Check for programmatic navigation request (e.g. from Create Course manager tiles)
    nav_request = st.session_state.pop("pcgs_navigate_to_tab", None)
    if nav_request and nav_request in tab_ids:
        st.session_state["pcgs_active_tab"] = nav_request

    # Determine current tab
    current_tab_id = st.session_state.get("pcgs_active_tab", tab_ids[0])
    if current_tab_id not in tab_ids:
        current_tab_id = tab_ids[0]
    current_index = tab_ids.index(current_tab_id)

    # Sidebar navigation
    st.sidebar.title("PCGS 2.0")
    st.sidebar.markdown("---")
    selected_label = st.sidebar.radio(
        "Navigation",
        tab_labels,
        index=current_index,
        key="pcgs_sidebar_nav",
    )

    # Resolve selected tab
    selected_index = tab_labels.index(selected_label)
    selected_tab = tabs[selected_index]
    st.session_state["pcgs_active_tab"] = selected_tab["id"]

    # Render the selected tab
    renderer = selected_tab["renderer"]
    renderer()


if __name__ == "__main__":
    main()

