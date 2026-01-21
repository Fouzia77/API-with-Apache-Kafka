CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS user_features (
    feature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    feature_value DOUBLE PRECISION NOT NULL,
    ingestion_timestamp TIMESTAMPTZ NOT NULL,
    UNIQUE(user_id, event_type, ingestion_timestamp)
);

CREATE INDEX IF NOT EXISTS idx_user_features_user
    ON user_features(user_id);

CREATE INDEX IF NOT EXISTS idx_user_features_time
    ON user_features(ingestion_timestamp);
