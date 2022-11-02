import json

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from time import sleep

def createTask(task_id, topic, message, data):
    msg_to_send = {
        'id': id,
        'message': message,
        'data': data
    }
    producer.send(topic, json.dumps(msg_to_send).encode())
    print(f"Published message to message broker.")
    print(message)

from kafka import KafkaConsumer


def listenToMsg(taskTopicsToListen):
    consumerList = []
    for tsk in taskTopicsToListen:
        print("Listening to topic: " + tsk)
        consumerList.append(KafkaConsumer(tsk))
    try:
        while True:
            for c in consumerList:
                for msg in c:
                    if msg != {}:
                        if msg is None:
                            continue
                        else:
                            data = json.loads(msg.value.decode())
                            print(data)


    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Exception reception ocurrend!")
        print(e)
    finally:
        c.close()

if __name__ == "__main__":

    SIGNUP_TOPIC = "task_Signup"
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    try:
        #Create Kafka topic
        topic = NewTopic(name=SIGNUP_TOPIC, num_partitions=1, replication_factor=1)
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
        admin.create_topics([topic])
        print("Created topic:")
        print([topic])
    except Exception as e:
        print(e)

    taskTopicsToListen = []

    for i in range(10):
        id = "task_" + str(i)
        message = "wt_" + id
        createTask(id, SIGNUP_TOPIC, message,
                   ["This", "is", "any", "kind", "of", "data"])
        taskTopicsToListen.append(message)
        sleep(0.1)

    #sleep(5)
    listenToMsg(taskTopicsToListen)

