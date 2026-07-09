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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="font-size: 20px; font-weight: 600; font-family: 'Poppins', sans-serif;">📜 Detection History</div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🌙</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔄</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔔</span>
        <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; display: flex; justify-content: center; align-items: center; font-weight: bold;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Detection History")
st.markdown("<p style='color: #94A3B8; font-size: 16px;'>View and manage all helmet detection records stored in Supabase.</p>", unsafe_allow_html=True)

history = database.get_history()

if not history:
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px; background: #1E293B; border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1); margin-top: 40px;">
        <div style="font-size: 64px; margin-bottom: 20px;">📂</div>
        <h3 style="margin: 0; color: #F8FAFC;">No Detection History Found</h3>
        <p style="color: #94A3B8; margin-top: 10px;">Your database is currently empty. Start a detection to see records here.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Top Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search = st.text_input("🔍 Search IDs")
    with col2:
        status_filter = st.selectbox("Status", ["All", "Safe", "Danger"])
    with col3:
        sort_order = st.selectbox("Sort By", ["Newest First", "Oldest First"])
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📥 Export CSV", use_container_width=True, type="secondary")

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
        return f"{day}{suffix} {dt.strftime('%b %Y, %I:%M %p')}"
    df['Timestamp'] = df['Timestamp'].apply(format_ist)
    
    # Status badges via emojis
    df["Status"] = df["Status"].apply(lambda x: "🟢 Safe" if x == "Safe" else "🔴 Danger")
    df["Confidence"] = df["Confidence"] * 100 # Convert to percentage for progress bar

    # Display Modern Table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "Timestamp": st.column_config.TextColumn("Date & Time", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Confidence": st.column_config.ProgressColumn("Confidence Score", help="AI Prediction Confidence", format="%.1f%%", min_value=0, max_value=100)
        }
    )
