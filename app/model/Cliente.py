from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class Cliente:
    id: Optional[int] = None
    ativo: bool = True
    nome: str = ""
    cpf: str = ""
    data_nascimento: date = field(default_factory=date.today)
    saldo_restante: Decimal = Decimal("0.00")
