import os
import sys

import streamlit as st

_THIS = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS, '..'))

from theme import inject_theme, html, hero_image_css
from nav_pages import render_navbar

inject_theme()
render_navbar(active="About")

html("<div class='page-h'>About <span style='color:var(--accent)'>DisasterGuard</span></div>")
html("<div class='page-sub'>An AI-powered platform for rainfall and landslide risk monitoring, built for safer communities.</div>")

# =========================================================
# MISSION + FEATURES  |  PHOTO PANEL
# =========================================================
left, right = st.columns([1.35, 1], gap="medium")

with left:
    with st.container(border=True):
        html("""
        <div class='feature-icon'>🎯</div>
        <div class='sec-h'>Our Mission</div>
        <p style='color:var(--muted);font-size:13.5px;line-height:1.65;margin:0;'>
        To reduce disaster risks and save lives by providing accurate, real-time
        insights through data and AI technology — tailored to Sri Lanka's dynamic
        microclimates.
        </p>
        """)

    st.write("")

    with st.container(border=True):
        html("""
        <div class='feature-icon'>📋</div>
        <div class='sec-h'>Key Features</div>
        <ul style='color:var(--muted);font-size:13.5px;line-height:2;margin:0;padding-left:18px;'>
        <li>Real-time rainfall monitoring</li>
        <li>AI-based risk prediction</li>
        <li>Interactive risk map with hazard zones</li>
        <li>Emergency alerts and evacuation routing</li>
        <li>Audit logs and reporting</li>
        </ul>
        """)

with right:
    # Same photo used by the hero, as a tall panel with an overlay caption.
    html(f"""
    <div style="
        position:relative;border-radius:14px;overflow:hidden;
        border:1px solid var(--border);min-height:396px;
        background:linear-gradient(180deg, rgba(7,13,17,.30) 0%, rgba(7,13,17,.55) 60%, rgba(7,13,17,.92) 100%), {hero_image_css()};
        background-size:cover,cover;background-position:center,center;
        display:flex;align-items:flex-end;justify-content:flex-end;padding:22px;">
      <div style="
          background:rgba(16,217,160,.92);color:#05201A;border-radius:10px;
          padding:12px 16px;font-weight:800;font-size:13.5px;line-height:1.4;text-align:right;">
        Safer Communities<br>Stronger Tomorrow
      </div>
    </div>
    """)

st.write("")

# =========================================================
# DATA PROCESSING PIPELINE
# =========================================================
with st.container(border=True):
    html("<div class='sec-h'>Our Data Processing Pipeline</div>")
    steps = [
        ("📥", "1. Collect Data", "Rainfall, weather and terrain data"),
        ("🧹", "2. Preprocess", "Clean and transform data"),
        ("🧠", "3. AI Model", "Predict disaster risk using ML"),
        ("🔔", "4. Alert &amp; Notify", "Send warnings to communities"),
    ]
    c = st.columns([2, .35, 2, .35, 2, .35, 2])
    for col, (icon, title, desc) in zip([c[0], c[2], c[4], c[6]], steps):
        with col:
            html(f"""
            <div class='step'>
            <div style='font-size:24px'>{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
            </div>
            """)
    for col in [c[1], c[3], c[5]]:
        with col:
            html("<div class='step-arrow'>➔</div>")

st.write("")

# =========================================================
# MODEL / DATA DETAIL
# =========================================================
d1, d2 = st.columns(2, gap="medium")

with d1:
    with st.container(border=True):
        html("""
        <div class='sec-h'>🤖 Adaptive Reinforcement Learning</div>
        <p style='color:var(--muted);font-size:13.5px;line-height:1.65;'>
        Existing disaster prediction methods rely on static supervised algorithms
        (Random Forest, Decision Tree). This system uses an autonomous
        Reinforcement Learning framework that adapts to environmental feedback,
        removing the latency of fixed-threshold rule engines.
        </p>
        """)
        st.progress(0.7514, text="Model accuracy — 75.14%")

with d2:
    with st.container(border=True):
        html("""
        <div class='sec-h'>🗄️ Data Sources</div>
        <p style='color:var(--muted);font-size:13.5px;line-height:1.65;'>
        Primary data is sourced from the Department of Meteorology, Sri Lanka.
        The dataset (ASPU DATA.xlsx) holds daily rainfall records from 2025–2026
        across Badulla, Colombo, Galle, Hambantota, Nuwara Eliya and Ratnapura.
        </p>
        """)

st.write("")

# =========================================================
# FOOTER
# =========================================================
with st.container(border=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        html("""
        <div class='brand'><div class='brand-badge'>🛡️</div>Disaster<span class='g'>Guard</span></div>
        <p style='color:var(--muted);font-size:12.5px;margin-top:8px;'>Predict Risk. Protect Lives.</p>
        """)
    with f2:
        html("""
        <div class='sec-h'>Project Team</div>
        <p style='color:var(--muted);font-size:12.5px;line-height:1.9;margin:0;'>
        👤 D.L. Senanayake<br>
        👤 A.S.P.U. Shanuka<br>
        👤 U.B.P. Shamika
        </p>
        """)
    with f3:
        html("""
        <div class='sec-h'>Contact</div>
        <p style='color:var(--muted);font-size:12.5px;line-height:1.9;margin:0;'>
        🏛️ Sabaragamuwa University of Sri Lanka<br>
        🏫 Department of Physical Sciences and Technology<br>
        🎓 Faculty of Applied Sciences
        </p>
        """)

html("<div class='ftr' style='text-align:center'>© 2026 DisasterGuard. All rights reserved.</div>")