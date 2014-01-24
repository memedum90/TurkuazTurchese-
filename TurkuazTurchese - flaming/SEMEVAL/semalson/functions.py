from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import nltk.classify.util
#from unigrams import bestwords,bestbigrams,bestposwords,bestposbigrams,freqwords,freqbigrams,trainset
from wordshape import *


def readTwo(path):
    f = open(path,'r')
    rset={}
    for line in f.readlines():
	line=line.strip().split("\t")
        rset[line[0].lower()]=line[1].lower()
    
    return rset

def readTwoArda(path):
    f = open(path,'r')
    rset={}
    for line in f.readlines():
	line=line.strip().split("\t")
        rset[line[1].lower()]=line[2].lower()
    
    return rset

def readTwoComma(path):
    f = open(path,'r')
    rset=[]
    for line in f.readlines():
        line=line.strip().split(",")
        rset.append(line[0].lower())
    
    return rset

def readOne(path):
    f = open(path,'r')
    rset=set()
    for line in f.readlines():
        line=line.strip()
        rset.add(line.lower())
    
    return list(rset)

def get_tweets(tweetset):
    res=[]
    
    for t in tweetset:
	res.append(t)
    
    return res

def get_arzu(wordset):
    res={}
    
    for t in wordset:
	res[t["word"]]={"sentiment":t["sentiment"],"poses":t["poses"]}
    return res

def get_arda(wordset):
    res={}
    
    for t in wordset:
    
	res[t["word"]]=t["sentiment"]
    
    return res

def get_hashlist(tweetset):
    res=[]
    for tweet in tweetset:
	for to in tweet["ark_output"]["tokens"]:
	    if to["tag"] == "#":
		if "#" in to["token"]:
		    res.append(to["token"])
		else:
		    res.append("#"+to["token"])
    
    for r in res:
	print r
    
    return res


def readEmotionPatterns(eset):
    res={}
    
    for e in eset:
	res[e["pattern_lhs"]]=e["pattern_rhs"]
    
    return res

def write_array(arr,name):
    s=""
    for w in arr:
	s= s+w.encode('utf-8')+"\n"
    
    myFile = open(name+".txt", 'w')
    myFile.write(s)
    myFile.close()
    
def find_all_tokens(trainset,extranot=[],pos=False):
    postokens=[]
    negtokens=[]
    neutokens=[]
    
    btweets=trainset

    nottaglist= ["U","@","$"] #ignore some tags
    nottaglist= nottaglist+extranot #add extra ignore tag list
    
    for t in btweets:
	temp=[]
	for to in t["ark_output"]["tokens"]:
	    if to["tag"] not in nottaglist:
                if to["tag"]=="^":
                    if pos:
                        temp.append(to["token"]+"_"+to["tag"])
                    else:
                        temp.append(to["token"])
                elif to["tag"]=="#":
                    #temp.append(to["token"])
                    a,b = shorten(to["token"][1:])
                    if pos:
                        temp.append(b+"_"+to["tag"])
                    else:
                        temp.append(b)
                else:
                    if pos:
                        #temp.append(to["token"]+"_"+to["tag"])
                        a,b = shorten(to["token"])
                        temp.append(b+"_"+to["tag"])
                    else:
                        #temp.append(to["token"])
                        a,b = shorten(to["token"])
                        temp.append(b)
	s = t["topic"]["sentiment"]
	
	if s == "positive":
	    postokens.extend(temp)
	elif s == "negative":
	    negtokens.extend(temp)
	else:
	    neutokens.extend(temp)
  
    return postokens, negtokens, neutokens

#def find_all_wanted_tokens(trainset,yes=[],pos=False):
#    postokens=[]
#    negtokens=[]
#    neutokens=[]
#    
#    btweets=trainset
#
#    #nottaglist= ["U","@","$"] #ignore some tags
#    #nottaglist= nottaglist+extranot #add extra ignore tag list
#    
#    for t in btweets:
#	temp=[]
#	for to in t["ark_output"]["tokens"]:
#	    if to["tag"] in yes:
#		if pos:
#		    temp.append(to["token"]+"_"+to["tag"])
#		else:
#		    temp.append(to["token"])
#	
#	s = t["topic"]["sentiment"]
#	
#	if s == "positive":
#	    postokens.extend(temp)
#	elif s == "negative":
#	    negtokens.extend(temp)
#	else:
#	    neutokens.extend(temp)
#  
#    return postokens, negtokens, neutokens   

def find_most_freq_words(trainset,n=100):
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","&"])
    
    alltokens = postokens + negtokens + neutokens
    
    all_words = nltk.FreqDist(w.lower() for w in alltokens)
    freq_words = all_words.keys()[:n]
    
    return freq_words

