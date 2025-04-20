from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .AdministradorSchemas import AdministradorEntrada, AdministradorSaida, AdministradorSaidaLista

endpoint = APIRouter()


@endpoint.post(
    "",
    response_model=AdministradorSaida,
    status_code=status.HTTP_201_CREATED,
    summary=f"Cria um novo administrador",
)
def criar(administrador: AdministradorEntrada):
    try:
        retorno = (
            supabase.rpc(
                "inserir_administrador",
                {
                    "p_nome": administrador.nome,
                    "p_login": administrador.login,
                    "p_senha": administrador.senha,
                    "p_ativo": administrador.ativo,
                },
            )
            .execute()
            .data
        )

        return retorno

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "",
    response_model=AdministradorSaidaLista,
    summary=f"Lista todos os administradores",
)
def listar():
    try:
        retorno = supabase.table("listar_administrador").select("*").execute().data
        print(retorno)
        resultado = {"quantidade": len(retorno), "resultado": retorno}

        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.get(
    "/{id}",
    response_model=AdministradorSaida,
    summary=f"Obtem um admnistrador pelo ID",
)
def obter(id: int):
    try:
        resultado = supabase.rpc("obter_administrador_id", {"p_id": id}).execute().data
        return resultado

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@endpoint.patch(
    "/{id}",
    response_model=AdministradorSaida,
    summary=f"Atualiza completamente ou parcialmente um Administrador pelo ID",
)
def atualizar(id: int, administrador: AdministradorEntrada):  # type: ignore
    try:
        parametros = {"p_id": id}

        if administrador.nome is not None:
            parametros["p_nome"] = administrador.nome
        if administrador.login is not None:
            parametros["p_login"] = administrador.login
        if administrador.senha is not None:
            parametros["p_senha"] = administrador.senha
        if administrador.ativo is not None:
            parametros["p_ativo"] = administrador.ativo

        resposta = supabase.rpc("atualizar_administrador", parametros).execute()

        return resposta.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
