-- Inserir
CREATE OR REPLACE FUNCTION inserir_cliente(
    p_nome VARCHAR,
    p_cpf VARCHAR,
    p_data_nascimento DATE,
    p_saldo_restante NUMERIC DEFAULT 0,
    p_ativo BOOLEAN DEFAULT TRUE
)
RETURNS cliente AS $$
DECLARE
    v_cliente cliente;
BEGIN
    -- Valida tamanho do CPF (sem pontuação)
    IF LENGTH(p_cpf) != 11 THEN
        RAISE EXCEPTION 'CPF inválido. Deve conter exatamente 11 caracteres numéricos.';
    END IF;

    -- Verifica se já existe CPF igual
    IF EXISTS (SELECT 1 FROM cliente WHERE cpf = p_cpf) THEN
        RAISE EXCEPTION 'Já existe um cliente com o CPF: %', p_cpf;
    END IF;

    INSERT INTO cliente (nome, cpf, data_nascimento, saldo_restante, ativo)
    VALUES (p_nome, p_cpf, p_data_nascimento, p_saldo_restante, p_ativo)
    RETURNING * INTO v_cliente;

    RETURN v_cliente;
END;
$$ LANGUAGE plpgsql;



-- Obter
CREATE OR REPLACE FUNCTION obter_cliente_id(
    p_id INTEGER
)
RETURNS cliente AS $$
DECLARE
    v_cliente cliente;
BEGIN
    SELECT * INTO v_cliente
    FROM cliente
    WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Cliente com ID % não encontrado.', p_id;
    END IF;

    RETURN v_cliente;
END;
$$ LANGUAGE plpgsql;


-- Atualizar
CREATE OR REPLACE FUNCTION atualizar_cliente(
    p_id INTEGER,
    p_nome VARCHAR DEFAULT NULL,
    p_cpf VARCHAR DEFAULT NULL,
    p_data_nascimento DATE DEFAULT NULL,
    p_saldo_restante NUMERIC DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT NULL
)
RETURNS cliente AS $$
DECLARE
    v_cliente cliente;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE id = p_id) THEN
        RAISE EXCEPTION 'Cliente com ID % não encontrado.', p_id;
    END IF;

    -- Valida CPF se for informado
    IF p_cpf IS NOT NULL THEN
        IF LENGTH(p_cpf) != 11 THEN
            RAISE EXCEPTION 'CPF inválido. Deve conter exatamente 11 caracteres numéricos.';
        END IF;

        IF EXISTS (SELECT 1 FROM cliente WHERE cpf = p_cpf AND id != p_id) THEN
            RAISE EXCEPTION 'Já existe outro cliente com o CPF: %', p_cpf;
        END IF;
    END IF;

    UPDATE cliente
    SET
        nome = COALESCE(p_nome, nome),
        cpf = COALESCE(p_cpf, cpf),
        data_nascimento = COALESCE(p_data_nascimento, data_nascimento),
        saldo_restante = COALESCE(p_saldo_restante, saldo_restante),
        ativo = COALESCE(p_ativo, ativo)
    WHERE id = p_id;

    SELECT * INTO v_cliente FROM cliente WHERE id = p_id;
    RETURN v_cliente;
END;
$$ LANGUAGE plpgsql;
