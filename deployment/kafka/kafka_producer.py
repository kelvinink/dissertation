from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:19092'])
future = producer.send('kelvin_topic', b'Hi from kafka')
producer.flush()