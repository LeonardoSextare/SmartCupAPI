from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .CopoSchemas import CopoEntrada, CopoEntradaPatch, CopoSaida, CopoSaidaLista

endpoint = APIRouter()


@endpoint.post(
    "",
    response_model=CopoSaida,
    status_code=status.HTTP_201_CREATED,
    summary=f"Cria um novo copo",
)
def criar(copo: CopoEntrada):
    try:
        retorno = supabase.rpc(
            "inserir_copo",
            {
                "p_capacidade": copo.capacidade,
                "p_codigo_nfc": copo.codigo_nfc,
                "p_permite_alcool": copo.permite_alcool,
                "p_cliente_id": copo.cliente_id,
            },
        ).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=CopoSaidaLista,
    summary=f"Lista todos os copos",
)
def listar():
    try:
        retorno = supabase.table("listar_copo").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        print(resultado)

        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=CopoSaida,
    summary="Obtém um copo pelo ID",
)
def obter(id: int):
    try:
        retorno = supabase.table("listar_copo").select("*").eq("id", id).execute().data

        if not retorno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Copo com ID {id} não encontrado."
            )

        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@endpoint.patch(
    "/{id}",
    response_model=CopoSaida,
    summary="Atualiza completamente ou parcialmente um copo pelo ID",
)
def atualizar(id: int, copo: CopoEntradaPatch):
    try:
        parametros = {"p_id": id}

        if copo.capacidade is not None:
            parametros["p_capacidade"] = copo.capacidade
        if copo.codigo_nfc is not None:
            parametros["p_codigo_nfc"] = copo.codigo_nfc
        if copo.permite_alcool is not None:
            parametros["p_permite_alcool"] = copo.permite_alcool
        if copo.ativo is not None:
            parametros["p_ativo"] = copo.ativo
        if copo.cliente_id is not None:
            parametros["p_cliente_id"] = copo.cliente_id

        retorno = supabase.rpc("atualizar_copo", parametros).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))