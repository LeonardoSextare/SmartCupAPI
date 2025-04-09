from dataclasses import dataclass
from app.model.AbstractModel import AbstractModel


@dataclass
class Administrador(AbstractModel):
    nome: str
    login: str
    senha: str
    ativo: bool = True
    id: int | None = None
