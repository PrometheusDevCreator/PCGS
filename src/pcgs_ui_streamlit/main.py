"""
Streamlit Entry Point

This is the main UI application. It should be run via `streamlit run src/pcgs_ui_streamlit/main.py`
or via the launcher script.
"""

import streamlit as st
import sys
import os

# Ensure the src directory is in the python path so we can import pcgs_core
# This allows running this file directly from the repo root or subdirectories
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from src.pcgs_core.config import load_config
    from src.pcgs_core import __version__
except ImportError:
    # Fallback if running from different context
    from pcgs_core.config import load_config
    from pcgs_core import __version__

def main():
    st.set_page_config(
        page_title="PCGS v2",
        page_icon="🔥",
        layout="wide"
    )
    
    config = load_config()

    st.title(f"Prometheus Course Generation System v{__version__}")
    st.markdown("---")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Course Setup", "Scalar Builder", "Lesson Builder", "Timetable", "Exports", "Settings"])

    if page == "Dashboard":
        st.header("Dashboard")
        st.info("Welcome to PCGS v2. This is a skeleton UI.")
        
    elif page == "Course Setup":
        st.header("Course Setup")
        st.write("Create or edit basic course details.")
        
    else:
        st.header(page)
        st.write(f"{page} functionality coming soon.")

    st.sidebar.markdown("---")
    st.sidebar.text(f"Env: {config.ENV}")

if __name__ == "__main__":
    main()