def find_most_freq_bigrams(trainset,n=100):
    
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","&"])
    
    alltokens = postokens + negtokens + neutokens
    
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(alltokens)
    bigrams=finder.nbest(bigram_measures.chi_sq,n)
    freq_bigrams = [(bigram[0]+' '+bigram[1]).lower() for bigram in bigrams]    
   
    return freq_bigrams

def find_best_words(trainset,n=500,POS=False): #find 1000 best words
    
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y"],pos=POS)
    
    for word in postokens:
        word_fd.inc(word.lower())
        label_word_fd['positive'].inc(word.lower())
     
    for word in negtokens:
        word_fd.inc(word.lower())
        label_word_fd['negative'].inc(word.lower())
    
    for word in neutokens:
        word_fd.inc(word.lower())
        label_word_fd['neutral'].inc(word.lower())
     
    pos_word_count = label_word_fd['positive'].N()
    neg_word_count = label_word_fd['negative'].N()
    neu_word_count = label_word_fd['neutral'].N()
    total_word_count = pos_word_count + neg_word_count + neu_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(label_word_fd['positive'][word],
            (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(label_word_fd['negative'][word],
            (freq, neg_word_count), total_word_count)
        neu_score = BigramAssocMeasures.chi_sq(label_word_fd['neutral'][word],
            (freq, neu_word_count), total_word_count)
        #word_scores[word] = pos_score + neg_score + neu_score
	word_scores[word] = pos_score + neg_score
	
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestwords = set([w for w, s in best])
    
    return bestwords

def find_positive_best_words(trainset,n=1000,POS=False): #find 1000 best words
    
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y"],pos=POS)
    #postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=[",","&","O","S","$","G","L","X","D","P","Z","M","Y"],pos=POS)
    
    #postokens,negtokens,neutokens = find_all_tokens(pos=POS)
    
    for word in postokens:
        word_fd.inc(word.lower())
        label_word_fd['positive'].inc(word.lower())
     
    for word in negtokens:
        word_fd.inc(word.lower())
        label_word_fd['not_positive'].inc(word.lower())
    
    for word in neutokens:
        word_fd.inc(word.lower())
        label_word_fd['not_positive'].inc(word.lower())
     
    pos_word_count = label_word_fd['positive'].N()
    oth_word_count = label_word_fd['not_positive'].N()
    total_word_count = pos_word_count + oth_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(label_word_fd['positive'][word],
            (freq, pos_word_count), total_word_count)
        oth_score = BigramAssocMeasures.chi_sq(label_word_fd['not_positive'][word],
            (freq, oth_word_count), total_word_count)
        #word_scores[word] = pos_score + oth_score
	word_scores[word] = pos_score
	
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestwords = set([w for w, s in best])
    
    return bestwords

def find_negative_best_words(trainset,n=1000,POS=False): #find 1000 best words
    
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    #postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y"],pos=POS)
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=[",","&","O","S","$","G","L","X","D","P","Z","M","Y"],pos=POS)
    
    for word in postokens:
        word_fd.inc(word.lower())
        label_word_fd['not_negative'].inc(word.lower())
     
    for word in negtokens:
        word_fd.inc(word.lower())
        label_word_fd['negative'].inc(word.lower())
    
    for word in neutokens:
        word_fd.inc(word.lower())
        label_word_fd['not_negative'].inc(word.lower())
     
    neg_word_count = label_word_fd['negative'].N()
    oth_word_count = label_word_fd['not_negative'].N()
    total_word_count = neg_word_count + oth_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        neg_score = BigramAssocMeasures.chi_sq(label_word_fd['negative'][word],
            (freq, neg_word_count), total_word_count)
        oth_score = BigramAssocMeasures.chi_sq(label_word_fd['not_negative'][word],
            (freq, oth_word_count), total_word_count)
        #word_scores[word] = neg_score + oth_score
	word_scores[word] = neg_score
	
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestwords = set([w for w, s in best])
    
    return bestwords

def find_best_bigrams(trainset,n=300,POS=False): #find 1000 best bigrams
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",",","&"])
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y","&"],pos=POS)
        
    posbigrams=nltk.util.bigrams(postokens)
    negbigrams=nltk.util.bigrams(negtokens)
    neubigrams=nltk.util.bigrams(neutokens)
    
    for bigram in posbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['positive'].inc(word.lower())
     
    for bigram in negbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['negative'].inc(word.lower())
    
    for bigram in neubigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['neutral'].inc(word.lower())
     
    pos_word_count = label_word_fd['positive'].N()
    neg_word_count = label_word_fd['negative'].N()
    neu_word_count = label_word_fd['neutral'].N()
    total_word_count = pos_word_count + neg_word_count + neu_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(label_word_fd['positive'][word],
            (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(label_word_fd['negative'][word],
            (freq, neg_word_count), total_word_count)
        neu_score = BigramAssocMeasures.chi_sq(label_word_fd['neutral'][word],
            (freq, neu_word_count), total_word_count)
        #word_scores[word] = pos_score + neg_score + neu_score
	word_scores[word] = pos_score + neg_score
	
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestbigrams = set([w for w, s in best])

    return bestbigrams

def find_positive_best_bigrams(trainset,n=5000, POS=False): #find 1000 best bigrams
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",",","&"])
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y","&"],pos=POS)
    #postokens,negtokens,neutokens = find_all_tokens(pos=POS)
        
    posbigrams=nltk.util.bigrams(postokens)
    negbigrams=nltk.util.bigrams(negtokens)
    neubigrams=nltk.util.bigrams(neutokens)
    
    for bigram in posbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['positive'].inc(word.lower())
     
    for bigram in negbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['not_positive'].inc(word.lower())
    
    for bigram in neubigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['not_positive'].inc(word.lower())
     
    pos_word_count = label_word_fd['positive'].N()
    oth_word_count = label_word_fd['not_positive'].N()
    total_word_count = pos_word_count + oth_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(label_word_fd['positive'][word],
            (freq, pos_word_count), total_word_count)
        oth_score = BigramAssocMeasures.chi_sq(label_word_fd['not_positive'][word],
            (freq, oth_word_count), total_word_count)
        word_scores[word] = pos_score + oth_score
    
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestbigrams = set([w for w, s in best])

    return bestbigrams

def find_negative_best_bigrams(trainset,n=5000,POS=False): #find 1000 best bigrams
    bestwords = []
    
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",","])
    #postokens,negtokens,neutokens = find_all_tokens(extranot=["P","O",",","&"])
    #postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=["P","O",",","D","L","Y","&"],pos=POS)
    postokens,negtokens,neutokens = find_all_tokens(trainset,extranot=[",","&","O","S","$","G","L","X"],pos=POS)
        
    posbigrams=nltk.util.bigrams(postokens)
    negbigrams=nltk.util.bigrams(negtokens)
    neubigrams=nltk.util.bigrams(neutokens)
    
    for bigram in posbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['not_negative'].inc(word.lower())
     
    for bigram in negbigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['negative'].inc(word.lower())
    
    for bigram in neubigrams:
	word= bigram[0]+' '+bigram[1]
        word_fd.inc(word.lower())
        label_word_fd['not_negative'].inc(word.lower())
     
    neg_word_count = label_word_fd['negative'].N()
    oth_word_count = label_word_fd['not_negative'].N()
    total_word_count = neg_word_count + oth_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
        neg_score = BigramAssocMeasures.chi_sq(label_word_fd['negative'][word],
            (freq, neg_word_count), total_word_count)
        oth_score = BigramAssocMeasures.chi_sq(label_word_fd['not_negative'][word],
            (freq, oth_word_count), total_word_count)
        word_scores[word] = neg_score + oth_score
    
    allbest= sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)
    #print len(allbest) #17025
    best = allbest[:n]
    bestbigrams = set([w for w, s in best])

    return bestbigrams

def parse_tweets(btweets,label=None):
    postweets=[]
    negtweets=[]
    neutweets=[]
    res=[]
    
    for t in btweets:
        s = t["topic"]["sentiment"]
        
        if s == "positive":
            postweets.append(t)
        elif s == "negative":
            negtweets.append(t)
        else:
            neutweets.append(t)
    
    if label == "positive":
	res= postweets,negtweets+neutweets
    elif label == "negative":
	res= negtweets, postweets+neutweets
    else:
	res=postweets, negtweets,neutweets
    
    return res

def getavg(l):
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')
    
def updateset(refset,addset):
    size= len(refset)
    
    i=0
    
    while i < size:
	refset[i] = refset[i] + addset[i]
	i=i+1
    
    return refset

def printres(refset):
    size= len(refset)
    
    i=0
    
    while i < size:
	refset[i] = refset[i]/10.0
	i=i+1
    
    print "avg_precision:",refset[0], " avg_recall:",refset[1], " avg_f:",refset[2]
    print "avg_precision2:",refset[3], " avg_recall2:",refset[4], " avg_f2:",refset[5]
    print "pos_precision:",refset[6], " pos_recall:",refset[7], " pos_f:",refset[8]
    print "neg_precision:",refset[9], " neg_recall:",refset[10], " neg_f:",refset[11]
    print "neu_precision:",refset[12], " neu_recall:",refset[13], " neu_f:",refset[14]


#def run_naive_all(trainset):
#    global bestwords
#    global bestposwords
#    global bestbigrams
#    global bestposbigrams
#    global freqwords
#    global freqbigrams
#    
#    #sentweets,othertweets=parse_tweets(trainset,label)
#    postweets,negtweets,neutweets=parse_tweets(trainset)
#    
##    if label == "positive":
##	bestwords=find_best_words(300) #iyi bu
##	#bestwords=find_negative_best_words()
##	#bestwords=find_positive_best_words(1000)
##	bestposwords=find_positive_best_words(3000,POS=True) #300
##	bestbigrams=find_positive_best_bigrams(1000)
##	bestposbigrams=find_positive_best_bigrams(1000,POS=True) #500
##    elif label == "negative":
##	bestwords=find_negative_best_words() #100
##	bestposwords=find_negative_best_words(POS=True)
##	bestbigrams=find_negative_best_bigrams() #300
##	bestposbigrams=find_negative_best_bigrams(POS=True)
#	
#    bestwords=find_best_words() #100
#    bestposwords=find_best_words(POS=True)
#    bestbigrams=find_best_bigrams() #300
#    bestposbigrams=find_best_bigrams(POS=True)
#    
#    freqwords=find_most_freq_words()
#    freqbigrams=find_most_freq_bigrams()
#    
#    # train
#    posfeats= apply_feats_all(postweets,"positive")
#    negfeats= apply_feats_all(negtweets,"negative")
#    neufeats= apply_feats_all(neutweets,"neutral")
#    trainingset = posfeats+negfeats+neufeats
#    
#    classifier = NaiveBayesClassifier.train(trainingset)
#
#    return classifier

#def test_classifier_all(classifier,testset):
#    pred = {}
#    import collections
#    refsets = collections.defaultdict(set)
#    testsets = collections.defaultdict(set)
#    
#    # test
#    postest,negtest,neutest=parse_tweets(testset)
#    testposfeats= apply_feats_all(postest,"positive")
#    testnegfeats= apply_feats_all(negtest,"negative")
#    testneufeats= apply_feats_all(neutest,"neutral")
#    
#    testingset = testposfeats+testnegfeats+testneufeats
#    
#    accuracy= nltk.classify.util.accuracy(classifier,testingset)
#    
#    for i,t in enumerate(testset):
#	tfeats= use_features(t)
#	guess = classifier.classify(tfeats)
#	
#	topic=t["topic"]["sentiment"]
#	
#	refsets[topic].add(i)
#	testsets[guess].add(i)
#    
#    precision= nltk.metrics.precision(refsets["positive"], testsets["positive"])
#    recall= nltk.metrics.recall(refsets["positive"], testsets["positive"])
#    f= nltk.metrics.f_measure(refsets["positive"], testsets["positive"])
#    
#    precision2= nltk.metrics.precision(refsets["negative"], testsets["negative"])
#    recall2= nltk.metrics.recall(refsets["negative"], testsets["negative"])
#    f2= nltk.metrics.f_measure(refsets["negative"], testsets["negative"])
#    
#    precision3= nltk.metrics.precision(refsets["neutral"], testsets["neutral"])
#    recall3= nltk.metrics.recall(refsets["neutral"], testsets["neutral"])
#    f3= nltk.metrics.f_measure(refsets["neutral"], testsets["neutral"])
#    
#    #print posclassifier.prob_classify(tweetfeat).prob('positive')
#    classifier.show_most_informative_features(50)
#    print "accuracy: ",accuracy
#    print "precision: ",precision, precision2, precision3
#    print "recall: ",recall, recall2,recall3
#    print "f score: ",f,f2,f3
#    
#    return accuracy
#    
#    #error_reporting(classifier,testset,label)

## 10-fold cross validation
#def k_fold_cross_validation(items, k, randomize=False):
#    from random import shuffle
#    
#    if randomize:
#        items = list(items)
#        shuffle(items)
#
#    slices = [items[i::k] for i in xrange(k)]
#
#    for i in xrange(k):
#        validation = slices[i]
#        training = [item
#                    for s in slices if s is not validation
#                    for item in s]
#        yield training, validation
#
#posacc=[]
#negacc=[]
#resset=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#i=0
#for training, validation in k_fold_cross_validation(btweets, 10):
#    print i
#    trainset=training #set global variable
#    posclassifier=run_naive(training,"positive")
#    acc1=test_classifier(posclassifier,validation,"positive")
#    posacc.append(acc1)
#    negclassifier=run_naive(training,"negative")
#    acc2=test_classifier(negclassifier,validation,"negative")
#    negacc.append(acc2)
#    
#    # all 2 together
#    res= run_test(posclassifier,negclassifier,validation)
#    resset= updateset(resset,res)
#    i=i+1
#
#printres(resset)    
#print getavg(posacc)
#print getavg(negacc)
