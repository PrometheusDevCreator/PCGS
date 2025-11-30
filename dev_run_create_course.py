import streamlit as st

# New v2 console tab
from pcgs_app.ui.tabs.tab_create_course import render_tab_create_course


def main() -> None:
    """
    Dev entry-point for the Prometheus V2 Create Course console.

    This does NOT affect the legacy UI – it's just a sandbox runner.
    """
    st.set_page_config(
        page_title="Prometheus V2 – Create Course (Dev)",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Run the neon console tab
    render_tab_create_course()


if __name__ == "__main__":
    main()
