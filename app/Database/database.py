from os import getenv
from typing import Any, Literal, Optional, Tuple

import psycopg2 as db
from psycopg2.extras import RealDictCursor


def __obter_conexao():
    conexao = db.connect(
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
    )
    return conexao


def executar_query(query: str, variaveis: Optional[Tuple[Any, ...]] = None) -> dict[Any, Any] | list[dict[Any, Any]] | Literal[True]:
    conexao = __obter_conexao()
    try:
        with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, variaveis)
            
            if cursor.description is None:
                conexao.commit()
                return True
            
            resultados = cursor.fetchall()
            conexao.commit()

            if len(resultados) == 1:
                return dict(resultados[0])

            return [dict(registro) for registro in resultados]
    except Exception as e:
        ...
    finally:
        conexao.close()
