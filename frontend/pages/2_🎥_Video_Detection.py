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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="font-size: 20px; font-weight: 600; font-family: 'Poppins', sans-serif;">🎥 Video Audit</div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🌙</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔄</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔔</span>
        <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; display: flex; justify-content: center; align-items: center; font-weight: bold;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Video Audit")
st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 30px;'>Upload pre-recorded footage to run continuous YOLOv8 analysis frame-by-frame.</p>", unsafe_allow_html=True)

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
    
    st.markdown("### Live Processing")
    col_video, col_stats = st.columns([2, 1])
    
    with col_video:
        stframe = st.empty()
        
    with col_stats:
        stop_button_pressed = st.button("⏹ Stop Processing", use_container_width=True, type="secondary")
        st.markdown("<br>", unsafe_allow_html=True)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stat_helmets = st.empty()
        stat_danger = st.empty()
    
    last_db_log_time = 0
    frame_count = 0
    
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            status_text.success("✅ Video processing complete.")
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
        if total_frames > 0:
            progress = min(frame_count / total_frames, 1.0)
            progress_bar.progress(progress)
            
        status_text.markdown(f"**Frames Processed:** {frame_count}/{total_frames} | **FPS:** {fps:.1f}")
        stat_helmets.metric("Helmets Detected", stats["helmet_count"])
        stat_danger.metric("No Helmet", stats["no_helmet_count"])
        
    cap.release()
