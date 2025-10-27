import streamlit as st

def require_login():
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to access this page.")
        st.stop()
