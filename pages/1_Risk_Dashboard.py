import datetime
import os
import sys

import folium
import streamlit as st
from streamlit_folium import st_folium

_THIS = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS, '..'))
sys.path.append(os.path.join(_THIS, '..', 'src'))

from data_loader import load_and_process_data
from rl_engine import DisasterPredictor
from theme import inject_theme, html
from nav_pages import render_navbar

inject_theme()
render_navbar(active="Risk Dashboard")

# ---------------- session state ----------------
st.session_state.setdefault("audit_log", [])
st.session_state.setdefault("assessments_logged", 0)
st.session_state.setdefault("critical_alerts_logged", 0)

DISTRICT_COORDS = {
    "BADULLA": [6.9934, 81.0550], "COLOMBO": [6.9271, 79.8612],
    "GALLE": [6.0535, 80.2210], "HAMBANTOTA": [6.1246, 81.1185],
    "NUWARA ELIYA": [6.9497, 80.7891], "RATNAPURA": [6.6828, 80.3992],
}


@st.cache_resource
def init_system():
    df = load_and_process_data('ASPU DATA.xlsx')
    model = DisasterPredictor()
    flood_acc, landslide_acc = model.train(df)
    return model, df['station_name'].unique().tolist(), flood_acc, landslide_acc


with st.spinner("Initializing AI engine..."):
    model, districts, flood_acc, landslide_acc = init_system()


def overall_danger(model_flag, soil, slope):
    score = 2 if model_flag else 0
    score += 2 if soil >= 75 else (1 if soil >= 50 else 0)
    score += 2 if slope >= 30 else (1 if slope >= 15 else 0)
    if score >= 4:
        return "High Risk", "alert-high", "pill-high", "#FF5A6E", min(0.55 + score * 0.06, 0.97)
    if score >= 2:
        return "Moderate Watch", "alert-mod", "pill-mod", "#FFB020", 0.40 + score * 0.05
    return "Low Risk", "alert-low", "pill-low", "#10D9A0", 0.18 + score * 0.05


# =========================================================
# LAYOUT: left input panel | right analytics
# =========================================================
left, right = st.columns([1, 2.45], gap="medium")

# ---------------- INPUT PARAMETERS ----------------
with left:
    with st.container(border=True):
        html("<div class='sec-h'>⚙️ Input Parameters</div>")
        district = st.selectbox("District", districts)
        town = st.text_input("Town / Location", "Main Town Center")
        rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 128.0, step=1.0)
        rain_3day = st.number_input("3-Day Rainfall (mm)", 0.0, 300.0, 220.0, step=1.0)
        rain_7day = st.number_input("7-Day Rainfall (mm)", 0.0, 400.0, 280.0, step=1.0)
        soil = st.slider("Soil Saturation (%)", 0.0, 100.0, 78.0)
        slope = st.slider("Slope Angle (°)", 0.0, 60.0, 32.0)
        predict_clicked = st.button("⚡ Predict Risk")

    # ---- prediction (your trained model, unchanged signature) ----
    flood_status, landslide_status = model.predict(rainfall, rain_3day, rain_7day)
    model_flag = "RESTRICTED" in flood_status or "RESTRICTED" in landslide_status
    label, alert_cls, pill_cls, colour, prob = overall_danger(model_flag, soil, slope)

    st.write("")
    icon = "🔺" if alert_cls == "alert-high" else ("🔶" if alert_cls == "alert-mod" else "✅")
    detail = {
        "alert-high": "High rainfall and steep slope detected. Be prepared for possible landslides.",
        "alert-mod": "Conditions are elevated. Continue monitoring rainfall and soil saturation.",
        "alert-low": "Conditions are stable. No immediate action required.",
    }[alert_cls]
    html(f"""
    <div class="alert-box {alert_cls}">
    <div class='lbl' style='color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.5px;'>Overall Danger Indicator</div>
    <div class="t">{icon} {label}</div>
    <div class="d">{detail}</div>
    </div>
    """)

    st.write("")
    if st.button("📝 Save Assessment to Log"):
        st.session_state.assessments_logged += 1
        if alert_cls == "alert-high":
            st.session_state.critical_alerts_logged += 1
        st.session_state.audit_log.append({
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "District": district, "Town": town,
            "Rainfall": rainfall, "Rain_3Day": rain_3day, "Rain_7Day": rain_7day,
            "Soil_Saturation_%": soil, "Slope_Angle_deg": slope,
            "Flood_Status": flood_status, "Landslide_Status": landslide_status,
            "Risk_Level": label,
        })
        st.success("Assessment saved.")
        st.rerun()

