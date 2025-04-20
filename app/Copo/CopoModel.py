from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from builders.AbstractModel import AbstractModel


@dataclass
class Copo(AbstractModel):
    capacidade: Decimal
    codigo_nfc: str
    permite_alcool: bool = False
    data_criacao: datetime = datetime.now()
    ativo: bool = True
    cliente_id: int
    id: int | None = None