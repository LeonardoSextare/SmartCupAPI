from pydantic import BaseModel
from datetime import date
from typing import Optional


class BebidaEntrada(BaseModel):
    nome: str
    preco: float
    alcolica: bool
    descricao: str
    
class BebidaEntradaPatch(BaseModel):
    nome: Optional[str]
    preco: Optional[float]
    alcolica: Optional[bool]
    ativo: Optional[bool]
    descricao: Optional[str]


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
