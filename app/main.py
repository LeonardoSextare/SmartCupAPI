from config import carregar_env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Administrador import administrador_endpoint
from Cliente import cliente_endpoint
from Bebida import bebida_endpoint
from Copo import copo_endpoint
from Maquina import maquina_endpoint
from Operacao import operacao_endpoint


carregar_env()


app = FastAPI(
    title="SmartCup API",
    description="Documentação da API do sistema SmartCup",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # ou ["GET","POST","PUT","PATCH","DELETE","OPTIONS"]
    allow_headers=["*"],
)


@app.get("/")
def ola_mundo():
    return {"mensagem": "Olá, mundo!"}


app.include_router(administrador_endpoint, prefix="/administrador", tags=["Administrador"])

app.include_router(cliente_endpoint, prefix="/cliente", tags=["Cliente"])

app.include_router(bebida_endpoint, prefix="/bebida", tags=["Bebida"])

app.include_router(copo_endpoint, prefix="/copo", tags=["Copo"])

app.include_router(maquina_endpoint, prefix="/maquina", tags=["Maquina"])

app.include_router(operacao_endpoint, prefix="/operacao", tags=["Operacao"])
