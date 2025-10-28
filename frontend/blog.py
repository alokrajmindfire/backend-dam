import streamlit as st
from api import get_blogs, create_blog, update_blog, delete_blog

def show_blog_page():
    st.subheader("📝 Blog Dashboard")
    st.write("Create, edit, and delete your blog posts below.")

    if "show_add_modal" not in st.session_state:
        st.session_state.show_add_modal = False
    if "edit_blog_id" not in st.session_state:
        st.session_state.edit_blog_id = None
    if "delete_blog_id" not in st.session_state:
        st.session_state.delete_blog_id = None

    res = get_blogs()
    if res.status_code == 200:
        blogs = res.json()
    else:
        st.warning("⚠️ Unable to fetch blogs.")
        st.write("Response:", res.status_code, res.text)
        blogs = []

    st.divider()
    st.write("### 🗂️ Existing Blogs")

    if st.button("➕ Add New Blog"):
        st.session_state.show_add_modal = True
        st.rerun()

    if st.session_state.show_add_modal:
        with st.dialog("Create a New Blog"):
            st.write("### ➕ Add Blog")
            title = st.text_input("Title")
            slug = st.text_input("Slug (optional)")
            content = st.text_area("Content", height=200)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Create"):
                    if not title or not content:
                        st.error("Title and content are required!")
                    else:
                        res = create_blog(title, slug or None, content)
                        if res.status_code == 200:
                            st.success("Blog created successfully!")
                            st.session_state.show_add_modal = False
                            st.rerun()
                        else:
                            st.error(f"Failed to create blog: {res.status_code} — {res.text}")

            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_add_modal = False
                    st.rerun()

    if not blogs:
        st.info("No blogs available yet.")
        return

    for blog in blogs:
        blog_id = blog.get("id")
        with st.expander(f"📄 {blog.get('title', '<No title>')}"):
            st.markdown(blog.get("content", ""))
            col1, col2 = st.columns(2)

            with col1:
                if st.button("✏️ Edit", key=f"edit_{blog_id}"):
                    st.session_state.edit_blog_id = blog_id
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{blog_id}"):
                    st.session_state.delete_blog_id = blog_id
                    st.rerun()

    if st.session_state.edit_blog_id:
        blog_id = st.session_state.edit_blog_id
        blog = next((b for b in blogs if b["id"] == blog_id), None)

        if blog:
            with st.dialog(f"Edit Blog: {blog['title']}"):
                new_title = st.text_input("Title", value=blog.get("title", ""))
                new_slug = st.text_input("Slug", value=blog.get("slug", ""))
                new_content = st.text_area("Content", value=blog.get("content", ""), height=200)
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Update"):
                        res = update_blog(blog_id, new_title, new_slug, new_content)
                        if res.status_code in (200, 204):
                            st.success("✅ Blog updated successfully!")
                            st.session_state.edit_blog_id = None
                            st.rerun()
                        else:
                            st.error(f"Update failed: {res.status_code} — {res.text}")

                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.edit_blog_id = None
                        st.rerun()

    if st.session_state.delete_blog_id:
        blog_id = st.session_state.delete_blog_id
        blog = next((b for b in blogs if b["id"] == blog_id), None)

        if blog:
            with st.dialog(f"Delete Blog: {blog['title']}"):
                st.warning(f"Are you sure you want to delete **{blog['title']}**?")
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("🚮 Confirm Delete"):
                        res = delete_blog(blog_id)
                        if res.status_code in (200, 204):
                            st.success("Blog deleted successfully!")
                            st.session_state.delete_blog_id = None
                            st.rerun()
                        else:
                            st.error(f"Delete failed: {res.status_code} — {res.text}")

                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.delete_blog_id = None
                        st.rerun()
