import requests
import json
from . import config
from kafka import KafkaConsumer
from kafka import KafkaProducer


consumer = KafkaConsumer(config.KAFKA['topic']['raw'],
                         bootstrap_servers=config.KAFKA['bootstrap_servers'],
                         auto_offset_reset='earliest')

producer = KafkaProducer(bootstrap_servers=config.KAFKA['bootstrap_servers'])


for msg in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    #print(message)

    json_msg = json.loads(msg)
    text = json_msg.text
    url = "http://{}:{}/api/ml/sentiment?text={}".format(
        config.MLSERVICE['host'],
        config.MLSERVICE['port'],
        text)
    resp = requests.get(url)

    print(msg)
    print(resp)

    # producer.send(config.KAFKA['topic']['after_sentiment'], b'Hi from kafka this is a sample message.')
