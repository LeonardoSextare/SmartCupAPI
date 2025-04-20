CREATE OR REPLACE VIEW listar_operacao AS
SELECT 
  json_build_object(
    'id', o.id,
    'data_operacao', o.data_operacao,
    'saldo_gasto', o.saldo_gasto,

    'cliente', json_build_object(
      'id', cli.id,
      'nome', cli.nome,
      'cpf', cli.cpf,
      'data_nascimento', cli.data_nascimento,
      'ativo', cli.ativo,
      'saldo_restante', cli.saldo_restante
    ),

    'copo', json_build_object(
      'id', c.id,
      'capacidade', c.capacidade,
      'data_criacao', c.data_criacao,
      'ativo', c.ativo,
      'permite_alcool', c.permite_alcool,
      'codigo_nfc', c.codigo_nfc
    ),

    'maquina', json_build_object(
      'id', m.id,
      'nome', m.nome,
      'qtd_reservatorio_max', m.qtd_reservatorio_max,
      'qtd_reservatorio_atual', m.qtd_reservatorio_atual,
      'ativo', m.ativo
    ),

    'bebida', json_build_object(
      'id', b.id,
      'nome', b.nome,
      'descricao', b.descricao,
      'preco', b.preco,
      'alcolica', b.alcolica,
      'ativo', b.ativo
    )
  ) AS operacoes
FROM
  operacao o
  JOIN cliente cli ON o.cliente_id = cli.id
  JOIN copo c ON o.copo_id = c.id
  JOIN maquina m ON o.maquina_id = m.id
  JOIN bebida b ON o.bebida_id = b.id;
