CREATE OR REPLACE VIEW listar_maquina AS
SELECT 
  m.id,
  m.nome,
  m.qtd_reservatorio_max,
  m.qtd_reservatorio_atual,
  m.ativo,
  CASE
    WHEN b.id IS NOT NULL THEN json_build_object(
      'id', b.id,
      'nome', b.nome,
      'descricao', b.descricao,
      'preco', b.preco,
      'alcolica', b.alcolica,
      'ativo', b.ativo
    )
    ELSE NULL
  END AS bebida
FROM maquina m
LEFT JOIN bebida b ON m.bebida_id = b.id;
