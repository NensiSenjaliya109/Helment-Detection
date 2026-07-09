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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background-color: var(--bg-panel); border-bottom: 1px solid var(--border-panel); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 24px;">🪖</span>
        <div class="header-title">SYSTEM DASHBOARD</div>
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

# --- SIDEBAR REWRITE ---
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <div class="header-title" style="font-size: 18px; margin-bottom: 5px;">HELMET AI</div>
        <div class="mono-text" style="font-size: 11px; color: var(--text-secondary); letter-spacing: 1px;">FORENSIC MONITORING SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True) # Push to bottom
    st.markdown("---")
    st.markdown("### SYSTEM DIAGNOSTICS", unsafe_allow_html=True)
    st.markdown("<div class='mono-text' style='font-size: 12px;'><span style='color: var(--accent-green)'>[OK]</span> YOLO CORE LOADED</div>", unsafe_allow_html=True)
    st.markdown("<div class='mono-text' style='font-size: 12px;'><span style='color: var(--accent-green)'>[OK]</span> DB CONNECTION ESTABLISHED</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD CONTENT ---
st.markdown("<h3>DASHBOARD OVERVIEW</h3>", unsafe_allow_html=True)

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
    st.metric(label="TOTAL SCANS", value=f"{total_detections:04d}")
with col2:
    st.metric(label="COMPLIANT (SAFE)", value=f"{helmets_safe:04d}")
with col3:
    st.metric(label="FLAGGED (DANGER)", value=f"{violations_danger:04d}")
with col4:
    st.metric(label="AVG CONFIDENCE", value=f"{avg_conf*100:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# Quick Actions
st.markdown("<h3>MODULE QUICK START</h3>", unsafe_allow_html=True)
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.markdown("""
    <div class="forensic-card">
        <h4 style="margin-top:0; font-size: 14px;">[01] IMAGE SCAN</h4>
        <p class="mono-text" style="color: var(--text-secondary); font-size: 12px; margin-bottom: 0;">Upload static images for bulk forensic compliance checking.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol2:
    st.markdown("""
    <div class="forensic-card">
        <h4 style="margin-top:0; font-size: 14px;">[02] VIDEO AUDIT</h4>
        <p class="mono-text" style="color: var(--text-secondary); font-size: 12px; margin-bottom: 0;">Process pre-recorded footage frame-by-frame through model.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol3:
    st.markdown("""
    <div class="forensic-card">
        <h4 style="margin-top:0; font-size: 14px;">[03] LIVE MONITOR</h4>
        <p class="mono-text" style="color: var(--text-secondary); font-size: 12px; margin-bottom: 0;">Connect to webcam for real-time live site monitoring.</p>
    </div>
    """, unsafe_allow_html=True)
