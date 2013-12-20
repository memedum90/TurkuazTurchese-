'''
This code is written by Mehmet Durna  
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

def init_2():
    consumer_key="NY9AK7xur7y4vMs3nE54KA"
    consumer_secret="0obr9aNiGe27AjDzkatEeul4nDFUxKMSVcNtjZzf4"
    access_token="1914766603-p6PnLYcWgMprjq8V2t1Fh1s93FAgWRPyGpTylEH"
    access_token_secret="Zal2KPlizVaoQUzB1Bqx0t3uCmM1OXCl5J2o2at9MW0Aj"
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
    dictt['lang']=tweet.user.lang
    dictt['flw_cnt']=tweet.user.followers_count
    dictt['flg_cnt']=tweet.user.friends_count
    dictt['lst_cnt']=tweet.user.listed_count
    dictt['us_fvt_cnt']=tweet.user.favourites_count
    dictt['stat_cnt']=tweet.user.statuses_count
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
 
def isInDict(checkedTweet, tlist):
    if not tlist==0:
        for tweet_obj in tlist:
            #print 'tweet_obj id:\t%s' % tweet_obj['id']
            #print 'smp id:\t\t%s'% checkedTweet.id
            if tweet_obj['id']==checkedTweet.id:
                return True
        return False
    else:
        return False    

   
# GLOBAL VARIABLES
api = init_2()

# Search keyword
#keyword = 'terrorist'

#list to store all the tweets gathered
tweet_list=[]



def gatherer(keyword):
    tlistfromfile=readfromfile(keyword)
    print "hahahah"
    # This line does the search, more parameters can be specified, count is the number of tweets gathered. max is 100
    tweets=api.search(q=keyword, count=100, lang='en')
    
    # The part to get tweets with their replied tweets and put them into the list making them dicts (from tweet objects)
    for tweet_obj in tweets:
    
        if not tweet_obj.in_reply_to_status_id ==None:
            to_reply_id=tweet_obj.in_reply_to_status_id
            reply=1
            #print 'text:' ,tweet_obj.text
            
            if not isInDict(tweet_obj, tlistfromfile):
                
                #tweet is dictionary of the object
                tweet=obj2dict(tweet_obj,reply, keyword)
                tweet_list.append(tweet)
            else:
                reply=0
            
            repcount=0 #this line is updated
            while reply==1:
                repcount+=1  #updated from here till ... 
                try: 
                    reply_tweet=api.get_status(to_reply_id)
                    if not reply_tweet.in_reply_to_status_id ==None:
                        to_reply_id=reply_tweet.in_reply_to_status_id
                        tweet=obj2dict(reply_tweet,reply,keyword)
                        tweet_list.append(tweet)
                    else:
                        reply=0
                        tweet=obj2dict(reply_tweet,reply,keyword)
                        tweet_list.append(tweet)
                   
                except:
                    print 'not authorized to see the replied tweet'
                    reply=0
                    if repcount==1:
                        tweet_list.pop()
                    elif repcount>1:
                        last_tweet=tweet_list.pop()
                        last_tweet['rep']=0
                        tweet_list.append(last_tweet)
           # ...here. copy till here         
    #write the tweets gathered into the relevant file, namely keyword.txt file
    write2file(tweet_list, keyword)
    #write to console  the list of tweets
    for tweet in tweet_list:
        print tweet
#the part from previous edition        
#     for tweet in tweets:
#         if not tweet.in_reply_to_status_id ==None:
#             to_reply_id=tweet.in_reply_to_status_id
#             reply=1
#             tweet_dict=obj2dict(tweet,reply,keyword)
#             tweets_dict.append(tweet_dict)
#             
#             repcount = 0
#             while reply==1:
#                 repcount+=1  #updated from here till ... 
#                 try: 
#                     reply_tweet=api.get_status(to_reply_id)
#                     if not reply_tweet.in_reply_to_status_id == None:
#                         to_reply_id=reply_tweet.in_reply_to_status_id
#                         tweet_dict=obj2dict(reply_tweet,reply,keyword)
#                         tweets_dict.append(tweet_dict)
#                     else:
#                         reply=0
#                         tweet_dict=obj2dict(reply_tweet,reply,keyword)
#                         tweets_dict.append(tweet_dict)
#                    
#                 except:
#                     print 'not authorized to see a replied tweet'
#                     reply=0
#                     if repcount==1:
#                         tweets_dict.pop()
#                     elif repcount>1:
#                         last_tweet=tweets_dict.pop()
#                         last_tweet['rep']=0
#                         tweets_dict.append(last_tweet)
# #              #   try: 
# #                 reply_tweet=api.get_status(to_reply_id)
# #           #         break
# #              #   except RuntimeError:
# #            #         print 'not authorized to see the replied tweet'
# #                 if not reply_tweet.in_reply_to_status_id ==None:
# #                     to_reply_id=reply_tweet.in_reply_to_status_id
# #                     tweet_dict=obj2dict(reply_tweet,reply,keyword)
# #                     tweets_dict.append(tweet_dict)
# #                 else:
# #                     reply=0
# #                     tweet_dict=obj2dict(reply_tweet,reply,keyword)
# #                     tweets_dict.append(tweet_dict)
#     # Write the tweets gathered into the relevant file, namely keyword.txt file
#     write2file(tweets_dict, keyword)
#     # Write to console  the list of tweets
#     for tweet in tweets_dict:
#         print tweet
        
### USER INFORMATIONS ###

#input userid as a string or as an int. 
#output user dict consisting of user attributes
def getUserInfo(userid):
    
    user={}
    user['id']=userid
    
    us=api.get_user(userid)
    #screen_name string The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject to change. 
    #Use id_str as a user identifier whenever possible. Typically a maximum of 15 characters long, but some historical accounts may exist with longer names.
    user['screen_name']=us.screen_name
    
    
    #name: string  The name of the user, as they've defined it. Not necessarily a person's name. Typically capped at 20 characters, but subject to change.
    user['name']=us.name
    
    #listed_count: int. The number of public lists that this user is a member of.
    user['listed_count']=us.listed_count
    
    #location: string Nullable. The user-defined location for this account's profile. 
    #Not necessarily a location nor parseable. This field will occasionally be fuzzily interpreted by the Search service.
    user['location']=us.location
    
    #lang: string The BCP 47 code for the user's self-declared user interface language. May or may not have anything to do with the content of their Tweets.
    user['lang']=us.lang
        
    #followers_count: int The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate "0."
    user['followers_count']=us.followers_count
    
    #friends_count: int The number of users this account is following (AKA their "followings"). Under certain conditions of duress, this field will temporarily indicate "0."
    user['friends_count']=us.friends_count
    
    #favourites_count int The number of tweets this user has favorited in the account's lifetime. British spelling used in the field name for historical reasons.
    user['favourites_count']=us.favourites_count
    
    #statuses_count int  The number of tweets (including retweets) issued by the user.
    user['statuses_count']= us.statuses_count
    
       
    
    
    return user
 #input a user id
 #output a list consisting of follower ids   
def getUserFollowers(userid):
    followerlist=[]
    
    follower_cursors = tweepy.Cursor(api.followers_ids, userid)
    
    for followerid in follower_cursors.items():
        
        followerlist.append(followerid)    
    return followerlist

 #input a user id
 #output a list consisting of friend ids   
 #  (a person1 who is being followed by a person2 is a friend of that person2)
def getUserFriends(userid):
    friendslist=[]
    
    friends_cursors = tweepy.Cursor(api.friends_ids, userid)
    
    for friendid in friends_cursors.items():
        
        friendslist.append(friendid)    
    return friendslist

def getUserAll(id):
    friendlist=getUserFriends(id)
    followerlist=getUserFollowers(id)
    user=getUserInfo(id)
    user['friends']=friendlist
    user['followers']=followerlist
    return user

def getTWUser(tweet):
    return (tweet['username'],tweet['user_id'],tweet['lang'],tweet['flw_cnt'],tweet['flg_cnt'],tweet['lst_cnt'],tweet['us_fvt_cnt'],tweet['stat_cnt'])
