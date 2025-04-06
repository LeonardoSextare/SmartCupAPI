from os import getenv
from typing import Any, Literal, Optional, Tuple

import psycopg2 as db
from psycopg2.extras import RealDictCursor

def __obter_conexao():

    print("Abrindo conexão com o banco...")
    conexao = db.connect(
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
    )
    print("Conexão com o banco aberta")

    return conexao

def executar_query(query: str, variaveis: Optional[Tuple[Any,...]]= None, retorno: Literal["one", "all", "none"] = "none"):

    conexao = __obter_conexao()

    try:
        with conexao:
            with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, variaveis)
                
                if retorno == "one":
                    return cursor.fetchone()
                elif retorno == "all":
                    return cursor.fetchall()
                else:
                    return None
                
    finally:
        conexao.close()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    teste = executar_query("Select * from administrador", retorno="one")
    print(teste)