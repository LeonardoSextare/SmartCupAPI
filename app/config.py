import os
from dotenv import load_dotenv, find_dotenv

def carregar_env():
    env_path = find_dotenv()
    
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)
