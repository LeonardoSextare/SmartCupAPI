from dataclasses import field
from datetime import datetime
from decimal import Decimal
from typing import Optional


class Copo:
    id: Optional[int] = None
    capacidade: Decimal = Decimal("0.00")
    data_criacao: datetime = field(default_factory=datetime.utcnow)
    ativo: bool = True
    permite_alcool: bool = False
    codigo_nfc: str = ""
