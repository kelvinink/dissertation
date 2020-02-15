# For more info please refer to: 
# http://docs.tweepy.org/en/v3.8.0/streaming_how_to.html
import tweepy
import twitter_credentials
import json

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

    def stream_tweets(self, outFile, tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        authHandler = self.twitter_autenticator.getAuthHandler()
        listener = TwitterListener(outFile)
        stream = tweepy.Stream(authHandler, listener)
        stream.filter(track=tag_list)


class TwitterListener(tweepy.streaming.StreamListener):
    """
    Twitter listener that just prints received tweets to stdout.
    """
    def __init__(self, outFile):
        self.outFile = outFile

    def on_data(self, data):
        try:
            print('Tweet ID: ', json.loads(data)['id'])
            with open(self.outFile, 'a') as f:
                f.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
 
if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]
    outFile = "tweets.txt"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(outFile, tag_list)