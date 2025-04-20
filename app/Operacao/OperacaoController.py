from supabase_api import supabase

from builders.AbstractModel import AbstractModel


class ControllerOperacao:
    def __init__(self, model_operacao: AbstractModel, service=None):
        self.model_operacao = model_operacao
        self.service = service

    def criar(self, data: dict):
        ...

    def obter(self, id: int):
        return self.model_cls.obter(id)

    def listar(self):
        retorno = (supabase.table("vw_operacao_detalhada").select("*").execute()).data

        resultado = []
        for item in retorno:
            operacao = {
                "id": item["operacao_id"],
                "data_operacao": item["data_operacao"],
                "saldo_gasto": float(item["saldo_gasto"]),
                "cliente": {
                    "id": item["cliente_id"],
                    "nome": item["cliente_nome"],
                    "cpf": item["cpf"],
                    "data_nascimento": item["data_nascimento"],
                    "saldo_restante": float(item["saldo_restante"]),
                },
                "copo": {
                    "id": item["copo_id"],
                    "capacidade": float(item["capacidade"]),
                    "codigo_nfc": item["codigo_nfc"],
                    "permite_alcool": item["permite_alcool"],
                },
                "maquina": {
                    "id": item["maquina_id"],
                    "nome": item["maquina_nome"],
                    "qtd_reservatorio_atual": float(item["qtd_reservatorio_atual"]),
                    "qtd_reservatorio_max": float(item["qtd_reservatorio_max"]),
                },
                "bebida": {
                    "id": item["bebida_id"],
                    "nome": item["bebida_nome"],
                    "descricao": item["descricao"],
                    "preco": float(item["preco"]),
                    "alcolica": item["alcolica"],
                },
            }
            resultado.append(operacao)

        return resultado
