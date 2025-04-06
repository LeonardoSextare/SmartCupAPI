from dotenv import load_dotenv
from tests.ExecutarTestes import executar_testes

print("Carregando as variaveis de ambiente...")
if not load_dotenv():
    raise FileNotFoundError("Não foi possivel carregar as variaveis de ambiente")
print("Variaveis de Ambiente Carregadas com sucesso!")

from fastapi import FastAPI

app = FastAPI()

@app.get("/soma")
def soma(a: float, b: float):
    return {"resultado": a + b}

