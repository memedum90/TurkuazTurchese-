# for task B (topic independent tweets)
import pymongo

#from pymongo import MongoClient
import itertools
from wordshape import *
from functions import *
from features import *
from core import *

#connection = MongoClient('localhost', 27017)
connection=pymongo.connection.Connection('79.123.176.106', 27017)
db = connection.SEMEVALTweet2013

all_tweets = db.Tweets;
btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"}]})
btweets = get_tweets(btweets)
devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"DevB"}]})
devtweets = get_tweets(devtweets)

trainset={}
devset={}

for i,tweet in enumerate(btweets):
    features={}
    
    print "processing train: ",i
    
    features["bestwords"]=feature_bestwords(tweet)
    features["bestbigrams"]=feature_bestbigrams(tweet) #500
    features["unigrams"]=feature_words(tweet)
    features["bigrams"]=feature_bigrams(tweet)
    features["afinn"]=feature_afinn(tweet)
    features["sent"]=feature_sent(tweet)
    features["arzu"]=feature_arzu(tweet)
    features["tag"]=feature_tags(tweet)
    features["repetition"]=feature_repetition(tweet)
    features["wordshape"]=feature_wordshape(tweet)
    features["firstlastword"]=feature_firstlastword(tweet)
    features["chat"]=feature_chat(tweet)
    features["abbrev"]=feature_abbrev(tweet)
    features["interjection"]=feature_interjection(tweet)
    features["punctuation"]=feature_punctuation(tweet)
    features["negation"]=feature_negation(tweet)
    features["hash"]=feature_hash(tweet)
    features["hash_positive"]=feature_hash_positive(tweet)
    features["emotion"]=feature_emotion(tweet)
    features["lingemotion"]=feature_lingemotion(tweet)
    features["wordnet"]=feature_wordnet(tweet)
    features["arda"]=feature_arda(tweet)
    features["epattern"]=feature_EPattern(tweet)
    features["afinn_epattern"]=feature_afinn_EPattern(tweet)
    features["emo"]=feature_emo(tweet)
    features["all_positive"]=feature_all_positive(tweet)
    features["all_negative"]=feature_all_positive(tweet)
    features["CAP"]=feature_CAP(tweet)
    features["quotation"]=feature_quotation(tweet)
    
    #POS
    features["posextras"]=feature_POSextras(tweet)
    features["pos_bestwords"]=feature_posbestwords(tweet)
    features["poswords"]=feature_poswords(tweet)
    features["posbigrams"]=feature_posbigrams(tweet)
    features["pos_firstlastword"]=feature_firstlastword(tweet,pos=True)
    features["pos_bestbigrams"]=feature_posbestbigrams(tweet)
    
    trainset[tweet["sid"]]=features
    
for i,tweet in enumerate(devtweets):
    features={}
    
    print "processing dev: ",i
    
    features["bestwords"]=feature_bestwords(tweet)
    features["bestbigrams"]=feature_bestbigrams(tweet) #500
    features["unigrams"]=feature_words(tweet)
    features["bigrams"]=feature_bigrams(tweet)
    features["afinn"]=feature_afinn(tweet)
    features["sent"]=feature_sent(tweet)
    features["arzu"]=feature_arzu(tweet)
    features["tag"]=feature_tags(tweet)
    features["repetition"]=feature_repetition(tweet)
    features["wordshape"]=feature_wordshape(tweet)
    features["firstlastword"]=feature_firstlastword(tweet)
    features["chat"]=feature_chat(tweet)
    features["abbrev"]=feature_abbrev(tweet)
    features["interjection"]=feature_interjection(tweet)
    features["punctuation"]=feature_punctuation(tweet)
    features["negation"]=feature_negation(tweet)
    features["hash"]=feature_hash(tweet)
    features["hash_positive"]=feature_hash_positive(tweet)
    features["emotion"]=feature_emotion(tweet)
    features["lingemotion"]=feature_lingemotion(tweet)
    features["wordnet"]=feature_wordnet(tweet)
    features["arda"]=feature_arda(tweet)
    features["epattern"]=feature_EPattern(tweet)
    features["afinn_epattern"]=feature_afinn_EPattern(tweet)
    features["emo"]=feature_emo(tweet)
    features["all_positive"]=feature_all_positive(tweet)
    features["all_negative"]=feature_all_positive(tweet)
    features["CAP"]=feature_CAP(tweet)
    features["quotation"]=feature_quotation(tweet)
    
    #POS
    features["posextras"]=feature_POSextras(tweet)
    features["pos_bestwords"]=feature_posbestwords(tweet)
    features["poswords"]=feature_poswords(tweet)
    features["posbigrams"]=feature_posbigrams(tweet)
    features["pos_firstlastword"]=feature_firstlastword(tweet,pos=True)
    features["pos_bestbigrams"]=feature_posbestbigrams(tweet)
    
    devset[tweet["sid"]]=features
    
