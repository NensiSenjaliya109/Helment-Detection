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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background-color: var(--bg-panel); border-bottom: 1px solid var(--border-panel); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 24px;">🔴</span>
        <div class="header-title">00:03 LIVE MONITOR</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="header-status-badge status-idle" id="live-status">● IDLE</div>
        <button class="header-btn">THEME</button>
        <button class="header-btn">SYNC</button>
        <button class="header-btn">ALERTS</button>
        <div class="user-badge">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>LIVE MONITOR</h3>", unsafe_allow_html=True)
st.markdown("<p class='mono-text' style='color: var(--text-secondary); font-size: 14px; margin-bottom: 30px;'>Connect to webcam for real-time live site monitoring.</p>", unsafe_allow_html=True)

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
    if st.button("ENGAGE FEED", use_container_width=True, type="primary"):
        st.session_state.run_camera = True
with col2:
    if st.button("HALT FEED", use_container_width=True, type="secondary"):
        st.session_state.run_camera = False

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.run_camera:
    
    # Update Header Status
    st.markdown("""
    <script>
        var statusBadge = window.parent.document.getElementById('live-status');
        if(statusBadge) {
            statusBadge.className = 'header-status-badge status-live';
            statusBadge.innerHTML = '● LIVE FEED';
        }
    </script>
    """, unsafe_allow_html=True)
    
    col_cam, col_analytics = st.columns([2, 1])
    
    with col_cam:
        st.markdown("<h4 style='font-size: 14px;'>[ LIVE FEED BEZEL ]</h4>", unsafe_allow_html=True)
        # st.camera_input natively manages camera. We use result_placeholder for the processed frames.
        camera_frame = st.camera_input(label="Webcam", label_visibility="collapsed")
        
        st.markdown('<div class="live-bezel scanline-sweep">', unsafe_allow_html=True)
        result_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_analytics:
        st.markdown("<h4 style='font-size: 14px;'>[ TELEMETRY ]</h4>", unsafe_allow_html=True)
        stat_helmets = st.empty()
        stat_danger = st.empty()
        stat_fps = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
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
        
        stat_helmets.metric("COMPLIANT (SAFE)", f"{helmets:02d}")
        stat_danger.metric("FLAGGED (DANGER)", f"{no_helmets:02d}")
        stat_fps.metric("FPS", f"{fps:.1f}")
        
        if no_helmets > 0:
            stats_placeholder.markdown(f"""
            <div style="border-left: 3px solid var(--accent-red); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--accent-red); font-size: 12px; font-weight: bold;">[!] DANGER DETECTED</div>
                <div class="mono-text" style="color: var(--text-secondary); font-size: 11px;">{no_helmets} NON-COMPLIANT</div>
            </div>
            """, unsafe_allow_html=True)
        elif helmets > 0:
            stats_placeholder.markdown(f"""
            <div style="border-left: 3px solid var(--accent-green); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--accent-green); font-size: 12px; font-weight: bold;">[+] SAFE / COMPLIANT</div>
                <div class="mono-text" style="color: var(--text-secondary); font-size: 11px;">{helmets} COMPLIANT</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            stats_placeholder.markdown("""
            <div style="border-left: 3px solid var(--text-secondary); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--text-secondary); font-size: 12px;">[-] NO SUBJECTS DETECTED</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="forensic-card mono-text" style="text-align: center; color: var(--text-secondary); padding: 40px; margin-top: 20px;">
        [ CONNECTION TO FEED TERMINATED. CLICK 'ENGAGE FEED' TO RECONNECT. ]
    </div>
    """, unsafe_allow_html=True)
