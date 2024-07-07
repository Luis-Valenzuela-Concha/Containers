CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    Texto VARCHAR(100),
    fechaHora TIMESTAMP,
    Sistema VARCHAR(100),
    Estado BOOLEAN
);

CREATE OR REPLACE FUNCTION last_tuple()
RETURNS TRIGGER AS $$
BEGIN
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER return_last_tuple
AFTER INSERT ON connections
FOR EACH ROW
EXECUTE FUNCTION last_tuple();