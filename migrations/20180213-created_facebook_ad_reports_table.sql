-- dev --
CREATE TABLE facebook_ad_reports(
    id SERIAL PRIMARY KEY NOT NULL,
    account VARCHAR(255),
    campaign_name VARCHAR(255),
    ad_set_name VARCHAR(255),
    ad_name VARCHAR(255),
    account_currency VARCHAR(10),
    clicks INTEGER,
    cpc REAL,
    cpm REAL,
    ctr REAL,
    impressions INTEGER,
    inline_link_clicks INTEGER,
    inline_link_click_ctr REAL,
    relevance_score REAL,
    spend REAL,
    offsite_conversion INTEGER,
    complete_registrations INTEGER,
    since TIMESTAMPTZ,
    until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);
-- end dev --

-- production --
CREATE TABLE facebook_ad_reports(
    id INT IDENTITY(1, 1) NOT NULL,
    account VARCHAR(255),
    campaign_name VARCHAR(255),
    ad_set_name VARCHAR(255),
    ad_name VARCHAR(255),
    account_currency VARCHAR(10),
    clicks INTEGER,
    cpc REAL,
    cpm REAL,
    ctr REAL,
    impressions INTEGER,
    inline_link_clicks INTEGER,
    inline_link_click_ctr REAL,
    relevance_score REAL,
    spend REAL,
    offsite_conversion INTEGER,
    complete_registrations INTEGER,
    since TIMESTAMPTZ,
    until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT GETDATE()
);
-- end production --
