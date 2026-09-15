import streamlit as st

from theme import inject_theme
from nav_pages import render_navbar

inject_theme()
render_navbar()

st.write("")

# =========================================================
# HERO — photo background, radar illustration, feature strip
# =========================================================
with st.container(border=True, key="hero_container"):
    hero_left, hero_right = st.columns([1.2, 1])

    with hero_left:
        st.markdown(
            "<div class='hero-title'>Predict risk.<span class='accent-line'>Protect lives.</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='hero-sub'>DisasterGuard is an AI-powered platform for monitoring "
            "rainfall and landslide risk, helping communities prepare and stay safe.</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        b1, b2 = st.columns([1, 1])
        with b1:
            st.page_link("pages/1_Risk_Dashboard.py", label="View risk dashboard", use_container_width=True)
        with b2:
            st.page_link("pages/3_About.py", label="Learn more", use_container_width=True)

    with hero_right:
        # Stylised Sri Lanka silhouette (not a precise map) with the six
        # monitoring stations placed at their approximate relative positions,
        # and a radar sweep rotating around it.
        STATION_POINTS = {
            "Colombo": (65, 108, "#F5A524"),
            "Ratnapura": (85, 165, "#EF4444"),
            "Galle": (75, 205, "#10B981"),
            "Hambantota": (112, 215, "#F5A524"),
            "Nuwara Eliya": (95, 143, "#10B981"),
            "Badulla": (117, 152, "#10B981"),
        }
        dots_svg = ""
        for i, (name, (x, y, color)) in enumerate(STATION_POINTS.items()):
            dots_svg += (
                f'<circle class="radar-dot-svg" cx="{x}" cy="{y}" r="4.5" fill="{color}" '
                f'style="animation-delay:{i * 0.3:.1f}s"><title>{name}</title></circle>'
            )

        st.markdown(f"""
            <div class="radar-wrap">
                <svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100,15 C130,12 150,35 155,70 C160,110 150,150 135,180
                             C120,205 110,220 100,232 C90,220 78,203 63,178
                             C48,150 40,110 45,72 C50,35 70,12 100,15 Z"
                          fill="rgba(16,185,129,0.10)" stroke="rgba(16,185,129,0.55)" stroke-width="1.6"/>
                    <circle cx="100" cy="120" r="105" fill="none" stroke="rgba(16,185,129,0.22)" stroke-width="1"/>
                    <circle cx="100" cy="120" r="75" fill="none" stroke="rgba(16,185,129,0.22)" stroke-width="1"/>
                    <circle cx="100" cy="120" r="45" fill="none" stroke="rgba(16,185,129,0.3)" stroke-width="1"/>
                    <circle cx="100" cy="120" r="16" fill="rgba(16,185,129,0.18)"/>
                    <path d="M100,120 L100,15 A105,105 0 0 1 190,90 Z" fill="rgba(16,185,129,0.32)">
                        <animateTransform attributeName="transform" type="rotate"
                                           from="0 100 120" to="360 100 120" dur="4s" repeatCount="indefinite"/>
                    </path>
                    {dots_svg}
                </svg>
            </div>
        """, unsafe_allow_html=True)
        st.caption("Six monitoring stations across the island feeding live telemetry.")

    st.write("")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("""
            <div class="feature-card"><div class="feature-icon">⏱</div>
            <h3>Real-time monitoring</h3><p>Track rainfall and weather data in real time.</p></div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
            <div class="feature-card"><div class="feature-icon">◈</div>
            <h3>AI prediction</h3><p>Accurate risk prediction using machine learning.</p></div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
            <div class="feature-card"><div class="feature-icon">🔔</div>
            <h3>Risk alerts</h3><p>Get instant alerts for high-risk areas.</p></div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown("""
            <div class="feature-card"><div class="feature-icon">🛡</div>
            <h3>Safer communities</h3><p>Support early preparedness and response.</p></div>
        """, unsafe_allow_html=True)

st.write("")
st.divider()
st.caption("© 2026 DisasterGuard — Department of Physical Sciences and Technology, Sabaragamuwa University")