from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .CopoSchemas import CopoEntrada, CopoSaida, CopoSaidaLista, CopoEntradaPatch
from debug import debug, erro

endpoint = APIRouter()

@endpoint.post(
    "",
    response_model=CopoSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo copo",
)
def criar(copo: CopoEntrada):
    # Cadastra um novo copo no banco de dados
    debug("Iniciando cadastro de copo", "Copo", {"copo": copo.dict()})
    try:
        retorno = supabase.rpc(
            "inserir_copo",
            {
                "p_codigo_nfc": copo.codigo_nfc,
                "p_capacidade": copo.capacidade,
                "p_permite_alcool": copo.permite_alcool,
                "p_cliente_id": copo.cliente_id,
            },
        ).execute()
        debug("Copo cadastrado com sucesso", "Copo", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao cadastrar copo", "Copo", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=CopoSaidaLista,
    summary="Lista todos os copos",
)
def listar():
    # Lista todos os copos cadastrados
    debug("Listando todos os copos", "Copo")
    try:
        retorno = supabase.table("listar_copo").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        debug("Copos listados", "Copo", {"quantidade": resultado["quantidade"]})
        return resultado

    except Exception as e:
        erro("Erro ao listar copos", "Copo", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=CopoSaida,
    summary="Obtém um copo pelo ID",
)
def obter(id: int):
    # Busca um copo pelo ID
    debug("Buscando copo pelo ID", "Copo", {"id": id})
    try:
        retorno = supabase.table("listar_copo").select("*").eq("id", id).execute().data

        if not retorno:
            debug("Copo não encontrado", "Copo", {"id": id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Copo com ID {id} não encontrado."
            )

        debug("Copo encontrado", "Copo", {"copo": retorno[0]})
        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao buscar copo", "Copo", {"erro": str(e)})
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
    # Atualiza os dados de um copo existente
    debug("Atualizando copo", "Copo", {"id": id, "dados": copo.dict()})
    try:
        parametros = {"p_id": id}

        if copo.codigo_nfc is not None:
            parametros["p_codigo_nfc"] = copo.codigo_nfc
        if copo.capacidade is not None:
            parametros["p_capacidade"] = copo.capacidade
        if copo.permite_alcool is not None:
            parametros["p_permite_alcool"] = copo.permite_alcool
        if copo.cliente_id is not None:
            parametros["p_cliente_id"] = copo.cliente_id

        retorno = supabase.rpc("atualizar_copo", parametros).execute()
        debug("Copo atualizado", "Copo", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao atualizar copo", "Copo", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))