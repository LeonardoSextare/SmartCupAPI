from pydantic import BaseModel
from typing import Optional


class MaquinaEntrada(BaseModel):
    nome: str
    qtd_reservatorio_max: float
    qtd_reservatorio_atual: float
    bebida_id: Optional[int]
    ativo: Optional[bool]


class MaquinaEntradaPatch(BaseModel):
    nome: Optional[str] = None
    qtd_reservatorio_max: Optional[float] = None
    qtd_reservatorio_atual: Optional[float] = None
    bebida_id: Optional[int] = None
    ativo: Optional[bool] = None


class BebidaSaida(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    alcolica: bool
    ativo: bool


class MaquinaSaida(BaseModel):
    id: int
    nome: str
    qtd_reservatorio_max: float
    qtd_reservatorio_atual: float
    ativo: bool
    bebida: Optional[BebidaSaida]


class MaquinaSaidaLista(BaseModel):
    quantidade: int
    resultado: list[MaquinaSaida]