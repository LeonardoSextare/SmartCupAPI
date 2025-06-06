from fastapi import APIRouter, HTTPException, status
from supabase_api import supabase
from .OperacaoSchema import OperacaoSaidaLista, OperacaoSaida, OperacaoEntrada
from debug import debug, erro

endpoint = APIRouter()

@endpoint.get(
    "",
    response_model=OperacaoSaidaLista,
    summary="Lista todas as operações",
)
def listar():
    # Lista todas as operações registradas
    debug("Listando todas as operações", "Operacao")
    try:
        retorno = supabase.table("listar_operacoes").select("*").execute().data
        resposta = {"quantidade": len(retorno), "resultado": retorno}
        debug("Operações listadas", "Operacao", {"quantidade": resposta["quantidade"]})
        return resposta

    except Exception as e:
        erro("Erro ao listar operações", "Operacao", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@endpoint.post(
    "",
    response_model=OperacaoSaida,
    status_code=status.HTTP_201_CREATED,
    summary="Registra uma nova operação",
)
def criar(operacao: OperacaoEntrada):
    # Registra uma nova operação de uso do copo
    debug("Iniciando registro de operação", "Operacao", {"operacao": operacao.dict()})
    try:
        # Busca o copo pelo código NFC
        copo = supabase.table("copo").select("*").eq("codigo_nfc", operacao.codigo_nfc).execute().data
        if not copo:
            debug("Copo não encontrado", "Operacao", {"codigo_nfc": operacao.codigo_nfc})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Copo não encontrado.")
        copo = copo[0]

        # Verifica se o copo está associado a um cliente
        if not copo["cliente_id"]:
            debug("Copo sem cliente associado", "Operacao", {"copo_id": copo["id"]})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Copo não está associado a um cliente.")

        # Busca o cliente associado ao copo
        cliente = supabase.table("cliente").select("*").eq("id", copo["cliente_id"]).execute().data
        if not cliente:
            debug("Cliente associado ao copo não encontrado", "Operacao", {"cliente_id": copo["cliente_id"]})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente associado ao copo não encontrado.")
        cliente = cliente[0]

        # Busca a máquina pelo ID
        maquina = supabase.table("maquina").select("*").eq("id", operacao.maquina_id).execute().data
        if not maquina:
            debug("Máquina não encontrada", "Operacao", {"maquina_id": operacao.maquina_id})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Máquina não encontrada.")
        maquina = maquina[0]

        # Busca a bebida associada à máquina
        bebida = supabase.table("bebida").select("*").eq("id", maquina["bebida_id"]).execute().data
        if not bebida:
            debug("Bebida associada à máquina não encontrada", "Operacao", {"bebida_id": maquina["bebida_id"]})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bebida associada à máquina não encontrada.")
        bebida = bebida[0]

        # Regras de negócio
        if not copo["permite_alcool"] and bebida["alcolica"]:
            debug("Copo não permite bebidas alcoólicas", "Operacao", {"copo_id": copo["id"]})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Copo não permite bebidas alcoólicas.")

        if maquina["qtd_reservatorio_atual"] < copo["capacidade"]:
            debug("Máquina sem bebida suficiente", "Operacao", {"maquina_id": maquina["id"]})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Máquina sem bebida suficiente.")

        # Calcula o valor a ser descontado
        valor_a_descontar = (bebida["preco"] / 1000) * copo["capacidade"]
        if cliente["saldo_restante"] < valor_a_descontar:
            debug("Saldo insuficiente do cliente", "Operacao", {"cliente_id": cliente["id"]})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente do cliente.")

        # Atualizações no banco
        novo_saldo = cliente["saldo_restante"] - valor_a_descontar
        supabase.table("cliente").update({"saldo_restante": novo_saldo}).eq("id", cliente["id"]).execute()
        debug("Saldo do cliente atualizado", "Operacao", {"cliente_id": cliente["id"], "novo_saldo": novo_saldo})

        nova_quantidade_reservatorio = maquina["qtd_reservatorio_atual"] - copo["capacidade"]
        supabase.table("maquina").update({"qtd_reservatorio_atual": nova_quantidade_reservatorio}).eq("id", maquina["id"]).execute()
        debug("Quantidade do reservatório da máquina atualizada", "Operacao", {"maquina_id": maquina["id"], "nova_quantidade": nova_quantidade_reservatorio})

        # Inserção da operação
        retorno = supabase.rpc(
            "inserir_operacao",
            {
                "p_cliente_id": cliente["id"],
                "p_maquina_id": maquina["id"],
                "p_copo_id": copo["id"],
                "p_bebida_id": bebida["id"],
                "p_saldo_gasto": valor_a_descontar,
            },
        ).execute()

        debug("Operação registrada com sucesso", "Operacao", {"retorno": retorno.data[0]})
        return retorno.data[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao registrar operação", "Operacao", {"erro": str(e)})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


@endpoint.get(
    "/{id}",
    response_model=OperacaoSaida,
    summary="Retorna uma operação pelo ID",
)
def obter(id: int):
    # Busca uma operação pelo ID
    debug("Buscando operação pelo ID", "Operacao", {"id": id})
    try:
        retorno = supabase.table("listar_operacoes").select("*").eq("operacao_id", id).execute().data

        if not retorno:
            debug("Operação não encontrada", "Operacao", {"id": id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Operação com ID {id} não encontrada."
            )

        debug("Operação encontrada", "Operacao", {"operacao": retorno[0]})
        return retorno[0]

    except HTTPException:
        raise
    except Exception as e:
        erro("Erro ao buscar operação", "Operacao", {"erro": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )
