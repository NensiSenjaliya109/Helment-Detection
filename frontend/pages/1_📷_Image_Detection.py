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
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; background-color: var(--bg-panel); border-bottom: 1px solid var(--border-panel); margin-top: -60px; margin-bottom: 30px; margin-left: -4rem; margin-right: -4rem;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 24px;">📷</span>
        <div class="header-title">00:01 IMAGE SCAN</div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="header-status-badge status-idle">● IDLE</div>
        <button class="header-btn">THEME</button>
        <button class="header-btn">SYNC</button>
        <button class="header-btn">ALERTS</button>
        <div class="user-badge">N</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>IMAGE SCAN</h3>", unsafe_allow_html=True)
st.markdown("<p class='mono-text' style='color: var(--text-secondary); font-size: 14px; margin-bottom: 30px;'>Upload static images for bulk compliance checking.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_detector():
    return HelmetDetector("backend/best.pt")

detector = load_detector()

uploaded_file = st.file_uploader("DRAG & DROP FRAME HERE", type=["jpg", "jpeg", "png"])

if uploaded_file is None:
    st.markdown("""
    <div class="forensic-card mono-text" style="text-align: center; color: var(--text-secondary); padding: 40px; margin-top: 20px;">
        [ NO IMAGE LOADED. DROP A FRAME TO BEGIN DETECTION. ]
    </div>
    """, unsafe_allow_html=True)
else:
    image = Image.open(uploaded_file)
    frame = np.array(image)
    if frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    with st.spinner("SCANNING FRAME..."):
        results = detector.detect(frame)
        annotated_frame, stats = utils.draw_boxes(frame, results, log_to_db=True)
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    
    # Split Layout
    st.markdown("<br>", unsafe_allow_html=True)
    col_img, col_stats = st.columns([2, 1])
    
    with col_img:
        st.markdown("<h4 style='font-size: 14px;'>[ DETECTION RESULT ]</h4>", unsafe_allow_html=True)
        # Using Streamlit width trick: use_container_width deprecation fix
        st.image(annotated_frame_rgb, width=None)
    
    with col_stats:
        st.markdown("<h4 style='font-size: 14px;'>[ ANALYSIS ]</h4>", unsafe_allow_html=True)
        
        st.metric(label="COMPLIANT (SAFE)", value=f"{stats['helmet_count']:02d}")
        st.metric(label="FLAGGED (DANGER)", value=f"{stats['no_helmet_count']:02d}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if stats["danger"]:
            st.markdown(f"""
            <div style="border-left: 3px solid var(--accent-red); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--accent-red); font-size: 12px; font-weight: bold;">[!] DANGER DETECTED</div>
                <div class="mono-text" style="color: var(--text-secondary); font-size: 11px;">CONFIDENCE: {stats['max_danger_conf']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        elif stats["helmet_count"] > 0:
            st.markdown(f"""
            <div style="border-left: 3px solid var(--accent-green); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--accent-green); font-size: 12px; font-weight: bold;">[+] SAFE / COMPLIANT</div>
                <div class="mono-text" style="color: var(--text-secondary); font-size: 11px;">AVG CONF: {stats['max_safe_conf']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="border-left: 3px solid var(--text-secondary); padding-left: 10px; margin-bottom: 20px;">
                <div class="mono-text" style="color: var(--text-secondary); font-size: 12px;">[-] NO SUBJECTS DETECTED</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.button("EXPORT LOG TO DB", type="primary", use_container_width=True)
        st.button("DOWNLOAD FRAME", type="secondary", use_container_width=True)
