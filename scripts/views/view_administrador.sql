CREATE OR REPLACE VIEW listar_administrador AS
SELECT row_to_json(t) AS administradores
FROM (
    SELECT * FROM administrador
) AS t;
