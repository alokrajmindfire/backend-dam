import streamlit as st
from api import get_blogs, create_blog, update_blog, delete_blog

def show_blog_page():
    st.subheader("📝 Blog Dashboard")
    st.write("Create, edit, and delete blog posts.")

    # --- Blog List ---
    res = get_blogs()
    if res.status_code == 200:
        blogs = res.json()
    else:
        st.warning("⚠️ Unable to fetch blogs.")
        blogs = []

    # --- Add New Blog Modal ---
    if st.button("➕ Add Blog"):
        with st.form("add_blog_form"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            submitted = st.form_submit_button("Create")
            if submitted:
                res = create_blog(title, content)
                if res.status_code == 200:
                    st.success("✅ Blog created!")
                    st.rerun()
                else:
                    st.error("Failed to create blog")

    st.divider()
    st.write("### Existing Blogs")

    if not blogs:
        st.info("No blogs found.")
        return

    for blog in blogs:
        with st.expander(f"📄 {blog['title']}"):
            st.markdown(blog["content"])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Edit", key=f"edit_{blog['id']}"):
                    with st.form(f"edit_form_{blog['id']}"):
                        new_title = st.text_input("New Title", value=blog["title"])
                        new_content = st.text_area("New Content", value=blog["content"])
                        submit_edit = st.form_submit_button("Update")
                        if submit_edit:
                            res = update_blog(blog["id"], new_title, new_content)
                            if res.status_code == 200:
                                st.success("✅ Blog updated!")
                                st.rerun()
                            else:
                                st.error("Update failed")

            with col2:
                if st.button("🗑️ Delete", key=f"del_{blog['id']}"):
                    res = delete_blog(blog["id"])
                    if res.status_code == 200:
                        st.success("✅ Blog deleted!")
                        st.rerun()
                    else:
                        st.error("Delete failed")
