from config import carregar_env
from fastapi import FastAPI
from Administrador import administrador_endpoint
from builders.Endpoint import criar_endpoint_dinamicamente
from models.Bebida import Bebida
from models.Cliente import Cliente
from models.Copo import Copo
from models.Maquina import Maquina
from models.Bebida import Bebida
from models.Operacao import Operacao
from Operacao import OperacaoService


carregar_env()


app = FastAPI(
    title="SmartCup API",
    description="Documentação da API do sistema SmartCup",
    version="2.0.0",
)


@app.get("/")
def ola_mundo():
    return {"mensagem": "Olá, mundo!"}


app.include_router(administrador_endpoint, prefix="/administrador", tags=["Administrador"])
# app.include_router(endpoint_operacao, prefix="/operacao", tags=["Operacao"])


endpoint_cliente = criar_endpoint_dinamicamente(Cliente)
app.include_router(endpoint_cliente, prefix="/cliente", tags=["Cliente"])

endpoint_copo = criar_endpoint_dinamicamente(Copo)
app.include_router(endpoint_copo, prefix="/copo", tags=["Copo"])

endpoint_bebida = criar_endpoint_dinamicamente(Bebida)
app.include_router(endpoint_bebida, prefix="/bebida", tags=["Bebida"])

endpoint_maquina = criar_endpoint_dinamicamente(Maquina)
app.include_router(endpoint_maquina, prefix="/maquina", tags=["Maquina"])

endpoint_operacao = criar_endpoint_dinamicamente(Operacao, service=OperacaoService())

