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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 30px; background-color: #101512; border-bottom: 1px solid #2A322D; margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 20px;">🎥</div>
        <div style="font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; text-transform: uppercase;">Video Audit</div>
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

st.title("VIDEO AUDIT")
st.markdown("<p style='color: #7C8B85; font-size: 14px; font-family: \"JetBrains Mono\", monospace; margin-bottom: 30px; text-transform: uppercase;'>Drop footage here. Every frame gets scanned against the detection model.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("Upload video file (MP4, AVI, MOV)", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    st.markdown("### LIVE PROCESSING")
    col_video, col_stats = st.columns([2, 1])
    
    with col_video:
        st.markdown('<div class="scanline-container scanline-active">', unsafe_allow_html=True)
        stframe = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_stats:
        stop_button_pressed = st.button("STOP SCAN", use_container_width=True, type="secondary")
        st.markdown("<br>", unsafe_allow_html=True)
        status_text = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        
        stat_helmets = st.empty()
        stat_danger = st.empty()
    
    last_db_log_time = 0
    frame_count = 0
    
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            status_text.markdown("<span class='text-safe mono-text'>[+] SCAN COMPLETE</span>", unsafe_allow_html=True)
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
        
        status_text.markdown(f"<span class='text-muted mono-text'>FRAME: {frame_count:04d} / {total_frames:04d} | FPS: {fps:.1f}</span>", unsafe_allow_html=True)
        stat_helmets.metric("HELMETS (SAFE)", stats["helmet_count"])
        stat_danger.metric("NO HELMET (DANGER)", stats["no_helmet_count"])
        
    cap.release()
