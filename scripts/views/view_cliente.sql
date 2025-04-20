CREATE OR REPLACE VIEW  listar_cliente AS
SELECT row_to_json(t) as clientes
FROM (
SELECT * FROM cliente
) as t;

