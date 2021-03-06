# Client Secrets ./Keys.
import praw, json
from youtubesearchpython import SearchVideos
from keys import *
from MetaScraper import random


reddit = praw.Reddit(
     client_id=redditAPI['clientID'],
     client_secret=redditAPI['clientSecret'],
     user_agent=redditAPI['userAgent'],
)

post_list = []
video_list = []
sound_list = ['https://soundcloud.com/soundhyana/jumping-on-comits', 'https://soundcloud.com/dark_cat/bubble-tea-feat-juu-cinders', 'https://soundcloud.com/sanholobeats/lmftg']


# Dynamic fetching of content
def getPost(subreddit, numOfResults):
    for posts in reddit.subreddit(subreddit).hot(limit=int(numOfResults)):
        post_list.append(f'https://reddit.com{posts.permalink}')
        
    return random.choice(post_list)

def getVideo(query, numOfResults):
    search = SearchVideos(str(query), offset=1, mode='dict', max_results=int(numOfResults))
    parse = search.result()
    for r in parse['search_result']:
        video_list.append(r['link'])
    return random.choice(video_list)
    
# Static fetching of content
def getAudio():
    return random.choice(sound_list)
