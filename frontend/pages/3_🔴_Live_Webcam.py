import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from backend import utils
from backend.detector import HelmetDetector
import time

st.set_page_config(page_title="Live Webcam", page_icon="🔴", layout="wide")

from frontend.ui_utils import apply_custom_css
apply_custom_css()

# --- TOP NAVIGATION BAR ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="font-size: 20px; font-weight: 600; font-family: 'Poppins', sans-serif;">🔴 Live Monitor</div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🌙</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔄</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔔</span>
        <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; display: flex; justify-content: center; align-items: center; font-weight: bold;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Live Camera Feed")
st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 30px;'>Real-time AI monitoring utilizing your browser's webcam feed.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

if "run_camera" not in st.session_state:
    st.session_state.run_camera = False
if "last_db_log_time" not in st.session_state:
    st.session_state.last_db_log_time = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Camera", use_container_width=True, type="primary"):
        st.session_state.run_camera = True
with col2:
    if st.button("⏹ Stop Camera", use_container_width=True, type="secondary"):
        st.session_state.run_camera = False

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.run_camera:
    col_cam, col_analytics = st.columns([2, 1])
    
    with col_cam:
        st.markdown("### Live Stream")
        camera_frame = st.camera_input(label="Webcam", label_visibility="collapsed")
        result_placeholder = st.empty()
        
    with col_analytics:
        st.markdown("### Realtime Analytics")
        stat_helmets = st.empty()
        stat_danger = st.empty()
        stat_fps = st.empty()
        stats_placeholder = st.empty()

    if camera_frame is not None:
        start_time = time.time()
        file_bytes = np.asarray(bytearray(camera_frame.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        results = detector.detect(frame)

        current_time = time.time()
        log_to_db = False
        if current_time - st.session_state.last_db_log_time > 5:
            log_to_db = True
            st.session_state.last_db_log_time = current_time

        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=log_to_db)
        fps = 1.0 / (time.time() - start_time)

        annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        result_placeholder.image(annotated_rgb, use_container_width=True)

        helmets = stats.get("helmet_count", 0)
        no_helmets = stats.get("no_helmet_count", 0)
        
        stat_helmets.metric("Helmets Detected", helmets)
        stat_danger.metric("No Helmet", no_helmets)
        stat_fps.metric("Processing Speed", f"{fps:.1f} FPS")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if no_helmets > 0:
            stats_placeholder.error(f"🚨 **DANGER**\n{no_helmets} person(s) without helmet detected!")
        elif helmets > 0:
            stats_placeholder.success(f"✅ **SAFE**\n{helmets} person(s) wearing helmets.")
        else:
            stats_placeholder.info("🔍 No persons detected in this frame.")
else:
    st.markdown("""
        <div style='text-align: center; padding: 60px; background: #1E293B; border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);'>
            <div style="font-size: 64px; margin-bottom: 20px;">📷</div>
            <h3 style="color: #F8FAFC;">Camera is stopped</h3>
            <p style="color: #94A3B8;">Click <strong>Start Camera</strong> to begin live detection.</p>
        </div>
    """, unsafe_allow_html=True)
