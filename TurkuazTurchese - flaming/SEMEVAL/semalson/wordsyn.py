import nltk
from nltk.corpus import wordnet as wn

import pymongo

from pymongo import MongoClient
import itertools
#from wordshape import *
from functions import *
from features import *
from core import *

connection = MongoClient('localhost', 27017)
db = connection.SEMEVALTweet2013

all_tweets = db.Tweets;
btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"}]})
btweets = get_tweets(btweets)
devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"DevB"}]})
devtweets = get_tweets(devtweets)

def find_syn(word,tag):
    
    if tag =="N":
        tag="noun"
    elif tag =="V":
        tag="verb"
    
    resset=[]
    synsets = wn.synsets(word)
    for synset in synsets:
        lex= synset.lexname
        lemmas=synset.lemma_names
        
        print lex, lemmas
        
        if tag in lex and "emotion" in lex:
            resset.extend(lemmas)
    
    return resset
            
print find_syn("hate","V")
        
        
        



