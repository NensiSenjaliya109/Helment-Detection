import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Warning: SUPABASE_URL or SUPABASE_KEY is missing from .env file.")

supabase: Client = create_client(url, key)

def log_detection(status: str, confidence: float):
    """
    Inserts a new detection record into the Supabase 'detections' table.
    status should be 'Safe' or 'Danger'.
    """
    try:
        data, count = supabase.table('detections').insert({
            "status": status,
            "confidence": confidence
        }).execute()
        print(f"✅ Logged to Database: {status} ({confidence:.2f})")
    except Exception as e:
        print(f"❌ Failed to log to Database: {e}")

def get_history():
    """
    Fetches the detection history from Supabase.
    Returns a list of dictionaries.
    """
    try:
        response = supabase.table('detections').select("*").order('created_at', desc=True).limit(100).execute()
        return response.data
    except Exception as e:
        print(f"❌ Failed to fetch history: {e}")
        return []
