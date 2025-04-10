# app/routers/dynamic_crud_router.py
from fastapi import APIRouter, HTTPException, status
from typing import List, Type
from app.Controller import ControllerGenerico
from app.models.AbstractModel import AbstractModel
from app.Schemas import gerar_schema_entrada, gerar_schema_saida, gerar_schema_atualizar

def criar_endpoint_dinamicamente(model_cls: Type[AbstractModel]) -> APIRouter:
    endpoint = APIRouter()
    controller = ControllerGenerico(model_cls)

    ModelEntrada = gerar_schema_entrada(model_cls)
    ModelSaida   = gerar_schema_saida(model_cls)
    ModelAtualizar = gerar_schema_atualizar(model_cls)

    @endpoint.post("", response_model=ModelSaida, status_code=status.HTTP_201_CREATED,
                   summary=f"Cria um novo {model_cls.__name__}")
    def criar(item: ModelEntrada):  # type: ignore
        try:
            instancia = controller.criar(item.dict())
            return instancia.to_dict()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @endpoint.get("", response_model=List[ModelSaida],
                  summary=f"Lista todos(as) {model_cls.__name__}s")
    def listar():
        try:
            instancias = controller.listar()
            return [instancia.to_dict() for instancia in instancias]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @endpoint.get("/{id}", response_model=ModelSaida,
                  summary=f"Recupera um {model_cls.__name__} pelo ID")
    def obter(id: int):
        try:
            instancia = controller.obter(id)
            return instancia.to_dict()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @endpoint.put("/{id}", response_model=ModelSaida,
                  summary=f"Atualiza um(a) {model_cls.__name__} pelo ID")
    def alterar(id: int, item: ModelEntrada):  # type: ignore
        try:
            instancia = controller.alterar(id, item.dict())
            return instancia.to_dict()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @endpoint.patch("/{id}", response_model=ModelSaida,
                    summary=f"Atualiza parcialmente um {model_cls.__name__} pelo ID")
    def atualizar(id: int, item: ModelAtualizar):  # type: ignore
        try:
            dados = item.dict(exclude_unset=True)
            instancia = controller.alterar(id, dados)
            return instancia.to_dict()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return endpoint
