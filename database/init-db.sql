CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    Texto VARCHAR(100),
    fechaHora TIMESTAMP,
    Sistema VARCHAR(100),
    Estado BOOLEAN
);

CREATE OR REPLACE FUNCTION notify_trigger() RETURNS trigger AS $$
DECLARE
    total_messages INT;
BEGIN
    -- Contar el total de registros por Sistema
    SELECT COUNT(*) INTO total_messages FROM connections WHERE Sistema = NEW.Sistema;

    -- Notificar con la carga útil incluyendo tipocliente, mensaje y total
    PERFORM pg_notify(
        'new_message',
        json_build_object(
            'id', NEW.id,
            'texto', NEW.Texto,
            'fechahora', NEW.fechaHora,
            'sistema', NEW.Sistema,
            'estado', NEW.Estado,
            'total', total_messages
        )::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER my_trigger
AFTER INSERT OR UPDATE ON connections
FOR EACH ROW EXECUTE FUNCTION notify_trigger();