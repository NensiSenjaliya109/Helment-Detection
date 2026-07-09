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

if "run_camera" not in st.session_state:
    st.session_state.run_camera = False
if "last_db_log_time" not in st.session_state:
    st.session_state.last_db_log_time = 0

status_badge = "<div style=\"font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #E14B4B; padding: 4px 8px; border: 1px solid rgba(225, 75, 75, 0.3); background: rgba(225, 75, 75, 0.05); animation: livePulse 2s infinite;\">● LIVE</div>" if st.session_state.run_camera else "<div style=\"font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #39FF88; padding: 4px 8px; border: 1px solid rgba(57, 255, 136, 0.3); background: rgba(57, 255, 136, 0.05);\">● IDLE</div>"

# --- TOP NAVIGATION BAR ---
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 30px; background-color: #101512; border-bottom: 1px solid #2A322D; margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 20px;">🔴</div>
        <div style="font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; text-transform: uppercase;">Live Monitor</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        {status_badge}
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">THEME</span>
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">SYNC</span>
        <span style="cursor: pointer; padding: 6px 12px; border: 1px solid #2A322D; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;">ALERTS</span>
        <div style="width: 28px; height: 28px; border: 1px solid #2A322D; background: #0B0D0C; color: #E8ECEA; display: flex; justify-content: center; align-items: center; font-weight: bold; font-family: 'JetBrains Mono', monospace; font-size: 12px;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("LIVE CAMERA FEED")
st.markdown("<p style='color: #7C8B85; font-size: 14px; font-family: \"JetBrains Mono\", monospace; margin-bottom: 30px; text-transform: uppercase;'>Real-time AI monitoring utilizing your browser's webcam feed.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ START CAMERA", use_container_width=True, type="primary"):
        st.session_state.run_camera = True
        st.rerun()
with col2:
    if st.button("⏹ STOP CAMERA", use_container_width=True, type="secondary"):
        st.session_state.run_camera = False
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.run_camera:
    col_cam, col_analytics = st.columns([2, 1])
    
    with col_cam:
        st.markdown("### LIVE STREAM")
        st.markdown('<div style="border: 1px solid #39FF88;" class="live-bezel-active">', unsafe_allow_html=True)
        camera_frame = st.camera_input(label="Webcam", label_visibility="collapsed")
        result_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        stats_overlay = st.empty()
        
    with col_analytics:
        st.markdown("### REALTIME ANALYTICS")
        stat_helmets = st.empty()
        stat_danger = st.empty()
        stat_fps = st.empty()

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
        
        stat_helmets.metric("HELMETS (SAFE)", helmets)
        stat_danger.metric("NO HELMET (DANGER)", no_helmets)
        stat_fps.metric("PROCESSING SPEED", f"{fps:.1f} FPS")
        
        if no_helmets > 0:
            stats_overlay.markdown(f"<div style='border-left: 3px solid #E14B4B; padding-left: 10px; margin-top: 10px;'><span class='text-danger mono-text'>[!] FLAG: {no_helmets} PERSON(S) WITHOUT HELMET DETECTED</span></div>", unsafe_allow_html=True)
        elif helmets > 0:
            stats_overlay.markdown(f"<div style='border-left: 3px solid #39FF88; padding-left: 10px; margin-top: 10px;'><span class='text-safe mono-text'>[+] CLEAR: {helmets} PERSON(S) WEARING HELMETS</span></div>", unsafe_allow_html=True)
        else:
            stats_overlay.markdown("<div style='border-left: 3px solid #7C8B85; padding-left: 10px; margin-top: 10px;'><span class='text-muted mono-text'>[-] NO TARGETS IDENTIFIED</span></div>", unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='text-align: center; padding: 60px; background: #101512; border: 1px solid #2A322D;'>
            <div style="font-size: 64px; margin-bottom: 20px;">🔴</div>
            <h3 style="color: #E8ECEA;">CAMERA IS STOPPED</h3>
            <p style="color: #7C8B85; font-family: 'JetBrains Mono', monospace; font-size: 13px; text-transform: uppercase;">Click <strong>START CAMERA</strong> to begin live detection.</p>
        </div>
    """, unsafe_allow_html=True)
