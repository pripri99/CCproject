"""Settings for producer and consumer."""

BROKER = "localhost:9092" 
#BROKER = "broker:29092"  # when use Docker

RECOMMENDATION_SERVICE_CONFIG = {
    'bootstrap.servers': BROKER,
    'group.id': "recommendation-group",
    'session.timeout.ms': 6000,
    'auto.offset.reset': 'latest',
}

PRODUCER_CONFIG = {
    'bootstrap.servers': BROKER,
}

STOCK_QUOTES_TOPIC = "task_signup" #'stock-quotes'
RECOMMENDATION_TOPIC = "task_response" #'recommendations'
DASHBOARD_TOPICS = [STOCK_QUOTES_TOPIC, RECOMMENDATION_TOPIC]