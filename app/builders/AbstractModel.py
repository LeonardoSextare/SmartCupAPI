from dataclasses import dataclass, asdict, fields
from database import executar_query
from typing import Any, Self


@dataclass
class AbstractModel:
    def salvar(self):
        if self.id is None:
            self._criar()
        else:
            self._alterar()

    @classmethod
    def obter(cls, id: int) -> Self:
        query = f"SELECT * FROM {cls.__name__} WHERE id = %s"
        resultado = executar_query(query, (id,))

        if not resultado:
            raise ValueError(f'O id "{id}" não foi encontrado na tabela: "{cls.__name__}"')

        instancia = cls(**resultado)

        return instancia
    
    @classmethod
    def listar(cls):
        query = f"SELECT * FROM {cls.__name__}"
        resultado = executar_query(query)

        print(*resultado, sep='\n')
        
        lista_administradores = [cls(**administrador) for administrador in resultado]

        return lista_administradores
    
    
    def _criar(self):
        tabela, dados = self.__obter_dados()

        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["%s"] * len(dados))
        query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders}) RETURNING id"

        retorno = executar_query(query, tuple(dados.values()))
        self.id = retorno["id"]

    def _alterar(self):
        tabela, dados = self.__obter_dados()
        dados.pop("id")

        clausulas_set = ", ".join([f"{coluna} = %s" for coluna in dados.keys()])
        query = f"UPDATE {tabela} SET {clausulas_set} WHERE id = %s"
        parametros = tuple(dados.values()) + (self.id,)

        executar_query(query, parametros)

    def __obter_dados(self):
        self._validar_dados()
        atributos_filtrados = {
            chave: valor for chave, valor in asdict(self).items() if valor is not None
        }
        nome_classe = self.__class__.__name__

        return nome_classe, atributos_filtrados

    def _validar_dados(self):
        for campo in fields(self):
            valor = getattr(self, campo.name)

            if not isinstance(valor, campo.type):
                raise TypeError(
                    f"Erro ao criar instância: o campo '{campo.name}' "
                    f"espera um valor do tipo '{campo.type.__name__}', "
                    f"mas recebeu '{type(valor).__name__}'."
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def __post_init__(self):
        if "id" not in asdict(self):
            raise NotImplementedError("Implemente o atributo id na classe")
            
        self._validar_dados()
