CREATE OR REPLACE VIEW listar_maquina AS
SELECT 
  json_build_object(
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
  ) AS maquinas
FROM maquina m
LEFT JOIN bebida b ON m.bebida_id = b.id;
