from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('kelvin_topic',
                         bootstrap_servers=['localhost:19092'],
                         auto_offset_reset='earliest')

print("List of Topics: ")
print(consumer.topics())

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print(message)