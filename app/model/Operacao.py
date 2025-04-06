from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Operacao:
    id: Optional[int] = None
    data_operacao: datetime = field(default_factory=datetime.utcnow)
    cliente_id: int = 0
    maquina_id: int = 0
    copo_id: int = 0
    bebida_id: int = 0
    saldo_gasto: Decimal = Decimal("0.00")
