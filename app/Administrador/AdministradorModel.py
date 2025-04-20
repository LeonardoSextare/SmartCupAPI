from dataclasses import dataclass
from builders.AbstractModel import AbstractModel


@dataclass
class AdministradorModel(AbstractModel):
    nome: str
    login: str
    senha: str
    ativo: bool = True
    id: int | None = None
