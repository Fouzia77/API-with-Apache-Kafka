from kafka_consumer_service.consumer import consumer_health_check

def test_health_check():
    assert consumer_health_check() is True
