import json

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from time import sleep






if __name__ == "__main__":

    topic_name = "task_Signup"
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    try:
        #Create Kafka topic
        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
        admin.create_topics([topic])
        print("Created topic:")
        print([topic])
    except Exception as e:
        print(e)

    for i in range(10):
        msg = {
            'id': "task_" + str(i),
            'message': "Hello world",
        }

        producer.send(topic_name, json.dumps(msg).encode())
        sleep(0.1)
        print(f"Published message to message broker.")
        print(msg)