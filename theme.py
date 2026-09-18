"""
Shared visual theme for DisasterGuard.

============================================================
 TO CHANGE THE BACKGROUND PHOTO, EDIT ONE LINE: HERO_FILENAME
============================================================
Set it to the exact filename of a photo sitting in assets/ (or right next to
app.py), e.g.:

    HERO_FILENAME = "image3.jpg"

That's it — save, rerun the app. No other line needs to change.

Full resolution order (first match wins):
  1. HERO_FILENAME (below) — if set, this exact file is used and nothing
     else is checked. This always wins, even if a hero_bg.* file also exists.
  2. hero_bg.jpg / .jpeg / .png — used automatically if HERO_FILENAME is
     empty. Checked in assets/ first, then next to app.py.
  3. HERO_URL — a real Sri Lanka photo loaded from the web, used only if
     steps 1 and 2 found nothing.
  4. A plain gradient — last-resort fallback.

Common mistake this avoids: previously, setting HERO_URL had no visible
effect whenever a leftover hero_bg.jpg was still sitting in the project —
the local file silently took priority. HERO_FILENAME exists so there's one
obvious, always-wins way to pick a specific photo.

IMPORTANT: render raw HTML through html() below, never a bare triple-quoted
st.markdown with indented lines — Markdown turns any line indented 4+ spaces
into a literal code block, which makes raw HTML/SVG show up as source text.
"""
import base64
import functools
import mimetypes
import os
import textwrap

import streamlit as st

_ROOT = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_ROOT, "assets")

# <<< EDIT THIS to switch the background photo. Leave as "" to fall back to
# the automatic hero_bg.jpg / .jpeg / .png search below.
HERO_FILENAME = "image2.jpg"

# Checked in order — first file that actually exists wins. Covers the two
# places people naturally save a downloaded photo (assets/, or right next
# to app.py) and the common extensions.
_LOCAL_HERO_CANDIDATES = [
    os.path.join(_ASSETS, "hero_bg.jpg"),
    os.path.join(_ASSETS, "hero_bg.jpeg"),
    os.path.join(_ASSETS, "hero_bg.png"),
    os.path.join(_ROOT, "hero_bg.jpg"),
    os.path.join(_ROOT, "hero_bg.jpeg"),
    os.path.join(_ROOT, "hero_bg.png"),
]

# Tea plantation on a green mountain slope, Nuwara Eliya, Sri Lanka.
# Photo by Egle Sidaraviciute on Unsplash (free under the Unsplash License).
# NOTE: keep this as ONE string. Splitting it across lines without the
# implicit-concatenation being a single valid URL (e.g. separating the path
# from its "?query=..." part) silently breaks the image — Python will still
# join the pieces into one string, but it won't be a working link.
# NOTE: this is a remote fallback only — see resolution order above. If a
# local photo is found (via HERO_FILENAME or hero_bg.*), this is never used.
HERO_URL = "https://images.unsplash.com/photo-1559038300-07cb5d6c3d27?fm=jpg&q=75&w=2400&auto=format&fit=crop"


def html(markup: str):
    """Render raw HTML, stripping indentation so Markdown can't turn it into
    a code block."""
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


def _load_image(path: str):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        mime = mimetypes.guess_type(path)[0] or "image/jpeg"
        return data, mime
    except OSError:
        return None, None


@functools.lru_cache(maxsize=8)
def _load_image_cached(path: str, _mtime: float):
    """_mtime is part of the cache key purely so that replacing the photo
    file (which changes its mtime) invalidates the cache automatically —
    without this, an lru_cache with no changing arguments would keep
    serving the first photo it ever loaded for the lifetime of the running
    Streamlit server, even after you swap the file."""
    return _load_image(path)


