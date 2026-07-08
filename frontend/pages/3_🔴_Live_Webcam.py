import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import cv2
from backend import utils
from backend.detector import HelmetDetector
import time

st.set_page_config(page_title="Live Webcam", page_icon="🔴", layout="wide")

st.title("🔴 Live Webcam Detection")
st.write("Real-time AI monitoring.")

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

start_btn = st.button("Start Camera")
stop_btn = st.button("Stop Camera")
stframe = st.empty()

# Use session state to handle start/stop logic
if "run_camera" not in st.session_state:
    st.session_state.run_camera = False

if start_btn:
    st.session_state.run_camera = True
if stop_btn:
    st.session_state.run_camera = False

if st.session_state.run_camera:
    cap = cv2.VideoCapture(0)
    
    # Cooldown timer to prevent database spam
    last_db_log_time = 0
    
    while st.session_state.run_camera:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera.")
            break
            
        results = detector.detect(frame)
        
        # Log to DB only every 5 seconds
        current_time = time.time()
        log_to_db = False
        if current_time - last_db_log_time > 5:
            log_to_db = True
            last_db_log_time = current_time
            
        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=log_to_db)
        
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        stframe.image(annotated_frame_rgb, use_container_width=True)
        
    cap.release()
