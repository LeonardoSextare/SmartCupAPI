from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .MaquinaSchemas import MaquinaEntrada, MaquinaSaida, MaquinaSaidaLista, MaquinaEntradaPatch
from debug import debug, erro

endpoint = APIRouter()

@endpoint.post(
    "",
    response_model=MaquinaSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma nova máquina",
)
def criar(maquina: MaquinaEntrada):
    # Cadastra uma nova máquina no banco de dados
    debug("Iniciando cadastro de máquina", "Maquina", {"maquina": maquina.dict()})
    try:
        retorno = supabase.rpc(
            "inserir_maquina",
            {
                "p_nome": maquina.nome,
                "p_bebida_id": maquina.bebida_id,
                "p_qtd_reservatorio_max": maquina.qtd_reservatorio_max,
                "p_qtd_reservatorio_atual": maquina.qtd_reservatorio_atual,
            },
        ).execute()
        debug("Máquina cadastrada com sucesso", "Maquina", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao cadastrar máquina", "Maquina", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=MaquinaSaidaLista,
    summary="Lista todas as máquinas",
)
def listar():
    # Lista todas as máquinas cadastradas
    debug("Listando todas as máquinas", "Maquina")
    try:
        retorno = supabase.table("listar_maquina").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        debug("Máquinas listadas", "Maquina", {"quantidade": resultado["quantidade"]})
        return resultado

    except Exception as e:
        erro("Erro ao listar máquinas", "Maquina", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=MaquinaSaida,
    summary="Obtém uma máquina pelo ID",
)
def obter(id: int):
    # Busca uma máquina pelo ID
    debug("Buscando máquina pelo ID", "Maquina", {"id": id})
    try:
        retorno = supabase.table("listar_maquina").select("*").eq("id", id).execute().data

        if not retorno:
            debug("Máquina não encontrada", "Maquina", {"id": id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Máquina com ID {id} não encontrada."
            )

        debug("Máquina encontrada", "Maquina", {"maquina": retorno[0]})
        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao buscar máquina", "Maquina", {"erro": str(e)})
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
    # Atualiza os dados de uma máquina existente
    debug("Atualizando máquina", "Maquina", {"id": id, "dados": maquina.dict()})
    try:
        parametros = {"p_id": id}

        if maquina.nome is not None:
            parametros["p_nome"] = maquina.nome
        if maquina.bebida_id is not None:
            parametros["p_bebida_id"] = maquina.bebida_id
        if maquina.qtd_reservatorio_max is not None:
            parametros["p_qtd_reservatorio_max"] = maquina.qtd_reservatorio_max
        if maquina.qtd_reservatorio_atual is not None:
            parametros["p_qtd_reservatorio_atual"] = maquina.qtd_reservatorio_atual

        retorno = supabase.rpc("atualizar_maquina", parametros).execute()
        debug("Máquina atualizada", "Maquina", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao atualizar máquina", "Maquina", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))