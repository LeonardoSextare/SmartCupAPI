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
                    "p_nome": f"{administrador.nome}",
                    "p_login": f"{administrador.login}",
                    "p_senha": f"{administrador.senha}",
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
def atualizar(id: int, item: AdministradorEntrada):  # type: ignore
    try:
        parametros = {"p_id": id}

        if item.nome is not None:
            parametros["p_nome"] = item.nome
        if item.login is not None:
            parametros["p_login"] = item.login
        if item.senha is not None:
            parametros["p_senha"] = item.senha
        if item.ativo is not None:
            parametros["p_ativo"] = item.ativo

        resposta = supabase.rpc("atualizar_administrador", parametros).execute()
        
        return resposta.data 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
