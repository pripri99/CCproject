import json

from kafka import KafkaConsumer


c = KafkaConsumer("user_signups")

last_timestamp = -1
count = {
    'short': 0,
    'long': 0
}

try:
    while True:
        msg = c.poll(0.5)
        if msg != {}:
            #data = json.loads(msg.value())
            print(msg)


except KeyboardInterrupt:
    pass
except Exception as e:
    print("Exception reception ocurrend!")
    print(e)
finally:
    c.close()