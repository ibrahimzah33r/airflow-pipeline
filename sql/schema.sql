CREATE TABLE IF NOT EXISTS dim_asset (
    id BIGSERIAL PRIMARY KEY,
    external_id VARCHAR(100) NOT NULL UNIQUE,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS fact_market_price (
    id BIGSERIAL PRIMARY KEY,

    asset_id BIGINT NOT NULL
        REFERENCES dim_asset(id),

    observed_at TIMESTAMPTZ NOT NULL,

    price_usd NUMERIC(20, 8),
    market_cap_usd NUMERIC(24, 2),
    volume_24h_usd NUMERIC(24, 2),
    price_change_24h_pct NUMERIC(10, 4),

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_asset_observation
        UNIQUE (asset_id, observed_at)
);


CREATE TABLE IF NOT EXISTS daily_asset_summary (
    id BIGSERIAL PRIMARY KEY,

    asset_id BIGINT NOT NULL
        REFERENCES dim_asset(id),

    summary_date DATE NOT NULL,

    open_price NUMERIC(20, 8),
    close_price NUMERIC(20, 8),
    high_price NUMERIC(20, 8),
    low_price NUMERIC(20, 8),
    average_price NUMERIC(20, 8),
    total_volume_usd NUMERIC(24, 2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_asset_daily_summary
        UNIQUE (asset_id, summary_date)
);


CREATE INDEX IF NOT EXISTS idx_market_price_asset
    ON fact_market_price(asset_id);


CREATE INDEX IF NOT EXISTS idx_market_price_observed_at
    ON fact_market_price(observed_at);


CREATE INDEX IF NOT EXISTS idx_daily_summary_date
    ON daily_asset_summary(summary_date);