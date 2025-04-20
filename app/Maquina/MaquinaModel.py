from dataclasses import dataclass
from decimal import Decimal
from builders.AbstractModel import AbstractModel


@dataclass
class Maquina(AbstractModel):
    nome: str
    qtd_reservatorio_max: Decimal
    qtd_reservatorio_atual: Decimal
    bebida_id: int
    ativo: bool = True
    id: int | None = None