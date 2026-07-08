import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import streamlit as st
import pandas as pd
from backend import database

st.set_page_config(page_title="Detection History", page_icon="🗄️", layout="wide")

st.title("🗄️ Supabase Detection History")
st.write("Live feed of all AI safety detections from your cloud database.")

history = database.get_history()

if not history:
    st.info("No detection history found in Supabase. Run some detections first!")
else:
    # Convert the list of dicts to a pandas DataFrame
    df = pd.DataFrame(history)
    
    # Reorder/rename columns for better UI
    if not df.empty:
        df = df[["id", "created_at", "status", "confidence"]]
        df.rename(columns={
            "id": "ID",
            "created_at": "Timestamp",
            "status": "Status",
            "confidence": "Confidence Score"
        }, inplace=True)
        
        # Convert ID to string to prevent Streamlit from automatically right-aligning numbers
        df["ID"] = df["ID"].astype(str)
        
        # Format the Confidence Score
        df["Confidence Score"] = df["Confidence Score"].apply(lambda x: f"{float(x):.2f}")
        
        # Convert Timestamp to India Time (IST) and format it beautifully
        # It parses the UTC string, converts to Kolkata, and formats to "8th July 2026, 11:50 AM (IST)"
        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.tz_convert('Asia/Kolkata')
        
        def format_ist(dt):
            day = dt.day
            suffix = 'th' if 11 <= day <= 13 else {1:'st', 2:'nd', 3:'rd'}.get(day % 10, 'th')
            return f"{day}{suffix} {dt.strftime('%B %Y, %I:%M %p')} (IST)"
            
        df['Timestamp'] = df['Timestamp'].apply(format_ist)
        
        # Center align all text in the dataframe
        styled_df = df.style.set_properties(**{'text-align': 'center'})
        styled_df = styled_df.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
        
        # Display as a dataframe
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )
