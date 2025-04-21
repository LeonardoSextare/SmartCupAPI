from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .ClienteSchemas import ClienteEntrada, ClienteSaida, ClienteSaidaLista, ClienteEntradaPatch

endpoint = APIRouter()


@endpoint.post(
    "",
    response_model=ClienteSaida,
    status_code=status.HTTP_201_CREATED,
    summary=f"Cria um novo cliente",
)
def criar(cliente: ClienteEntrada):
    try:
        retorno = supabase.rpc(
            "inserir_cliente",
            {
                "p_nome": cliente.nome,
                "p_cpf": cliente.cpf,
                "p_data_nascimento": cliente.data_nascimento.isoformat(),
                "p_saldo_restante": 0,
            },
        ).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=ClienteSaidaLista,
    summary=f"Lista todos os clientes",
)
def listar():
    try:
        retorno = supabase.table("listar_cliente").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}

        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=ClienteSaida,
    summary="Obtém um cliente pelo ID",
)
def obter(id: int):
    try:
        retorno = supabase.table("listar_cliente").select("*").eq("id", id).execute().data

        if not retorno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {id} não encontrado."
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
    response_model=ClienteSaida,
    summary=f"Atualiza completamente ou parcialmente um cliente pelo ID",
)
def atualizar(id: int, cliente: ClienteEntradaPatch):
    try:
        parametros = {"p_id": id}

        if cliente.nome is not None:
            parametros["p_nome"] = cliente.nome
        if cliente.cpf is not None:
            parametros["p_cpf"] = cliente.cpf
        if cliente.data_nascimento is not None:
            parametros["p_data_nascimento"] = cliente.data_nascimento.isoformat()
        if cliente.saldo_restante is not None:
            parametros["p_saldo_restante"] = cliente.saldo_restante
        if cliente.ativo is not None:
            parametros["p_ativo"] = cliente.ativo

        retorno = supabase.rpc("atualizar_cliente", parametros).execute()

        return retorno.data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
