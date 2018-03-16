-- dev --
CREATE TABLE backend_event(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    event VARCHAR(255),
    created_at TIMESTAMPTZ,
    value VARCHAR(255),
    status VARCHAR(120)
)
-- end dev --


-- production --
CREATE TABLE backend_event(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    event VARCHAR(255),
    created_at TIMESTAMPTZ,
    value VARCHAR(255),
    status VARCHAR(120)
)
-- end production --
