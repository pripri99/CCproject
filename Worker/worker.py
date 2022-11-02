import json
from time import sleep
from kafka import KafkaConsumer
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic

SIGNUP_TOPIC = "task_signup"
RESPONSE_TOPIC = "task_response"

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
signup_consumer = KafkaConsumer(SIGNUP_TOPIC)

last_timestamp = -1
count = {
    'short': 0,
    'long': 0
}


def responseSignup(task_id, topic, message, data):
    msg_to_send = {
        'id': task_id,
        'message': message,
        'data': data
    }
    producer.send(topic, json.dumps(msg_to_send).encode())
    print(f"Responded with message:")
    print(message)


try:
    while True:
        # msg = c.poll(0.5)

        for msg in signup_consumer:
            if msg != {}:
                if msg is None:
                    continue
                else:
                    data = json.loads(msg.value.decode())
                    print(data)
                    sleep(0.1)
                    responseSignup(data["id"], RESPONSE_TOPIC, "Hello, this is my response.", data["data"])


except KeyboardInterrupt:
    pass
except Exception as e:
    print("Exception reception ocurrend!")
    print(e)
finally:
    signup_consumer.close()
