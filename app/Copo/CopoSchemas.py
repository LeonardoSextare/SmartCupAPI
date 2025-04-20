from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class CopoEntrada(BaseModel):
    capacidade: float
    codigo_nfc: str
    permite_alcool: Optional[bool]
    cliente_id: Optional[int] 


class CopoEntradaPatch(BaseModel):
    capacidade: Optional[float]
    codigo_nfc: Optional[str]
    permite_alcool: Optional[bool]
    ativo: Optional[bool]
    cliente_id: Optional[int]


class ClienteSaida(BaseModel):
    id: Optional[int]
    nome: Optional[str]
    cpf: Optional[str]
    data_nascimento: Optional[date]
    ativo: Optional[bool]
    saldo_restante: Optional[float]


class CopoSaida(BaseModel):
    id: int
    capacidade: float
    codigo_nfc: str
    permite_alcool: bool
    data_criacao: datetime
    ativo: bool
    cliente: ClienteSaida | None


class CopoSaidaLista(BaseModel):
    quantidade: int
    resultado: list[CopoSaida]