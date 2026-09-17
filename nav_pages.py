"""
Single source of truth for pages + the top navigation bar.

st.page_link() only accepts string paths for the entrypoint file and files
inside pages/. home_view.py is neither, so nav links use the actual st.Page
objects registered by get_nav_pages() — this is what makes "Home" work from
every sub-page.
"""
import streamlit as st

NAV_ITEMS = [
    ("home_view.py", "Home"),
    ("pages/1_Risk_Dashboard.py", "Risk Dashboard"),
    ("pages/2_Audit_Logs.py", "Audit Logs"),
    ("pages/3_About.py", "About"),
]

_PAGES: dict = {}


def get_nav_pages():
    pages = []
    for i, (path, title) in enumerate(NAV_ITEMS):
        page = st.Page(path, title=title, default=(i == 0))
        _PAGES[title] = page
        pages.append(page)
    return pages


def page_target(title: str):
    if title in _PAGES:
        return _PAGES[title]
    for path, t in NAV_ITEMS:
        if t == title:
            return path
    raise KeyError(title)


def render_navbar(active: str = "Home"):
    """Top navigation bar. `active` must match a NAV_ITEMS title."""
    from theme import html

    # Keyed container, not a raw <div>: a markdown div cannot wrap Streamlit
    # columns (Streamlit closes it immediately, leaving an empty stripe).
    with st.container(key="navshell"):
        cols = st.columns([2.2, 0.85, 1.3, 1.1, 0.9, 1.5], vertical_alignment="center")

        with cols[0]:
            html("<div class='brand'><div class='brand-badge'>🛡️</div>Disaster<span class='g'>Guard</span></div>")

        for i, (_path, title) in enumerate(NAV_ITEMS):
            with cols[i + 1]:
                key = "navactive" if title == active else f"navitem{i}"
                with st.container(key=key):
                    st.page_link(page_target(title), label=title)

        with cols[5]:
            html("<div class='sys-online'><span class='dot'></span>System Online</div>")