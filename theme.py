import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0A1210;
    --bg-deep: #060B0A;
    --panel: #0F1C18;
    --panel-alt: #13241F;
    --border: #1E322C;

    --accent: #10B981;
    --accent-soft: rgba(16,185,129,0.14);
    --accent2: #34D399;

    --danger: #EF4444;
    --danger-soft: rgba(239,68,68,0.14);
    --warning: #F5A524;
    --warning-soft: rgba(245,165,36,0.14);

    --text: #EAF2EF;
    --muted: #8FA39C;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, .hero-title, .brand-row, .section-title { font-family: 'Sora', sans-serif; }

.stApp {
    background: var(--bg);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }

/* ---------- Nav bar ---------- */
.brand-row {
    display: flex; align-items: center; gap: 10px;
    font-size: 19px; font-weight: 700; color: #fff; padding: 6px 0;
}
.brand-shield {
    width: 30px; height: 30px; border-radius: 8px;
    background: var(--accent-soft); display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
div[data-testid="stPageLink"] a {
    border-radius: 8px !important;
    padding: 8px 14px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    color: var(--muted) !important;
    transition: color 0.15s ease, background 0.15s ease;
    justify-content: center !important;
}
div[data-testid="stPageLink"] a:hover {
    background: var(--accent-soft) !important;
    color: var(--accent) !important;
}
.status-online {
    display: flex; align-items: center; gap: 6px; justify-content: flex-end;
    font-size: 12px; color: var(--muted); padding: 8px 4px;
}
.status-online .dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--accent);
    box-shadow: 0 0 8px var(--accent); animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.55); }
    70% { box-shadow: 0 0 0 9px rgba(16,185,129,0); }
    100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

/* ---------- Hero photo background ----------
   Swap the url() for your own licensed forest / valley photo.
   Selectors are chained + !important because Streamlit's own
   stylesheet also sets a background-color on this wrapper. */
div[data-testid="stVerticalBlockBorderWrapper"].st-key-hero_container,
div[data-testid="stVerticalBlockBorderWrapper"].st-key-hero_container > div,
div[data-testid="stVerticalBlockBorderWrapper"].st-key-hero_container div[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
    background-image:
        linear-gradient(100deg, rgba(6,11,10,0.94) 24%, rgba(6,11,10,0.55) 60%, rgba(6,11,10,0.25) 100%),
        url('https://picsum.photos/seed/disasterguard-forest/1600/900') !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    padding: 12px !important;
}

/* ---------- Hero ---------- */
.hero-title {
    font-size: 44px; font-weight: 700; line-height: 1.12; margin: 10px 0 14px 0;
    color: #FFFFFF; letter-spacing: -0.5px;
}
.hero-title .accent-line { color: var(--accent); display: block; }
.hero-sub { color: #C7D3CE; font-size: 15.5px; max-width: 440px; line-height: 1.6; }

/* ---------- Radar illustration (Sri Lanka silhouette + sweep) ---------- */
.radar-wrap { width: 100%; max-width: 240px; margin: 10px auto; }
.radar-wrap svg { width: 100%; height: auto; display: block; }
.radar-dot-svg { animation: blink2 2.2s infinite; }
@keyframes blink2 { 0%, 100% { opacity: 0.45; } 50% { opacity: 1; } }

/* ---------- Feature / stat cards ---------- */
.feature-card {
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    padding: 20px 18px; transition: border-color .2s ease;
}
.feature-card:hover { border-color: var(--accent); }
.feature-icon {
    width: 40px; height: 40px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 19px;
    background: var(--accent-soft); margin-bottom: 12px; color: var(--accent);
}
.feature-card h3 { color: #fff; font-size: 15px; margin: 0 0 6px 0; font-weight: 600; }
.feature-card p { color: var(--muted); font-size: 12.5px; line-height: 1.5; margin: 0; }

.stat-box {
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    padding: 18px; text-align: center;
}
.stat-box h2 { color: var(--accent); font-size: 24px; margin: 0; font-weight: 700; }
.stat-box p { color: var(--muted); font-size: 12px; margin-top: 6px; }

/* ---------- Metric / status ---------- */
.metric-card {
    background: var(--panel); padding: 16px 18px; border-radius: 12px;
    border: 1px solid var(--border);
}
.metric-card .m-label { color: var(--muted); font-size: 12px; margin-bottom: 6px; }
.metric-card h3 { color: var(--text); font-size: 21px; margin: 0; font-weight: 700; }
.metric-card .m-sub { font-size: 11.5px; margin-top: 4px; }
.m-sub.up { color: var(--danger); }
.m-sub.ok { color: var(--accent); }

.risk-pill {
    display: inline-block; padding: 4px 14px; border-radius: 999px;
    font-weight: 700; font-size: 13px;
}
.risk-pill.high { background: var(--danger); color: #fff; }
.risk-pill.moderate { background: var(--warning); color: #3D2A05; }
.risk-pill.low { background: var(--accent); color: #06281C; }

.status-pill { padding: 15px 18px; border-radius: 10px; font-weight: 600; border-left: 3px solid transparent; }
.status-safe { background: var(--accent-soft); color: var(--accent); border-left-color: var(--accent); }
.status-risk { background: var(--danger-soft); color: var(--danger); border-left-color: var(--danger); }

.danger-banner { padding: 16px 18px; border-radius: 10px; font-weight: 700; font-size: 15px; margin-top: 14px; }
.danger-low      { background: var(--accent-soft); color: var(--accent); }
.danger-moderate { background: var(--warning-soft); color: var(--warning); }
.danger-high     { background: var(--danger-soft);  color: var(--danger); }
.danger-banner .db-sub { font-weight: 400; font-size: 12.5px; color: var(--muted); margin-top: 6px; }

/* ---------- Panels / lists ---------- */
.panel-card {
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
    padding: 18px 20px;
}
.panel-card h4 { margin: 0 0 14px 0; font-size: 14.5px; color: #fff; font-weight: 600; }
.legend-row { display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: var(--muted); margin: 6px 0; }
.legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }

.check-list { list-style: none; padding: 0; margin: 0; }
.check-list li { display: flex; align-items: center; gap: 8px; font-size: 13.5px; color: var(--text); padding: 5px 0; }
.check-list li:before { content: "✓"; color: var(--accent); font-weight: 700; }

.pipeline-row { display: flex; align-items: flex-start; gap: 6px; }
.pipeline-node { flex: 1; text-align: center; }
.pipeline-icon {
    width: 46px; height: 46px; border-radius: 50%; background: var(--accent-soft);
    display: flex; align-items: center; justify-content: center; font-size: 19px;
    color: var(--accent); margin: 0 auto 10px auto;
}
.pipeline-node h5 { color: #fff; font-size: 13px; margin: 0 0 4px 0; font-weight: 600; }
.pipeline-node p { color: var(--muted); font-size: 11.5px; margin: 0; line-height: 1.4; }
.pipeline-arrow { color: var(--border); font-size: 20px; padding-top: 12px; }

.glass {
    background: rgba(15,28,24,0.6);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--border); border-radius: 14px;
}

.section-title { font-weight: 700; font-size: 23px; margin-bottom: 4px; color: #fff; }
.section-title .accent-word { color: var(--accent); }
.section-sub { color: var(--muted); margin-bottom: 20px; font-size: 14px; }
hr { border-color: var(--border) !important; }
</style>
"""

def inject_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)