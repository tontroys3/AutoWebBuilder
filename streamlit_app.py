"""
Streamlit App Entry Point for Deployment
Auto Website Builder - Professional Website Management System

This file serves as the main entry point for streamlit.app deployment.
"""

import streamlit as st
import sys
import traceback

def main():
    """Main application entry point with error handling"""
    try:
        # Try to import and run the main app
        from app import main as app_main
        app_main()
    except ImportError as e:
        st.error("Failed to import required modules. Please check dependencies.")
        st.code(str(e))
        st.stop()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        with st.expander("Error Details"):
            st.code(traceback.format_exc())
        st.stop()

if __name__ == "__main__":
    main()
else:
    # For streamlit.app deployment
    main()