import praw
import reddit_credentials

reddit = praw.Reddit(client_id=reddit_credentials.CLIENT_ID,
                     client_secret=reddit_credentials.CLIENT_SECRET,
                     user_agent=reddit_credentials.USER_AGENT)

for submission in reddit.subreddit('bitcoin').hot(limit=10):
    print(submission.title)