-- dev --
CREATE TABLE chargebacks(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    merchant_user_id VARCHAR(255),
    webid VARCHAR(15),
    country VARCHAR (255),
    original_id INT,
    status VARCHAR(120),
    type VARCHAR(120),
    mode VARCHAR(15),
    amount REAL,
    currency VARCHAR(15),
    bank_id INT,
    bank_authcode VARCHAR(255),
    bank_time VARCHAR(255),
    bank_update_time VARCHAR(255),
    reference VARCHAR(255),
    base_reference VARCHAR(255),
    transaction_unique_id VARCHAR(255),
    created_at TIMESTAMPTZ,
    custom_mid_name VARCHAR(255),
    response TEXT,
    time VARCHAR(255)
);
-- end dev --

-- production --
CREATE TABLE chargebacks(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    merchant_user_id VARCHAR(255),
    webid VARCHAR(15),
    country VARCHAR (255),
    original_id INT,
    status VARCHAR(120),
    type VARCHAR(120),
    mode VARCHAR(15),
    amount REAL,
    currency VARCHAR(15),
    bank_id INT,
    bank_authcode VARCHAR(255),
    bank_time VARCHAR(255),
    bank_update_time VARCHAR(255),
    reference VARCHAR(255),
    base_reference VARCHAR(255),
    transaction_unique_id VARCHAR(255),
    created_at TIMESTAMPTZ,
    custom_mid_name VARCHAR(255),
    response varchar(MAX),
    time VARCHAR(255)
);
-- end production --
