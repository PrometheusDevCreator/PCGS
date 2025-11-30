"""
PCGS v2 Launcher

This script acts as a simple convenience wrapper to launch the Streamlit app.
"""

import os
import sys
from streamlit.web import cli as stcli

def main():
    # Path to the actual Streamlit entry point
    app_path = os.path.join(os.path.dirname(__file__), "src", "pcgs_ui_streamlit", "main.py")
    
    # Construct the command
    sys.argv = ["streamlit", "run", app_path]
    
    # Run Streamlit
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()







