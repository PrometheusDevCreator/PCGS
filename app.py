"""
PCGS v2 Launcher

This script acts as a simple convenience wrapper to launch the Streamlit app.
It now routes to the V2 app shell (pcgs_app.app_root) instead of the legacy
pcgs_ui_streamlit placeholder.

Usage:
    python app.py
"""

import os
import sys
from streamlit.web import cli as stcli


def main():
    # Determine repo root (directory containing this file)
    repo_root = os.path.dirname(os.path.abspath(__file__))

    # Ensure the "src" directory is on PYTHONPATH so `pcgs_app` is importable
    src_dir = os.path.join(repo_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    # Also set the environment variable so child processes (Streamlit) inherit it
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    if src_dir not in existing_pythonpath:
        os.environ["PYTHONPATH"] = src_dir + os.pathsep + existing_pythonpath

    # Path to the V2 Streamlit entry point (app shell that uses app_root.get_app_tabs)
    app_path = os.path.join(src_dir, "pcgs_app", "main_shell.py")

    # Construct the command
    sys.argv = ["streamlit", "run", app_path, "--server.headless", "true"]

    # Run Streamlit
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()







