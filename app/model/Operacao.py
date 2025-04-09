from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from app.model.AbstractModel import AbstractModel


@dataclass
class Operacao(AbstractModel):
    saldo_gasto: Decimal
    cliente_id: int
    maquina_id: int
    copo_id: int
    bebida_id: int
    data_operacao: datetime = datetime.now()
    id: int | None = None

teste = Operacao(Decimal("10.11"), cliente_id=3, maquina_id=1, copo_id=1, bebida_id=1)
teste.salvar()