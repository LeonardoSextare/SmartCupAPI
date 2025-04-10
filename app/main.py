from config import carregar_env
from fastapi import FastAPI
from app.Endpoint import criar_endpoint_dinamicamente
from app.models.Administrador import Administrador
from app.models.Cliente import Cliente
from app.models.Bebida import Bebida
from app.models.Copo import Copo
from app.models.Maquina import Maquina
from app.models.Operacao import Operacao


carregar_env()


app = FastAPI(
    title="SmartCup API",
    description="Documentação da API do sistema SmartCup",
    version="2.0.0",
)


@app.get("/")
def ola_mundo():
    return {"mensagem": "Olá, mundo!"}


endpoint_administrador = criar_endpoint_dinamicamente(Administrador)
app.include_router(endpoint_administrador, prefix="/administrador", tags=["Administrador"])

endpoint_cliente = criar_endpoint_dinamicamente(Cliente)
app.include_router(endpoint_cliente, prefix="/cliente", tags=["Cliente"])

endpoint_maquina = criar_endpoint_dinamicamente(Maquina)
app.include_router(endpoint_maquina, prefix="/maquina", tags=["Maquina"])

endpoint_bebida = criar_endpoint_dinamicamente(Bebida)
app.include_router(endpoint_bebida, prefix="/bebida", tags=["Bebida"])

endpoint_copo = criar_endpoint_dinamicamente(Copo)
app.include_router(endpoint_copo, prefix="/copo", tags=["Copo"])

endpoint_operacao = criar_endpoint_dinamicamente(Operacao)
app.include_router(endpoint_operacao, prefix="/operacao", tags=["Operacao"])



