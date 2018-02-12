-- dev --
CREATE TABLE transactions(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    merchant_user_id VARCHAR(255),
    transaction_type VARCHAR(120),
    mode VARCHAR(15),
    code INT,
    amount REAL,
    currency VARCHAR(15),
    card_holder VARCHAR(255),
    brand VARCHAR(255),
    bank VARCHAR(255),
    level VARCHAR(255),
    type VARCHAR(255),
    bin VARCHAR(255),
    last VARCHAR(255),
    exp_month VARCHAR(255),
    exp_year VARCHAR(255),
    bank_id INT,
    bank_authcode VARCHAR(255),
    bank_time VARCHAR(255),
    charge_time VARCHAR(255),
    token VARCHAR(255),
    reference VARCHAR(255),
    base_reference VARCHAR(255),
    transaction_unique_id VARCHAR(255),
    fraudulent BOOLEAN default false,
    created_at TIMESTAMPTZ,
    response TEXT,
    webid VARCHAR(15),
    country VARCHAR (255),
    original_id INT,
    status VARCHAR(120)
);
-- end dev --

-- production --
CREATE TABLE transactions(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    merchant_user_id VARCHAR(255),
    transaction_type VARCHAR(120),
    mode VARCHAR(15),
    code INT,
    amount REAL,
    currency VARCHAR(15),
    card_holder VARCHAR(255),
    brand VARCHAR(255),
    bank VARCHAR(255),
    level VARCHAR(255),
    type VARCHAR(255),
    bin VARCHAR(255),
    last VARCHAR(255),
    exp_month VARCHAR(255),
    exp_year VARCHAR(255),
    bank_id INT,
    bank_authcode VARCHAR(255),
    bank_time VARCHAR(255),
    charge_time VARCHAR(255),
    token VARCHAR(255),
    reference VARCHAR(255),
    base_reference VARCHAR(255),
    transaction_unique_id VARCHAR(255),
    fraudulent BOOLEAN default false,
    created_at TIMESTAMPTZ,
    response varchar(MAX),
    webid VARCHAR(15),
    country VARCHAR (255),
    original_id INT,
    status VARCHAR(120)
);
-- end production --
