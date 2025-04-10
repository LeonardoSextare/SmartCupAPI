from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from builders.AbstractModel import AbstractModel
from models.Cliente import Cliente
from models.Maquina import Maquina
from models.Copo import Copo
from models.Bebida import Bebida


@dataclass
class Operacao(AbstractModel):
    saldo_gasto: Decimal
    cliente_id: int | Cliente
    copo_id: int | Copo
    bebida_id: int | Bebida
    maquina_id: int | Maquina
    data_operacao: datetime = datetime.now()
    id: int | None = None