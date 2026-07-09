import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from backend import utils
from backend.detector import HelmetDetector

st.set_page_config(page_title="Image Detection", page_icon="📷", layout="wide")

from frontend.ui_utils import apply_custom_css
apply_custom_css()

# --- TOP NAVIGATION BAR ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background-color: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.05); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="font-size: 20px; font-weight: 600; font-family: 'Poppins', sans-serif;">📷 Image Scanner</div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🌙</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔄</span>
        <span style="cursor: pointer; padding: 8px; border-radius: 8px; background: #1E293B;">🔔</span>
        <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; display: flex; justify-content: center; align-items: center; font-weight: bold;">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Image Scan")
st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 30px;'>Upload high-resolution images to run YOLOv8 object detection instantly.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("Drag & drop an image here", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    frame = np.array(image)
    if frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    with st.spinner("Processing image through AI model..."):
        results = detector.detect(frame)
        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=True)
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    
    # Split Layout
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_img, col_stats = st.columns([2, 1])
    
    with col_img:
        st.markdown("### Detection Result")
        st.image(annotated_frame_rgb, use_container_width=True)
    
    with col_stats:
        st.markdown("### Analysis")
        st.metric(label="Helmets (Safe) 🟢", value=stats["helmet_count"])
        st.metric(label="No Helmet (Danger) 🔴", value=stats["no_helmet_count"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if stats["danger"]:
            st.error(f"🚨 **DANGER**\nMissing Helmet detected! (Confidence: {stats['max_danger_conf']*100:.1f}%)")
        elif stats["helmet_count"] > 0:
            st.success(f"✅ **SAFE**\nAll personnel compliant. (Avg Confidence: {stats['max_safe_conf']*100:.1f}%)")
        else:
            st.info("🔍 No persons detected in the image.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("💾 Save to Database", type="primary", use_container_width=True)
        st.button("📥 Download Result", type="secondary", use_container_width=True)
