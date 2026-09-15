import streamlit as st
import folium
from streamlit_folium import st_folium
import sys
import os
import datetime
import requests

_THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS_DIR, '..'))
sys.path.append(os.path.join(_THIS_DIR, '..', 'src'))

from data_loader import load_and_process_data
from rl_engine import DisasterPredictor
from theme import inject_theme
from nav_pages import render_navbar

inject_theme()
render_navbar()

if 'assessments_logged' not in st.session_state: st.session_state.assessments_logged = 0
if 'critical_alerts_logged' not in st.session_state: st.session_state.critical_alerts_logged = 0
if 'audit_log' not in st.session_state: st.session_state.audit_log = []

@st.cache_resource
def init_system():
    df = load_and_process_data('ASPU DATA.xlsx')
    model = DisasterPredictor()
    flood_acc, landslide_acc = model.train(df)
    districts = df['station_name'].unique().tolist()
    return model, districts, flood_acc, landslide_acc

with st.spinner("Initializing AI engine..."):
    model, districts, flood_acc, landslide_acc = init_system()

COORDS = {
    "BADULLA": [6.9934, 81.0550], "COLOMBO": [6.9271, 79.8612],
    "GALLE": [6.0535, 80.2210], "HAMBANTOTA": [6.1246, 81.1185],
    "NUWARA ELIYA": [6.9497, 80.7891], "RATNAPURA": [6.6828, 80.3992],
}

@st.cache_data(ttl=600)
def fetch_weather(lat, lon):
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True,
                    "hourly": "relative_humidity_2m", "timezone": "auto"},
            timeout=5,
        )
        data = r.json()
        temp = data["current_weather"]["temperature"]
        code = data["current_weather"]["weathercode"]
        hum = data["hourly"]["relative_humidity_2m"][0]
        return temp, code, hum
    except Exception:
        return None, None, None

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 51: "Light drizzle", 61: "Light rain", 63: "Rain",
    65: "Heavy rain", 80: "Rain showers", 95: "Thunderstorm",
}

def compute_overall_danger(model_flag, soil_pct, slope_deg):
    score = 0
    if model_flag: score += 2
    if soil_pct >= 75: score += 2
    elif soil_pct >= 50: score += 1
    if slope_deg >= 30: score += 2
    elif slope_deg >= 15: score += 1
    if score >= 4: return "HIGH RISK", "high", "High rainfall and steep slope detected. Be prepared for possible landslides."
    elif score >= 2: return "MODERATE RISK", "moderate", "Conditions are elevated. Continue monitoring rainfall and soil saturation."
    else: return "LOW RISK", "low", "Conditions are stable across the monitored parameters."

st.write("")
st.markdown("<div class='section-title'>Risk <span class='accent-word'>Dashboard</span></div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Real-time AI telemetry for flood and landslide risk prediction.</div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.6])

with left_col:
    st.markdown("<div class='panel-card'><h4>Input parameters</h4></div>", unsafe_allow_html=True)
    with st.container(border=True):
        district = st.selectbox("District", districts)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 79.0)
        rain_3day = st.number_input("3-day rainfall (mm)", 0.0, 400.0, 100.0)
        rain_7day = st.number_input("7-day rainfall (mm)", 0.0, 500.0, 150.0)
        soil_saturation = st.number_input("Soil saturation (%)", 0.0, 100.0, 45.0)
        slope_angle = st.number_input("Slope angle (°)", 0.0, 60.0, 15.0)
        predict_clicked = st.button("Predict risk", use_container_width=True)

    flood_status, landslide_status = model.predict(rainfall, rain_3day, rain_7day)
    model_risk_flag = "RESTRICTED" in flood_status or "RESTRICTED" in landslide_status
    overall_label, overall_css, overall_desc = compute_overall_danger(model_risk_flag, soil_saturation, slope_angle)

    st.markdown(f"""
        <div class="danger-banner danger-{overall_css}">
            Overall danger indicator — {overall_label}
            <div class="db-sub">{overall_desc}</div>
        </div>
    """, unsafe_allow_html=True)

    if predict_clicked:
        st.session_state.assessments_logged += 1
        if model_risk_flag or overall_css == "high":
            st.session_state.critical_alerts_logged += 1
        st.session_state.audit_log.append({
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "District": district, "Rainfall": rainfall, "Rain_3Day": rain_3day,
            "Rain_7Day": rain_7day, "Soil_Saturation_%": soil_saturation,
            "Slope_Angle_deg": slope_angle, "Flood_Status": flood_status,
            "Landslide_Status": landslide_status, "Overall_Danger": overall_label,
        })
        st.rerun()

