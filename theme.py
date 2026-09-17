"""
Shared visual theme for DisasterGuard.

BACKGROUND PHOTO — how it resolves (first match wins):
  1. assets/hero_bg.jpg  -> your own photo, embedded as base64 (works offline)
  2. HERO_URL below      -> a real Sri Lanka photo loaded from the web
  3. a plain gradient    -> last-resort fallback

To use your own photo, just save it as assets/hero_bg.jpg. Nothing else to change.

IMPORTANT: render raw HTML through html() below, never a bare triple-quoted
st.markdown with indented lines — Markdown turns any line indented 4+ spaces
into a literal code block, which makes raw HTML/SVG show up as source text.
"""
import base64
import functools
import os
import textwrap

import streamlit as st

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Tea plantation on a green mountain slope, Nuwara Eliya, Sri Lanka.
# Photo by Egle Sidaraviciute on Unsplash (free under the Unsplash License).
HERO_URL = (
    "hero_bg.jpg"
    "?fm=jpg&q=75&w=2400&auto=format&fit=crop"
)


def html(markup: str):
    """Render raw HTML, stripping indentation so Markdown can't turn it into
    a code block."""
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


@functools.lru_cache(maxsize=4)
def _b64_asset(filename: str) -> str:
    try:
        with open(os.path.join(_ASSETS, filename), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except (FileNotFoundError, OSError):
        return ""


def hero_image_css() -> str:
    """CSS value for the hero photo layer."""
    local = _b64_asset("hero_bg.jpg")
    if local:
        return f"url('data:image/jpeg;base64,{local}')"
    if HERO_URL:
        return f"url('{HERO_URL}')"
    return "linear-gradient(140deg, #0d2a24 0%, #14463a 50%, #0a1a18 100%)"


def _css() -> str:
    photo = hero_image_css()
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {{
    --bg: #070D11;
    --panel: #0F1A1F;
    --panel-2: #132228;
    --border: #1E3038;
    --accent: #10D9A0;
    --accent-2: #16B37E;
    --accent-soft: rgba(16,217,160,0.12);
    --danger: #FF5A6E;
    --warning: #FFB020;
    --info: #3B9EFF;
    --text: #EAF2F2;
    --muted: #8FA5AE;
}}

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
h1,h2,h3,h4,.brand,.hero-h,.page-h {{ font-family: 'Plus Jakarta Sans', sans-serif; }}

.stApp {{ background: var(--bg); color: var(--text); }}
.stApp, section.main {{ overflow-x: hidden; }}
#MainMenu, footer, header {{ visibility: hidden; }}
section.main > div.block-container {{ padding-top: 1rem; max-width: 1280px; }}

/* ============ NAV ============ */
.st-key-navshell {{
    background: rgba(9,20,24,0.92);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 4px 16px;
    margin-bottom: 16px;
}}
.brand {{
    display: flex; align-items: center; gap: 10px;
    font-size: 19px; font-weight: 800; color: #fff; white-space: nowrap; padding: 4px;
}}
.brand .g {{ color: var(--accent); }}
.brand-badge {{
    width: 32px; height: 32px; border-radius: 9px; flex: none;
    background: var(--accent-soft); border: 1px solid rgba(16,217,160,0.45);
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}}
.sys-online {{
    display: flex; align-items: center; justify-content: flex-end; gap: 8px;
    color: var(--muted); font-size: 12.5px; font-weight: 600; white-space: nowrap; padding: 8px 2px;
}}
.sys-online .dot {{
    width: 8px; height: 8px; border-radius: 50%; flex: none;
    background: var(--accent); box-shadow: 0 0 9px var(--accent);
    animation: pulse 1.9s infinite;
}}
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(16,217,160,.6); }}
    70% {{ box-shadow: 0 0 0 10px rgba(16,217,160,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(16,217,160,0); }}
}}
div[data-testid="stPageLink"] a {{
    border-radius: 8px !important; padding: 10px 6px !important;
    font-weight: 600 !important; font-size: 14px !important;
    color: var(--muted) !important; justify-content: center !important;
    transition: all .18s ease;
}}
div[data-testid="stPageLink"] a:hover {{ color: #fff !important; background: rgba(255,255,255,.06) !important; }}
/* active tab: green text + underline, like the mockup */
.st-key-navactive div[data-testid="stPageLink"] a {{
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    border-radius: 8px 8px 0 0 !important;
}}

/* ============ HERO (photo) ============ */
.hero {{
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--border);
    background:
        linear-gradient(100deg, rgba(7,13,17,0.94) 0%, rgba(7,13,17,0.80) 42%, rgba(7,13,17,0.45) 70%, rgba(7,13,17,0.35) 100%),
        {photo};
    background-size: cover, cover;
    background-position: center, center;
    padding: 58px 46px;
    margin-bottom: 18px;
}}
.hero-h {{
    font-size: clamp(34px, 4.4vw, 58px); font-weight: 800; line-height: 1.06;
    letter-spacing: -1.5px; color: #fff; margin: 0;
}}
.hero-h .accent {{ color: var(--accent); }}
.hero-sub {{
    color: #CBD9DD; font-size: 16px; line-height: 1.7; max-width: 460px; margin: 18px 0 0 0;
}}

.st-key-cta-primary div[data-testid="stPageLink"] a {{
    background: var(--accent) !important; color: #05201A !important;
    font-weight: 700 !important; padding: 13px 18px !important;
    border-radius: 999px !important; box-shadow: 0 10px 26px rgba(16,217,160,.28);
}}
.st-key-cta-primary div[data-testid="stPageLink"] a:hover {{ transform: translateY(-2px); }}
.st-key-cta-ghost div[data-testid="stPageLink"] a {{
    background: rgba(255,255,255,.04) !important; border: 1px solid rgba(255,255,255,.35) !important;
    color: #fff !important; font-weight: 600 !important; padding: 13px 18px !important;
    border-radius: 999px !important;
}}
.st-key-cta-ghost div[data-testid="stPageLink"] a:hover {{ background: rgba(255,255,255,.12) !important; transform: translateY(-2px); }}

/* radar */
.radar-spin {{ transform-origin: 160px 160px; animation: spin 4.5s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.blip {{ animation: blink 2.6s infinite; }}
@keyframes blink {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}

/* ============ CARDS ============ */
.card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px;
}}
.feature-card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px; min-height: 172px;
    transition: transform .22s, border-color .22s;
}}
.feature-card:hover {{ transform: translateY(-6px); border-color: var(--accent); }}
.feature-icon {{
    width: 44px; height: 44px; border-radius: 50%;
    background: var(--accent-soft); border: 1px solid rgba(16,217,160,.35);
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; margin-bottom: 14px;
}}
.feature-card h3 {{ color: #fff; font-size: 15.5px; margin: 0 0 7px 0; }}
.feature-card p {{ color: var(--muted); font-size: 13px; line-height: 1.55; margin: 0; }}

.metric-card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px;
}}
.metric-card .lbl {{ color: var(--muted); font-size: 11.5px; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 8px; }}
.metric-card .val {{ color: #fff; font-size: 27px; font-weight: 800; line-height: 1; }}
.metric-card .sub {{ color: var(--muted); font-size: 12px; margin-top: 7px; }}

.pill {{ display: inline-block; padding: 5px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; }}
.pill-high {{ background: rgba(255,90,110,.15); color: var(--danger); border: 1px solid rgba(255,90,110,.5); }}
.pill-mod  {{ background: rgba(255,176,32,.15); color: var(--warning); border: 1px solid rgba(255,176,32,.5); }}
.pill-low  {{ background: rgba(16,217,160,.15); color: var(--accent); border: 1px solid rgba(16,217,160,.5); }}

.alert-box {{ border-radius: 14px; padding: 20px; border: 1px solid; }}
.alert-high {{ background: rgba(255,90,110,.10); border-color: rgba(255,90,110,.55); }}
.alert-mod  {{ background: rgba(255,176,32,.10); border-color: rgba(255,176,32,.55); }}
.alert-low  {{ background: rgba(16,217,160,.10); border-color: rgba(16,217,160,.55); }}
.alert-box .t {{ font-weight: 800; font-size: 18px; margin: 8px 0 6px 0; }}
.alert-box .d {{ color: var(--muted); font-size: 13px; line-height: 1.55; }}
.alert-high .t {{ color: var(--danger); }}
.alert-mod .t {{ color: var(--warning); }}
.alert-low .t {{ color: var(--accent); }}

.legend-row {{ display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: 12.5px; margin-bottom: 8px; }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 50%; flex: none; }}

.page-h {{ font-size: 28px; font-weight: 800; color: #fff; margin: 4px 0 2px 0; }}
.page-sub {{ color: var(--muted); font-size: 14px; margin-bottom: 18px; }}
.sec-h {{ font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 12px; }}

.tbl {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.tbl th {{ color: var(--muted); font-weight: 600; text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 11.5px; text-transform: uppercase; letter-spacing: .4px; }}
.tbl td {{ color: var(--text); padding: 11px 12px; border-bottom: 1px solid rgba(30,48,56,.6); }}
.tbl tr:last-child td {{ border-bottom: none; }}

.step {{ background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 18px 14px; text-align: center; min-height: 150px; }}
.step .n {{ color: var(--accent); font-size: 12px; font-weight: 700; }}
.step h4 {{ color: #fff; font-size: 14px; margin: 6px 0; }}
.step p {{ color: var(--muted); font-size: 12px; margin: 0; line-height: 1.5; }}
.step-arrow {{ text-align: center; color: var(--accent); font-size: 18px; padding-top: 62px; }}

.ftr {{ border-top: 1px solid var(--border); margin-top: 26px; padding-top: 18px; color: var(--muted); font-size: 12.5px; }}

section[data-testid="stSidebar"] {{ background: #0A1418; border-right: 1px solid var(--border); }}

/* Streamlit widget polish */
div[data-testid="stMetricValue"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
.stButton > button {{
    background: var(--accent); color: #05201A; font-weight: 700;
    border: none; border-radius: 10px; padding: 11px 18px; width: 100%;
}}
.stButton > button:hover {{ background: #14F0B0; color: #05201A; }}

@media (max-width: 900px) {{
    .hero {{ padding: 34px 22px; }}
    .feature-card, .step {{ min-height: auto; }}
}}
</style>
"""


def inject_theme():
    st.markdown(_css(), unsafe_allow_html=True)
    st.markdown(hero_container_css(), unsafe_allow_html=True)


# Hero container styling is appended here so it can reference hero_image_css()
def hero_container_css() -> str:
    return f"""
<style>
.st-key-hero {{
    position: relative;
    border-radius: 18px;
    border: 1px solid var(--border);
    background:
        linear-gradient(100deg, rgba(7,13,17,0.95) 0%, rgba(7,13,17,0.82) 40%,
                        rgba(7,13,17,0.48) 70%, rgba(7,13,17,0.38) 100%),
        {hero_image_css()};
    background-size: cover, cover;
    background-position: center, center;
    padding: 52px 42px;
    margin-bottom: 18px;
}}
</style>
"""