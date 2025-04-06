-- Active: 1743954815830@@aws-0-sa-east-1.pooler.supabase.com@6543@postgres@public

CREATE TABLE bebida (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10, 2) NOT NULL,
    alcolica BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE maquina (
    id SERIAL PRIMARY KEY,
    qtd_reservatorio_max NUMERIC(10, 2) NOT NULL,
    qtd_reservatorio_atual NUMERIC(10, 2) NOT NULL,
    bebida_id INTEGER NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_bebida_maquina FOREIGN KEY (bebida_id) REFERENCES bebida (id) ON DELETE RESTRICT
);

CREATE TABLE copo (
    id SERIAL PRIMARY KEY,
    capacidade NUMERIC(10, 2) NOT NULL,
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW(),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    permite_alcool BOOLEAN NOT NULL DEFAULT FALSE,
    codigo_nfc VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    data_nascimento DATE NOT NULL,
    saldo_restante NUMERIC(10, 2) NOT NULL DEFAULT 0
);

CREATE TABLE administrador (
    id SERIAL PRIMARY KEY,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    nome VARCHAR(100) NOT NULL,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);

CREATE TABLE operacao (
    id SERIAL PRIMARY KEY,
    data_operacao TIMESTAMP NOT NULL DEFAULT NOW(),
    cliente_id INTEGER NOT NULL,
    maquina_id INTEGER NOT NULL,
    copo_id INTEGER NOT NULL,
    bebida_id INTEGER NOT NULL,
    saldo_gasto NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_cliente_operacao FOREIGN KEY (cliente_id) REFERENCES cliente (id) ON DELETE RESTRICT,
    CONSTRAINT fk_maquina_operacao FOREIGN KEY (maquina_id) REFERENCES maquina (id) ON DELETE RESTRICT,
    CONSTRAINT fk_copo_operacao FOREIGN KEY (copo_id) REFERENCES copo (id) ON DELETE RESTRICT,
    CONSTRAINT fk_bebida_operacao FOREIGN KEY (bebida_id) REFERENCES bebida (id) ON DELETE RESTRICT
);
