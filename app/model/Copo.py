
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from app.model.AbstractModel import AbstractModel

@dataclass
class Copo(AbstractModel):
    capacidade: Decimal
    codigo_nfc: str
    permite_alcool: bool = False
    data_criacao: datetime = datetime.now()
    ativo: bool = True
    id: int | None = None


teste = Copo(Decimal(200), "ab2")
print(teste)
teste.salvar()