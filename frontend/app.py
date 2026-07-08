import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

st.set_page_config(
    page_title="Helmet Detection System",
    page_icon="🪖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
try:
    with open("frontend/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Sidebar
with st.sidebar:
    st.markdown("## 🪖 Helmet Detection")
    st.markdown("*AI Powered Safety Monitoring*")
    st.markdown("---")
    
    st.markdown("### Model Information")
    st.markdown("**Status:** ✅ Ready (`best.pt`)")
    st.markdown("**Framework:** YOLOv8")
    st.markdown("**Database:** Connected (Supabase)")
    st.markdown("---")
    st.markdown("*Developed by Nensi*")

# Main Dashboard
st.title("Helmet Detection System")
st.markdown("*AI-based Safety Compliance Monitoring using Computer Vision.*")

from backend import database

# Fetch basic stats
history = database.get_history()
total_detections = len(history)

# Count Safe vs Danger
helmets_safe = sum(1 for item in history if item.get('status') == 'Safe')
violations_danger = sum(1 for item in history if item.get('status') == 'Danger')

# Calculate average confidence
avg_conf = 0
if total_detections > 0:
    total_conf = sum(item.get('confidence', 0) for item in history)
    avg_conf = total_conf / total_detections

st.markdown("### 📊 Live Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Detections", value=total_detections)
with col2:
    st.metric(label="Helmets Detected (Safe)", value=helmets_safe)
with col3:
    st.metric(label="Violations (Danger)", value=violations_danger, delta="-Danger" if violations_danger > 0 else None, delta_color="inverse")
with col4:
    st.metric(label="Average Confidence", value=f"{avg_conf:.2%}")

st.markdown("---")
st.markdown("### 🚀 Features")

fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.info("**📷 Image Detection**\nUpload an image and run AI to detect helmets instantly.")
with fcol2:
    st.warning("**🎥 Video Detection**\nAnalyze a pre-recorded video frame-by-frame for violations.")
with fcol3:
    st.success("**🔴 Live Webcam**\nTurn on your camera and run real-time YOLOv8 inference.")

st.markdown("👈 **Please select a feature from the sidebar navigation menu to begin.**")
