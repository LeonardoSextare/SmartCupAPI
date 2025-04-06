from dataclasses import dataclass
from typing import Optional
from app.database.Connection import executar_query

@dataclass
class Administrador:
    id: Optional[int] = None
    ativo: Optional[bool] = True
    nome: str = ""
    login: str = ""
    senha: str = ""

    @classmethod
    def criar(cls, nome: str, login: str, senha: str, ativo: Optional[bool] = True) -> "Administrador":

        consulta = """
            INSERT INTO administrador (ativo, nome, login, senha)
            VALUES (%s, %s, %s, %s)
            RETURNING id, ativo, nome, login, senha
        """
        resultado = executar_query(
            query=consulta, 
            variaveis=(ativo, nome, login, senha), 
            retorno="one"
        )
            
        return cls(**resultado)

    @classmethod
    def obter_por_id(cls, admin_id: int) -> Optional["Administrador"]:
        """
        Busca e retorna um administrador pelo ID.
        """
        consulta = "SELECT * FROM administrador WHERE id = %s"
        resultado = executar_query(
            query=consulta, 
            variaveis=(admin_id,), 
            retorno="one"
        )
        if resultado:
            return cls(**resultado)
        return None

    def atualizar(self) -> "Administrador":
        """
        Atualiza os dados deste administrador no banco e retorna a instância atualizada.
        """
        consulta = """
            UPDATE administrador
            SET ativo = %s, nome = %s, login = %s, senha = %s
            WHERE id = %s
            RETURNING id, ativo, nome, login, senha
        """
        resultado = executar_query(
            query=consulta, 
            variaveis=(self.ativo, self.nome, self.login, self.senha, self.id), 
            retorno="one"
        )
        return Administrador(**resultado)

    def excluir(self) -> bool:
        """
        Exclui este administrador do banco de dados.
        """
        consulta = "DELETE FROM administrador WHERE id = %s"
        executar_query(
            query=consulta, 
            variaveis=(self.id,), 
            retorno="none"
        )
        return True
