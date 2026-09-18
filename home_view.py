import streamlit as st

from theme import inject_theme, html
from nav_pages import render_navbar

inject_theme()
render_navbar(active="Home")

# =========================================================
# ONE background photo spans the whole home page from here down.
# Everything — hero, feature cards, stats, footer — lives inside this
# single keyed container so the photo shows through all of it, with the
# cards turned into frosted glass (see .st-key-homepage in theme.py).
# =========================================================
with st.container(key="homepage"):

    # ---------------- HERO ----------------
    hl, hr = st.columns([1.12, 1], vertical_alignment="center")

    with hl:
        html("""
        <div class='hero-h'>Predict Risk.<br><span class='accent'>Protect Lives.</span></div>
        <div class='hero-sub'>
        DisasterGuard is an AI-powered platform for monitoring rainfall and
        landslide risk, helping communities prepare and stay safe.
        </div>
        """)
        st.write("")
        c1, c2, c3 = st.columns([1.25, 0.8, 0.5])
        with c1:
            with st.container(key="cta-primary"):
                st.page_link("pages/1_Risk_Dashboard.py", label="View Risk Dashboard  →")
        with c2:
            with st.container(key="cta-ghost"):
                st.page_link("pages/3_About.py", label="Learn More")

    with hr:
        html("""
        <svg viewBox="0 0 320 320" width="100%" style="max-width:320px;display:block;margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        <defs>
        <radialGradient id="rg" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#10D9A0" stop-opacity="0.20"/>
        <stop offset="70%" stop-color="#10D9A0" stop-opacity="0.05"/>
        <stop offset="100%" stop-color="#10D9A0" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#10D9A0" stop-opacity="0.60"/>
        <stop offset="100%" stop-color="#10D9A0" stop-opacity="0"/>
        </linearGradient>
        </defs>
        <circle cx="160" cy="160" r="150" fill="url(#rg)"/>
        <circle cx="160" cy="160" r="150" fill="none" stroke="#10D9A0" stroke-opacity="0.35" stroke-width="1.2"/>
        <circle cx="160" cy="160" r="112" fill="none" stroke="#10D9A0" stroke-opacity="0.28" stroke-width="1.2"/>
        <circle cx="160" cy="160" r="74" fill="none" stroke="#10D9A0" stroke-opacity="0.24" stroke-width="1.2"/>
        <circle cx="160" cy="160" r="36" fill="none" stroke="#10D9A0" stroke-opacity="0.22" stroke-width="1.2"/>
        <line x1="10" y1="160" x2="310" y2="160" stroke="#10D9A0" stroke-opacity="0.15" stroke-width="1"/>
        <line x1="160" y1="10" x2="160" y2="310" stroke="#10D9A0" stroke-opacity="0.15" stroke-width="1"/>
        <g class="radar-spin"><path d="M160 160 L160 10 A150 150 0 0 1 272 60 Z" fill="url(#sweep)"/></g>
        <circle class="blip" cx="212" cy="104" r="6" fill="#FFB020" style="animation-delay:0s"/>
        <circle class="blip" cx="128" cy="212" r="6" fill="#10D9A0" style="animation-delay:.4s"/>
        <circle class="blip" cx="216" cy="198" r="6" fill="#10D9A0" style="animation-delay:.8s"/>
        <circle class="blip" cx="104" cy="142" r="6" fill="#FF5A6E" style="animation-delay:1.2s"/>
        <circle class="blip" cx="244" cy="246" r="6" fill="#FFB020" style="animation-delay:1.6s"/>
        <circle class="blip" cx="92" cy="238" r="6" fill="#10D9A0" style="animation-delay:2s"/>
        <circle class="blip" cx="176" cy="88" r="6" fill="#10D9A0" style="animation-delay:2.3s"/>
        <circle cx="160" cy="160" r="6" fill="#10D9A0"/>
        </svg>
        """)

    st.write("")

    # ---------------- FEATURE CARDS ----------------
    features = [
        ("🕒", "Real-time Monitoring", "Track rainfall and weather data in real time."),
        ("🧬", "AI Prediction", "Accurate risk prediction using machine learning."),
        ("⚠️", "Risk Alerts", "Get instant alerts for high-risk areas."),
        ("🛡️", "Safer Communities", "Support early preparedness and response."),
    ]
    for col, (icon, title, desc) in zip(st.columns(4), features):
        with col:
            html(f"""
            <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
            </div>
            """)

    st.write("")

    # ---------------- STATS ----------------
    stats = [("6", "Districts Monitored"), ("75.14%", "Model Accuracy"),
             ("24/7", "Live Telemetry"), ("RL", "Adaptive AI Engine")]
    for col, (v, l) in zip(st.columns(4), stats):
        with col:
            html(f"<div class='metric-card'><div class='lbl'>{l}</div><div class='val'>{v}</div></div>")

    html("<div class='ftr'>© 2026 DisasterGuard · Department of Physical Sciences and Technology, Sabaragamuwa University</div>")