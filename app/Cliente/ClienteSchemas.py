from pydantic import BaseModel
from datetime import date
from typing import Optional


class ClienteEntrada(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date


class ClienteEntradaPatch(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    saldo_restante: Optional[float] = None
    ativo: Optional[bool] = None


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
