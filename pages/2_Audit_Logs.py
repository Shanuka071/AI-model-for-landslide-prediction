import datetime
import os
import sys

import pandas as pd
import streamlit as st

_THIS = os.path.dirname(__file__)
sys.path.append(os.path.join(_THIS, '..'))
sys.path.append(os.path.join(_THIS, '..', 'src'))

from data_loader import load_and_process_data
from theme import inject_theme, html
from nav_pages import render_navbar

inject_theme()
render_navbar(active="Audit Logs")

st.session_state.setdefault("audit_log", [])

html("<div class='page-h'>Audit Logs</div>")
html("<div class='page-sub'>View and manage system logs, risk predictions and alerts.</div>")

df_log = pd.DataFrame(st.session_state.audit_log)

# =========================================================
# FILTERS
# =========================================================
with st.container(border=True):
    f1, f2, f3, f4 = st.columns([1, 1, 1.4, 0.8], vertical_alignment="bottom")

    with f1:
        district_opts = ["All Districts"] + (sorted(df_log["District"].unique().tolist()) if not df_log.empty else [])
        sel_district = st.selectbox("District", district_opts)
    with f2:
        sel_level = st.selectbox("Danger Level", ["All Levels", "High Risk", "Moderate Watch", "Low Risk"])
    with f3:
        today = datetime.date.today()
        date_range = st.date_input("Date Range", (today - datetime.timedelta(days=30), today))
    with f4:
        export_placeholder = st.empty()

# ---------------- apply filters ----------------
filtered = df_log.copy()
if not filtered.empty:
    filtered["_dt"] = pd.to_datetime(filtered["Timestamp"], errors="coerce")

    if sel_district != "All Districts":
        filtered = filtered[filtered["District"] == sel_district]
    if sel_level != "All Levels":
        filtered = filtered[filtered["Risk_Level"] == sel_level]
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["_dt"].dt.date >= start) & (filtered["_dt"].dt.date <= end)
        ]
    filtered = filtered.drop(columns=["_dt"], errors="ignore")

with export_placeholder:
    st.download_button(
        "⬇️ Export CSV",
        data=(filtered.to_csv(index=False).encode("utf-8") if not filtered.empty else b""),
        file_name="disasterguard_audit_logs.csv",
        mime="text/csv",
        disabled=filtered.empty,
        use_container_width=True,
    )

st.write("")

# =========================================================
# STAT CARDS
# =========================================================
def count_level(name):
    if filtered.empty:
        return 0
    return int((filtered["Risk_Level"] == name).sum())


stats = [
    ("📄", str(len(filtered)), "Total Records", "var(--info)"),
    ("🔺", str(count_level("High Risk")), "High Risk", "var(--danger)"),
    ("🔶", str(count_level("Moderate Watch")), "Moderate Risk", "var(--warning)"),
    ("✅", str(count_level("Low Risk")), "Low Risk", "var(--accent)"),
]
for col, (icon, val, lbl, colour) in zip(st.columns(4), stats):
    with col:
        html(f"""
        <div class='metric-card'>
        <div style='font-size:18px;color:{colour};margin-bottom:6px;'>{icon}</div>
        <div class='val'>{val}</div>
        <div class='sub'>{lbl}</div>
        </div>
        """)

st.write("")

# =========================================================
# CHART + RECENT LOGS
# =========================================================
chart_col, logs_col = st.columns([1, 1.25], gap="medium")

with chart_col:
    with st.container(border=True):
        html("<div class='sec-h'>Risk Distribution</div>")
        if filtered.empty:
            st.caption("No data yet. Save assessments from the Risk Dashboard.")
        else:
            dist = (
                filtered["Risk_Level"]
                .value_counts()
                .reindex(["High Risk", "Moderate Watch", "Low Risk"])
                .fillna(0)
                .astype(int)
            )
            st.bar_chart(dist, color="#10D9A0", height=260)

with logs_col:
    with st.container(border=True):
        html("<div class='sec-h'>Recent Logs</div>")
        if filtered.empty:
            st.caption("No log entries match these filters.")
        else:
            recent = filtered.tail(8)[::-1]
            rows = ""
            for _, r in recent.iterrows():
                lvl = r["Risk_Level"]
                pill = "pill-high" if lvl == "High Risk" else ("pill-mod" if "Moderate" in lvl else "pill-low")
                rows += (
                    f"<tr><td>{r['Timestamp']}</td><td>{str(r['District']).title()}</td>"
                    f"<td>{r['Rainfall']:.0f} mm</td>"
                    f"<td><span class='pill {pill}'>{lvl}</span></td></tr>"
                )
            html(
                "<table class='tbl'><tr><th>Date &amp; Time</th><th>District</th>"
                f"<th>Rainfall</th><th>Risk Level</th></tr>{rows}</table>"
            )

st.write("")

# =========================================================
# HISTORICAL RAINFALL
# =========================================================
with st.container(border=True):
    html("<div class='sec-h'>📈 Historical Rainfall Trends (ASPU DATA.xlsx)</div>")
    with st.spinner("Loading historical data..."):
        df_hist = load_and_process_data('ASPU DATA.xlsx')

    station = st.selectbox("Station", df_hist['station_name'].unique().tolist())
    series = df_hist[df_hist['station_name'] == station].set_index('Date')['Rainfall_mm']
    st.line_chart(series, color="#10D9A0", height=260)

    h1, h2, h3 = st.columns(3)
    for col, (v, l) in zip(
        [h1, h2, h3],
        [(f"{series.max():.1f} mm", "Peak Daily Rainfall"),
         (f"{series.mean():.1f} mm", "Average Daily Rainfall"),
         (f"{len(series)}", "Total Records")],
    ):
        with col:
            html(f"<div class='metric-card'><div class='lbl'>{l}</div><div class='val'>{v}</div></div>")

html("<div class='ftr'>© 2026 DisasterGuard · Predict Risk. Protect Lives.</div>")