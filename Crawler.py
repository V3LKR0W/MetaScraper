# Client Secrets ./Keys.
import praw
from keys import *
from MetaScraper import random


reddit = praw.Reddit(
     client_id=redditAPI['clientID'],
     client_secret=redditAPI['clientSecret'],
     user_agent=redditAPI['userAgent'],
)

post_list = []

def getPost(subreddit, numOfResults):
    for posts in reddit.subreddit(subreddit).hot(limit=int(numOfResults)):
        post_list.append(f'https://reddit.com{posts.permalink}')
        
    return random.choice(post_list)
