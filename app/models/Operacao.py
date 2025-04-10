from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from app.models.AbstractModel import AbstractModel


@dataclass
class Operacao(AbstractModel):
    saldo_gasto: Decimal
    cliente_id: int
    maquina_id: int
    copo_id: int
    bebida_id: int
    data_operacao: datetime = datetime.now()
    id: int | None = None