with right_col:
    m1, m2, m3, m4 = st.columns(4)
    pill_class = {"high": "high", "moderate": "moderate", "low": "low"}[overall_css]
    with m1:
        st.markdown(f"""<div class="metric-card"><div class="m-label">Predicted risk level</div>
        <span class="risk-pill {pill_class}">{overall_label.split()[0].title()}</span>
        <div class="m-sub">Probability estimate</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card"><div class="m-label">Rainfall (mm)</div>
        <h3>{rainfall:.0f}</h3><div class="m-sub {'up' if rainfall > 100 else 'ok'}">Current</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card"><div class="m-label">Soil saturation (%)</div>
        <h3>{soil_saturation:.0f}</h3><div class="m-sub {'up' if soil_saturation >= 75 else 'ok'}">{'High' if soil_saturation >= 75 else 'Normal'}</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card"><div class="m-label">Slope angle (°)</div>
        <h3>{slope_angle:.0f}</h3><div class="m-sub {'up' if slope_angle >= 30 else 'ok'}">{'Steep' if slope_angle >= 30 else 'Moderate'}</div></div>""", unsafe_allow_html=True)

    st.write("")
    center = COORDS.get(district, [7.8731, 80.7718])
    m = folium.Map(location=center, zoom_start=10, tiles="CartoDB dark_matter")
    marker_color = "red" if overall_css == "high" else ("orange" if overall_css == "moderate" else "green")
    folium.Marker(center, popup=f"{district} — {overall_label}", tooltip=district,
                  icon=folium.Icon(color=marker_color)).add_to(m)
    hazard_hex = {"high": "#EF4444", "moderate": "#F5A524", "low": "#10B981"}[overall_css]
    folium.Circle(center, radius=6000, color=hazard_hex, fill=True, fill_opacity=0.15).add_to(m)
    evac_target = COORDS["COLOMBO"] if district != "COLOMBO" else COORDS["RATNAPURA"]
    folium.PolyLine([center, evac_target], color="#EAF2EF", weight=2.5, dash_array="8,6").add_to(m)
    folium.Marker(evac_target, tooltip="Safe zone", icon=folium.Icon(color="green", icon="flag")).add_to(m)
    st_folium(m, width=None, height=380, use_container_width=True)

    st.markdown("""
        <div class="legend-row"><span class="legend-dot" style="background:#EF4444"></span>High risk zone
        &nbsp;&nbsp;<span class="legend-dot" style="background:#F5A524"></span>Moderate risk zone
        &nbsp;&nbsp;<span class="legend-dot" style="background:#10B981"></span>Safe zone
        &nbsp;&nbsp;— &nbsp;Evacuation route</div>
    """, unsafe_allow_html=True)

    st.write("")
    t1, t2 = st.columns([1.5, 1])
    with t1:
        st.markdown("<div class='panel-card'><h4>Recent prediction</h4></div>", unsafe_allow_html=True)
        if st.session_state.audit_log:
            last = st.session_state.audit_log[-1]
            st.dataframe(
                {"Date & time": [last["Timestamp"]], "District": [last["District"]],
                 "Risk level": [last["Overall_Danger"]]},
                use_container_width=True, hide_index=True,
            )
        else:
            st.caption("No predictions logged yet — use the panel on the left.")
    with t2:
        st.markdown("<div class='panel-card'><h4>Current weather</h4></div>", unsafe_allow_html=True)
        temp, code, hum = fetch_weather(center[0], center[1])
        if temp is not None:
            st.markdown(f"""
                <div style='font-size:20px;font-weight:700;color:#fff;'>{temp:.0f}°C</div>
                <div style='color:var(--muted);font-size:12.5px;'>{WEATHER_CODES.get(code, 'Mixed conditions')}</div>
                <div style='color:var(--muted);font-size:12.5px;'>Humidity: {hum:.0f}%</div>
            """, unsafe_allow_html=True)
            st.caption("Live data via Open-Meteo")
        else:
            st.caption("Weather feed unavailable — check network settings.")