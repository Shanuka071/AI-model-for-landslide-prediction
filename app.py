import streamlit as st
import folium
from streamlit_folium import st_folium
import sys
import os
import datetime

# Add 'src' to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from data_loader import load_and_process_data
from rl_engine import DisasterPredictor

# --- Page Config ---
st.set_page_config(page_title="DisasterGuard | Sri Lanka", layout="wide", initial_sidebar_state="expanded")

# --- Initialize System State ---
if 'assessments_logged' not in st.session_state:
    st.session_state.assessments_logged = 0
if 'critical_alerts_logged' not in st.session_state:
    st.session_state.critical_alerts_logged = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

@st.cache_resource
def init_system():
    df = load_and_process_data('ASPU DATA.xlsx')
    model = DisasterPredictor()
    flood_acc, landslide_acc = model.train(df)
    districts = df['station_name'].unique().tolist()
    return model, districts, flood_acc, landslide_acc

with st.spinner("Initializing DisasterGuard AI..."):
    model, districts, flood_acc, landslide_acc = init_system()

# --- Custom CSS for Cards ---
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; }
    .status-safe { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 8px; font-weight: bold; }
    .status-risk { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar (Environmental Controls) ---
st.sidebar.title("🌍 Environmental Controls")
st.sidebar.markdown("---")
district = st.sidebar.selectbox("District", districts)
town = st.sidebar.text_input("Town / Location Detail", "Main Town Center")
rainfall = st.sidebar.slider("Daily Rainfall (mm)", 0.0, 300.0, 79.0)
rain_3day = st.sidebar.slider("3-Day Cumulative Rainfall (mm)", 0.0, 300.0, 100.0)
rain_7day = st.sidebar.slider("7-Day Cumulative Rainfall (mm)", 0.0, 400.0, 150.0)

# --- Main UI Header ---
st.title("🌐 DisasterGuard")
st.markdown("### Sri Lanka Disaster Early Warning Platform")
st.markdown("Real-time AI telemetry for flood & landslide risk prediction across high-vulnerability districts.")

# --- Dashboard Metrics Row ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><h3>{st.session_state.assessments_logged}</h3><p>Total Assessments Logged</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>{st.session_state.critical_alerts_logged}</h3><p>Critical Alerts Logged</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>{flood_acc*100:.1f}%</h3><p>Flood Model Accuracy</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h3>{landslide_acc*100:.1f}%</h3><p>Landslide Model Accuracy</p></div>", unsafe_allow_html=True)

st.divider()

# --- Prediction ---
flood_status, landslide_status = model.predict(rainfall, rain_3day, rain_7day)

st.subheader("📊 Live Prediction & Map")

# Display Selected Parameters
st.markdown(f"**Selected District:** {district} ({town}) | **Rainfall:** {rainfall} mm | **Soil Saturation (Proxy):** {rain_3day} mm")

# Status Cards
c1, c2 = st.columns(2)
with c1:
    if "RESTRICTED" in flood_status:
        st.markdown(f"<div class='status-risk'>🌊 Flood Status: {flood_status}</div>", unsafe_allow_html=True)
        risk_flag = True
    else:
        st.markdown(f"<div class='status-safe'>🌊 Flood Status: {flood_status}</div>", unsafe_allow_html=True)
        risk_flag = False

with c2:
    if "RESTRICTED" in landslide_status:
        st.markdown(f"<div class='status-risk'>⛰️ Landslide Status: {landslide_status}</div>", unsafe_allow_html=True)
        risk_flag = True
    else:
        st.markdown(f"<div class='status-safe'>⛰️ Landslide Status: {landslide_status}</div>", unsafe_allow_html=True)

# --- Save Assessment / Audit Log ---
if st.button("📝 Save Assessment to Log"):
    st.session_state.assessments_logged += 1
    if risk_flag:
        st.session_state.critical_alerts_logged += 1
    
    log_entry = {
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "District": district,
        "Rainfall": rainfall,
        "Flood_Status": flood_status,
        "Landslide_Status": landslide_status
    }
    st.session_state.audit_log.append(log_entry)
    st.success("Assessment saved to audit log!")

st.divider()

# --- Map (Folium) ---
coords = {
    "BADULLA": [6.9934, 81.0550], "COLOMBO": [6.9271, 79.8612], 
    "GALLE": [6.0535, 80.2210], "HAMBANTOTA": [6.1246, 81.1185], 
    "NUWARA ELIYA": [6.9497, 80.7891], "RATNAPURA": [6.6828, 80.3992]
}

m = folium.Map(location=coords.get(district, [7.8731, 80.7718]), zoom_start=10)
marker_color = 'red' if risk_flag else 'green'

folium.Marker(
    coords.get(district, [7.8731, 80.7718]), 
    popup=f"{district} - Flood: {flood_status} | Landslide: {landslide_status}", 
    tooltip="Selected Location",
    icon=folium.Icon(color=marker_color)
).add_to(m)

st_folium(m, width=1000, height=400)

# --- Audit Log Archive ---
with st.expander("📁 View Audit Log Archive"):
    if st.session_state.audit_log:
        st.dataframe(st.session_state.audit_log, use_container_width=True)
    else:
        st.write("No assessments logged yet.")

st.caption("Data Source: ASPU DATA.xlsx | RL Feedback Loop Active")