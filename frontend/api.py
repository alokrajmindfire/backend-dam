import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

def get_session():
    if "session" not in st.session_state:
        st.session_state.session = requests.Session()
    return st.session_state.session

def login(email, password):
    session = get_session()
    return session.post(f"{API_URL}/auth/login", json={"email": email, "password": password})

def register(email, full_name, password):
    return requests.post(f"{API_URL}/auth/register", json={
        "email": email,
        "full_name": full_name,
        "password": password
    })

def logout():
    session = get_session()
    return session.post(f"{API_URL}/auth/logout")

def get_blogs():
    session = get_session()
    return session.get(f"{API_URL}/blogs/")

def create_blog(title, slug, content):
    session = get_session()
    payload = {
        "title": title,
        "slug": slug,
        "content": content
    }
    return session.post(f"{API_URL}/blogs/", json=payload)

def update_blog(blog_id, title, slug, content):
    """
    slug may be empty. Only include slug in payload if provided (some backends don't expect it).
    """
    print("update_blog called with", blog_id, title, slug)
    session = get_session()
    payload = {"title": title, "content": content}
    if slug:
        payload["slug"] = slug
    return session.put(f"{API_URL}/blogs/{blog_id}", json=payload)

def delete_blog(blog_id):
    session = get_session()
    return session.delete(f"{API_URL}/blogs/{blog_id}")
