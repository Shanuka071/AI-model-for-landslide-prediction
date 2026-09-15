import streamlit as st
import sys
import os

_THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS_DIR, '..'))

from theme import inject_theme
from nav_pages import render_navbar

inject_theme()
render_navbar()

st.write("")
st.markdown("<div class='section-title'>About <span class='accent-word'>DisasterGuard</span></div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>An AI-powered platform for rainfall and landslide risk monitoring, built for safer communities.</div>", unsafe_allow_html=True)

top_left, top_right = st.columns([1.3, 1])
with top_left:
    st.markdown("""
        <div class="panel-card" style="margin-bottom:14px;">
            <h4>Our mission</h4>
            <p style="color:var(--muted);font-size:13.5px;line-height:1.6;">
            To reduce disaster risks and save lives by providing accurate, real-time insights
            through data and AI technology.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="panel-card">
            <h4>Key features</h4>
            <ul class="check-list">
                <li>Real-time rainfall monitoring</li>
                <li>AI-based risk prediction</li>
                <li>Interactive risk map</li>
                <li>Emergency alerts</li>
                <li>Audit logs and reporting</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with top_right:
    st.markdown("""
        <div style="border-radius:12px;overflow:hidden;border:1px solid var(--border);
             background-image: linear-gradient(180deg, rgba(6,11,10,0) 55%, rgba(6,11,10,0.85) 100%),
             url('https://picsum.photos/seed/disasterguard-valley/700/500');
             background-size:cover;background-position:center;height:280px;
             display:flex;align-items:flex-end;padding:16px;">
            <div>
                <div style="color:#fff;font-weight:700;font-size:15px;">Safer communities</div>
                <div style="color:var(--muted);font-size:12px;">Stronger tomorrow</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("<div class='panel-card'><h4>Our data processing pipeline</h4></div>", unsafe_allow_html=True)
with st.container(border=True):
    p1, a1, p2, a2, p3, a3, p4 = st.columns([2, 0.4, 2, 0.4, 2, 0.4, 2])
    steps = [
        ("1", "Collect data", "Rainfall, weather, and terrain data"),
        ("2", "Preprocess", "Clean and transform data"),
        ("3", "AI model", "Predict disaster risk using ML"),
        ("4", "Alert and notify", "Send warnings to communities"),
    ]
    for col, (num, title, desc) in zip([p1, p2, p3, p4], steps):
        with col:
            st.markdown(f"""
                <div class="pipeline-node">
                    <div class="pipeline-icon">{num}</div>
                    <h5>{title}</h5><p>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
    for col in [a1, a2, a3]:
        with col:
            st.markdown("<div class='pipeline-arrow'>→</div>", unsafe_allow_html=True)

st.write("")
st.divider()
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
        <div class='brand-row' style='font-size:15px;'><span class='brand-shield'>🛡️</span>DisasterGuard</div>
        <p style='color:var(--muted);font-size:12px;'>Predict risk. Protect lives.</p>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
        <p style='color:#fff;font-size:13px;font-weight:600;margin-bottom:6px;'>Project team</p>
        <p style='color:var(--muted);font-size:12px;margin:2px 0;'>D.L. Senanayake (Developer)</p>
        <p style='color:var(--muted);font-size:12px;margin:2px 0;'>A.S.P.U. Shanuka, U.B.P. Shamika</p>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
        <p style='color:#fff;font-size:13px;font-weight:600;margin-bottom:6px;'>Contact</p>
        <p style='color:var(--muted);font-size:12px;margin:2px 0;'>Sabaragamuwa University of Sri Lanka</p>
        <p style='color:var(--muted);font-size:12px;margin:2px 0;'>Department of Physical Sciences and Technology</p>
    """, unsafe_allow_html=True)

st.caption("© 2026 DisasterGuard. All rights reserved.")