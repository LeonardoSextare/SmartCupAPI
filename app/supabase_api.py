from supabase import create_client, Client
from os import getenv

url = getenv("SUPABASE_URL")
key = getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)
