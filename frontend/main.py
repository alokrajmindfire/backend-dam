import streamlit as st
from auth import show_auth_page, handle_logout
from blog import show_blog_page
from utils import require_login

st.set_page_config(page_title="Blog App", page_icon="📝", layout="centered")

st.title("📰 Blog Application")

if not st.session_state.get("logged_in"):
    show_auth_page()
else:
    handle_logout()
    show_blog_page()
