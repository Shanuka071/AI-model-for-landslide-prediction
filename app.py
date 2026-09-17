import streamlit as st
from nav_pages import get_nav_pages

st.set_page_config(page_title="DisasterGuard", page_icon="🌐", layout="wide")

pages = get_nav_pages()

# 'position="hidden"' hides Streamlit's own auto-generated sidebar nav list,
# since we render a custom top nav bar instead. Older Streamlit versions
# (<1.36) don't support this kwarg, so we fall back gracefully.
try:
    pg = st.navigation(pages, position="hidden")
except TypeError:
    pg = st.navigation(pages)

pg.run()