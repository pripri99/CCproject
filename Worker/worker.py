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
        #msg = c.poll(0.5)

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