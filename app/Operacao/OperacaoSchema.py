from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class ClienteSaida(BaseModel):
    id: int
    nome: str
    cpf: str
    saldo: float
    data_nascimento: date


class CopoSaida(BaseModel):
    id: int
    capacidade: float
    codigo_nfc: str
    permite_alcool: bool


class MaquinaSaida(BaseModel):
    id: int
    nome: str
    qtd_reservatorio_atual: float
    qtd_reservatorio_max: float


class BebidaSaida(BaseModel):
    id: int
    nome: str
    preco: float
    descricao: Optional[str]
    alcolica: bool


class OperacaoSaida(BaseModel):
    operacao_id: int
    data_operacao: datetime
    saldo_gasto: float
    cliente: ClienteSaida
    copo: CopoSaida
    maquina: MaquinaSaida
    bebida: BebidaSaida


class OperacaoSaidaLista(BaseModel):
    quantidade: int
    resultado: list[OperacaoSaida]


class OperacaoEntrada(BaseModel):
    maquina_id: int
    codigo_nfc: str