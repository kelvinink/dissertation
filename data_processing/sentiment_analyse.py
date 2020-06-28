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
        group_id="sentiment"
    )

def twitter_sentiment():
    consumer = kafka_consumer(config.KAFKA['topic']['rcas_twitter_raw'])
    producer = kafka_producer()

    # Fetching data from kafka
    count = 0
    for msg in consumer:
        count += 1
        try:
            # Extracting text
            msg_val = json.loads(msg.value.decode('utf-8'))
            text = msg_val["text"]

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
        except BaseException as e:
            print(e)
            continue

        if count%10000 == 0:
            print("#msg processed: " + str(count))

def reddit_sentiment():
    consumer = kafka_consumer(config.KAFKA['topic']['rcas_reddit_raw'])
    producer = kafka_producer()

    # Fetching data from kafka
    count = 0
    for msg in consumer:
        count += 1
        try:
            # Extracting text
            msg_val = json.loads(msg.value.decode('utf-8'))
            text = msg_val["body"]

            # Call sentiment analysis service
            url = "http://{}:{}/api/ml/sentiment?text='{}'".format(
                config.MLSERVICE['host'],
                config.MLSERVICE['port'],
                text)
            resp = requests.get(url)

            sentiment_res = re.sub('\'', '\"', resp.content.decode('utf-8'))
            item = json.loads(sentiment_res)

            msg_val["sentiment"] = item
            #print(json.dumps(msg_val))

            # Pushing analyzed data back into kafka
            producer.send(config.KAFKA['topic']['rcas_reddit_after_sentiment'],  json.dumps(msg_val).encode('utf-8'))

        except BaseException as e:
            print(e)
            continue

        if count%10000 == 0:
            print("#msg processed: " + str(count))

if __name__ == '__main__':
    print("Start sentiment analysis")
    #twitter_sentiment()
    reddit_sentiment()
