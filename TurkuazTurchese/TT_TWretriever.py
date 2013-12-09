import facebook
import urllib
import urlparse
import subprocess
import warnings
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key="ZBswvG6Iy6jcKUS7Y9TvhA"
consumer_secret="0sbDaAJyXVRg8xwLu22HRuZG0IPGRZHtfH8zVw8Xpk"

access_token="136962327-CMU75RcaKcZVh3cqxfVPP1MIkdVLVrxjLdfRAD4q"
access_token_secret="s6UZaKV7In4ZpVvGV9tkDYkVhq2nU1uVp0hkHSy7f8gqq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
just=api.search(q='justinbieber', count=30)

#tweepy.models.Status.

count=0
for an in just:
    count+=1
    print count,an.__str__() 
    
#public_tweets = api.home_timeline()
#for tweet in public_tweets: 
# print tweet.text

#print api.me().name 
#print api.search.tweets(q='justinbieber', count=30, until='2013-03-01') 

class StdOutListener(StreamListener): """ A listener handles tweets are the received from the stream. This is a basic listener that just prints received tweets to stdout.""" 
    def on_data(self, data): 
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__': 
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l) # stream.filter(track=['justinbieber'])

# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError). warnings.filterwarnings('ignore', category=DeprecationWarning)