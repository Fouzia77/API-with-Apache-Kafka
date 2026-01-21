import psycopg2
import os
import time

# Read Postgres config from environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "feature_store_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fouzia")

def get_connection():
    """
    Retry connecting to Postgres until successful
    """
    while True:
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            print("✅ Connected to Postgres successfully")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Postgres not ready yet: {e}")
            time.sleep(3)

def init_db():
    """
    Initialize the database table if it doesn't exist
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_features (
            feature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id VARCHAR(255) NOT NULL,
            event_type VARCHAR(255) NOT NULL,
            feature_value DOUBLE PRECISION NOT NULL,
            ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, event_type, ingestion_timestamp)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ user_features table is ready")

def insert_feature(user_id, event_type, feature_value, timestamp):
    """
    Insert a feature into the database
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO user_features (user_id, event_type, feature_value, ingestion_timestamp)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, event_type, ingestion_timestamp) DO NOTHING;
        """, (user_id, event_type, feature_value, timestamp))
        conn.commit()
    except Exception as e:
        print(f"Error inserting feature: {e}")
    finally:
        cur.close()
        conn.close()
