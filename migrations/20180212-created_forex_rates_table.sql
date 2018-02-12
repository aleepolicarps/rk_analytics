-- dev --
CREATE TABLE forex_rates(
    updated_at TIMESTAMPTZ DEFAULT now(),
    rate REAL,
    currency VARCHAR(15)
);
-- end dev --

-- production --
CREATE TABLE forex_rates(
    updated_at TIMESTAMPTZ DEFAULT GETDATE(),
    rate REAL,
    currency VARCHAR(15)
);
-- end production --