# ---------------- ANALYTICS ----------------
with right:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        html(f"""
        <div class='metric-card'>
        <div class='lbl'>Predicted Risk Level</div>
        <span class='pill {pill_cls}'>{label}</span>
        <div class='sub'>Probability: {prob*100:.0f}%</div>
        </div>
        """)
    with m2:
        html(f"""
        <div class='metric-card'><div class='lbl'>Rainfall (mm)</div>
        <div class='val'>{rainfall:.0f}</div><div class='sub'>Current daily</div></div>
        """)
    with m3:
        html(f"""
        <div class='metric-card'><div class='lbl'>Soil Saturation (%)</div>
        <div class='val'>{soil:.0f}</div><div class='sub'>{'High' if soil>=70 else 'Normal'}</div></div>
        """)
    with m4:
        html(f"""
        <div class='metric-card'><div class='lbl'>Slope Angle (°)</div>
        <div class='val'>{slope:.0f}</div><div class='sub'>{'Steep' if slope>=30 else 'Moderate'}</div></div>
        """)

    st.write("")
    map_col, legend_col = st.columns([3, 1], gap="small")

    with map_col:
        center = DISTRICT_COORDS.get(district, [7.8731, 80.7718])
        fmap = folium.Map(location=center, zoom_start=10, tiles="CartoDB dark_matter")

        folium.Circle(center, radius=7000, color=colour, fill=True, fill_opacity=0.28,
                      weight=2, tooltip=f"{district} — {label}").add_to(fmap)
        folium.Marker(center, tooltip=f"{district} ({town})",
                      popup=f"Flood: {flood_status} | Landslide: {landslide_status}",
                      icon=folium.Icon(color='red' if alert_cls == 'alert-high' else
                                       ('orange' if alert_cls == 'alert-mod' else 'green'))).add_to(fmap)

        # neighbouring districts as context zones
        for name, coord in DISTRICT_COORDS.items():
            if name == district:
                continue
            folium.CircleMarker(coord, radius=6, color="#3B9EFF", fill=True,
                                fill_opacity=0.7, tooltip=name).add_to(fmap)

        # evacuation route toward the nearest safe hub
        hub = DISTRICT_COORDS["COLOMBO"] if district != "COLOMBO" else DISTRICT_COORDS["GALLE"]
        folium.PolyLine([center, hub], color="#FFFFFF", weight=2.5, dash_array="7,7",
                        tooltip="Evacuation route").add_to(fmap)
        folium.Marker(hub, tooltip="Safe Zone",
                      icon=folium.Icon(color="green", icon="flag")).add_to(fmap)

        st_folium(fmap, height=340, use_container_width=True)

    with legend_col:
        with st.container(border=True):
            html("""
            <div class='sec-h'>Legend</div>
            <div class='legend-row'><span class='legend-dot' style='background:#FF5A6E'></span>High Risk Zone</div>
            <div class='legend-row'><span class='legend-dot' style='background:#FFB020'></span>Moderate Risk</div>
            <div class='legend-row'><span class='legend-dot' style='background:#10D9A0'></span>Safe Zone</div>
            <div class='legend-row'><span class='legend-dot' style='background:#3B9EFF'></span>Other Stations</div>
            <div class='legend-row'><span class='legend-dot' style='background:#FFFFFF'></span>Evacuation Route</div>
            """)

    st.write("")
    rec_col, wx_col = st.columns([2.1, 1], gap="small")

    with rec_col:
        with st.container(border=True):
            html("<div class='sec-h'>Recent Predictions</div>")
            log = st.session_state.audit_log[-5:][::-1]
            if log:
                rows = "".join(
                    f"<tr><td>{r['Timestamp']}</td><td>{r['District'].title()}</td>"
                    f"<td><span class='pill {'pill-high' if r['Risk_Level']=='High Risk' else ('pill-mod' if 'Moderate' in r['Risk_Level'] else 'pill-low')}'>{r['Risk_Level']}</span></td></tr>"
                    for r in log
                )
                html(f"<table class='tbl'><tr><th>Date &amp; Time</th><th>District</th><th>Risk Level</th></tr>{rows}</table>")
            else:
                st.caption("No predictions saved yet — use **Save Assessment to Log**.")

    with wx_col:
        with st.container(border=True):
            condition = "Heavy Rain" if rainfall >= 100 else ("Light Rain" if rainfall >= 20 else "Cloudy")
            wicon = "🌧️" if rainfall >= 100 else ("🌦️" if rainfall >= 20 else "☁️")
            humidity = min(60 + soil * 0.35, 99)
            html(f"""
            <div class='sec-h'>Current Weather</div>
            <div style='font-size:34px;line-height:1;'>{wicon}</div>
            <div style='color:#fff;font-weight:700;margin-top:8px;'>{condition}</div>
            <div style='color:var(--muted);font-size:13px;margin-top:6px;'>
            {district.title()}<br>Humidity: {humidity:.0f}%<br>Rainfall: {rainfall:.0f} mm
            </div>
            """)

    st.write("")
    a1, a2, a3, a4 = st.columns(4)
    for col, (v, l) in zip(
        [a1, a2, a3, a4],
        [(str(st.session_state.assessments_logged), "Assessments Logged"),
         (str(st.session_state.critical_alerts_logged), "Critical Alerts"),
         (f"{flood_acc*100:.1f}%", "Flood Model Accuracy"),
         (f"{landslide_acc*100:.1f}%", "Landslide Model Accuracy")],
    ):
        with col:
            html(f"<div class='metric-card'><div class='lbl'>{l}</div><div class='val'>{v}</div></div>")

html("<div class='ftr'>© 2026 DisasterGuard · Predict Risk. Protect Lives.</div>")