CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    Texto VARCHAR(100),
    fechaHora TIMESTAMP,
    Sistema VARCHAR(100),
    Estado BOOLEAN
);