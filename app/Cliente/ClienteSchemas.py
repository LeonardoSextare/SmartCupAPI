from pydantic import BaseModel
from datetime import date
from typing import Optional


class ClienteEntrada(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date


class ClienteEntradaPatch(BaseModel):
    nome: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[date]
    saldo_restante: Optional[float]
    ativo: Optional[bool]


class ClienteSaida(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    saldo_restante: float
    ativo: bool


class ClienteSaidaLista(BaseModel):
    quantidade: int
    resultado: list[ClienteSaida]
