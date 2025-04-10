from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from builders.AbstractModel import AbstractModel


@dataclass
class Bebida(AbstractModel):
    nome: str
    preco: Decimal
    alcolica: bool = False
    ativo: bool = True
    descricao: Optional[str] = None
    id: Optional[int] = None
