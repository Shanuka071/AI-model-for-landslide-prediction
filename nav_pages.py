import streamlit as st

NAV_ITEMS = [
    ("home_view.py", "Home"),
    ("pages/1_Risk_Dashboard.py", "Risk Dashboard"),
    ("pages/2_Audit_Logs.py", "Audit Logs"),
    ("pages/3_About.py", "About"),
]

def get_nav_pages():
    """Build the st.Page objects used by st.navigation in app.py."""
    pages = []
    for i, (path, title) in enumerate(NAV_ITEMS):
        pages.append(st.Page(path, title=title, default=(i == 0)))
    return pages

def render_navbar():
    """Render the top navigation bar. Call at the top of every page."""
    with st.container(border=True):
        cols = st.columns([2, 1, 1, 1, 1, 1.3])
        with cols[0]:
            st.markdown(
                "<div class='brand-row'><span class='brand-shield'>🛡️</span>DisasterGuard</div>",
                unsafe_allow_html=True,
            )
        for i, (path, title) in enumerate(NAV_ITEMS):
            with cols[i + 1]:
                st.page_link(path, label=title)
        with cols[5]:
            st.markdown(
                "<div class='status-online'><span class='dot'></span>System online</div>",
                unsafe_allow_html=True,
            )