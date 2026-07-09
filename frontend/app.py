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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="font-size: 20px; font-weight: 600; font-family: 'Poppins', sans-serif;">🏠 Dashboard</div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🌙</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔄</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔔</span>
        <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; display: flex; justify-content: center; align-items: center; font-weight: bold;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR REWRITE ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
        <div style="font-size: 28px;">🪖</div>
        <div style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 20px;">Helmet AI</div>
    </div>
    <div style="font-size: 12px; color: #94A3B8; margin-bottom: 30px;">AI Safety Monitoring System</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True) # Push to bottom
    st.markdown("---")
    st.markdown("### System Status")
    st.markdown("🟢 **YOLO Model Loaded**")
    st.markdown("🟢 **Supabase Connected**")

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
    <div style="background: #1E293B; padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
        <h3 style="margin-top:0; font-size: 18px;">📷 Image Scan</h3>
        <p style="color: #94A3B8; font-size: 14px;">Upload static images for bulk compliance checking.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol2:
    st.markdown("""
    <div style="background: #1E293B; padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
        <h3 style="margin-top:0; font-size: 18px;">🎥 Video Audit</h3>
        <p style="color: #94A3B8; font-size: 14px;">Process pre-recorded footage frame-by-frame.</p>
    </div>
    """, unsafe_allow_html=True)
with fcol3:
    st.markdown("""
    <div style="background: #1E293B; padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
        <h3 style="margin-top:0; font-size: 18px;">🔴 Live Monitor</h3>
        <p style="color: #94A3B8; font-size: 14px;">Connect to webcam for real-time site monitoring.</p>
    </div>
    """, unsafe_allow_html=True)
