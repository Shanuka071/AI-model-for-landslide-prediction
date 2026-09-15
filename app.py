import streamlit as st
from nav_pages import get_nav_pages

st.set_page_config(page_title="DisasterGuard", page_icon="🌐", layout="wide")

pages = get_nav_pages()

# Hide Streamlit's default sidebar navigation
try:
    pg = st.navigation(pages, position="hidden")
except TypeError:
    pg = st.navigation(pages)

pg.run()