def _find_local_hero():
    """Return (base64_data, mime_type, path) for the active local hero photo,
    or (None, None, None) if none is found."""
    # 1. Explicit override always wins, checked in assets/ then root.
    if HERO_FILENAME:
        for base in (_ASSETS, _ROOT):
            path = os.path.join(base, HERO_FILENAME)
            if os.path.isfile(path):
                data, mime = _load_image_cached(path, os.path.getmtime(path))
                if data:
                    return data, mime, path
        # HERO_FILENAME was set but the file wasn't found anywhere —
        # fall through to the generic hero_bg.* search rather than silently
        # showing nothing.

    # 2. Generic hero_bg.* search.
    for path in _LOCAL_HERO_CANDIDATES:
        if os.path.isfile(path):
            data, mime = _load_image_cached(path, os.path.getmtime(path))
            if data:
                return data, mime, path

    return None, None, None


def hero_photo_status() -> str:
    """Human-readable status of which background source is active — handy
    for debugging, e.g. python3 -c "import theme; print(theme.hero_photo_status())" """
    data, _, path = _find_local_hero()
    if data:
        return f"Using local photo: {path}"
    if HERO_FILENAME:
        return (
            f"HERO_FILENAME is set to '{HERO_FILENAME}' but that file was not "
            f"found in {_ASSETS} or {_ROOT} — falling through to remote/gradient."
        )
    if HERO_URL:
        return f"Using remote photo: {HERO_URL}"
    return "No photo found — using gradient fallback."


def hero_image_css() -> str:
    """CSS value for the hero photo layer."""
    data, mime, _path = _find_local_hero()
    if data:
        return f"url('data:{mime};base64,{data}')"
    if HERO_URL:
        return f"url('{HERO_URL}')"
    return "linear-gradient(140deg, #0d2a24 0%, #14463a 50%, #0a1a18 100%)"


def _css() -> str:
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

/* ============ HERO (typography only — the photo lives on
   .st-key-homepage in home_background_css(), not here) ============ */
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
    st.markdown(home_background_css(), unsafe_allow_html=True)


def home_background_css() -> str:
    """
    Full-page photo background for the Home page only.

    Scoped entirely under .st-key-homepage, which home_view.py uses as the
    single outer container wrapping the hero, feature cards, stats and
    footer. Every other page is unaffected, since they never render a
    'homepage' keyed container.

    The panels inside (.feature-card, .metric-card) are turned translucent
    here so the photo shows through them too ("penetrable", as requested),
    with a text-shadow added to headings/labels so text stays legible
    regardless of how bright the photo is at that spot.
    """
    return f"""
<style>
.st-key-homepage {{
    position: relative;
    border-radius: 20px;
    border: 1px solid var(--border);
    background:
        linear-gradient(180deg,
            rgba(7,13,17,0.32) 0%,
            rgba(7,13,17,0.50) 32%,
            rgba(7,13,17,0.78) 68%,
            rgba(7,13,17,0.94) 100%),
        {hero_image_css()};
    background-size: cover, cover;
    background-position: center top, center top;
    background-repeat: no-repeat, no-repeat;
    padding: 52px 42px 34px 42px;
    margin-bottom: 18px;
}}

/* Text over the photo needs a shadow so it stays readable at any point */
.st-key-homepage .hero-h,
.st-key-homepage .hero-sub {{
    text-shadow: 0 2px 18px rgba(0,0,0,.55);
}}

/* Cards inside the home page become frosted glass, so the photo shows
   through them consistently rather than sitting on a solid dark box. */
.st-key-homepage .feature-card,
.st-key-homepage .metric-card {{
    background: rgba(15,26,31,0.42) !important;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.12) !important;
}}
.st-key-homepage .feature-card h3,
.st-key-homepage .feature-card p,
.st-key-homepage .metric-card .val,
.st-key-homepage .metric-card .lbl {{
    text-shadow: 0 1px 10px rgba(0,0,0,.5);
}}
.st-key-homepage .ftr {{
    border-top-color: rgba(255,255,255,0.18);
    text-shadow: 0 1px 8px rgba(0,0,0,.5);
}}
</style>
"""