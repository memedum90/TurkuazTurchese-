'''
This code is written by Mehmet Durna (finally! :P)
Anyways, so Fede, what you'll find here is working. If you run the code, it will put tweets with keyword 
(defined in line 80)  into a file named keyword.txt. The function to read from these files are also available 
in the code(commented out). Everything works if twitter allows. Sometimes we are not allowed to retrieve the tweets by to_reply ID
if they're private tweets and the program ends. I will try to find a way for this. 
 Also there is a limit by Twitter, so try not to overuse it. 
350 requests in 1 hour. remember we have different request when we try to get a tweet by ID, 
so it may reach to limit faster than expected.

'''

import glob
import tweepy
import os
import json

from random import randint

relevant = ["terrorist","muslim","islam","morsi","erdogan","gaymarriage","euthanasia","syria","abortion","feminism","gender","racism","jesus","religion","church","communism","massacre","holocaust"]

# Pick randomly one of the relevant argument
def pick():
    return relevant[randint(0,(len(relevant) - 1))] 

# Keys to initialize twitter API. DO NOT PLAY with this function
def init(): 
    consumer_key="ZBswvG6Iy6jcKUS7Y9TvhA"
    consumer_secret="0sbDaAJyXVRg8xwLu22HRuZG0IPGRZHtfH8zVw8Xpk"
    access_token="136962327-CMU75RcaKcZVh3cqxfVPP1MIkdVLVrxjLdfRAD4q"
    access_token_secret="s6UZaKV7In4ZpVvGV9tkDYkVhq2nU1uVp0hkHSy7f8gqq"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# function to take tweet object and turn it into a dict and return the resulting dict.
# rep is whether it was replied to someone or not. 1 means it was a reply, 0 means it wasn't
def obj2dict(tweet,rep,keyword):
    dictt={}
    dictt['rep']=rep
    dictt['id']=tweet.id
    dictt['text']=tweet.text
    dictt['fvt_cnt']=tweet.favorite_count
    dictt['rt_cnt']=tweet.retweet_count
    dictt['username']=tweet.user.screen_name
    dictt['user_id']= tweet.user.id_str
    dictt['reply_to']=tweet.in_reply_to_status_id
    dictt['topic']=keyword
    
    return dictt

# This function simply writes the dicts into files given the tweet list and the keyword to name the file
def write2file(tweets_list,keyword):
    if os.path.exists("archives/%s.txt" % keyword):
        f=open("archives/%s.txt" % keyword, 'a+')
    else:
        f=open("archives/%s.txt" % keyword, 'w')
    for tweet in tweets_list:
        f.write(unicode(tweet))
        f.write("\n")
    f.close()

# TODO 
def write2cvs(tweets_list,keyword):
    return 0

# This function can read the written dicts from the file into a list of dicts, dicts being tweets and 
# returns the tweet list.
# keyword is the name of the file
# if file is not in the directory, error message is printed and 0 is returned
def readfromfile(keyword):
    tweetlist=[]
    if os.path.exists("archives/%s.txt" % keyword):
        f=open("archives/%s.txt" % keyword, 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
        return tweetlist
    else: 
        print "File %s.txt is not in the current directory" % keyword
        return 0
# Variation
def readfromall():
    tweetlist=[]
    for filename in glob.glob(os.path.join('archives/','*.txt')):
        f=open(filename, 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
    return tweetlist
    
# GLOBAL VARIABLES
api = init()

# Search keyword
#keyword = 'terrorist'

# This is how a file can be read into a list of tweets as dicts
# tweetlist = readfromfile(keyword)

# List to store all the tweets gathered
tweets_dict=[]

def gatherer(keyword):
    
    # This line does the search, more parameters can be specified, count is the number of tweets gathered. max is 100
    tweets=api.search(q=keyword, count=100, lang='en')
    
    # The part to get tweets with their replied tweets and put them into the list making them dicts (from tweet objects)
    for tweet in tweets:
        if not tweet.in_reply_to_status_id ==None:
            to_reply_id=tweet.in_reply_to_status_id
            reply=1
            tweet_dict=obj2dict(tweet,reply,keyword)
            tweets_dict.append(tweet_dict)
            
            repcount = 0
            while reply==1:
                repcount+=1  #updated from here till ... 
                try: 
                    reply_tweet=api.get_status(to_reply_id)
                    if not reply_tweet.in_reply_to_status_id == None:
                        to_reply_id=reply_tweet.in_reply_to_status_id
                        tweet_dict=obj2dict(reply_tweet,reply,keyword)
                        tweets_dict.append(tweet_dict)
                    else:
                        reply=0
                        tweet_dict=obj2dict(reply_tweet,reply,keyword)
                        tweets_dict.append(tweet_dict)
                   
                except:
                    print 'not authorized to see a replied tweet'
                    reply=0
                    if repcount==1:
                        tweets_dict.pop()
                    elif repcount>1:
                        last_tweet=tweets_dict.pop()
                        last_tweet['rep']=0
                        tweets_dict.append(last_tweet)
#              #   try: 
#                 reply_tweet=api.get_status(to_reply_id)
#           #         break
#              #   except RuntimeError:
#            #         print 'not authorized to see the replied tweet'
#                 if not reply_tweet.in_reply_to_status_id ==None:
#                     to_reply_id=reply_tweet.in_reply_to_status_id
#                     tweet_dict=obj2dict(reply_tweet,reply,keyword)
#                     tweets_dict.append(tweet_dict)
#                 else:
#                     reply=0
#                     tweet_dict=obj2dict(reply_tweet,reply,keyword)
#                     tweets_dict.append(tweet_dict)
    # Write the tweets gathered into the relevant file, namely keyword.txt file
    write2file(tweets_dict, keyword)
    # Write to console  the list of tweets
    for tweet in tweets_dict:
        print tweet