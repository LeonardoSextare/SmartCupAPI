from os import getenv
from typing import Any, Optional, Tuple
import psycopg2 as db
from psycopg2.extras import RealDictCursor
from psycopg2.errors import *


def __obter_conexao():
    conexao = db.connect(
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
    )
    return conexao


def executar_query(
    query: str, variaveis: Optional[Tuple[Any, ...]] = None
) -> dict[Any, Any] | list[dict[Any, Any]]:
    conexao = __obter_conexao()
    try:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, variaveis)

            resultados = []
            if cursor.description is not None:
                resultados = cursor.fetchall()
                print(resultados)

                resultados = [dict(registro) for registro in resultados]
                if len(resultados) == 1:
                    resultados = resultados[0]

            conexao.commit()
            return resultados

    finally:
        conexao.close()
