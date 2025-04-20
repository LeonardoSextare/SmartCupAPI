from pydantic import BaseModel
from typing import Optional

class AdministradorEntrada(BaseModel):
    nome: str
    login: str
    senha: str


class AdministradorEntradaPatch(BaseModel):
    nome: Optional[str]
    login: Optional[str]
    senha: Optional[str]
    ativo: Optional[bool]

class AdministradorSaida(BaseModel):
    id: int
    nome: str
    login: str
    senha: str
    ativo: bool

    
class AdministradorSaidaLista(BaseModel):
    quantidade: int
    resultado: list[AdministradorSaida]

