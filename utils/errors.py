import traceback
import streamlit as st

def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.expander("Show Detailed Error").code(traceback.format_exc())
    return wrapper
