
-- Inserir
CREATE OR REPLACE FUNCTION inserir_administrador(
    p_nome VARCHAR,
    p_login VARCHAR,
    p_senha VARCHAR,
    p_ativo BOOLEAN DEFAULT TRUE
)
RETURNS administrador AS $$
DECLARE
    v_admin administrador;
BEGIN
    -- Verifica se já existe um login igual
    IF EXISTS (SELECT 1 FROM administrador WHERE login = p_login) THEN
        RAISE EXCEPTION 'Já existe um administrador com esse login: %', p_login;
    END IF;

    -- Insere e retorna a linha completa
    INSERT INTO administrador (nome, login, senha, ativo)
    VALUES (p_nome, p_login, p_senha, p_ativo)
    RETURNING * INTO v_admin;

    RETURN v_admin;
END;
$$ LANGUAGE plpgsql;



-- Obter
CREATE OR REPLACE FUNCTION obter_administrador_id(
    p_id INTEGER
)
RETURNS administrador AS $$
DECLARE
    v_admin administrador;
BEGIN
    SELECT *
    INTO v_admin
    FROM administrador
    WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Administrador com ID % não encontrado.', p_id;
    END IF;

    RETURN v_admin;
END;
$$ LANGUAGE plpgsql;


-- Atualizar
CREATE OR REPLACE FUNCTION atualizar_administrador(
    p_id INTEGER,
    p_nome VARCHAR DEFAULT NULL,
    p_login VARCHAR DEFAULT NULL,
    p_senha VARCHAR DEFAULT NULL,
    p_ativo BOOLEAN DEFAULT NULL
)
RETURNS administrador AS $$
DECLARE
    v_admin administrador;
BEGIN
    -- Verifica se o ID existe
    IF NOT EXISTS (SELECT 1 FROM administrador WHERE id = p_id) THEN
        RAISE EXCEPTION 'Administrador com ID % não encontrado.', p_id;
    END IF;

    -- Verifica duplicidade de login, se foi passado
    IF p_login IS NOT NULL AND EXISTS (
        SELECT 1 FROM administrador WHERE login = p_login AND id != p_id
    ) THEN
        RAISE EXCEPTION 'Já existe outro administrador com o login: %', p_login;
    END IF;

    -- Atualiza somente os campos enviados (não-nulos)
    UPDATE administrador
    SET
        nome = COALESCE(p_nome, nome),
        login = COALESCE(p_login, login),
        senha = COALESCE(p_senha, senha),
        ativo = COALESCE(p_ativo, ativo)
    WHERE id = p_id;

    -- Retorna o registro atualizado
    SELECT * INTO v_admin FROM administrador WHERE id = p_id;
    RETURN v_admin;
END;
$$ LANGUAGE plpgsql;
