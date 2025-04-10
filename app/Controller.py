from typing import Type, TypeVar, List
from app.models.AbstractModel import AbstractModel

T = TypeVar("T", bound=AbstractModel)

class ControllerGenerico:
    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls

    def criar(self, data: dict) -> T:
        instancia: T = self.model_cls(**data)
        instancia.salvar()
        return instancia

    def obter(self, id: int) -> T:
        return self.model_cls.obter(id)

    def listar(self) -> List[T]:
        return self.model_cls.listar()

    def alterar(self, id: int, data: dict) -> T:
        instancia = self.obter(id)
        for chave, valor in data.items():
            setattr(instancia, chave, valor)
        instancia.salvar() 
        return instancia
