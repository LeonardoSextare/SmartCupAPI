from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from app.builders.AbstractModel import AbstractModel


@dataclass
class Cliente(AbstractModel):
    nome: str
    cpf: str
    data_nascimento: date
    saldo_restante: Decimal = Decimal("0.00")
    ativo: bool = True
    id: int | None = None
