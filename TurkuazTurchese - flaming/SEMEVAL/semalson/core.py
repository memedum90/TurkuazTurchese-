from functions import *
from features import *

def run_alg(trainset,label,alg): # sentiment tweets, others, label for classifier
    sentweets,othertweets=parse_tweets(trainset,label)
    
    compute_words(trainset,label)
    # train
    feats= apply_feats(sentweets,label)
    others= apply_feats(othertweets,"not_"+label)
    trainingset = feats+others
    
    if alg == "naive":
        classifier = nltk.classify.NaiveBayesClassifier.train(trainingset)
    elif alg == "maxent":
        classifier = nltk.classify.MaxentClassifier.train(trainingset,max_iter=50,min_lldelta=0.01)
	#classifier = nltk.classify.MaxentClassifier.train(trainingset,max_iter=20)
    else:
	classifier = nltk.DecisionTreeClassifier.train(trainingset, entropy_cutoff=0,support_cutoff=0)
	print classifier
    
    return classifier

import cPickle as pickle
feats1=pickle.load(open("trainfeatures1.p","rb"))
feats2=pickle.load(open("devfeatures1.p","rb"))
allfeats=feats1
allfeats.update(feats2)

def use_features(tweet,label=None):
    features={}
    
    if label == "positive" or label == "not_positive" :
	#features.update(allfeats[tweet["sid"]]["bestwords"])
	#features.update(allfeats[tweet["sid"]]["bestbigrams"])
	#features.update(allfeats[tweet["sid"]]["unigrams"])
	#features.update(allfeats[tweet["sid"]]["bigrams"])
#	features.update(allfeats[tweet["sid"]]["afinn"])
#	features.update(allfeats[tweet["sid"]]["sent"])
#        features.update(allfeats[tweet["sid"]]["arzu"]) #off
	features.update(allfeats[tweet["sid"]]["tag"]) #off
        features.update(allfeats[tweet["sid"]]["repetition"]) #deprecated
#	features.update(allfeats[tweet["sid"]]["wordshape"]) #in best words called function
	features.update(allfeats[tweet["sid"]]["firstlastword"])
        features.update(allfeats[tweet["sid"]]["chat"])
#	features.update(allfeats[tweet["sid"]]["abbrev"])
	features.update(allfeats[tweet["sid"]]["interjection"])
#	features.update(allfeats[tweet["sid"]]["punctuation"])
#	features.update(allfeats[tweet["sid"]]["negation"])
#	features.update(allfeats[tweet["sid"]]["hash"])
	features.update(allfeats[tweet["sid"]]["hash_positive"])
#	features.update(allfeats[tweet["sid"]]["emotion"]) #deprecated
#	features.update(allfeats[tweet["sid"]]["lingemotion"])
#	features.update(allfeats[tweet["sid"]]["wordnet"])
	features.update(allfeats[tweet["sid"]]["emo"]) #deprecated
	features.update(allfeats[tweet["sid"]]["arda"])#degisken
#	features.update(allfeats[tweet["sid"]]["epattern"])
	features.update(allfeats[tweet["sid"]]["afinn_epattern"])
	features.update(allfeats[tweet["sid"]]["all_positive"])
#	features.update(allfeats[tweet["sid"]]["all_negative"])
#	features.update(allfeats[tweet["sid"]]["CAP"])
#	features.update(allfeats[tweet["sid"]]["quotation"])
#	
#	
#	# POS features TODO gercek pos tagger ile dene
#	features.update(allfeats[tweet["sid"]]["posextras"]) #off
#	features.update(allfeats[tweet["sid"]]["pos_bestwords"])
#	features.update(allfeats[tweet["sid"]]["poswords"])
#	features.update(allfeats[tweet["sid"]]["posbigrams"])
#	features.update(allfeats[tweet["sid"]]["pos_firstlastword"])
#	features.update(allfeats[tweet["sid"]]["pos_bestbigrams"])
    elif label == "negative" or label == "not_negative" :
	#features.update(allfeats[tweet["sid"]]["bestwords"])
	#features.update(allfeats[tweet["sid"]]["bestbigrams"])
	#features.update(allfeats[tweet["sid"]]["unigrams"])
	#features.update(allfeats[tweet["sid"]]["bigrams"])
#	features.update(allfeats[tweet["sid"]]["afinn"])
#	features.update(allfeats[tweet["sid"]]["sent"])
#        features.update(allfeats[tweet["sid"]]["arzu"]) #off
	features.update(allfeats[tweet["sid"]]["tag"]) #off
        features.update(allfeats[tweet["sid"]]["repetition"]) #deprecated
#	features.update(allfeats[tweet["sid"]]["wordshape"]) #in best words called function
	features.update(allfeats[tweet["sid"]]["firstlastword"])
        features.update(allfeats[tweet["sid"]]["chat"])
