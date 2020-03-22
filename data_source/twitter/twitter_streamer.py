# For more info please refer to: 
# http://docs.tweepy.org/en/v3.8.0/streaming_how_to.html
import tweepy
import time
import json
import datetime

from kafka import KafkaProducer

from data_source.twitter import twitter_credentials


class TwitterAuthenticator():
    """
    Twitter Account Authentication
    """
    def __init__(self):
        self.authHandler = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        self.authHandler.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    def getAuthHandler(self, credentials = None):
        if(credentials is not None):
            self.authHandler = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
            self.authHandler.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return self.authHandler


class TwitterStreamer():
    """
    Streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream2file(self, outFile, tag_list, attrs):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        authHandler = self.twitter_autenticator.getAuthHandler()
        with open(outFile, 'a') as f:
            listener = TwitterListener(f, attrs)
            stream = tweepy.Stream(authHandler, listener)
            stream.filter(track=tag_list)
    
    def stream2kafka(self, kafka, tag_list, attrs):
        authHandler = self.twitter_autenticator.getAuthHandler()
        listener = TwitterListener(kafka, attrs)
        stream = tweepy.Stream(authHandler, listener)
        stream.filter(track=tag_list)


class TwitterListener(tweepy.streaming.StreamListener):
    """
    Twitter listener that just prints received tweets to stdout.
    """
    def __init__(self, sink, attrs):
        self.sink = sink
        self.attrs = attrs
        self.kafka_topic = "rcas_raw"

    def on_data(self, data):
        try:
            json_tweet = json.loads(data)
            print('Tweet ID: ', json_tweet['id'])

            record = {}
            for attr in self.attrs:
                item = str(json_tweet[attr]).replace('\n', '')
                record[attr] = item if item is not None else ""

            if isinstance(self.sink, KafkaProducer):
                self.sink.send(self.kafka_topic, json.dumps(record).encode('utf-8'))
                print(json.dumps(record).encode('utf-8'))
            else:
                self.sink.write(json.dumps(record) + "\n")

            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))

        return True
          
    def on_error(self, status):
        if status == 420:
            # Rate limit
            time.sleep(20*60)
            return False
        print(status)
 
if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    tag_list = ["croptocurrency", "bitcoin", "ethereum", ""]

    attrs = ["id_str", "created_at", "quote_count", "reply_count", "retweet_count", "favorite_count",
            "geo", "coordinates",  "timestamp_ms", "lang", "source", "text"]

    curr_time = datetime.datetime.now()
    daymonth = curr_time.strftime("%Y%m%d")
    outFile = "tweets" + daymonth + ".txt"
        
    twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream2file(outFile, tag_list, attrs)
    twitter_streamer.stream2kafka(KafkaProducer(bootstrap_servers=['129.204.135.185:19092']), tag_list, attrs)

    