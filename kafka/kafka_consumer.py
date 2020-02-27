import time
from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('kelvin_topic',
                         bootstrap_servers=['106.13.90.40:19092'],
                         auto_offset_reset='earliest')

print("List of Topics: ")
print(consumer.topics())

n = 0
m = 0
start = time.time()

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    
    #print(message)
    n += 1
    if n == 10000:
        m += n
        n = 0
        print("Msgs: ", m, "  Throughput: ", m / (time.time()-start))