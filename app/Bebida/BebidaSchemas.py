from pydantic import BaseModel
from datetime import date
from typing import Optional


class BebidaEntrada(BaseModel):
    nome: str
    preco: float
    alcolica: bool
    descricao: str


class BebidaEntradaPatch(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    alcolica: Optional[bool] = None
    ativo: Optional[bool] = None
    descricao: Optional[str] = None


class BebidaSaida(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    alcolica: bool
    ativo: bool


class BebidaSaidaLista(BaseModel):
    quantidade: int
    resultado: list[BebidaSaida]
