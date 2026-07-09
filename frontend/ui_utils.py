import streamlit as st

import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0F172A;
            color: #F8FAFC;
        }
        
        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Modern Button Styling */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
            color: #ffffff;
            border: none;
        }

        /* Secondary Button (for forms/stop) */
        div.stButton > button[kind="secondary"] {
            background: #334155;
            box-shadow: none;
        }
        div.stButton > button[kind="secondary"]:hover {
            background: #475569;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Rounded Corners for Images & Videos */
        img, video {
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.3s ease;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #1E293B;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            border-color: rgba(59, 130, 246, 0.5);
        }

        /* Headers / Titles */
        h1 {
            font-size: 40px !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
            margin-bottom: 20px !important;
        }
        
        /* Expander/Cards Styling */
        .streamlit-expanderHeader {
            border-radius: 8px;
            background-color: #1E293B;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        /* File Uploader Container */
        [data-testid="stFileUploader"] {
            background-color: #1E293B;
            border: 2px dashed #3B82F6;
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #60A5FA;
            background-color: rgba(59, 130, 246, 0.05);
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Sidebar Restyling */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

