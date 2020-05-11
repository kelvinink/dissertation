# For more info please refer to: 
# https://praw.readthedocs.io/en/latest/tutorials/comments.html
import datetime
import json

import praw
from kafka import KafkaProducer

from data_source.reddit import reddit_credentials


bootstrap_servers=['129.204.135.185:19092']


class RedditStreamer:
    """
    Streaming and processing live subreddits.
    """

    def __init__(self):
        self.count = 0
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def stream2file(self, subreddit, attrs):
        curr_time = datetime.datetime.now()
        daymonth = curr_time.strftime("%Y%m%d")
        outFile = "reddits" + daymonth + ".txt"

        reddit = praw.Reddit(client_id=reddit_credentials.CLIENT_ID,
                             client_secret=reddit_credentials.CLIENT_SECRET,
                             user_agent=reddit_credentials.USER_AGENT)

        subRed = reddit.subreddit(subreddit)
        with open(outFile, 'a') as f:
            for comment in subRed.stream.comments(skip_existing=False):
                self.count += 1
                print('Reddit ID: ', comment.__dict__['id'], '  count: ', self.count)
                record = self.parse_comment(comment, attrs)
                f.write(json.dumps(record) + "\n")

    def stream2kafka(self, subreddit, topic, attrs):
        reddit = praw.Reddit(client_id=reddit_credentials.CLIENT_ID,
                             client_secret=reddit_credentials.CLIENT_SECRET,
                             user_agent=reddit_credentials.USER_AGENT)

        sub_red = reddit.subreddit(subreddit)
        for comment in sub_red.stream.comments(skip_existing=False):
            self.count += 1
            print('Reddit ID: ', comment.__dict__['id'], '  count: ', self.count)
            record = self.parse_comment(comment, attrs)
            self.producer.send(topic, json.dumps(record).encode('utf-8'))

    def parse_comment(self, comment, attrs):
        record = {}
        for attr in attrs:
            item = str(comment.__dict__[attr]).replace('\n', '')
            record[attr] = item if item is not None else ""
        return record


if __name__ == '__main__':
    attrs = ["id", "created_utc", "link_id", "link_title", "subreddit_id",
             "score", "stickied", "likes", "permalink", "body"]

    topic = "rcas_reddit_raw"

    redditStreamer = RedditStreamer()
    redditStreamer.stream2kafka('CryptoCurrency', topic, attrs)
    #redditStreamer.stream2file('CryptoCurrency', attrs)
