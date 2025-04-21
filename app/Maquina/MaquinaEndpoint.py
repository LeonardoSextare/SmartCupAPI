from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .MaquinaSchemas import MaquinaEntrada, MaquinaEntradaPatch, MaquinaSaida, MaquinaSaidaLista

endpoint = APIRouter()


@endpoint.post(
    "",
    response_model=MaquinaSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova máquina",
)
def criar(maquina: MaquinaEntrada):
    try:
        retorno = supabase.rpc(
            "inserir_maquina",
            {
                "p_nome": maquina.nome,
                "p_qtd_reservatorio_max": maquina.qtd_reservatorio_max,
                "p_qtd_reservatorio_atual": maquina.qtd_reservatorio_atual,
                "p_bebida_id": maquina.bebida_id,
                "p_ativo": maquina.ativo,
            },
        ).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=MaquinaSaidaLista,
    summary="Lista todas as máquinas",
)
def listar():
    try:
        retorno = supabase.table("listar_maquina").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}

        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=MaquinaSaida,
    summary="Obtém uma máquina pelo ID",
)
def obter(id: int):
    try:
        retorno = supabase.table("listar_maquina").select("*").eq("id", id).execute().data

        if not retorno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Máquina com ID {id} não encontrada."
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
    response_model=MaquinaSaida,
    summary="Atualiza completamente ou parcialmente uma máquina pelo ID",
)
def atualizar(id: int, maquina: MaquinaEntradaPatch):
    try:
        parametros = {"p_id": id}

        if maquina.nome is not None:
            parametros["p_nome"] = maquina.nome
        if maquina.qtd_reservatorio_max is not None:
            parametros["p_qtd_reservatorio_max"] = maquina.qtd_reservatorio_max
        if maquina.qtd_reservatorio_atual is not None:
            parametros["p_qtd_reservatorio_atual"] = maquina.qtd_reservatorio_atual
        if maquina.bebida_id is not None:
            parametros["p_bebida_id"] = maquina.bebida_id
        if maquina.ativo is not None:
            parametros["p_ativo"] = maquina.ativo

        retorno = supabase.rpc("atualizar_maquina", parametros).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))