#	features.update(allfeats[tweet["sid"]]["abbrev"])
	features.update(allfeats[tweet["sid"]]["interjection"])
#	features.update(allfeats[tweet["sid"]]["punctuation"])
	features.update(allfeats[tweet["sid"]]["negation"])
	features.update(allfeats[tweet["sid"]]["hash"])
#	features.update(allfeats[tweet["sid"]]["hash_positive"])
#	features.update(allfeats[tweet["sid"]]["emotion"]) #deprecated
#	features.update(allfeats[tweet["sid"]]["lingemotion"])
#	features.update(allfeats[tweet["sid"]]["wordnet"])
	features.update(allfeats[tweet["sid"]]["emo"]) #deprecated
	features.update(allfeats[tweet["sid"]]["arda"])#degisken
#	features.update(allfeats[tweet["sid"]]["epattern"])
	features.update(allfeats[tweet["sid"]]["afinn_epattern"])
#	features.update(allfeats[tweet["sid"]]["all_positive"])
	features.update(allfeats[tweet["sid"]]["all_negative"])
#	features.update(allfeats[tweet["sid"]]["CAP"])
#	features.update(allfeats[tweet["sid"]]["quotation"])
#	
#	
#	# POS features TODO gercek pos tagger ile dene
#	features.update(allfeats[tweet["sid"]]["posextras"]) #off
#	features.update(allfeats[tweet["sid"]]["pos_bestwords"])
#	features.update(allfeats[tweet["sid"]]["poswords"])
#	features.update(allfeats[tweet["sid"]]["posbigrams"])
#	features.update(allfeats[tweet["sid"]]["pos_firstlastword"])
#	features.update(allfeats[tweet["sid"]]["pos_bestbigrams"])
    
        #print features
    return features

def apply_feats(tweetset,label):
    result=[]
    
    for t in tweetset:
	feats=use_features(t,label)
	result.append((feats,label))
    
    return result

def prepare_files(testset,testsets,name):
    pred=""
    gs=""
    negset=testsets["negative"]
    posset=testsets["positive"]
    neuset=testsets["neutral"]
    
    for i,t in enumerate(testset):
	reel= t["topic"]["sentiment"]
	tid= "NA"
	uid= t["uid"]
	
	label=""
	if i in negset:
	    label="negative"
	elif i in posset:
	    label="positive"
	else:
	    label="neutral"
	
	#twit= "blabla\t"
	#pred=pred+"NA\t"+"NA\t"+label+"\t"+twit+"\n"
	#gs=gs+"NA\t"+"NA\t"+reel+"\t"+twit+"\n"
	
	twit= "NA"
	pred=pred+tid+"\t"+uid+"\t"+label+"\t"+twit+"\n"
	gs=gs+tid+"\t"+uid+"\t"+reel+"\t"+twit+"\n"
	
    f1 = open(name+".pred", 'w')
    f1.write(pred)
    f2 = open(name+".gs", 'w')
    f2.write(gs)
	
def test_classifier(classifier,testset,label):
    pred = {}
    import collections
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    
    # test
    testsen,testother=parse_tweets(testset,label)
    testfeats= apply_feats(testsen,label)
    testothers= apply_feats(testother,"not_"+label)
    testingset = testfeats+testothers
    
    accuracy= nltk.classify.util.accuracy(classifier,testingset)
    
    for i,t in enumerate(testset):
	tfeats= use_features(t,label)
	guess = classifier.classify(tfeats)
	
	topic=t["topic"]["sentiment"]
	if topic != label:
	    topic="not_"+label
	
	refsets[topic].add(i)
	testsets[guess].add(i)
    
    precision= nltk.metrics.precision(refsets[label], testsets[label])
    recall= nltk.metrics.recall(refsets[label], testsets[label])
    f= nltk.metrics.f_measure(refsets[label], testsets[label])
    
    #print posclassifier.prob_classify(tweetfeat).prob('positive')
    #classifier.show_most_informative_features(50)
    
    #error_reporting(classifier,testset,label)
    print "accuracy: ",accuracy
    print "precision: ",precision
    print "recall: ",recall
    print "f score: ",f
    
    return accuracy
	
def error_reporting(classifier,testset,label):
    errors = []
    for t in testset:
	tfeats= use_features(t,label)
	guess = classifier.classify(tfeats)
	tag = t["topic"]["sentiment"]
	
	if tag != label:
	    tag = "not_"+label
	    
	if guess != tag:
	    errors.append( (tag, guess, t["tweet"], tfeats))
    
    print "total error=%d in %d test tweets" % (len(errors),len(testset)) 	
    for (tag, guess, name, feats) in sorted(errors):
	print "tweet: ", name.encode("utf-8")
	print "correct label: ",tag
	print "predicted label: ", guess
	print "features: ", feats
	print "\n\n"
	

