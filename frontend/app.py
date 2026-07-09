import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from frontend.ui_utils import apply_custom_css
from backend import database

st.set_page_config(
    page_title="AI Safety Dashboard",
    page_icon="🪖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject massive custom CSS
apply_custom_css()

# --- TOP NAVIGATION BAR (Custom HTML) ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 30px; background-color: #101512; border-bottom: 1px solid #2A322D; margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 20px;">🪖</div>
        <div style="font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; text-transform: uppercase;">System Overview</div>
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

# --- SIDEBAR REWRITE ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
        <div style="font-size: 28px;">🪖</div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 20px; text-transform: uppercase;">Helmet AI</div>
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #7C8B85; margin-bottom: 30px; text-transform: uppercase;">Forensic Monitor Desk</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True) # Push to bottom
    st.markdown("---")
    st.markdown("### System Status")
    st.markdown("<span style='color: #39FF88; font-family: \"JetBrains Mono\", monospace; font-size: 12px;'>● YOLO MODEL LOADED</span>", unsafe_allow_html=True)
    st.markdown("<span style='color: #39FF88; font-family: \"JetBrains Mono\", monospace; font-size: 12px;'>● DB CONNECTED</span>", unsafe_allow_html=True)

# --- MAIN DASHBOARD CONTENT ---
st.markdown("<h1>Dashboard Overview</h1>", unsafe_allow_html=True)

# Fetch basic stats
history = database.get_history()
total_detections = len(history)
helmets_safe = sum(1 for item in history if item.get('status') == 'Safe')
violations_danger = sum(1 for item in history if item.get('status') == 'Danger')
avg_conf = 0
if total_detections > 0:
    total_conf = sum(item.get('confidence', 0) for item in history)
    avg_conf = total_conf / total_detections

# Summary Cards Layout
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Detections", value=total_detections)
with col2:
    st.metric(label="Safe 🟢", value=helmets_safe)
with col3:
    st.metric(label="No Helmet 🔴", value=violations_danger)
with col4:
    st.metric(label="Avg Confidence ⚡", value=f"{avg_conf*100:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# Quick Actions
st.markdown("### Quick Actions")
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin-top:0; font-size: 16px;">[01] IMAGE SCAN</h3>
        <p style="color: #7C8B85; font-size: 13px;">Upload static images for bulk compliance checking.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin-top:0; font-size: 16px;">[02] VIDEO AUDIT</h3>
        <p style="color: #7C8B85; font-size: 13px;">Process pre-recorded footage frame-by-frame.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin-top:0; font-size: 16px;">[03] LIVE MONITOR</h3>
        <p style="color: #7C8B85; font-size: 13px;">Connect to webcam for real-time site monitoring.</p>
    </div>
    """, unsafe_allow_html=True)
