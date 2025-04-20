from fastapi import APIRouter, HTTPException, status
from typing import List
from .OperacaoController import ControllerOperacao
from .OperacaoModel import OperacaoModel
from .OperacaoService import OperacaoService
from .OperacaoSchema import OperacaoEntrada, OperacaoSaida, OperacaoSaidaLista

endpoint = APIRouter()
controller = ControllerOperacao(OperacaoModel, OperacaoService)


@endpoint.post(
    "/operacao",
    response_model=OperacaoSaida,
    status_code=status.HTTP_201_CREATED,
    summary=f"Registra uma operação",
)
def criar(item: OperacaoEntrada):  # type: ignore
    try:
        controller.criar()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/operacao",
    response_model=OperacaoSaidaLista,
    summary=f"Lista todas as operações",
)
def listar():
    try:
        retorno = controller.listar()
        resposta = {"mensagem": "Ok", "quantidade": len(retorno), "resultado": retorno}
        print(resposta)
        return resposta
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=OperacaoSaida,
    summary=f"Retorna uma operação pelo id",
)
def obter(id: int):
    try:
        instancia = controller.obter(id)
        return instancia.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
