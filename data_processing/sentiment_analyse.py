import re
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
        group_id = "sentiment"
    )

def twitter_sentiment():
    consumer = kafka_consumer(config.KAFKA['topic']['rcas_twitter_raw'])
    producer = kafka_producer()

    # Fetching data from kafka
    for msg in consumer:
        # Extracting text
        msg_val = json.loads(msg.value.decode('utf-8'))
        try:
            text = msg_val["text"]
        except BaseException as e:
            continue

        # Call sentiment analysis service
        url = "http://{}:{}/api/ml/sentiment?text='{}'".format(
            config.MLSERVICE['host'],
            config.MLSERVICE['port'],
            text)
        resp = requests.get(url)

        sentiment_res = re.sub('\'', '\"', resp.content.decode('utf-8'))
        item = json.loads(sentiment_res)

        msg_val["sentiment"] = item
        print(json.dumps(msg_val))

        # Pushing analyzed data back into kafka
        producer.send(config.KAFKA['topic']['rcas_twitter_after_sentiment'],  json.dumps(msg_val).encode('utf-8'))

def reddit_sentiment():
    consumer = kafka_consumer(config.KAFKA['topic']['rcas_reddit_raw'])
    producer = kafka_producer()

    # Fetching data from kafka
    for msg in consumer:
        # Extracting text
        msg_val = json.loads(msg.value.decode('utf-8'))
        try:
            text = msg_val["body"]
        except BaseException as e:
            continue

        # Call sentiment analysis service
        url = "http://{}:{}/api/ml/sentiment?text='{}'".format(
            config.MLSERVICE['host'],
            config.MLSERVICE['port'],
            text)
        resp = requests.get(url)

        sentiment_res = re.sub('\'', '\"', resp.content.decode('utf-8'))
        item = json.loads(sentiment_res)

        msg_val["sentiment"] = item
        print(json.dumps(msg_val))

        # Pushing analyzed data back into kafka
        producer.send(config.KAFKA['topic']['rcas_reddit_after_sentiment'],  json.dumps(msg_val).encode('utf-8'))

if __name__ == '__main__':
    twitter_sentiment()
    #reddit_sentiment()
