import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Modern Button Styling */
        div.stButton > button:first-child {
            background-color: transparent;
            color: #00FFAA;
            border: 2px solid #00FFAA;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        div.stButton > button:first-child:hover {
            background-color: #00FFAA;
            color: #0E1117;
            box-shadow: 0 0 15px rgba(0, 255, 170, 0.4);
            transform: translateY(-2px);
        }

        /* Rounded Corners for Images */
        img {
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #1E212B;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #00FFAA;
        }

        /* Headers */
        h1 {
            background: -webkit-linear-gradient(45deg, #00FFAA, #00B8FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }
        
        /* Expander/Cards Styling */
        .streamlit-expanderHeader {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
