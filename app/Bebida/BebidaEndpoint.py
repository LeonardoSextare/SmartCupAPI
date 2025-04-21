from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .BebidaSchemas import BebidaEntrada, BebidaSaida, BebidaSaidaLista, BebidaEntradaPatch
from debug import debug, erro

endpoint = APIRouter()

@endpoint.post(
    "",
    response_model=BebidaSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova bebida",
)
def criar(bebida: BebidaEntrada):
    # Cria uma nova bebida no banco de dados
    debug("Iniciando criação de bebida", "Bebida", {"bebida": bebida.dict()})
    try:
        retorno = supabase.rpc(
            "inserir_bebida",
            {
                "p_nome": bebida.nome,
                "p_preco": bebida.preco,
                "p_estoque": bebida.estoque,
            },
        ).execute()
        debug("Bebida criada com sucesso", "Bebida", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao criar bebida", "Bebida", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=BebidaSaidaLista,
    summary="Lista todas as bebidas",
)
def listar():
    # Lista todas as bebidas cadastradas
    debug("Listando todas as bebidas", "Bebida")
    try:
        retorno = supabase.table("listar_bebida").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        debug("Bebidas listadas", "Bebida", {"quantidade": resultado["quantidade"]})
        return resultado

    except Exception as e:
        erro("Erro ao listar bebidas", "Bebida", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=BebidaSaida,
    summary="Obtém uma bebida pelo ID",
)
def obter(id: int):
    # Busca uma bebida pelo ID
    debug("Buscando bebida pelo ID", "Bebida", {"id": id})
    try:
        retorno = supabase.table("listar_bebida").select("*").eq("id", id).execute().data

        if not retorno:
            debug("Bebida não encontrada", "Bebida", {"id": id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bebida com ID {id} não encontrada."
            )

        debug("Bebida encontrada", "Bebida", {"bebida": retorno[0]})
        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao buscar bebida", "Bebida", {"erro": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@endpoint.patch(
    "/{id}",
    response_model=BebidaSaida,
    summary="Atualiza completamente ou parcialmente uma bebida pelo ID",
)
def atualizar(id: int, bebida: BebidaEntradaPatch):
    # Atualiza os dados de uma bebida existente
    debug("Atualizando bebida", "Bebida", {"id": id, "dados": bebida.dict()})
    try:
        parametros = {"p_id": id}

        if bebida.nome is not None:
            parametros["p_nome"] = bebida.nome
        if bebida.preco is not None:
            parametros["p_preco"] = bebida.preco
        if bebida.estoque is not None:
            parametros["p_estoque"] = bebida.estoque
        if bebida.ativo is not None:
            parametros["p_ativo"] = bebida.ativo

        retorno = supabase.rpc("atualizar_bebida", parametros).execute()
        debug("Bebida atualizada", "Bebida", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao atualizar bebida", "Bebida", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
