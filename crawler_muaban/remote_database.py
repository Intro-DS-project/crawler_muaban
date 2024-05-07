import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')


def init():
    supabase = create_client(url, key)
    return supabase