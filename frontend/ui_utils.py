import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@600;700&display=swap');

        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0B0D0C;
            color: #E8ECEA;
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            text-transform: uppercase;
            letter-spacing: -0.5px;
        }

        .mono-text {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Modern Button Styling */
        div.stButton > button:first-child {
            background-color: #39FF88;
            color: #0B0D0C;
            border: none;
            border-radius: 2px;
            padding: 8px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            text-transform: uppercase;
            transition: all 0.2s ease;
            box-shadow: none;
        }
        div.stButton > button:first-child:hover {
            background-color: #2ED872;
            color: #0B0D0C;
            transform: translateY(-1px);
        }

        /* Secondary Button (for forms/stop) */
        div.stButton > button[kind="secondary"] {
            background: transparent;
            color: #E8ECEA;
            border: 1px solid #7C8B85;
        }
        div.stButton > button[kind="secondary"]:hover {
            background: rgba(124, 139, 133, 0.1);
            color: #ffffff;
            border-color: #E8ECEA;
        }

        /* Rounded Corners for Images & Videos - Sharp in this theme */
        img, video {
            border-radius: 0px;
            box-shadow: none;
            border: 1px solid #2A322D;
        }

        /* Metric Cards / Panels */
        div[data-testid="stMetric"], .metric-card {
            background-color: #101512;
            border-radius: 0px;
            padding: 16px;
            border: 1px solid #2A322D;
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover, .metric-card:hover {
            border-color: rgba(57, 255, 136, 0.5);
            transform: none;
            box-shadow: none;
        }
        
        div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            color: #39FF88;
        }
        div[data-testid="stMetricLabel"] {
            color: #7C8B85;
            text-transform: uppercase;
            font-size: 12px;
            font-family: 'Space Grotesk', sans-serif;
        }

        /* Headers / Titles */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            margin-bottom: 16px !important;
        }
        
        /* Expander/Cards Styling */
        .streamlit-expanderHeader {
            border-radius: 0px;
            background-color: #101512;
            border: 1px solid #2A322D;
        }
        
        /* File Uploader Container (Scanner Gate) */
        [data-testid="stFileUploader"] {
            background-color: #101512;
            border: 1px solid #2A322D;
            border-radius: 0px;
            padding: 24px;
            position: relative;
            transition: all 0.2s ease;
        }
        [data-testid="stFileUploader"]::before {
            content: '';
            position: absolute;
            top: -1px; left: -1px; right: -1px; bottom: -1px;
            border: 1px solid transparent;
            background: linear-gradient(90deg, #39FF88 10px, transparent 10px) 0 0,
                        linear-gradient(90deg, #39FF88 10px, transparent 10px) 0 100%,
                        linear-gradient(0deg, #39FF88 10px, transparent 10px) 0 0,
                        linear-gradient(0deg, #39FF88 10px, transparent 10px) 100% 0;
            background-repeat: no-repeat;
            background-size: 20px 20px;
            pointer-events: none;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #39FF88;
            background-color: rgba(57, 255, 136, 0.02);
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 0px;
            overflow: hidden;
            border: 1px solid #2A322D;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }
        
        /* Sidebar Restyling - Film Reel Style */
        [data-testid="stSidebar"] {
            background-color: #101512;
            border-right: 1px solid #2A322D;
        }
        [data-testid="stSidebarNav"] span {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            text-transform: uppercase;
        }
        [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"] {
            border-radius: 0;
            background-color: transparent !important;
        }
        /* Target the active link indicator */
        [data-testid="stSidebarNav"] [aria-current="page"] {
             border-left: 3px solid #39FF88;
        }
        [data-testid="stSidebarNav"] [aria-current="page"] span {
             color: #39FF88;
        }

        /* Scanline Animation */
        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        .scanline-container {
            position: relative;
            overflow: hidden;
            border: 1px solid #2A322D;
            display: inline-block;
            width: 100%;
        }
        .scanline-active::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: rgba(57, 255, 136, 0.3);
            box-shadow: 0 0 10px rgba(57, 255, 136, 0.5);
            animation: scanline 3s linear infinite;
            pointer-events: none;
            z-index: 10;
        }
        
        /* Live Bezel Pulse */
        @keyframes livePulse {
            0% { border-color: #2A322D; }
            50% { border-color: #39FF88; box-shadow: 0 0 8px rgba(57, 255, 136, 0.2) inset; }
            100% { border-color: #2A322D; }
        }
        .live-bezel-active {
            animation: livePulse 2s infinite;
        }

        /* Danger Status Colors */
        .text-danger { color: #E14B4B !important; font-family: 'JetBrains Mono', monospace; font-size: 14px;}
        .text-warning { color: #FF9F1C !important; font-family: 'JetBrains Mono', monospace; font-size: 14px;}
        .text-safe { color: #39FF88 !important; font-family: 'JetBrains Mono', monospace; font-size: 14px;}
        .text-muted { color: #7C8B85 !important; font-family: 'JetBrains Mono', monospace; font-size: 14px;}
        
        </style>
    """, unsafe_allow_html=True)
