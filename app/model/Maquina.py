from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Maquina:
    id: Optional[int] = None
    qtd_reservatorio_max: Decimal = Decimal("0.00")
    qtd_reservatorio_atual: Decimal = Decimal("0.00")
    bebida_id: int = 0
    ativo: bool = True
