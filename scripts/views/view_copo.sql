CREATE OR REPLACE VIEW listar_copos AS
SELECT 
  json_build_object(
    'id', c.id,
    'capacidade', c.capacidade,
    'data_criacao', c.data_criacao,
    'ativo', c.ativo,
    'permite_alcool', c.permite_alcool,
    'codigo_nfc', c.codigo_nfc,

    'cliente', CASE 
                 WHEN cli.id IS NOT NULL THEN json_build_object(
                   'id', cli.id,
                   'nome', cli.nome,
                   'cpf', cli.cpf,
                   'data_nascimento', cli.data_nascimento,
                   'ativo', cli.ativo,
                   'saldo_restante', cli.saldo_restante
                 )
                 ELSE NULL
               END
  ) AS copos
FROM copo c
LEFT JOIN cliente cli ON c.cliente_id = cli.id;
