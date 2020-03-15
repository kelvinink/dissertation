import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

bootstrap_servers=['129.204.135.185:19092']
topic = 'raw'


n = 0
elapsed = 0
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

while True:
    # Async
    start = time.time()
    future = producer.send(topic, b'Hi from kafka this is a sample message.')
    end = time.time()

    elapsed += end - start
    n += 1

    print(future.get())
    # if n == 10000:
    #     print("Throughput: ", elapsed / n)
    #     n = 0
    #     elapsed = 0
    


