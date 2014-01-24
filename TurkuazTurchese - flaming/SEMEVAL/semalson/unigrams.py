# for task B (topic independent tweets)
# import pymongo

#from pymongo import MongoClient
import itertools
#from wordshape import *
from functions import *
#from features import *
from core import *

#TODO nltk pos tagger
#TODO stemming

# connection = pymongo.connection.Connection('79.123.176.106', 27017)
# #connection = MongoClient('localhost', 27017)
# db = connection.SEMEVALTweet2013
# 
# #all_tweets = db.Tweets;
# #btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"}]})
# #btweets = get_tweets(btweets)
# #devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"DevB"}]})
# #devtweets = get_tweets(devtweets)
# all_tweets = db.Tweets;
# #btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"},{"task":"DevB"}]})
# btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"}]})
# btweets = get_tweets(btweets)
# #devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"TestB"}]})
# devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"DevB"}]})
# devtweets = get_tweets(devtweets)
# 
# #a,b,c=parse_tweets(btweets)
# #print len(btweets),len(a),len(b),len(c)
# #a,b,c=parse_tweets(devtweets)
# #print len(btweets),len(a),len(b),len(c)
# 
# print "reading tweets done.."
# # uncomment this and run!
# #trainset,testset = btweets[:4000], btweets[4000:]
run=7
# 
# trainset,testset=btweets,devtweets
# 
# alg="maxent"
# ##alg="dec"
# posclassifier=run_alg(trainset,"positive",alg)
# alg="naive"
# negclassifier=run_alg(trainset,"negative",alg)
#
import cPickle as pickle
## writing to pickle
#pickle.dump(posclassifier,open("runs/run"+str(run)+"/posc1.p","wb"))
#pickle.dump(negclassifier,open("runs/run"+str(run)+"/negc1.p","wb"))

## reading from pickle
path="runs/run"+str(run)
posclassifier=pickle.load(open("runs/run"+str(run)+"/posc1.p","rb"))
negclassifier=pickle.load(open("runs/run"+str(run)+"/negc1.p","rb"))

print "testing started..."
#run=10
run_test(posclassifier,negclassifier,testset,"runs/run"+str(run)+"/run"+str(run),run)
#test_classifier(negclassifier,testset,"negative")
#test_classifier(posclassifier,testset,"positive")

#all testing
#classifier=run_naive_all(trainset)
#test_classifier_all(classifier,testset)
############################################################