import streamlit as st
import cv2
import numpy as np
from PIL import Image
from backend import utils
from backend.detector import HelmetDetector

st.set_page_config(page_title="Image Detection", page_icon="📷", layout="wide")

st.title("📷 Image Detection")
st.write("Upload an image to detect helmets and safety violations.")

# Initialize the detector once and cache it for performance
@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image via PIL
    image = Image.open(uploaded_file)
    
    # Convert PIL image to OpenCV format (numpy array)
    frame = np.array(image)
    
    # Convert RGB to BGR for OpenCV
    if frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    st.write("Processing image...")
    
    # Run Detection
    results = detector.detect(frame)
    
    # Draw Boxes and Log to Database
    annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=True)
    
    # Convert back to RGB for Streamlit displaying
    annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    
    st.image(annotated_frame_rgb, caption='Detection Results', use_container_width=True)
    
    st.markdown("### Detection Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Helmets Detected ✅", value=stats["helmet_count"])
    with col2:
        st.metric(label="No Helmet (Violations) 🚨", value=stats["no_helmet_count"])
    with col3:
        if stats["danger"]:
            st.error(f"DANGER: Missing Helmet! (Conf: {stats['max_danger_conf']:.2f})")
        elif stats["helmet_count"] > 0:
            st.success(f"SAFE: Helmet Detected! (Conf: {stats['max_safe_conf']:.2f})")
        else:
            st.info("No persons detected.")
