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

st.title("🔴 Live Webcam Detection")
st.write("Real-time AI monitoring using your browser's camera.")

st.info(
    "📷 **How to use:** Allow camera access in your browser when prompted, "
    "then click **Start Camera**. Your webcam frames will be sent to the AI model for detection."
)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

# --- Session State ---
if "run_camera" not in st.session_state:
    st.session_state.run_camera = False
if "last_db_log_time" not in st.session_state:
    st.session_state.last_db_log_time = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Camera", use_container_width=True, type="primary"):
        st.session_state.run_camera = True

with col2:
    if st.button("⏹ Stop Camera", use_container_width=True):
        st.session_state.run_camera = False

st.divider()

if st.session_state.run_camera:
    # st.camera_input captures a single frame from the USER's browser webcam.
    # It works on any cloud server because the camera runs in the user's browser, not on the server!
    camera_frame = st.camera_input(
        label="Your webcam feed (one frame at a time)",
        label_visibility="collapsed"
    )

    result_placeholder = st.empty()
    stats_placeholder = st.empty()

    if camera_frame is not None:
        # Convert the captured browser frame to a numpy array for OpenCV
        file_bytes = np.asarray(bytearray(camera_frame.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Run AI detection
        results = detector.detect(frame)

        # Log to DB only every 5 seconds to avoid spam
        current_time = time.time()
        log_to_db = False
        if current_time - st.session_state.last_db_log_time > 5:
            log_to_db = True
            st.session_state.last_db_log_time = current_time

        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=log_to_db)

        # Convert BGR to RGB for display
        annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        result_placeholder.image(annotated_rgb, caption="AI Detection Result", use_container_width=True)

        # Show detection stats
        helmets = stats.get("helmets", 0)
        no_helmets = stats.get("no_helmets", 0)
        if no_helmets > 0:
            stats_placeholder.error(f"🚨 **DANGER:** {no_helmets} person(s) without helmet detected!")
        elif helmets > 0:
            stats_placeholder.success(f"✅ **Safe:** {helmets} person(s) wearing helmets.")
        else:
            stats_placeholder.info("🔍 No persons detected in this frame.")

        st.caption("📸 Click the camera capture button above to take and analyse the next frame.")
else:
    st.markdown(
        """
        <div style='text-align: center; padding: 60px; color: #888;'>
            <h3>📷 Camera is stopped</h3>
            <p>Click <strong>Start Camera</strong> to begin live detection.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
