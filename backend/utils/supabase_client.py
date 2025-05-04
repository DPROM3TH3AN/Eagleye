# backend/utils/supabase_client.py
from supabase import create_client, Client

# Replace with your actual Supabase URL and API key
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your_supabase_api_key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_tracking_data(data: dict):
    response = supabase.table("tracking").insert([data]).execute()
    return response
