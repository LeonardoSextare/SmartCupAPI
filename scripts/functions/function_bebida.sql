-- Inserir

CREATE OR REPLACE FUNCTION inserir_bebida(
    p_nome VARCHAR,
    p_preco NUMERIC,
    p_descricao TEXT DEFAULT NULL,
    p_alcolica BOOLEAN DEFAULT FALSE,
    p_ativo BOOLEAN DEFAULT TRUE
)
RETURNS bebida AS $$
DECLARE
    v_bebida bebida;
BEGIN
    IF p_preco < 0 THEN
        RAISE EXCEPTION 'Preço inválido. Deve ser maior ou igual a 0.';
    END IF;

    INSERT INTO bebida (nome, descricao, preco, alcolica, ativo)
    VALUES (p_nome, p_descricao, p_preco, p_alcolica, p_ativo)
    RETURNING * INTO v_bebida;

    RETURN v_bebida;
END;
$$ LANGUAGE plpgsql;


-- Obter
CREATE OR REPLACE FUNCTION obter_bebida_id(
    p_id INTEGER
)
RETURNS bebida AS $$
DECLARE
    v_bebida bebida;
BEGIN
    SELECT * INTO v_bebida
    FROM bebida
    WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Bebida com ID % não encontrada.', p_id;
    END IF;

    RETURN v_bebida;
END;
$$ LANGUAGE plpgsql;


-- Atualizar
CREATE OR REPLACE FUNCTION atualizar_bebida(
    p_id INTEGER,
    p_nome VARCHAR DEFAULT NULL,
    p_descricao TEXT DEFAULT NULL,
    p_preco NUMERIC DEFAULT NULL,
    p_alcolica BOOLEAN DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT NULL
)
RETURNS bebida AS $$
DECLARE
    v_bebida bebida;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM bebida WHERE id = p_id) THEN
        RAISE EXCEPTION 'Bebida com ID % não encontrada.', p_id;
    END IF;

    IF p_preco IS NOT NULL AND p_preco < 0 THEN
        RAISE EXCEPTION 'Preço inválido. Deve ser maior ou igual a 0.';
    END IF;

    UPDATE bebida
    SET
        nome = COALESCE(p_nome, nome),
        descricao = COALESCE(p_descricao, descricao),
        preco = COALESCE(p_preco, preco),
        alcolica = COALESCE(p_alcolica, alcolica),
        ativo = COALESCE(p_ativo, ativo)
    WHERE id = p_id;

    SELECT * INTO v_bebida FROM bebida WHERE id = p_id;
    RETURN v_bebida;
END;
$$ LANGUAGE plpgsql;
