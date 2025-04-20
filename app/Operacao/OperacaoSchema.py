from datetime import datetime
from pydantic import BaseModel
from models.Copo import Copo
from models.Bebida import Bebida
from models.Maquina import Maquina
from models.Operacao import Operacao
from models.Cliente import Cliente


class MaquinaSaidaOperacao(BaseModel):
    nome: str
    bebida_id: int | Bebida | None = None
    qtd_reservatorio_max: float
    qtd_reservatorio_atual: float
    ativo: bool = True
    id: int | None = None

class OperacaoEntrada(BaseModel):
    copo_id: int
    maquina_id: int

class OperacaoResultado(BaseModel):
    id: int
    saldo_gasto: float
    data_operacao: datetime
    cliente: Cliente
    copo: Copo
    maquina: Maquina.dic
    bebida: Bebida

class OperacaoSaida(BaseModel):
    mensagem: str
    resultado: OperacaoResultado
    
class OperacaoSaidaLista(BaseModel):
    mensagem: str
    quantidade: int
    resultado: list[OperacaoResultado]

