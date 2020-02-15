# For more info please refer to: 
# https://praw.readthedocs.io/en/latest/tutorials/comments.html

import praw
import reddit_credentials

class RedditStreamer():
    """
    Streaming and processing live subreddits.
    """
    def __init__(self):
        pass

    def stream_comments(self, subreddit, outFile):
        reddit = praw.Reddit(client_id=reddit_credentials.CLIENT_ID,
                             client_secret=reddit_credentials.CLIENT_SECRET,
                             user_agent=reddit_credentials.USER_AGENT)

        subRed = reddit.subreddit(subreddit)
        for comment in subRed.stream.comments(skip_existing=False):
            try:
                print('Reddit ID: ', comment)
                with open(outFile, 'a') as f:
                    f.write(comment.body)
            except BaseException as e:
                print("Error on_data %s" % str(e))

if __name__ == '__main__':
    redditStreamer = RedditStreamer()
    redditStreamer.stream_comments('Bitcoin', 'reddit_comments.txt')