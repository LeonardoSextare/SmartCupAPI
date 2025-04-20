CREATE OR REPLACE VIEW listar_copo AS
SELECT 
  c.id AS id,
  c.capacidade,
  c.data_criacao,
  c.ativo,
  c.permite_alcool,
  c.codigo_nfc,
  CASE 
    WHEN cli.id IS NOT NULL THEN json_build_object(
        'id', cli.id,
        'nome', cli.nome,
        'cpf', cli.cpf,
        'data_nascimento', cli.data_nascimento,
        'ativo', cli.ativo,
        'saldo_restante', cli.saldo_restante
    )
    ELSE NULL
  END AS cliente
FROM copo c
LEFT JOIN cliente cli ON c.cliente_id = cli.id;
