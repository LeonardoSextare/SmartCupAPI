CREATE OR REPLACE FUNCTION inserir_maquina(
    p_nome VARCHAR,
    p_qtd_reservatorio_max NUMERIC,
    p_qtd_reservatorio_atual NUMERIC,
    p_bebida_id INTEGER DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT TRUE
)
RETURNS JSON AS $$
DECLARE
    novo_id INTEGER;
    result JSON;
BEGIN
    -- Validação: verificar se a bebida existe, se fornecida
    IF p_bebida_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM bebida WHERE id = p_bebida_id) THEN
        RAISE EXCEPTION 'Bebida com ID % não encontrada.', p_bebida_id;
    END IF;

    -- Inserir registro na tabela maquina e capturar o ID gerado
    INSERT INTO maquina (nome, qtd_reservatorio_max, qtd_reservatorio_atual, bebida_id, ativo)
    VALUES (p_nome, p_qtd_reservatorio_max, p_qtd_reservatorio_atual, p_bebida_id, p_ativo)
    RETURNING id INTO novo_id;

    -- Retornar a máquina inserida com a bebida como JSON
    SELECT json_build_object(
        'id', m.id,
        'nome', m.nome,
        'qtd_reservatorio_max', m.qtd_reservatorio_max,
        'qtd_reservatorio_atual', m.qtd_reservatorio_atual,
        'ativo', m.ativo,
        'bebida', CASE
            WHEN b.id IS NOT NULL THEN json_build_object(
                'id', b.id,
                'nome', b.nome,
                'descricao', b.descricao,
                'preco', b.preco,
                'alcolica', b.alcolica,
                'ativo', b.ativo
            )
            ELSE NULL
        END
    )
    INTO result
    FROM maquina m
    LEFT JOIN bebida b ON m.bebida_id = b.id
    WHERE m.id = novo_id;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION obter_maquina_id(p_id INTEGER)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'id', m.id,
        'nome', m.nome,
        'qtd_reservatorio_max', m.qtd_reservatorio_max,
        'qtd_reservatorio_atual', m.qtd_reservatorio_atual,
        'ativo', m.ativo,
        'bebida', CASE
            WHEN b.id IS NOT NULL THEN json_build_object(
                'id', b.id,
                'nome', b.nome,
                'descricao', b.descricao,
                'preco', b.preco,
                'alcolica', b.alcolica,
                'ativo', b.ativo
            )
            ELSE NULL
        END
    )
    INTO result
    FROM maquina m
    LEFT JOIN bebida b ON m.bebida_id = b.id
    WHERE m.id = p_id;

    IF result IS NULL THEN
        RAISE EXCEPTION 'Máquina com ID % não encontrada.', p_id;
    END IF;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualizar_maquina(
    p_id INTEGER,
    p_nome VARCHAR DEFAULT NULL,
    p_qtd_reservatorio_max NUMERIC DEFAULT NULL,
    p_qtd_reservatorio_atual NUMERIC DEFAULT NULL,
    p_bebida_id INTEGER DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT NULL
)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    -- Validação: verificar se a máquina existe
    IF NOT EXISTS (SELECT 1 FROM maquina WHERE id = p_id) THEN
        RAISE EXCEPTION 'Máquina com ID % não encontrada.', p_id;
    END IF;

    -- Validação: verificar se a bebida existe, se fornecida (permitir NULL)
    IF p_bebida_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM bebida WHERE id = p_bebida_id) THEN
        RAISE EXCEPTION 'Bebida com ID % não encontrada.', p_bebida_id;
    END IF;

    -- Atualizar registro na tabela maquina
    UPDATE maquina
    SET
        nome = COALESCE(p_nome, nome),
        qtd_reservatorio_max = COALESCE(p_qtd_reservatorio_max, qtd_reservatorio_max),
        qtd_reservatorio_atual = COALESCE(p_qtd_reservatorio_atual, qtd_reservatorio_atual),
        bebida_id = p_bebida_id, -- Permitir NULL diretamente
        ativo = COALESCE(p_ativo, ativo)
    WHERE id = p_id;

    -- Retornar a máquina atualizada com a bebida como JSON
    SELECT json_build_object(
        'id', m.id,
        'nome', m.nome,
        'qtd_reservatorio_max', m.qtd_reservatorio_max,
        'qtd_reservatorio_atual', m.qtd_reservatorio_atual,
        'ativo', m.ativo,
        'bebida', CASE
            WHEN b.id IS NOT NULL THEN json_build_object(
                'id', b.id,
                'nome', b.nome,
                'descricao', b.descricao,
                'preco', b.preco,
                'alcolica', b.alcolica,
                'ativo', b.ativo
            )
            ELSE NULL
        END
    )
    INTO result
    FROM maquina m
    LEFT JOIN bebida b ON m.bebida_id = b.id
    WHERE m.id = p_id;

    RETURN result;
END;
$$ LANGUAGE plpgsql;