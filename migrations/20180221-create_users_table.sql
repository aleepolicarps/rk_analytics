-- dev --
CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    customer_id VARCHAR(255),
    email VARCHAR(255),
    fname VARCHAR(255),
    lname VARCHAR(255),
    webid VARCHAR(255),
    country VARCHAR(255),
    pubid VARCHAR(255),
    subid VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_term VARCHAR(255),
    utm_content VARCHAR(255),
    utm_campaign VARCHAR(255),
    referrer_url VARCHAR(511),
    ip_address VARCHAR(255),
    click_id VARCHAR(255),
    user_agent VARCHAR(511),
    is_missing BOOLEAN,
    original_id INT,
    created_at TIMESTAMPTZ
)
-- end dev --

-- production --
CREATE TABLE users(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    customer_id VARCHAR(255),
    email VARCHAR(255),
    fname VARCHAR(255),
    lname VARCHAR(255),
    webid VARCHAR(255),
    country VARCHAR(255),
    pubid VARCHAR(255),
    subid VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_term VARCHAR(255),
    utm_content VARCHAR(255),
    utm_campaign VARCHAR(255),
    referrer_url VARCHAR(511),
    ip_address VARCHAR(255),
    click_id VARCHAR(255),
    user_agent VARCHAR(511),
    is_missing BOOLEAN,
    original_id INT,
    created_at TIMESTAMPTZ
)
-- end production --
