from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .BebidaSchemas import BebidaEntrada, BebidaEntradaPatch, BebidaSaida, BebidaSaidaLista

endpoint = APIRouter()


@endpoint.post(
    "",
    response_model=BebidaSaida,
    status_code=status.HTTP_201_CREATED,
    summary=f"Cria uma nova bebida",
)
def criar(bebida: BebidaEntrada):
    try:
        retorno = supabase.rpc(
            "inserir_bebida",
            {
                "p_nome": bebida.nome,
                "p_descricao": bebida.descricao,
                "p_preco": bebida.preco,
                "p_alcolica": bebida.alcolica,
            },
        ).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=BebidaSaidaLista,
    summary=f"Lista todos as bebidas",
)
def listar():
    try:
        retorno = supabase.table("listar_bebida").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        print(resultado)

        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=BebidaSaida,
    summary=f"Obtem uma bebida pelo ID",
)
def obter(id: int):
    try:
        resultado = supabase.rpc("obter_bebida_id", {"p_id": id}).execute().data
        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@endpoint.patch(
    "/{id}",
    response_model=BebidaSaida,
    summary=f"Atualiza completamente ou parcialmente uma bebida pelo ID",
)
def atualizar(id: int, bebida: BebidaEntradaPatch):
    try:
        params = {"p_id": id}

        if bebida.nome is not None:
            params["p_nome"] = bebida.nome
        if bebida.descricao is not None:
            params["p_descricao"] = bebida.descricao
        if bebida.preco is not None:
            params["p_preco"] = bebida.preco
        if bebida.alcolica is not None:
            params["p_alcolica"] = bebida.alcolica
        if bebida.ativo is not None:
            params["p_ativo"] = bebida.ativo

        retorno = supabase.rpc("atualizar_bebida", params).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