def run_test(posclassifier,negclassifier,testset,name,run):
    import collections
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    up=0.6
    low=0.44
    errors=[]
    
    # buyuk olana atiyorum, 0.4-0.6 arasi neutral diyelim.. fark olayina bak gerekecek mi..
    # arzucan list. hem kelimeyi, hem de duygusunu ekle, basit rule-based bir sey olsa, decision tree
    
    for i,t in enumerate(testset):
	print "Processing: ",i," total:",len(testset)
	postweetfeat=use_features(t,"positive")
	negtweetfeat=use_features(t,"negative")
	
	topic=t["topic"]["sentiment"]
	if topic != "positive" and topic != "negative":
	    topic="neutral"
	
	refsets[topic].add(i)
	#print t["tweet"]
	posprob= posclassifier.prob_classify(postweetfeat).prob('positive')
	negprob= negclassifier.prob_classify(negtweetfeat).prob('negative')
	
	
	#if posprob>pth:
	#    testsets["positive"].add(i)
	#elif negprob>nth:
	#    testsets["negative"].add(i)
	#else:
	#    testsets["neutral"].add(i)
	guess=""
	if posprob>negprob:
	    if posprob>low:
		testsets["positive"].add(i)
		guess="positive"
	    else:
		testsets["neutral"].add(i)
		guess="neutral"
	
	if negprob>posprob:
		
	    if negprob>low:
		#if negprob-posprob>0.75:
		#    testsets["neutral"].add(i)
		#    guess="neutral"
		##elif negprob>0.9: # no trust in negative classifier
		##    if posprob>low:
		##	testsets["positive"].add(i)
		##	guess="positive"
		#else:
		    testsets["negative"].add(i)
		    guess="negative"
	    else:
		testsets["neutral"].add(i)
		guess="neutral"
		
	if guess != topic:
	    errors.append( (topic, guess, t["tweet"], postweetfeat,negtweetfeat, posprob, negprob))
	
    #prepare_files(testset,testsets,name)
    
    pos_precision= nltk.metrics.precision(refsets['positive'], testsets['positive'])
    pos_recall= nltk.metrics.recall(refsets['positive'], testsets['positive'])
    pos_f= nltk.metrics.f_measure(refsets['positive'], testsets['positive'])
    neg_precision= nltk.metrics.precision(refsets['negative'], testsets['negative'])
    neg_recall= nltk.metrics.recall(refsets['negative'], testsets['negative'])
    neg_f= nltk.metrics.f_measure(refsets['negative'], testsets['negative'])
    neu_precision= nltk.metrics.precision(refsets['neutral'], testsets['neutral'])
    neu_recall= nltk.metrics.recall(refsets['neutral'], testsets['neutral'])
    neu_f= nltk.metrics.f_measure(refsets['neutral'], testsets['neutral'])
    
    plen= len(refsets["positive"])
    nlen= len(refsets["negative"])
    #print pos_precision, neg_precision
    
    avg_precision= (pos_precision+neg_precision)/2.0
    avg_recall= (pos_recall+neg_recall)/2.0
    avg_f= (pos_f+neg_f)/2.0
    
    avg_precision2= (plen*pos_precision+nlen*neg_precision)/float(plen+nlen)
    avg_recall2= (plen*pos_recall+nlen*neg_recall)/float(plen+nlen)
    avg_f2= (plen*pos_f+nlen*neg_f)/float(plen+nlen)
    
       
    import cPickle as pickle
    # writing to pickle
    #pickle.dump(errors,open("runs/run"+str(run)+"/errors.p","wb"))
    #pickle.dump([avg_precision, avg_recall, avg_f, pos_precision, pos_recall, pos_f, neg_precision, neg_recall, neg_f, neu_precision, neu_recall, neu_f],open("runs/run"+str(run)+"/scores.p","wb"))

#    print "total error=%d in %d test tweets" % (len(errors),len(testset)) 	
#    for (tag, guess, name, feats,feats2, pos, neg) in sorted(errors): 
#	print 'tweet: ',name.encode('utf-8')
#	print 'correct: ',tag,'guess: ',guess
#	print pos, "pos feats: ",feats
#	print neg, "neg feats: ",feats2
#	print "pos prob: ",pos
#	print "neg prob: ",neg
#	print "\n\n"
    
    print avg_precision, avg_recall, avg_f
    #print avg_precision2, avg_recall2, avg_f2
    print pos_precision, pos_recall, pos_f
    print neg_precision, neg_recall, neg_f
    print neu_precision, neu_recall, neu_f
    
    return avg_precision, avg_recall, avg_f, pos_precision, pos_recall, pos_f, neg_precision, neg_recall, neg_f, neu_precision, neu_recall, neu_f


	
	    