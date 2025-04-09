from dataclasses import dataclass
from app.model.AbstractModel import AbstractModel



@dataclass
class Administrador(AbstractModel):
    nome: str
    login: str
    senha: str
    ativo: bool = True
    id: int | None = None


teste = Administrador("teste", "ad2sd223a", "adsa")
print(teste.id)

# teste.nome = "testemudado3"
# teste.salvar()
# print(teste)


# teste2 = Administrador.obter(1)
# teste2.ativo = True

# teste2.salvar()