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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 30px; background-color: #101512; border-bottom: 1px solid #2A322D; margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 20px;">🗄️</div>
        <div style="font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; text-transform: uppercase;">Detection Logs</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #39FF88; padding: 4px 8px; border: 1px solid rgba(57, 255, 136, 0.3); background: rgba(57, 255, 136, 0.05);">● IDLE</div>
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">THEME</span>
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">SYNC</span>
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">ALERTS</span>
        <div style="width: 28px; height: 28px; border: 1px solid #2A322D; background: #0B0D0C; color: #E8ECEA; display: flex; justify-content: center; align-items: center; font-weight: bold; font-family: 'JetBrains Mono', monospace; font-size: 12px;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("DETECTION LOGS")
st.markdown("<p style='color: #7C8B85; font-size: 14px; font-family: \"JetBrains Mono\", monospace; margin-bottom: 30px; text-transform: uppercase;'>View and manage all helmet detection records stored in Supabase.</p>", unsafe_allow_html=True)

history = database.get_history()

if not history:
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px; background: #101512; border: 1px solid #2A322D; margin-top: 40px;">
        <div style="font-size: 64px; margin-bottom: 20px;">🗄️</div>
        <h3 style="margin: 0; color: #E8ECEA;">NO SCANS LOGGED YET</h3>
        <p style="color: #7C8B85; margin-top: 10px; font-family: 'JetBrains Mono', monospace; font-size: 13px; text-transform: uppercase;">Runs from any page will appear here.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Top Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search = st.text_input("🔍 SEARCH ID")
    with col2:
        status_filter = st.selectbox("STATUS", ["All", "Safe", "Danger"])
    with col3:
        sort_order = st.selectbox("SORT", ["Newest First", "Oldest First"])
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📥 EXPORT LOG", use_container_width=True, type="secondary")

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
    df.rename(columns={"id": "ID", "created_at": "TIMESTAMP", "status": "STATUS", "confidence": "CONFIDENCE"}, inplace=True)
    df["ID"] = df["ID"].astype(str)
    
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP']).dt.tz_convert('Asia/Kolkata')
    def format_ist(dt):
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1:'st', 2:'nd', 3:'rd'}.get(day % 10, 'th')
        return f"{dt.strftime('%Y-%m-%d %H:%M:%S')} (IST)"
    df['TIMESTAMP'] = df['TIMESTAMP'].apply(format_ist)
    
    # Status badges via emojis
    df["STATUS"] = df["STATUS"].apply(lambda x: "[+] SAFE" if x == "Safe" else "[!] DANGER")
    df["CONFIDENCE"] = df["CONFIDENCE"] * 100 # Convert to percentage for progress bar

    # Display Modern Table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "TIMESTAMP": st.column_config.TextColumn("TIMESTAMP", width="medium"),
            "STATUS": st.column_config.TextColumn("STATUS", width="small"),
            "CONFIDENCE": st.column_config.NumberColumn("CONFIDENCE (%)", help="AI Prediction Confidence", format="%.1f%%")
        }
    )
