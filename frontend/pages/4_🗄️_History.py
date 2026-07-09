import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import pandas as pd
from backend import database
from frontend.ui_utils import apply_custom_css

st.set_page_config(page_title="Detection History", page_icon="🗄️", layout="wide")
apply_custom_css()

# --- TOP NAVIGATION BAR ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background-color: var(--bg-panel); border-bottom: 1px solid var(--border-panel); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 24px;">🗄️</span>
        <div class="header-title">00:04 HISTORY</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="header-status-badge status-idle">● IDLE</div>
        <button class="header-btn">THEME</button>
        <button class="header-btn">SYNC</button>
        <button class="header-btn">ALERTS</button>
        <div class="user-badge">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>DETECTION LOGS</h3>", unsafe_allow_html=True)
st.markdown("<p class='mono-text' style='color: var(--text-secondary); font-size: 14px; margin-bottom: 30px;'>Review archived scan records from the database.</p>", unsafe_allow_html=True)

history = database.get_history()

if not history:
    st.markdown("""
    <div class="forensic-card mono-text" style="text-align: center; color: var(--text-secondary); padding: 40px; margin-top: 20px;">
        [ NO SCANS LOGGED YET. RUNS FROM ANY PAGE WILL APPEAR HERE. ]
    </div>
    """, unsafe_allow_html=True)
else:
    # Top Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search = st.text_input("SEARCH ID", placeholder="Enter ID...")
    with col2:
        status_filter = st.selectbox("FILTER STATUS", ["All", "Safe", "Danger"])
    with col3:
        sort_order = st.selectbox("SORT ORDER", ["Newest First", "Oldest First"])
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("EXPORT LOGS", use_container_width=True, type="secondary")

    # Prepare Data
    df = pd.DataFrame(history)
    df = df[["id", "created_at", "status", "confidence"]]
    
    # Filtering
    if status_filter != "All":
        df = df[df["status"] == status_filter]
    if search:
        df = df[df["id"].astype(str).str.contains(search)]
        
    # Sorting
    df = df.sort_values(by="created_at", ascending=(sort_order == "Oldest First"))

    # Formatting
    df.rename(columns={"id": "ID", "created_at": "Timestamp", "status": "Status", "confidence": "Confidence"}, inplace=True)
    df["ID"] = df["ID"].astype(str)
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.tz_convert('Asia/Kolkata')
    def format_ist(dt):
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1:'st', 2:'nd', 3:'rd'}.get(day % 10, 'th')
        return f"{dt.strftime('%Y-%m-%d')} | {dt.strftime('%H:%M:%S')}"
    df['Timestamp'] = df['Timestamp'].apply(format_ist)
    
    # Status badges
    df["Status"] = df["Status"].apply(lambda x: "🟢 COMPLIANT" if x == "Safe" else "🔴 FLAGGED")
    df["Confidence"] = df["Confidence"] * 100 # Convert to percentage for progress bar

    # Display Modern Table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("RECORD ID", width="small"),
            "Timestamp": st.column_config.TextColumn("TIMESTAMP (IST)", width="medium"),
            "Status": st.column_config.TextColumn("STATUS", width="small"),
            "Confidence": st.column_config.ProgressColumn("CONFIDENCE", help="AI Prediction Confidence", format="%.1f%%", min_value=0, max_value=100)
        }
    )
