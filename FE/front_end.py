import json
from time import sleep
import threading

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka import KafkaConsumer


SIGNUP_TOPIC = "task_signup"
RESPONSE_TOPIC = "task_response"

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

response_consumer = KafkaConsumer(RESPONSE_TOPIC)

def createTaskMessage(task_id, topic, message, data):
    msg_to_send = {
        'id': id,
        'message': message,
        'data': data
    }
    producer.send(topic, json.dumps(msg_to_send).encode())
    print(f"Published task to broker - Task ID [" + task_id + "]")

def listenToMsg(taskIds):

    #for tsk in taskIds:
        #print("Requested Tasks: " + tsk)
    print(" Starting listening to responses...")
    try:
        while True:
                for msg in response_consumer:
                    if msg != {}:
                        if msg is None:
                            continue
                        else:
                            data = json.loads(msg.value.decode())
                            print("[-] RECEIVED MSG - Task RESULTS message for Task ID" + data["id"])
                            print(data)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Exception reception ocurred!")
        print(e)
    finally:
        response_consumer.close()

if __name__ == "__main__":

    try:
        # Create Kafka topic
        #topic = NewTopic(name=SIGNUP_TOPIC, num_partitions=1, replication_factor=1)
        #admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
        #admin.create_topics([topic])

        taskIds = []

        for i in range(10):
            id = "task_" + str(i)
            taskIds.append(id)
            sleep(0.1)

        # START LISTENER
        x = threading.Thread(target=listenToMsg, args=(taskIds,))

        for identifier in taskIds:
            message = "(FRONTEND) Hello world, process this please."
            createTaskMessage(identifier, SIGNUP_TOPIC, message,
                              ["This", "is", "any", "kind", "of", "data"])


        x.start()
        print("Main    : wait for the thread to finish")
        x.join()
        print("Main    : all done")

    except Exception as e:
        print("Main exception")
        print(e)