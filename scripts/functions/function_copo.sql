-- Inserir
CREATE OR REPLACE FUNCTION inserir_copo(
    p_capacidade NUMERIC,
    p_codigo_nfc VARCHAR,
    p_cliente_id INTEGER DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT TRUE,
    p_permite_alcool BOOLEAN DEFAULT FALSE
)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    -- Validação: capacidade deve ser maior que 0
    IF p_capacidade <= 0 THEN
        RAISE EXCEPTION 'Capacidade inválida. Deve ser maior que 0.';
    END IF;

    -- Validação: código NFC deve ser único
    IF EXISTS (SELECT 1 FROM copo WHERE codigo_nfc = p_codigo_nfc) THEN
        RAISE EXCEPTION 'Código NFC % já está em uso.', p_codigo_nfc;
    END IF;

    -- Validação: cliente deve existir, se fornecido
    IF p_cliente_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM cliente WHERE id = p_cliente_id) THEN
        RAISE EXCEPTION 'Cliente com ID % não encontrado.', p_cliente_id;
    END IF;

    -- Inserir registro na tabela copo
    INSERT INTO copo (capacidade, codigo_nfc, ativo, permite_alcool, cliente_id)
    VALUES (p_capacidade, p_codigo_nfc, p_ativo, p_permite_alcool, p_cliente_id);

    -- Retornar o copo inserido com o JSON do cliente (ou NULL se cliente_id for NULL)
    SELECT json_build_object(
        'id', c.id,
        'capacidade', c.capacidade,
        'codigo_nfc', c.codigo_nfc,
        'ativo', c.ativo,
        'data_criacao', c.data_criacao,
        'permite_alcool', c.permite_alcool,
        'cliente', CASE
            WHEN cl.id IS NOT NULL THEN json_build_object(
                'id', cl.id,
                'nome', cl.nome,
                'cpf', cl.cpf,
                'data_nascimento', cl.data_nascimento,
                'ativo', cl.ativo,
                'saldo_restante', cl.saldo_restante
            )
            ELSE NULL
        END
    )
    INTO result
    FROM copo c
    LEFT JOIN cliente cl ON c.cliente_id = cl.id
    WHERE c.codigo_nfc = p_codigo_nfc; -- Garantir que estamos pegando o copo recém-inserido

    RETURN result;
END;
$$ LANGUAGE plpgsql;


-- Atualizar
CREATE OR REPLACE FUNCTION atualizar_copo(
    p_id INTEGER,
    p_capacidade NUMERIC DEFAULT NULL,
    p_codigo_nfc VARCHAR DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT NULL,
    p_permite_alcool BOOLEAN DEFAULT NULL,
    p_cliente_id INTEGER DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    -- Validação: verificar se o copo existe
    IF NOT EXISTS (SELECT 1 FROM copo WHERE id = p_id) THEN
        RAISE EXCEPTION 'Copo com ID % não encontrado.', p_id;
    END IF;

    -- Validação: capacidade deve ser maior que 0, se fornecida
    IF p_capacidade IS NOT NULL AND p_capacidade <= 0 THEN
        RAISE EXCEPTION 'Capacidade inválida. Deve ser maior que 0.';
    END IF;

    -- Validação: código NFC deve ser único, se fornecido
    IF p_codigo_nfc IS NOT NULL AND EXISTS (SELECT 1 FROM copo WHERE codigo_nfc = p_codigo_nfc AND id != p_id) THEN
        RAISE EXCEPTION 'Código NFC % já está em uso.', p_codigo_nfc;
    END IF;

    -- Validação: cliente deve existir, se fornecido
    IF p_cliente_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM cliente WHERE id = p_cliente_id) THEN
        RAISE EXCEPTION 'Cliente com ID % não encontrado.', p_cliente_id;
    END IF;

    -- Atualizar registro na tabela copo
    UPDATE copo
    SET
        capacidade = COALESCE(p_capacidade, capacidade),
        codigo_nfc = COALESCE(p_codigo_nfc, codigo_nfc),
        ativo = COALESCE(p_ativo, ativo),
        permite_alcool = COALESCE(p_permite_alcool, permite_alcool),
        cliente_id = COALESCE(p_cliente_id, cliente_id)
    WHERE id = p_id;

    -- Retornar o copo atualizado com o JSON do cliente (ou NULL se cliente_id for NULL)
    SELECT json_build_object(
        'id', c.id,
        'capacidade', c.capacidade,
        'codigo_nfc', c.codigo_nfc,
        'ativo', c.ativo,
        'data_criacao', c.data_criacao,
        'permite_alcool', c.permite_alcool,
        'cliente', CASE
            WHEN cl.id IS NOT NULL THEN json_build_object(
                'id', cl.id,
                'nome', cl.nome,
                'cpf', cl.cpf,
                'data_nascimento', cl.data_nascimento,
                'ativo', cl.ativo,
                'saldo_restante', cl.saldo_restante
            )
            ELSE NULL
        END
    )
    INTO result
    FROM copo c
    LEFT JOIN cliente cl ON c.cliente_id = cl.id
    WHERE c.id = p_id;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
