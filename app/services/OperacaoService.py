from models.Operacao import Operacao
from models.Cliente import Cliente
from models.Maquina import Maquina
from models.Copo import Copo
from models.Bebida import Bebida
from decimal import Decimal

class OperacaoService:
    def realizar_operacao(self, data: dict) -> Operacao:
        
        cliente = Cliente.obter(data["cliente_id"])
        maquina = Maquina.obter(data["maquina_id"])
        copo = Copo.obter(data["copo_id"])
        bebida = Bebida.obter(maquina.bebida_id) 
        
        if copo.permite_alcool is False and bebida.alcolica is True:
            raise ValueError("Copo não permite alcool.")
        
        if maquina.qtd_reservatorio_atual < copo.capacidade:
            raise ValueError("Quantidade de liquido insuficiente")
        
        valor_a_descontar = Decimal((bebida.preco / 1000) * copo.capacidade)
        if cliente.saldo_restante < valor_a_descontar:
            raise ValueError("Cliente com Saldo Insuficiente")
        
        try:
            cliente.saldo_restante -= valor_a_descontar
            maquina.qtd_reservatorio_atual -= copo.capacidade
            
            cliente.salvar()
            maquina.salvar()
            data["bebida_id"] = bebida.id
            operacao = Operacao(**data, saldo_gasto=valor_a_descontar)
            operacao.salvar()
            return operacao
        
        except Exception as e:
            raise ValueError(f"Erro durante a Operaçao: {e}")
        
       