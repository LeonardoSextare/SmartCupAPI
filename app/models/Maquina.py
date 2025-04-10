from dataclasses import dataclass
from decimal import Decimal
from app.builders.AbstractModel import AbstractModel


@dataclass
class Maquina(AbstractModel):
    nome: str
    bebida_id: int | None = None
    qtd_reservatorio_max: Decimal = Decimal("0.00")
    qtd_reservatorio_atual: Decimal = Decimal("0.00")
    ativo: bool = True
    id: int | None = None

