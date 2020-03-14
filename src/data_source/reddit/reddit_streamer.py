# For more info please refer to: 
# https://praw.readthedocs.io/en/latest/tutorials/comments.html

import praw
import json
import os.path
import datetime
import reddit_credentials

DELIMITER = ';'

class RedditStreamer():
    """
    Streaming and processing live subreddits.
    """
    def __init__(self):
        self.count = 0

    def stream_comments(self, subreddit, outFile, attrs):
        reddit = praw.Reddit(client_id=reddit_credentials.CLIENT_ID,
                             client_secret=reddit_credentials.CLIENT_SECRET,
                             user_agent=reddit_credentials.USER_AGENT)

        subRed = reddit.subreddit(subreddit)
        with open(outFile, 'a') as f:
            for comment in subRed.stream.comments(skip_existing=False):
                #print(comment.__dict__)
                #print(comment.body)
                try:
                    print('Reddit ID: ', comment.__dict__['id'], '  count: ', self.count)
                    self.count += 1
                    record = []
                    for attr in attrs:
                        item = str(comment.__dict__[attr]).replace('\n','').replace(DELIMITER, '')
                        record.append(item if item is not None else "")
                    f.write(DELIMITER.join(record) + "\n")
                except BaseException as e:
                    print("Error on_data %s" % str(e))

if __name__ == '__main__':
    attrs = ["id", "created_utc", "link_id", "link_title" , "subreddit_id",
            "score", "stickied",  "likes", "permalink", "body"]

    curr_time = datetime.datetime.now()
    daymonth = curr_time.strftime("%Y%m%d")
    
    outFile = "reddits" + daymonth + ".csv"

    if os.path.isfile(outFile) == False:
        with open(outFile, "w") as f:
            f.write(DELIMITER.join(attrs) + "\n")

    redditStreamer = RedditStreamer()
    redditStreamer.stream_comments('CryptoCurrency', outFile, attrs)