#import cPickle as pickle
## writing to pickle
#pickle.dump(trainset,open("trainfeatures.p","wb"))
#pickle.dump(devset,open("devfeatures.p","wb"))
##pickle.dump(negclassifier,open("runs/run"+str(run)+"/negc.p","wb"))

#import cPickle as pickle
#feats1=pickle.load(open("feats/trainfeatures.p","rb"))
#feats2=pickle.load(open("feats/devfeatures.p","rb"))
#allfeats=feats1
#allfeats.update(feats2)
#
#temp=[]
#for k,v in allfeats.iteritems():
#    a=v["emotion"]
#    
#    for x,y in a.iteritems():
#        temp.append(x)
#    
#    
#a=set(temp)
#
#for i in sorted(a):
#    print str(i)

import cPickle as pickle
#feats1=pickle.load(open("feats/trainfeatures.p","rb"))
#feats2=pickle.load(open("feats/devfeatures.p","rb"))
#trainset={}
#devset={}
#
#for i,tweet in enumerate(btweets):
#    if not feats1.has_key(tweet["sid"]):
#        #features=feats1[tweet["sid"]]
#        features={}
#        print "processing train: ",i
#    
#        features["afinn"]=feature_afinn(tweet)
#        features["sent"]=feature_sent(tweet)
#        features["arzu"]=feature_arzu(tweet)
#        features["tag"]=feature_tags(tweet)
#        #features["extras"]=feature_extras(tweet)
#        features["firstlastword"]=feature_firstlastword(tweet)
#        features["chat"]=feature_chat(tweet)
#        features["abbrev"]=feature_abbrev(tweet)
#        features["interjection"]=feature_interjection(tweet)
#        features["punctuation"]=feature_punctuation(tweet)
#        features["negation"]=feature_negation(tweet)
#        features["hash"]=feature_hash(tweet)
#        features["emotion"]=feature_emotion(tweet)
#        features["lingemotion"]=feature_lingemotion(tweet)
#        features["wordnet"]=feature_wordnet(tweet)
#        features["posextras"]=feature_POSextras(tweet)
#        features["repetition"]=feature_repetition(tweet)
#        features["wordshape"]=feature_wordshape(tweet)
#        
#        #features["hash"]=feature_hash(tweet)
#        #features["sent"]=feature_sent(tweet)
#    else:
#        features=feats1[tweet["sid"]]
#    
#    trainset[tweet["sid"]]=features
    
#for i,tweet in enumerate(devtweets):
#    if not feats2.has_key(tweet["sid"]):
#        #features=feats1[tweet["sid"]]
#        features={}
#        
#        print "processing train: ",i
#        
#        features["afinn"]=feature_afinn(tweet)
#        features["sent"]=feature_sent(tweet)
#        features["arzu"]=feature_arzu(tweet)
#        features["tag"]=feature_tags(tweet)
#        features["extras"]=feature_extras(tweet)
#        features["firstlastword"]=feature_firstlastword(tweet)
#        features["chat"]=feature_chat(tweet)
#        features["abbrev"]=feature_abbrev(tweet)
#        features["interjection"]=feature_interjection(tweet)
#        features["punctuation"]=feature_punctuation(tweet)
#        features["negation"]=feature_negation(tweet)
#        features["hash"]=feature_hash(tweet)
#        features["emotion"]=feature_emotion(tweet)
#        features["lingemotion"]=feature_lingemotion(tweet)
#        features["wordnet"]=feature_wordnet(tweet)
#        features["posextras"]=feature_POSextras(tweet)
#        features["repetition"]=feature_repetition(tweet)
#        features["wordshape"]=feature_wordshape(tweet)
#        
#        
#        #features["hash"]=feature_hash(tweet)
#        #features["sent"]=feature_sent(tweet)
#    
#    else:
#        features=feats1[tweet["sid"]]
#    
#    devset[tweet["sid"]]=features
    
## writing to pickle
pickle.dump(trainset,open("trainfeatures1.p","wb"))
pickle.dump(devset,open("devfeatures1.p","wb"))




