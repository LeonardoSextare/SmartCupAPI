from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Bebida:
    id: Optional[int] = None
    nome: str = ""
    descricao: Optional[str] = None
    preco: Decimal = Decimal("0.00")
    alcolica: bool = False
