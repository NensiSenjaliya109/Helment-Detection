import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* 
           GLOBAL DESIGN TOKENS
        */
        :root {
            --bg-base: #0B0D0C;
            --bg-panel: #101512;
            --bg-raised: #171C19;
            --accent-green: #39FF88;
            --accent-amber: #FF9F1C;
            --accent-red: #E14B4B;
            --text-primary: #E8ECEA;
            --text-secondary: #7C8B85;
            --border-panel: #2A322D;
            
            --font-display: 'Space Grotesk', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: var(--font-body);
            background-color: var(--bg-base);
            color: var(--text-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-display);
            text-transform: uppercase;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .mono-text {
            font-family: var(--font-mono);
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Modern Button Styling */
        div.stButton > button {
            border-radius: 4px;
            padding: 8px 16px;
            font-family: var(--font-mono);
            text-transform: uppercase;
            font-weight: 700;
            transition: all 0.2s ease;
            letter-spacing: 0.05em;
        }

        /* Primary Button */
        div.stButton > button:first-child:not([kind="secondary"]) {
            background-color: var(--accent-green);
            color: #000000;
            border: 1px solid var(--accent-green);
            box-shadow: none;
        }
        div.stButton > button:first-child:not([kind="secondary"]):hover {
            background-color: #2ED870;
            border-color: #2ED870;
            color: #000000;
            box-shadow: 0 0 10px rgba(57, 255, 136, 0.3);
        }

        /* Secondary Button (Ghost Outline) */
        div.stButton > button[kind="secondary"] {
            background-color: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border-panel);
            box-shadow: none;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: var(--bg-raised);
            border-color: var(--text-secondary);
            color: var(--text-primary);
        }

        /* Cards/Panels */
        div[data-testid="stMetric"], .forensic-card {
            background-color: var(--bg-panel);
            border-radius: 0px;
            padding: 15px;
            border: 1px solid var(--border-panel);
            box-shadow: none;
        }
        div[data-testid="stMetric"] label {
            font-family: var(--font-mono);
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.8rem;
        }
        div[data-testid="stMetric"] div {
            font-family: var(--font-mono);
            color: var(--text-primary);
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            border-radius: 0px;
            background-color: var(--bg-panel);
            border: 1px solid var(--border-panel);
            font-family: var(--font-mono);
            text-transform: uppercase;
        }
        
        /* File Uploader Container (Scanner Gate) */
        [data-testid="stFileUploader"] {
            background-color: var(--bg-base);
            border: 1px solid var(--border-panel);
            border-radius: 0px;
            padding: 20px;
            position: relative;
        }
        [data-testid="stFileUploader"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border: 2px solid transparent;
            background: linear-gradient(to right, var(--border-panel) 50%, transparent 50%) top / 20px 2px repeat-x,
                        linear-gradient(to right, var(--border-panel) 50%, transparent 50%) bottom / 20px 2px repeat-x,
                        linear-gradient(to bottom, var(--border-panel) 50%, transparent 50%) left / 2px 20px repeat-y,
                        linear-gradient(to bottom, var(--border-panel) 50%, transparent 50%) right / 2px 20px repeat-y;
            pointer-events: none;
        }

        /* Dataframes (History Table) */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border-panel);
            border-radius: 0px;
        }
        [data-testid="stDataFrame"] table {
            font-family: var(--font-mono);
            font-size: 0.85rem;
        }
        [data-testid="stDataFrame"] th {
            background-color: var(--bg-panel) !important;
            color: var(--text-secondary) !important;
            text-transform: uppercase;
            border-bottom: 1px solid var(--border-panel) !important;
        }
        [data-testid="stDataFrame"] tr:nth-child(even) {
            background-color: var(--bg-panel) !important;
        }
        [data-testid="stDataFrame"] tr:nth-child(odd) {
            background-color: var(--bg-base) !important;
        }
        
        /* Sidebar Restyling (Film Reel Index) */
        [data-testid="stSidebar"] {
            background-color: var(--bg-panel);
            border-right: 1px solid var(--border-panel);
        }
        
        /* Scanline Animation */
        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        .scanline-sweep {
            position: relative;
            overflow: hidden;
        }
        .scanline-sweep::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 10px;
            background: linear-gradient(to bottom, transparent, rgba(57, 255, 136, 0.5), transparent);
            animation: scanline 3s linear infinite;
            pointer-events: none;
            z-index: 10;
        }
        
        /* Pulse Animation (for Live state) */
        @keyframes pulse-amber {
            0% { border-color: rgba(255, 159, 28, 0.2); }
            50% { border-color: rgba(255, 159, 28, 1); }
            100% { border-color: rgba(255, 159, 28, 0.2); }
        }
        .live-bezel {
            border: 2px solid var(--accent-amber);
            animation: pulse-amber 2s infinite;
            position: relative;
            padding: 5px;
            background-color: var(--bg-panel);
        }
        
        /* Global Header custom classes */
        .header-title {
            font-family: var(--font-display);
            font-size: 24px;
            letter-spacing: 2px;
            font-weight: 700;
        }
        .header-status-badge {
            font-family: var(--font-mono);
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 2px;
            border: 1px solid;
        }
        .status-idle {
            color: var(--text-secondary);
            border-color: var(--border-panel);
            background-color: var(--bg-base);
        }
        .status-scanning {
            color: var(--accent-green);
            border-color: var(--accent-green);
            background-color: rgba(57, 255, 136, 0.1);
        }
        .status-live {
            color: var(--accent-amber);
            border-color: var(--accent-amber);
            background-color: rgba(255, 159, 28, 0.1);
        }
        .header-btn {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--text-secondary);
            background: transparent;
            border: 1px solid var(--border-panel);
            padding: 4px 10px;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s;
        }
        .header-btn:hover {
            color: var(--text-primary);
            border-color: var(--text-secondary);
            background: var(--bg-raised);
        }
        .user-badge {
            width: 28px;
            height: 28px;
            background-color: var(--bg-raised);
            border: 1px solid var(--border-panel);
            color: var(--text-primary);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
