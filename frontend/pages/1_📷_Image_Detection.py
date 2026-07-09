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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 30px; background-color: #101512; border-bottom: 1px solid #2A322D; margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-size: 20px;">📷</div>
        <div style="font-size: 20px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; text-transform: uppercase;">Image Scanner</div>
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

st.title("IMAGE SCAN")
st.markdown("<p style='color: #7C8B85; font-size: 14px; font-family: \"JetBrains Mono\", monospace; margin-bottom: 30px; text-transform: uppercase;'>No image loaded. Drop a frame to begin detection.</p>", unsafe_allow_html=True)

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
        st.markdown("### ANALYSIS")
        st.metric(label="HELMETS (SAFE)", value=stats["helmet_count"])
        st.metric(label="NO HELMET (DANGER)", value=stats["no_helmet_count"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if stats["danger"]:
            st.markdown(f"<div style='border-left: 3px solid #E14B4B; padding-left: 10px;'><span class='text-danger mono-text'>[!] FLAG: MISSING HELMET</span><br><span class='text-muted mono-text'>CONF: {stats['max_danger_conf']*100:.1f}%</span></div>", unsafe_allow_html=True)
        elif stats["helmet_count"] > 0:
            st.markdown(f"<div style='border-left: 3px solid #39FF88; padding-left: 10px;'><span class='text-safe mono-text'>[+] CLEAR: ALL COMPLIANT</span><br><span class='text-muted mono-text'>CONF: {stats['max_safe_conf']*100:.1f}%</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='border-left: 3px solid #7C8B85; padding-left: 10px;'><span class='text-muted mono-text'>[-] NO TARGETS IDENTIFIED</span></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SAVE TO DB", type="primary", use_container_width=True)
        st.button("EXPORT RESULT", type="secondary", use_container_width=True)
