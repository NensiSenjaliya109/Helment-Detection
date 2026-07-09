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

st.title("🎥 Video Detection")
st.write("Upload a video file to run YOLOv8 frame-by-frame.")

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    stframe = st.empty()
    stop_button_pressed = st.button("Stop")
    
    last_db_log_time = 0
    
    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            st.write("End of video.")
            break
            
        # Detect
        results = detector.detect(frame)
        
        # Log to DB only every 5 seconds of real-time processing
        current_time = time.time()
        log_to_db = False
        if current_time - last_db_log_time > 5:
            log_to_db = True
            last_db_log_time = current_time
            
        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=log_to_db) 
        
        # Display in UI
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        stframe.image(annotated_frame_rgb, use_container_width=True)
        
    cap.release()
