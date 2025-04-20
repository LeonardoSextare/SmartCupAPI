from supabase import create_client, Client
from os import getenv
from config import carregar_env

carregar_env()


url = getenv("SUPABASE_URL")
key = getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)
