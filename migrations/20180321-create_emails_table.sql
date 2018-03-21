-- dev --
CREATE TABLE emails(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    recipient VARCHAR(255),
    sender VARCHAR(255),
    subject VARCHAR(255),
    send_date TIMESTAMPTZ,
    read_date TIMESTAMPTZ,
    ip_address VARCHAR(255),
    tracking_uuid VARCHAR(255),
    referrer_url VARCHAR(500)
)
-- end dev --


-- production --
CREATE TABLE emails(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    recipient VARCHAR(255),
    sender VARCHAR(255),
    subject VARCHAR(255),
    send_date TIMESTAMPTZ,
    read_date TIMESTAMPTZ,
    ip_address VARCHAR(255),
    tracking_uuid VARCHAR(255),
    referrer_url VARCHAR(500)
)
-- end production --
