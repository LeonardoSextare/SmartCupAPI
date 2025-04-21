from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .AdministradorSchemas import AdministradorEntrada, AdministradorEntradaPatch, AdministradorSaida, AdministradorSaidaLista
from debug import debug, erro

endpoint = APIRouter()

@endpoint.post(
    "",
    response_model=AdministradorSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo administrador",
)
def criar(adm: AdministradorEntrada):
    # Cadastra um novo administrador no banco de dados
    debug("Iniciando cadastro de administrador", "Administrador", {"administrador": adm.dict()})
    try:
        retorno = supabase.rpc(
            "inserir_administrador",
            {
                "p_nome": adm.nome,
                "p_login": adm.login,
                "p_senha": adm.senha,
            },
        ).execute()
        debug("Administrador cadastrado com sucesso", "Administrador", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao cadastrar administrador", "Administrador", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=AdministradorSaidaLista,
    summary="Lista todos os administradores",
)
def listar():
    # Lista todos os administradores cadastrados
    debug("Listando todos os administradores", "Administrador")
    try:
        retorno = supabase.table("listar_administrador").select("*").execute().data
        resultado = {"quantidade": len(retorno), "resultado": retorno}
        debug("Administradores listados", "Administrador", {"quantidade": resultado["quantidade"]})
        return resultado

    except Exception as e:
        erro("Erro ao listar administradores", "Administrador", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=AdministradorSaida,
    summary="Obtém um administrador pelo ID",
)
def obter(id: int):
    # Busca um administrador pelo ID
    debug("Buscando administrador pelo ID", "Administrador", {"id": id})
    try:
        retorno = supabase.table("listar_administrador").select("*").eq("id", id).execute().data

        if not retorno:
            debug("Administrador não encontrado", "Administrador", {"id": id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Administrador com ID {id} não encontrado."
            )

        debug("Administrador encontrado", "Administrador", {"administrador": retorno[0]})
        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao buscar administrador", "Administrador", {"erro": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@endpoint.patch(
    "/{id}",
    response_model=AdministradorSaida,
    summary="Atualiza completamente ou parcialmente um administrador pelo ID",
)
def atualizar(id: int, adm: AdministradorEntradaPatch):
    # Atualiza os dados de um administrador existente
    debug("Atualizando administrador", "Administrador", {"id": id, "dados": adm.dict()})
    try:
        parametros = {"p_id": id}

        if adm.nome is not None:
            parametros["p_nome"] = adm.nome
        if adm.login is not None:
            parametros["p_login"] = adm.login
        if adm.senha is not None:
            parametros["p_senha"] = adm.senha
        if adm.ativo is not None:
            parametros["p_ativo"] = adm.ativo

        retorno = supabase.rpc("atualizar_administrador", parametros).execute()
        debug("Administrador atualizado", "Administrador", {"retorno": retorno.data})
        return retorno.data

    except Exception as e:
        erro("Erro ao atualizar administrador", "Administrador", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
