import re
import time
import json
import requests

from kafka import KafkaConsumer
from kafka import KafkaProducer

from data_processing import config


def kafka_producer():
    return KafkaProducer(bootstrap_servers=config.KAFKA['bootstrap_servers'])

def kafka_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=config.KAFKA['bootstrap_servers'],
        auto_offset_reset='earliest'
    )


if __name__ == '__main__':
    consumer = kafka_consumer(config.KAFKA['topic']['raw'])
    producer = kafka_producer()

    for msg in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        # print(message)

        text = msg.value.decode('utf-8')
        url = "http://{}:{}/api/ml/sentiment?text='{}'".format(
            config.MLSERVICE['host'],
            config.MLSERVICE['port'],
            text)
        resp = requests.get(url)

        sentiment_res = re.sub('\'', '\"', resp.content.decode('utf-8'))
        item = json.loads(sentiment_res)
        item["text"] = text

        print( json.dumps(item))

        producer.send(config.KAFKA['topic']['after_sentiment'],  json.dumps(item).encode('utf-8'))

        time.sleep(3)