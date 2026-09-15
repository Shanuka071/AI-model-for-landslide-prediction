import streamlit as st
import pandas as pd
import sys
import os

_THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS_DIR, '..'))
sys.path.append(os.path.join(_THIS_DIR, '..', 'src'))

from data_loader import load_and_process_data
from theme import inject_theme
from nav_pages import render_navbar

inject_theme()
render_navbar()

st.write("")
st.markdown("<div class='section-title'>Audit <span class='accent-word'>Logs</span></div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>View and manage system logs, risk predictions, and alerts.</div>", unsafe_allow_html=True)

if 'audit_log' in st.session_state and st.session_state.audit_log:
    df_log = pd.DataFrame(st.session_state.audit_log)

    f1, f2, f3, f4 = st.columns([1, 1, 1.4, 0.8])
    with f1:
        districts = df_log['District'].unique().tolist()
        selected_district = st.selectbox("District", ["All districts"] + districts)
    with f2:
        danger_options = df_log['Overall_Danger'].unique().tolist() if 'Overall_Danger' in df_log else []
        selected_danger = st.selectbox("Danger level", ["All levels"] + danger_options)
    with f3:
        st.date_input("Date range", value=())
    with f4:
        st.write("")
        st.write("")
        csv = df_log.to_csv(index=False).encode('utf-8')
        st.download_button("Export CSV", data=csv, file_name="disasterguard_audit_log.csv", mime="text/csv", use_container_width=True)

    df_filtered_log = df_log.copy()
    if selected_district != "All districts": df_filtered_log = df_filtered_log[df_filtered_log['District'] == selected_district]
    if selected_danger != "All levels" and 'Overall_Danger' in df_filtered_log: df_filtered_log = df_filtered_log[df_filtered_log['Overall_Danger'] == selected_danger]

    st.write("")
    high_count = df_log['Overall_Danger'].str.contains("HIGH", na=False).sum()
    mod_count = df_log['Overall_Danger'].str.contains("MODERATE", na=False).sum()
    low_count = df_log['Overall_Danger'].str.contains("LOW", na=False).sum()

    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown(f"<div class='metric-card'><div class='m-label'>Total records</div><h3>{len(df_log)}</h3></div>", unsafe_allow_html=True)
    with s2: st.markdown(f"<div class='metric-card'><div class='m-label'>High risk</div><h3 style='color:var(--danger)'>{high_count}</h3></div>", unsafe_allow_html=True)
    with s3: st.markdown(f"<div class='metric-card'><div class='m-label'>Moderate risk</div><h3 style='color:var(--warning)'>{mod_count}</h3></div>", unsafe_allow_html=True)
    with s4: st.markdown(f"<div class='metric-card'><div class='m-label'>Low risk</div><h3 style='color:var(--accent)'>{low_count}</h3></div>", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown("<div class='panel-card'><h4>Risk distribution</h4></div>", unsafe_allow_html=True)
        st.bar_chart(df_log['Overall_Danger'].value_counts(), color="#10B981")
    with c2:
        st.markdown("<div class='panel-card'><h4>Recent logs</h4></div>", unsafe_allow_html=True)
        st.dataframe(
            df_filtered_log[['Timestamp', 'District', 'Overall_Danger']].rename(
                columns={'Timestamp': 'Date & time', 'Overall_Danger': 'Risk level'}
            ).sort_values('Date & time', ascending=False),
            use_container_width=True, hide_index=True,
        )
else:
    st.info("No assessments have been logged yet. Go to the risk dashboard and click 'Predict risk' to save your first entry.")

with st.expander("Historical rainfall trends"):
    with st.spinner("Loading historical data..."):
        df_hist = load_and_process_data('ASPU DATA.xlsx')
    stations = df_hist['station_name'].unique().tolist()
    selected_station = st.selectbox("Select station", stations)
    df_filtered = df_hist[df_hist['station_name'] == selected_station].set_index('Date')
    st.line_chart(df_filtered['Rainfall_mm'], color="#10B981")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><div class='m-label'>Peak daily rainfall</div><h3>{df_filtered['Rainfall_mm'].max():.1f} mm</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><div class='m-label'>Average daily rainfall</div><h3>{df_filtered['Rainfall_mm'].mean():.1f} mm</h3></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><div class='m-label'>Total records</div><h3>{len(df_filtered)}</h3></div>", unsafe_allow_html=True)