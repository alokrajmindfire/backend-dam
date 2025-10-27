import streamlit as st
from api import login, register, logout

def show_auth_page():
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])

    # --- Login Tab ---
    with tab1:
        st.subheader("Login to your account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login(email, password)
            if res.status_code == 200:
                st.success("✅ Logged in successfully!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error(res.json().get("detail", "Invalid credentials"))

    # --- Register Tab ---
    with tab2:
        st.subheader("Create new account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register"):
            res = register(reg_email, reg_name, reg_password)
            if res.status_code == 200:
                st.success("✅ Account created! Please login.")
            else:
                st.error(res.json().get("detail", "Registration failed"))

def handle_logout():
    if st.button("🚪 Logout"):
        logout()
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
        st.rerun()
