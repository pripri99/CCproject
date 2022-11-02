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


def responseMessage(task_id, topic, message, data):
    msg_to_send = {
        'id': task_id,
        'message': message,
        'data': data
    }
    producer.send(topic, json.dumps(msg_to_send).encode())
    print("TaskID [" + task_id + "] responded with message:")
    print(message)


try:
    print("Starting listening to signup...")
    while True:
        # msg = c.poll(0.5)

        for msg in signup_consumer:
            if msg != {}:
                if msg is None:
                    continue
                else:
                    data = json.loads(msg.value.decode())
                    print("[+] RECEIVED MSG - Task REQUEST message for Task ID" + data["id"])
                    print(data)
                    #TODO Sleep for testing
                    sleep(1)
                    responseMessage(data["id"], RESPONSE_TOPIC, "(WORKER) Bye World, this is my response.", data["data"])


except KeyboardInterrupt:
    pass
except Exception as e:
    print("Exception reception ocurrend!")
    print(e)
finally:
    signup_consumer.close()
