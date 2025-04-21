CREATE OR REPLACE VIEW listar_operacoes AS
SELECT 
    o.id AS operacao_id,
    o.data_operacao,
    o.saldo_gasto,
    
    json_build_object(
        'id', c.id,
        'nome', c.nome,
        'cpf', c.cpf,
        'saldo', c.saldo_restante,
        'data_nascimento', c.data_nascimento
    ) AS cliente,
    
    json_build_object(
        'id', cp.id,
        'capacidade', cp.capacidade,
        'codigo_nfc', cp.codigo_nfc,
        'permite_alcool', cp.permite_alcool
    ) AS copo,
    
    json_build_object(
        'id', m.id,
        'nome', m.nome,
        'qtd_reservatorio_atual', m.qtd_reservatorio_atual,
        'qtd_reservatorio_max', m.qtd_reservatorio_max
    ) AS maquina,
    
    json_build_object(
        'id', b.id,
        'nome', b.nome,
        'preco', b.preco,
        'descricao', b.descricao,
        'alcolica', b.alcolica
    ) AS bebida
FROM 
    operacao o
JOIN 
    cliente c ON o.cliente_id = c.id
JOIN 
    copo cp ON o.copo_id = cp.id
JOIN 
    maquina m ON o.maquina_id = m.id
JOIN 
    bebida b ON o.bebida_id = b.id;
