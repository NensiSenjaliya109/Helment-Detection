import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import cv2
import tempfile
import time
from backend import utils
from backend.detector import HelmetDetector

st.set_page_config(page_title="Video Detection", page_icon="🎥", layout="wide")

from frontend.ui_utils import apply_custom_css
apply_custom_css()

# --- TOP NAVIGATION BAR ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background-color: var(--bg-panel); border-bottom: 1px solid var(--border-panel); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 24px;">🎥</span>
        <div class="header-title">00:02 VIDEO AUDIT</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="header-status-badge status-idle" id="video-status">● IDLE</div>
        <button class="header-btn">THEME</button>
        <button class="header-btn">SYNC</button>
        <button class="header-btn">ALERTS</button>
        <div class="user-badge">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>VIDEO AUDIT</h3>", unsafe_allow_html=True)
st.markdown("<p class='mono-text' style='color: var(--text-secondary); font-size: 14px; margin-bottom: 30px;'>Drop footage here. Every frame gets scanned against the detection model.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("DROP FOOTAGE HERE", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is None:
    st.markdown("""
    <div class="forensic-card mono-text" style="text-align: center; color: var(--text-secondary); padding: 40px; margin-top: 20px;">
        [ NO FOOTAGE LOADED. AWAITING INPUT. ]
    </div>
    """, unsafe_allow_html=True)
else:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    st.markdown("<h4 style='font-size: 14px; margin-top: 20px;'>[ LIVE PROCESSING FEED ]</h4>", unsafe_allow_html=True)
    col_video, col_stats = st.columns([2, 1])
    
    with col_video:
        # We can't wrap st.image directly in a custom div class, but we can display the image.
        stframe = st.empty()
        
    with col_stats:
        stop_button_pressed = st.button("HALT SCAN", type="secondary", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        status_text = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        stat_helmets = st.empty()
        stat_danger = st.empty()
    
    last_db_log_time = 0
    frame_count = 0
    
    # Update Header Status
    st.markdown("""
    <script>
        var statusBadge = window.parent.document.getElementById('video-status');
        if(statusBadge) {
            statusBadge.className = 'header-status-badge status-scanning';
            statusBadge.innerHTML = '● SCANNING';
        }
    </script>
    """, unsafe_allow_html=True)
    
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            status_text.markdown("<div class='mono-text' style='color: var(--accent-green);'>[+] SCAN COMPLETE</div>", unsafe_allow_html=True)
            break
            
        frame_count += 1
        
        # Detect
        start_time = time.time()
        results = detector.detect(frame)
        
        # Log to DB only every 5 seconds of real-time processing
        current_time = time.time()
        log_to_db = False
        if current_time - last_db_log_time > 5:
            log_to_db = True
            last_db_log_time = current_time
            
        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=log_to_db) 
        fps = 1.0 / (time.time() - start_time)
        
        # Display in UI
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        stframe.image(annotated_frame_rgb, use_container_width=True)
        
        # Update Stats
        progress = (frame_count / total_frames) * 100 if total_frames > 0 else 0
        
        status_text.markdown(f"""
        <div style="background-color: var(--bg-panel); border: 1px solid var(--border-panel); padding: 10px;">
            <div class="mono-text" style="color: var(--text-secondary); font-size: 11px;">PROGRESS</div>
            <div class="mono-text" style="font-size: 14px; margin-bottom: 5px;">FRAME {frame_count:04d} / {total_frames:04d}</div>
            <div style="width: 100%; height: 4px; background-color: var(--bg-base);">
                <div style="width: {progress}%; height: 100%; background-color: var(--accent-green);"></div>
            </div>
            <div class="mono-text" style="color: var(--text-secondary); font-size: 11px; margin-top: 5px; text-align: right;">{fps:.1f} FPS</div>
        </div>
        """, unsafe_allow_html=True)
        
        stat_helmets.metric("COMPLIANT (SAFE)", f"{stats['helmet_count']:02d}")
        stat_danger.metric("FLAGGED (DANGER)", f"{stats['no_helmet_count']:02d}")
        
    cap.release()

