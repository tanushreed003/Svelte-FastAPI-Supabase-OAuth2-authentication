import os

import supabase
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client():
    """Returns a Supabase client instance"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase configuration missing. Check environment variables.")

    return supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
