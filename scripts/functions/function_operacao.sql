CREATE OR REPLACE FUNCTION inserir_operacao(
    p_saldo_gasto NUMERIC,
    p_cliente_id INT,
    p_maquina_id INT,
    p_copo_id INT,
    p_bebida_id INT
)
RETURNS TABLE (
    operacao_id INT,
    data_operacao TIMESTAMP,
    saldo_gasto NUMERIC,
    cliente JSON,
    copo JSON,
    maquina JSON,
    bebida JSON
) AS $$
DECLARE
    v_operacao_id INT;
    v_data_operacao TIMESTAMP;
    v_saldo_gasto NUMERIC;
BEGIN
    -- Insere a operação na tabela operacao
    INSERT INTO operacao (cliente_id, maquina_id, copo_id, bebida_id, saldo_gasto, data_operacao)
    VALUES (p_cliente_id, p_maquina_id, p_copo_id, p_bebida_id, p_saldo_gasto, NOW())
    RETURNING operacao.id AS operacao_id, 
              operacao.data_operacao, 
              operacao.saldo_gasto
    INTO v_operacao_id, v_data_operacao, v_saldo_gasto;

    -- Retorna os objetos relacionados como JSON
    RETURN QUERY
    SELECT
        v_operacao_id,
        v_data_operacao,
        v_saldo_gasto,
        (
            SELECT row_to_json(c)
            FROM (
                SELECT id, nome, cpf, saldo_restante AS saldo, data_nascimento
                FROM cliente
                WHERE id = p_cliente_id
            ) c
        ) AS cliente,
        (
            SELECT row_to_json(cp)
            FROM (
                SELECT id, capacidade, codigo_nfc, permite_alcool
                FROM copo
                WHERE id = p_copo_id
            ) cp
        ) AS copo,
        (
            SELECT row_to_json(m)
            FROM (
                SELECT id, nome, qtd_reservatorio_atual, qtd_reservatorio_max
                FROM maquina
                WHERE id = p_maquina_id
            ) m
        ) AS maquina,
        (
            SELECT row_to_json(b)
            FROM (
                SELECT id, nome, preco, descricao, alcolica
                FROM bebida
                WHERE id = p_bebida_id
            ) b
        ) AS bebida;
END;
$$ LANGUAGE plpgsql;