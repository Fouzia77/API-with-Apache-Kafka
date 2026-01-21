from kafka import KafkaConsumer
import json
import logging
from database import init_db, insert_feature
import os

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_data_events")

def consume_messages(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='feature-ingestor-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    logging.info("✅ Kafka consumer started")
    for message in consumer:
        try:
            data = message.value
            logging.info(f"Received message: {data}")

            user_id = data.get('user_id')
            event_type = data.get('event_type')
            feature_value = data.get('value')
            timestamp = data.get('timestamp')

            if user_id and event_type and feature_value is not None and timestamp:
                insert_feature(user_id, event_type, feature_value, timestamp)
                logging.info(f"Feature for {user_id} stored successfully.")
            else:
                logging.warning(f"Invalid message format: {data}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {e} - Message: {message.value}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

if __name__ == '__main__':
    # Initialize Postgres table and ensure DB is ready
    init_db()
    # Start consuming messages
    consume_messages(KAFKA_TOPIC)
