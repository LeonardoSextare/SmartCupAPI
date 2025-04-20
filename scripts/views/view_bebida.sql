CREATE OR REPLACE VIEW listar_bebida AS
SELECT row_to_json(t) AS bebidas
FROM (
    SELECT * FROM bebida
) AS t;
