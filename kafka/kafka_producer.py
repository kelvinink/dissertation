import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

n = 0
elapsed = 0
producer = KafkaProducer(bootstrap_servers=['106.13.90.40:19092'])

while True:
    # Async
    start = time.time()
    future = producer.send('kelvin_topic', b'Hi from kafka this is a sample message.')
    end = time.time()

    elapsed += end - start
    n += 1

    print(future.get())
    # if n == 10000:
    #     print("Throughput: ", elapsed / n)
    #     n = 0
    #     elapsed = 0
    


