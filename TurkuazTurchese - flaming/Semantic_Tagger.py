#sentiment140.com
#Copyright Mehmet Durna ;)


import json
import requests

def generateJson(tweetlist):
    data={"data" : []}
    for tweet in tweetlist:
        data["data"].append({"text" : tweet })
    return json.dumps(data)


def sendRequest(dataj):
    host = "http://www.sentiment140.com/api/bulkClassifyJson?appid=mehmet.durna@boun.edu.tr"
    r = requests.post(host, data=dataj)
    
    return r


    
def makeDict(tweetlist):
    dict={}
    for tweet in tweetlist:
        dict[tweet['id']]= tweet    
    return dict

#takes a list, returns the same list with dicts full with sentiment values
def classifyTweets(tweetlist):
    tdict=makeDict(tweetlist)
    dataj=generateJson(tweetlist)
    print 'request has been prepared'
    r= sendRequest(dataj)
    print "request sent"
    js=r.json()
    jsonlist=js['data']
    tlist=[]
    for tweet in jsonlist:
        dic=tdict[tweet['id']]
        dic['sentiment']=polarity2str(tweet['polarity'])
        tlist.append(dic)
    return tlist

import json

def polarity2str(polarity):
    if polarity==0:
        return "negative"
    elif polarity==2:
        return "neutral"
    elif polarity==4:
        return "positive"
    else:
        return 0
    
    
def classifyTweet(tweet):
    tlist=[]
    tlist.append(tweet)
    dataj=generateJson(tlist)
    #print 'request has been prepared'
    r= sendRequest(dataj)
    
    #print "request sent"
    
    js=json.loads(r.content)
    
    polarity=js['data'][0]['polarity']
    return polarity2str(polarity)





def readTweets(filename):
    tweetlist=[]
    
    
    f=open(filename, 'r')
    tweetstr=f.readline()
    count=0
    while tweetstr:
        count+=1
        tweet=eval(tweetstr)
        tweetlist.append(tweet)
        tweetstr=f.readline()
        # Return tweet_list
    f.close()
    return [count,tweetlist ] 
def write2file(tweetlist, filename):
    
    f=open(filename, 'w')
    for tweet in tweetlist:
        f.write(unicode(tweet))
        f.write("\n")
    f.close()
    
    
def main():
    file2read='flaming2.txt'
    file2write='flaming3.txt'
    
    [count,tweetlist]=readTweets(file2read)
    print "%d tweets gathered" % count
    
    #returns the same list with the sentiment field
    tlist=classifyTweets(tweetlist)
    
    #writes the list to the file
    write2file(tlist, file2write)
#not necessary to look down from here

# def testTool():
#     from pymongo import MongoClient
#     connection = MongoClient('localhost', 27017)
#     db = connection.SEMEVALTweet2013
#     
#     
#     
#     all_tweets = db.Tweets;
#     #btweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"},{"task":"DevB"}]})
#     bweets = all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"FullTrainingB"}]})
#     btweets = []
#     
#     for t in bweets:
#         btweets.append(t)
#     
#     #devtweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"TestB"}]})
#     detweets= all_tweets.find({"tweet":{'$ne':'Not Available'}, "$or":[{"task":"DevB"}]})
#     devtweets =[]
#     for t in detweets:
#         devtweets.append(t)
#      
#     testset=devtweets
#     testset.extend(btweets)
#     print "reading tweets done.."
#     tweetlist=[]
#     
#     for tweet in testset:
#         topic=tweet["topic"]["sentiment"]
#         tw={'text': tweet['tweet'] , 'id': tweet['sid'] , 'sentiment' : topic}
#         tweetlist.append(tw)
#     print 'tweetlist prepared with %d tweets'% len(tweetlist) 
#     data={"data" : []}
#     for tweet in tweetlist:
#         data["data"].append({"text" : tweet["text"]  , "id" : tweet["id"], "sentiment" : tweet['sentiment']})
#       
#     dataj=json.dumps(data) 
#     print 'request has been prepared'
#     r= sendRequest(dataj)
#     print "request sent"
#       
#     js=r.json() 
#     
#     tpneg=0.0
#     tppos=0.0
#     tpneut=0.0
#     fppos=0.0
#     fpneg=0.0
#     fpneut=0.0
#     fnneg=0.0
#     fnpos=0.0
#     fnneut=0.0
#     error=0.0
#     baderror=0.0
#     
#     for tweet in js['data']:
#         if tweet['polarity']==0:
#             if tweet['sentiment']=="negative":
#                 tpneg+=1
#             else:
#                 fpneg+=1
#         else:
#             if tweet['sentiment']=="negative":
#                 fnneg+=1
#         if tweet['polarity']==2:
#             if tweet['sentiment']=="neutral":
#                 tpneut+=1
#             else:
#                 fpneut+=1
#         else:
#             if tweet['sentiment']=="neutral":
#                 fnneut+=1
#         if tweet['polarity']==4:
#             if tweet['sentiment']=="positive":
#                 tppos+=1
#             else:
#                 fppos+=1
#         else:
#             if tweet['sentiment']=="positive":
#                 fnpos+=1
#         if tweet['polarity']==0 and tweet['sentiment']=="positive":
#             baderror+=1
#         if tweet['polarity']==4 and tweet['sentiment']=="negative":
#             baderror+=1
#     posprecision=tppos/(tppos+fppos)
#     posrecall=tppos/(tppos+fnpos)  
#     negprecision=tpneg/(tpneg+fpneg)
#     negrecall=tpneg/(tpneg+fnneg)
#     neutprecision=tpneut/(tpneut+fpneut)
#     neutrecall=tpneut/(tpneut+fnneut)
#     fpos=2*posprecision*posrecall/(posprecision+posrecall)
#     fneg=2*negprecision*negrecall/(negprecision+negrecall)
#     fneut=2*neutprecision*neutrecall/(neutprecision+neutrecall)   
#     print "Positive Precision, Recall, F score: %f %f %f" % (posprecision, posrecall,fpos)
#     print "Negative Precision, Recall, F score: %f %f %f" % (negprecision, negrecall,fneg)
#     print "Neutral Precision, Recall, F score: %f %f %f" % (neutprecision, neutrecall,fneut)
#     print "bad errors : %d" %baderror
#     f=open("json_output1.txt", 'w')
#     for tweet in js['data']:
#         f.write(unicode(tweet))
#         f.write('\n')
#     f.close()
