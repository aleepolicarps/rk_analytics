-- dev --
CREATE TABLE user_actions(
    id SERIAL PRIMARY KEY NOT NULL,
    account CHAR(255),
    action CHAR(120),
    user_id INT,
    customer_id CHAR(64),
    web_id CHAR(64),
    first_name CHAR(64),
    last_name CHAR(64),
    email CHAR(120),
    ip_address CHAR(255),
    referrer_url CHAR(510),
    session CHAR(255),
    section CHAR(255),
    subsection CHAR(255),
    value CHAR(255),
    utm_source CHAR(120),
    utm_medium CHAR(120),
    utm_campaign CHAR(120),
    utm_term CHAR(120),
    utm_content CHAR(120)
);


CREATE INDEX idx_account ON user_actions (account);
CREATE INDEX idx_section ON user_actions (section);
CREATE INDEX idx_section_subsection ON user_actions (section, subsection);

-- end dev --

-- production --
CREATE TABLE user_actions(
    id INT IDENTITY(1, 1) NOT NULL,
    account CHAR(255),
    action CHAR(120),
    user_id INT,
    customer_id CHAR(64),
    web_id CHAR(64),
    first_name CHAR(64),
    last_name CHAR(64),
    email CHAR(120),
    ip_address CHAR(255),
    referrer_url CHAR(510),
    session CHAR(255),
    section CHAR(255),
    subsection CHAR(255),
    value CHAR(255),
    utm_source CHAR(120),
    utm_medium CHAR(120),
    utm_campaign CHAR(120),
    utm_term CHAR(120),
    utm_content CHAR(120)
);
-- end production --
