from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import WhitespaceTokenizer
from wordshape import *
from functions import *
#from pymongo import MongoClient
import pymongo
import en

bestwords=[]
bestposwords=[]
bestbigrams=[]
bestposbigrams=[]
freqwords=[]
freqbigrams=[]
afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))

#connection = MongoClient('localhost', 27017)
# connection=pymongo.connection.Connection('79.123.176.106', 27017)
# db = connection.SEMEVALTweet2013
# 
# all_features = db.TweetFeatures
# all_extras = db.IntervalFeatures
# 
# arzlist = db.ArzucanWordList.find()
# arzlist = get_arzu(arzlist)
# 
# ardalist= db.OurSentimentWords.find()
# ardalist= get_arda(ardalist)
# 
# ePatterns= db.EmotionPatterns.find()
# ePatterns= readEmotionPatterns(ePatterns)

chatlist= readTwo("lists/chat.csv")
emolist=readTwo("lists/emoticons.csv")	
twlist= readOne("lists/tw.csv")
plist = readTwoComma("lists/Positive.csv")
nlist= readTwoComma("lists/Negative.csv")
llist= readTwoComma("lists/Litigious.csv")
ulist= readTwoComma("lists/Uncertainty.csv")
mslist= readTwoComma("lists/ModalStrong.csv")
mwlist= readTwoComma("lists/ModalWeak.csv")
#allist= plist+nlist+llist+ulist+mslist+mwlist
allist= llist+ulist+mslist+mwlist

Alist= readTwoArda("lists/pos-neg-intervals")

negations = []
negations.append("ain't")
negations.append("aint")
negations.append("isn't")
negations.append("isnt")
negations.append("aren't")
negations.append("arent")
negations.append("wasn't")
negations.append("wasnt")
negations.append("won't")
negations.append("wont")
negations.append("no")
negations.append("n[o+]")
negations.append("[n+]o")
negations.append("[n+][o+]")
negations.append("n0")
negations.append("n[0+]")
negations.append("[n+]0")
negations.append("[n+][0+]")
negations.append("not")
negations.append("n[o+]t")
negations.append("no[t+]")
negations.append("[n+]ot")
negations.append("n[o+][t+]")
negations.append("[n+][o+][t+]")
negations.append("n0t")
negations.append("n[0+]t")
negations.append("n0[t+]")
negations.append("[n+]0t")
negations.append("n[0+][t+]")
negations.append("[n+][0+][t+]")
negations.append("cannot")
negations.append("can't")
negations.append("cant")
negations.append("shouldn't")
negations.append("shouldnt")
negations.append("wouldn't")
negations.append("wouldnt")
negations.append("don't")
negations.append("dont")
negations.append("doesn't")
negations.append("doesnt")
negations.append("hasn't")
negations.append("hasnt")
negations.append("haven't")
negations.append("havent")
negations.append("didn't")
negations.append("didnt")
negations.append("never")
negations.extend(["neva","nvr","nevr","nev[a+]","#never","n[e+]ver","nevva","neve[r+]","nver","nevah","nva","ne'er","-never","nev[e+]r","#inever"])
negations.extend(["couldn't","couldnt","nt","n0t","nawt","nto","not-","_not","naht","n't","-not-","noit","/not/","noht"])


def compute_words(trainset,label):
    global bestwords
    global bestposwords
    global bestbigrams
    global bestposbigrams
    global freqwords
    global freqbigrams

    if label == "positive":
	#bestwords=find_best_words(300) #iyi bu
	#bestwords=find_negative_best_words()
	bestwords=find_positive_best_words(trainset,300)
	bestposwords=find_positive_best_words(trainset,300,POS=True) #300
	bestbigrams=find_positive_best_bigrams(trainset,100)
	bestposbigrams=find_positive_best_bigrams(trainset,500,POS=True) #500
    elif label == "negative":
	bestwords=find_negative_best_words(trainset,200) #100
	bestposwords=find_negative_best_words(trainset,100,POS=True)
	bestbigrams=find_negative_best_bigrams(trainset,100) #300
	bestposbigrams=find_negative_best_bigrams(trainset,100,POS=True)
    
    #print bestbigrams
    #print len(bestwords)

def feature_quotation(tweet):
    features={}
    
    text=tweet["tweet"]
    s=[(a.start(), a.end()) for a in list(re.finditer("\"", text))]
    
    if len(s)>1:
	features["quotation"]=True
	features["quotation_count"]=len(s)/2
    
    return features


def feature_all_positive(tweet):
    features={}
    sl=[]
    
    tf= list(all_extras.find({"task":"FullTrainingB","sid" :tweet["sid"]}))
    if len(tf)==0:
	tf= list(all_extras.find({"task":"DevB","sid" :tweet["sid"]}))
	
    
    for d in tf:
	if d["feature"]=="slang":
	    #features[d["value"]]= True
	    for s in d["value"]:
		if len(s)>1:
		    sl.append(s)
	#if d["feature"]=="numOfNegSentIndicator":
	#    features["numOfNegSentIndicator"]=d["value"]
	#if d["feature"]=="numOfPosSentIndicator":
	#    features["numOfPosSentIndicator"]=d["value"]
	#if d["feature"]=="afinn_tag_seq":
	#    features["afinn_tag_seq"]=d["value"]
	#if d["feature"]=="our_sentimentword_tag_seq":
	#    features["our_sentimentword_tag_seq"]=d["value"]
	#if d["feature"]=="wnscore_negative":
	#    features["wnscore_negative"]=d["value"]
	#if d["feature"]=="wnscore_positive":
	#    features["wnscore_positive"]=d["value"]
	#if d["feature"]=="wnscore_seq":
	#    features["wnscore_seq"]=d["value"]
	#if d["feature"]=="endsWExlamation":
	    #features["endsWExlamation"]=d["value"]
	    #features["endsWExlamation_count"]=len(tweet["ark_output"]["tokens"][-1]["token"])
	
    for s in sl:
	features["slang"]=s
	
    return features

def feature_all_negative(tweet):
    features={}
    sl=[]
    
    tf= list(all_extras.find({"task":"FullTrainingB","sid" :tweet["sid"]}))
    if len(tf)==0:
	tf= list(all_extras.find({"task":"DevB","sid" :tweet["sid"]}))
    
    for d in tf:
	#if d["feature"]=="afinn":
	#    features["afinn_label"]= d["value"]
	#if d["feature"]=="afinn_avg":
	#    features["afinn_avg"]= d["value"]
	#if d["feature"]=="slang":
	#    #features[d["value"]]= True
	#    for s in d["value"]:
	#	if len(s)>1:
	#	    sl.append(s)
	#if d["feature"]=="numOfNegSentIndicator":
	#    features["numOfNegSentIndicator"]=d["value"]
	#if d["feature"]=="numOfPosSentIndicator":
	#    features["numOfPosSentIndicator"]=d["value"]
	#if d["feature"]=="afinn_tag_seq":
	#    features["afinn_tag_seq"]=d["value"]
	#if d["feature"]=="our_sentimentword_tag_seq":
	#    features["our_sentimentword_tag_seq"]=d["value"]
	#if d["feature"]=="wnscore_negative":
	#    features["wnscore_negative"]=d["value"]
	#if d["feature"]=="wnscore_positive":
	#    features["wnscore_positive"]=d["value"]
	#if d["feature"]=="wnscore_seq":
	#    features["wnscore_seq"]=d["value"]
	if d["feature"]=="endsWExlamation":
	    features["endsWExlamation"]=d["value"]
	    features["endsWExlamation_count"]=len(tweet["ark_output"]["tokens"][-1]["token"])
	
#    for s in sl:
#	features["slang"]=s
	
    
    return features


def feature_afinn_EPattern(tweet):
    features={}
    pat=[]
    sense = []
    
    text=tweet["tweet"].lower()
    patSeq=""
    
    # add patterns!
    for p in ePatterns:
	if ":" not in p or "=" not in p:
	    if p in text:
		features[p]=True
		if ePatterns[p]=="POSITIVE" or ePatterns[p]=="NEGATIVE":
		    patSeq=patSeq+ePatterns[p].lower()[0]
		pat.append(p)
    
    features["pattern_seq"]=patSeq
    
    if len(patSeq) != 0:	
	features["pattern_first_sense"]= patSeq[0]
	features["pattern_last_sense"]= patSeq[-1]
    else:
	features["pattern_first_sense"]= ""
	features["pattern_last_sense"]= ""
    
    for p in pat:
	text=text.replace(p,"").strip()
    
    for to in tweet["ark_output"]["tokens"]:
	if to["token"] in text and to["tag"] not in ["U","@","^"]:
	    if to["token"].lower() in afinn:
		features[to["token"].lower()]=True
		sc= afinn[to["token"].lower()]
		label=0
		
		if sc>3:
		    label=2
		elif sc>0:
		    label=1
		elif sc==0:
		    label=0
		elif sc > -3:
		    label=-1
		else:
		    label=-2
		    
		if "not "+to["token"].lower() in tweet["tweet"].lower():
		    features["not "+to["token"].lower()]=True
		    label = -1*label
		    sense.append(label)
		elif "don't "+to["token"].lower() in tweet["tweet"].lower():
		    features["don't "+to["token"].lower()]=True
		    label = -1*label
		    sense.append(label)
		else:
		    sense.append(label)
	    else:
		a,b = shorten(to["token"])
		
		if a in afinn:
		    features[a]=True
		    features[b]=True
		    sc= afinn[a]
		    label=0
		    
		    if sc>3:
			label=2
		    elif sc>0:
			label=1
		    elif sc==0:
			label=0
		    elif sc > -3:
			label=-1
		    else:
			label=-2
		    
		    if "not "+a in tweet["tweet"].lower():
			features["not "+a]=True
			label = -1*label
			sense.append(label)
		    elif "don't "+a in tweet["tweet"].lower():
			features["don't "+a]=True
			label = -1*label
			sense.append(label)
		    else:
			sense.append(label)
		    
    
    senseSeq=""
    #if len(sense) != 0:
	
    if 1 in sense or 2 in sense:
	features["afinn_pos_sense"]= sense.count(1) + 2*sense.count(2)
    else:
	features["afinn_pos_sense"]=""
    if -1 in sense or -2 in sense:
	features["afinn_neg_sense"]= -1*sense.count(-1) + -2*sense.count(-2)
    else:
	features["afinn_neg_sense"]=""
    
    if len(sense) != 0:	
	features["afinn_first_sense"]= sense[0]
	features["afinn_last_sense"]= sense[-1]
    else:
	features["afinn_first_sense"]= ""
	features["afinn_last_sense"]= ""
    
    for s in sense:
	if 1 in sense or 2 in sense:
	    senseSeq=senseSeq+"p"
	if -1 in sense or -2 in sense:
	    senseSeq=senseSeq+"n"
    
    if len(senseSeq)>=2:
	features["afinn_first_last"]= senseSeq[0]+senseSeq[-1]
    elif len(senseSeq)==1:
	features["afinn_first_last"]= senseSeq[0]
    else:
	features["afinn_first_last"]=""
    
    features["afinn_seq"]=senseSeq
	
    
    return features

def feature_EPattern(tweet):
    features={}
    
    text=tweet["tweet"].lower()
    
    for p in ePatterns:
	if p in text:
	    features[p]=True
	    
	    #for ep in ePatterns[p].split(","):
		#features[p]=ep.strip()
	    
    
    return features


def featureA(tweet):
    features={}
    mc=0
    pc=0
    nc=0
    
    for l,v in Alist.iteritems():
	if l.lower() in tweet["tweet"].lower():
	    features[l]=True
	    mc= mc+1
	    if v=="positive":
		pc=pc+1
	    elif v=="negative":
		nv=nc+1
	    
    features["A_match_count"]=mc
    if pc>0:
	features["positive_match"]=True
	features["positive_match_count"]=pc
    if nc>0:
	features["negative_match"]=True
	features["negative_match_count"]=nc
	
    return features


def feature_chat(tweet):
    features={}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","$","P","O",",","D","L","Y"]:
	    token = to["token"].lower()
	    ts= shorten(to["token"].lower())[0]
	    if token in chatlist:
		features[chatlist[token]]=True
	    if ts in chatlist:
		features[chatlist[ts]]=True
    
    return features

def feature_CAP(tweet):
    features={}
    uc=0
    for to in tweet["ark_output"]["tokens"]:
	dan1=wordShapeDan1(to["token"])
	
	if dan1=="ALL-UPPER":
	    uc=uc+1
	#    features[to["token"]]=True
	#    a,b=shorten(to["token"])
	#    if a!=b:
	#	features[b]=True
    
    if uc>0:
	features["ALL-UPPER"]=True
    features["ALL-UPPER-count"]=uc
	
    return features


def feature_abbrev(tweet):
    features={}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","$","P","O",",","D","L","Y"]:
	    token = to["token"].lower()
	    
	    if token in twlist:
		features[token]=True
    
    return features

def feature_emo(tweet):
    features={}
    emos=[]
    tokens= WhitespaceTokenizer().tokenize(tweet["tweet"])
    
    for t in tokens:
	a,t=shorten(t)
	if t in emolist:
	    emos.append(t)
	if a in emolist:
	    emos.append(t)
    
    for e in emos:
	try:
	    features["emo_pattern"]=emolist[e]
	except:
	    pass
    
    return features


def feature_wordnet(tweet):
    features={}
    
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] in ["N","V","R","A"]:
            a,b = shorten(to["token"])
            
            if to["tag"]=="N":
                a=en.noun.singular(a)
                sent=en.noun.lexname(a)
                if sent!="":
                    features["category_"+sent]=True
            elif to["tag"]=="V":
                a=en.verb.infinitive(a)
                sent=en.verb.lexname(a)
                if sent!="":
                    features["category_"+sent]=True 
    
    return features


def feature_negation(tweet):
    features={}
   
    negc=0
    upc=0
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","$"]:
	    if to["token"].lower() in negations:
		features[to["token"].lower()]=True
		dan=wordShapeDan1(to["token"])
		if dan == "ALL-UPPER":
		    features[to["token"]]=True
		    upc= upc+1
		negc=negc+1
	    else:
		a,b = shorten(to["token"])
		if b in negations:
		    features[b]=True
		    negc=negc+1
		elif a in negations:
		    features[a]=True
		    negc=negc+1
		    
	#    if to["token"].lower() in ardalist:
	#	if ardalist[to["token"].lower()] == "negative":
	#	    dan=wordShapeDan1(to["token"])
	#	    if dan == "ALL-UPPER":
	#		#features[to["token"]]=True
	#		upc= upc+1
	#	    negc=negc+1
	#    else:
	#	a,b = shorten(to["token"])
	#	if b in ardalist:
	#	    negc=negc+1
	#	elif a in ardalist:
	#	    negc=negc+1
    #if negc!=0:
    #	features["neg_count"]=negc
    features["neg_count"]=negc
    features["upper_neg_count"]=upc
    
    return features


def feature_sent(tweet):
    features={}
    sense=[]
    label=0
    uc=0
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","$","P","O",","]:
	    token = to["token"].lower()
	    
	    if token in allist:
		#if token in plist: # 1
		#    features[token]=True
		#    label=1
		#elif token in nlist: # -1
		#    features[token]=True
		#    label=-1
		if token in llist:
		    features[token]=True
		elif token in ulist:
		    uc = uc+1
		    features[token]=True
		elif token in mslist:
		    features[token]=True
		elif token in mwlist:
		    features[token]=True
		    
		if "not "+to["token"].lower() in tweet["tweet"].lower():
		    features["not "+to["token"].lower()]=True
		    label = -1*label
		    sense.append(label)
		elif "don't "+to["token"].lower() in tweet["tweet"].lower():
		    features["don't "+to["token"].lower()]=True
		    label = -1*label
		    sense.append(label)
		else:
		    if label!=0:
			sense.append(label)
	    else:
		a,b = shorten(to["token"])
		token=a
		if token in allist:
		#    if token in plist: # 1
		#	features[token]=True
		#	features[b]=True
		#	label=1
		#    elif token in nlist: # -1
		#	features[token]=True
		#	features[b]=True
		#	label=-1
		    if token in llist:
			features[token]=True
			features[b]=True
		    elif token in ulist:
			uc = uc+1
			features[token]=True
			features[b]=True
		    elif token in mslist:
			features[token]=True
			features[b]=True
		    elif token in mwlist:
			features[token]=True
			features[b]=True
		    
		    if "not "+token in tweet["tweet"].lower():
			features["not "+to["token"].lower()]=True
			label = -1*label
			sense.append(label)
		    elif "don't "+token in tweet["tweet"].lower():
			features["don't "+to["token"].lower()]=True
			label = -1*label
		        sense.append(label)
		    else:
			if label!=0:
			    sense.append(label)
	    
#    if len(sense) != 0:
#	if 1 in sense:
#	    features["pos_sense"]= sense.count(1)
#	if -1 in sense:
#	    features["neg_sense"]= sense.count(-1)
#	features["first_sense"]= sense[0]
#	features["last_sense"]= sense[-1]
    
    features["uncertainity"]=uc
    
    return features

def feature_interjection(tweet):
    features={}
    ilist=[]
    for i,to in enumerate(tweet["ark_output"]["tokens"]):
	if to["tag"] == "!":
	    a,b=shorten(to["token"])
	    #features[b.lower()] = True
	    ilist.append(b.lower())
	    #features[tweet["ark_output"]["tokens"][i-1]["token"]+b]=True
	    #features[tweet["ark_output"]["tokens"][i-1]["token"]+b]=True
    
    for i in ilist:
	features["interjection"]=i
    
    return features

def feature_punctuation(tweet):
    features={}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == ",":
	    a,b=shorten(to["token"])
	    if b!= to["token"]:
		features[b.lower()] = True
    
    return features

def feature_hash_positive(tweet):
    features={}
    hset=[]
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == "#":
	    w=""
	    hset=[]
	    if "#" in to["token"]:
		#features[to["token"].lower()] = True
		features[to["token"].lower()[1:]] = True
		features[to["token"].lower()] = True
		w=to["token"].lower()[1:]
	    else:
		features[to["token"].lower()] = True
		features["#"+to["token"].lower()] = True
		w=to["token"].lower()
		
		if w in ardalist:
		    hset.append(w)
		else:
		    a=shorten(w)
		    if a!=w:
			if a in ardalist:
			    hset.append(a)
		
	    for a in ardalist:
		if a in w:
		    hset.append(a)
		
		#if wordShapeDan1(w)=="MIXED-CASE":	    
		#    ws=split_uppercase(w)
		#    
		#    for t in ws:
		#	t=t.strip()
		#	if t in ardalist:
		#	    hset.append(t)
		#	else:
		#	    a=shorten(t)
		#	    if a!=t:
		#		if a in ardalist:
		#		    hset.append(a)
    
    for h in hset:
	features["hash_sentiment"]=ardalist[h]
    
    return features

def feature_hash(tweet):
    features={}
    hset=[]
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == "#":
	    w=""
	    hset=[]
	    if "#" in to["token"]:
		#features[to["token"].lower()] = True
		features[to["token"].lower()[1:]] = True
		features[to["token"].lower()] = True
		w=to["token"].lower()[1:]
	    else:
		features[to["token"].lower()] = True
		features["#"+to["token"].lower()] = True
		w=to["token"].lower()
		
		if w in ardalist:
		    hset.append(w)
		else:
		    a=shorten(w)
		    if a!=w:
			if a in ardalist:
			    hset.append(a)
		
	    for a in ardalist:
		if a in w:
		    hset.append(a)
		
		#if wordShapeDan1(w)=="MIXED-CASE":	    
		#    ws=split_uppercase(w)
		#    
		#    for t in ws:
		#	t=t.strip()
		#	if t in ardalist:
		#	    hset.append(t)
		#	else:
		#	    a=shorten(t)
		#	    if a!=t:
		#		if a in ardalist:
		#		    hset.append(a)
    
    for h in hset:
	features["hash_sentiment"]=ardalist[h]
    
    return features

def feature_emotion(tweet):
    features={}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == "E":
	    features[to["token"].lower()] = True
    
    return features


def feature_lingemotion(tweet):
    features={}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] in ["N","V","R","A"]:
            a,b = shorten(to["token"])
            
            if to["tag"]=="N":
                a=en.noun.singular(a)
                sent=en.noun.is_emotion(a, boolean=False)
                if sent is not None:
                    features["noun_"+sent]=True
            elif to["tag"]=="A":
                sent=en.adjective.is_emotion(a, boolean=False)
                if sent is not None:
                    features["adj_"+sent]=True
            elif to["tag"]=="V":
                a=en.verb.infinitive(a)
                sent=en.verb.is_emotion(a, boolean=False)
                if sent is not None:
                    features["v_"+sent]=True
            elif to["tag"]=="R":
                sent=en.adverb.is_emotion(a, boolean=False)
                if sent is not None:
                    features["adv_"+sent]=True    
    
    return features

def feature_afinn(tweet):
    features = {}
    sense = []
	
    for to in tweet["ark_output"]["tokens"]:
	if to["token"].lower() in afinn:
            features[to["token"].lower()]=True
            sc= afinn[to["token"].lower()]
            label=0
            
            if sc>3:
                label=2
            elif sc>0:
                label=1
            elif sc==0:
                label=0
            elif sc > -3:
                label=-1
            else:
                label=-2
            
            if "not "+to["token"].lower() in tweet["tweet"].lower():
		features["not "+to["token"].lower()]=True
                label = -1*label
                sense.append(label)
	    elif "don't "+to["token"].lower() in tweet["tweet"].lower():
		features["don't "+to["token"].lower()]=True
		label = -1*label
                sense.append(label)
	    else:
                sense.append(label)
        else:
            a,b = shorten(to["token"])
            
            if a in afinn:
                features[a]=True
                features[b]=True
                sc= afinn[a]
                label=0
                
                if sc>3:
                    label=2
                elif sc>0:
                    label=1
                elif sc==0:
                    label=0
                elif sc > -3:
                    label=-1
                else:
                    label=-2
                
                if "not "+a in tweet["tweet"].lower():
		    features["not "+a]=True
		    label = -1*label
		    sense.append(label)
		elif "don't "+a in tweet["tweet"].lower():
		    features["don't "+a]=True
		    label = -1*label
		    sense.append(label)
                else:
                    sense.append(label)
    
    if len(sense) != 0:
	
	if 1 in sense or 2 in sense:
	    features["afinn_pos_sense"]= sense.count(1) + 2*sense.count(2)
	if -1 in sense or -2 in sense:
	    features["afinn_neg_sense"]= -1*sense.count(-1) + -2*sense.count(-2)
	features["afinn_first_sense"]= sense[0]
	features["afinn_last_sense"]= sense[-1]
	
    return features

#def feature_afinn(tweet):
#    features = {}
#    
#    for to in tweet["ark_output"]["tokens"]:
#	if to["token"].lower() in afinn:
#            features[to["token"].lower()+"_afinn"]=True
#            sc= afinn[to["token"].lower()]
#            label=0
#            labelname=""
#            
#            if sc>3:
#                label=2
#                labelname="strong pos"
#            elif sc>0:
#                label=1
#                labelname="weak pos"
#            elif sc==0:
#                label=0
#                labelname="neutral"
#            elif sc > -3:
#                label=-1
#                labelname="weak neg"
#            else:
#                label=-2
#                labelname="strong neg"
#            
#            if "not "+to["token"].lower() in tweet["tweet"].lower() or "not"+to["token"].lower() in tweet["tweet"].lower():
#                label = -1*label
#                features[to["token"].lower()+"_notafinn_label"]=label
#	    else:
#                features[to["token"].lower()+"_afinn_label"] = label
#        else:
#            a,b = shorten(to["token"])
#            
#            if a in afinn:
#                features[a+"_afinn"]=True
#                features[b+"_afinn"]=True
#                sc= afinn[a]
#                label=0
#                labelname=""
#                
#                if sc>3:
#                    label=2
#                    labelname="strong pos"
#                elif sc>0:
#                    label=1
#                    labelname="weak pos"
#                elif sc==0:
#                    label=0
#                    labelname="neutral"
#                elif sc > -3:
#                    label=-1
#                    labelname="weak neg"
#                else:
#                    label=-2
#                    labelname="strong neg"
#                
#                if "not "+a in tweet["tweet"].lower() or "not"+a in tweet["tweet"].lower():
#                    label = -1*label
#                    features[a+"_notafinn_label"]=label
#                else:
#                    features[a+"_afinn_label"] = label
#    
#    return features

def feature_arda(tweet):
    features={}
    sense=""
    label=0
    uc=0
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","$","P","O",",","^"]:
	    token = to["token"].lower()
	    
	    if token in ardalist:
		features[token]=True
		label=ardalist[token]
		    
		if "not "+to["token"].lower() in tweet["tweet"].lower():
		    features["not "+to["token"].lower()]=True
		    if label == "positive":
                        label = "negative"
                    else:
                        label = "positive"
		    sense=sense+label[0]
		elif "don't "+to["token"].lower() in tweet["tweet"].lower():
		    features["don't "+to["token"].lower()]=True
		    if label == "positive":
                        label = "negative"
                    else:
                        label = "positive"
		    sense=sense+label[0]
		else:
		    sense=sense+label[0]
	    else:
		a,b = shorten(to["token"])
		token=a
		if token in ardalist:
		    features[token]=True
		    label=ardalist[token]
			
		    if "not "+token in tweet["tweet"].lower():
			features["not "+token]=True
			if label == "positive":
			    label = "negative"
			else:
			    label = "positive"
			sense=sense+label[0]
		    elif "don't "+token in tweet["tweet"].lower():
			features["don't "+token]=True
			if label == "positive":
			    label = "negative"
			else:
			    label = "positive"
			    sense=sense+label[0]
		    else:
			sense=sense+label[0]
	    
    #if len(sense) != 0:
	#features["oursent_pos_sense"]= sense.count("p")
	#features["oursent_neg_sense"]= sense.count("n")
#    p= sense.count("p")
#    n= sense.count("n")
#    if p>0:
#	p=1
#    if n>0:
#	n=1
#    features["oursent_pos_neg"]=str(p)+str(n)
	#features["arda_first_sense"]= sense[0]
	#features["arda_last_sense"]= sense[-1]
    
    if len(sense) >= 2:
	features["oursent_shortseq"]=shorten_pattern(sense)
	features["oursent_longseq"]=sense
	features["oursent_first_last"]=sense[0]+sense[-1]
    
    return features

def feature_arzu(tweet):
    features = {}
    sense=[]
    
    for to in tweet["ark_output"]["tokens"]:
	token= to["token"].lower() 
	if token in arzlist:
            features[token]=True
	    tag=to["tag"]
            poses=arzlist[token]["poses"]
	    if tag.lower() in poses:
                label=arzlist[token]["sentiment"]
		
                if "not "+token in tweet["tweet"].lower():
		    features["not "+token]=True
                    if label == "positive":
                        label = "negative"
                    else:
                        label = "positive"
		elif "don't "+token.lower() in tweet["tweet"].lower():
		    features["don't "+token]=True
                    if label == "positive":
                        label = "negative"
                    else:
                        label = "positive"
                    
                sense.append(label)
	
        else:
            a,b = shorten(to["token"])
	    token=a
	    if token in arzlist:
		features[token]=True
		tag=to["tag"]
		poses=arzlist[token]["poses"]
		if tag.lower() in poses:
		    label=arzlist[token]["sentiment"]
		    
		    if "not "+token in tweet["tweet"].lower():
			features["not "+token]=True
			if label == "positive":
			    label = "negative"
			else:
			    label = "positive"
		    elif "don't "+token.lower() in tweet["tweet"].lower():
		        features["don't "+token]=True
		        if label == "positive":
		            label = "negative"
		        else:
		            label = "positive"
			
		    sense.append(label)
    
    if len(sense) != 0:
	if "positive" in sense:
	    features["arzu_pos_sense"]= sense.count("positive")
	if "negative" in sense:
	    features["arzu_neg_sense"]= sense.count("negative")
	features["arzu_first_sense"]= sense[0]
	features["arzu_last_sense"]= sense[-1]
    
    return features

def feature_wordshape(tweet):
    features={}
    ktag={}
    ttext= tweet["tweet"]
    tokens= WhitespaceTokenizer().tokenize(ttext)
    
    for to in tweet["ark_output"]["tokens"]:
	ktag[to["token"]]=to["tag"]
	
    inlist= ["N","V","A","R","^","#"]
    
    for to in tokens:
	if to in ktag.keys():
	    tag=ktag[to]
	    if tag in inlist:
		m=wordShapeChris4(to)
		features[m]=True
	else:
	    m=wordShapeChris4(to)
	    features[m]=True
	
    return features

def feature_bigramshape(tweet):
    features={}
    tokenlist= []
    
    inlist= ["N","V","A","R","^","#"]
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] in inlist:
	    tokenlist.append(to["token"])
    
    bigrams = nltk.util.bigrams(tokenlist)
    features= dict([(wordShapeChris4(bigram[0]+' '+bigram[1]), True) for bigram in bigrams])
    return features

def feature_firstlastword(tweet,pos=False):
    features={}
#    yes=["N","V","A","R","E","#","!",","]
#    l=[]
#    for to in tweet["ark_output"]["tokens"]:
#	if to["tag"] in yes:
#	    if pos:
#		l.append(to["token"].lower()+"_"+to["tag"])
#	    else:
#		l.append(to["token"].lower())
#    if len(l)>=1:
#	features["firstword"]=l[0]
#	#features["firstwordshape"]=wordShapeChris4(l[0])
#	features["lastword"]=l[-1]
#	features["lastwordshape"]=wordShapeChris4(l[-1])
	
    l= WhitespaceTokenizer().tokenize(tweet["tweet"])
#    if "@" in l[0]:
#	features["firstword"]="@"
#    elif "http" in l[0]:
#	features["firstword"]="URL"
#    else:
    #features["firstword"]=l[0]
#    dan1=wordShapeDan1(l[0])
#    chris4=wordShapeChris4(l[0])
#    if dan1=="ALL-UPPER" or dan1=="MIXED-CASE":
#	#features[chris4]= True
#	features["firstwordshape"]=chris4
    p=""	
    if "@" in l[-1]:
	p=""
    elif "http" in l[-1] or ".com" in l[-1]:
	p=""
    elif "#" in l[-1]:
	p=""
    else:
	features["lastword"]=shorten(l[-1])[1]
	features["lastwordshape"]=wordShapeChris4(l[-1])
    
    return features

#def feature_firstlastsentiment(tweet):
#    features = {}
#    l=[]
#    for to in tweet["ark_output"]["tokens"]:
#	if to["token"].lower() in afinn:
#	    sc=afinn[to["token"].lower()]
#	    label=1
#            labelname={0:"neutral",1:"positive",-1:"negative"}
#	    if sc==0:
#		label=0
#	    elif sc<0:
#		label=-1
#	    
#            if "not "+to["token"].lower() in tweet["tweet"].lower() or "not"+to["token"].lower() in tweet["tweet"].lower():
#                label = -1*label
#            
#	    l.append(label)
#    
#    if len(l)>=2:
#	features["firstsent"]=labelname[l[0]]
#	features["lastsent"]=labelname[l[-1]]
#    if len(l)==1:
#	features["firstsent"]=labelname[l[0]]
#    if (-1 in l) and (1 in l):
#	features["polarity"]=True
#    else:
#	features["polarity"]=False
#	
#    return features


#def feature_repetition(tweet):
#    features = {}
#    
#    for to in tweet["ark_output"]["tokens"]:
#        rep=list(repetitions(to["token"]))
#	for r in rep:
#	    features[r[0]+"_count"]=r[1]
#    
#    return features

def feature_repetition(tweet):
    features = {}
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in ["U","@","^"]:
	    rep=list(repetitions(to["token"]))
	    for r in rep:
		features[shorten(to["token"])[1]]=True
		features[r[0]+"_count"]=r[1]	
    
    return features

def feature_POSextras(tweet):
    features = {}
    
    Nc=0
    Vc=0
    Ac=0
    Rc=0
    tlen= len(tweet["ark_output"]["tokens"])
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == "N":
	    Nc= Nc+1
	if to["tag"] == "V":
	    Vc= Vc+1
	if to["tag"] == "A":
	    Ac= Ac+1
	if to["tag"] == "R":
	    Rc= Rc+1	   
    
    features["noun_count"]=Nc
    features["verb_count"]=Vc
    features["adjadv_count"]=Ac+Rc
    if Ac!=0:
	features["noun/adj"]= Nc/(1.0*Ac)
    if Rc!=0:
	features["verb/adv"]= Vc/(1.0*Rc)
    if tlen !=0:
	features["noun/tokens"]= Nc/(1.0*tlen)
	features["verb/tokens"]= Vc/(1.0*tlen)
	features["adjadv/tokens"]= (Ac+Rc)/(1.0*tlen)
        
    return features
    

def feature_tags(tweet):
    features = {}
    
    mc=0
    uc=0
    hc=0
    ec=0
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] == "E":
	    features[to["token"]] = True
	    ec = ec+1
	if to["tag"] == "@":
	    features["@"] = True
	    mc = mc+1
	if to["tag"] == "U":
	    features["URL"] = True
	    uc = uc+1
	if to["tag"] == "#":
	    features["#"] = True
	    hc = hc+1
	    
    if mc>=2:
	features["mention_count"] = mc
    if uc>=2:
	features["url_count"] = uc
    if hc>=2:
	features["#_count"] = hc
    if ec>=2:
	features["emotion_count"] = ec
    
    return features

def feature_extras(tweet):
    features={}
    
    temp= all_features.find({'tweet_id' : tweet['_id']})[0]
    feats = temp["features"]
    for d in feats:
	#if d["feature"]=="afinn":
	#    features["afinn_label"]= d["value"]
	#if d["feature"]=="afinn_avg":
	#    features["afinn_avg"]= d["value"]
	if d["feature"]=="slang":
	    features[d["value"]]= True
	if d["feature"]=="emoticon":
	    features[d["value"]]= True
	if d["feature"]=="emitted_emotion":
	    features["emotion_"+d["value"]]= True 
	if d["feature"]=="etopic":
	    features["etopic_"+d["value"]]= True
		    
    return features

def feature_words(tweet):
    features = {}
    
    #TODO case ile oynamayi unutma
    for to in tweet["ark_output"]["tokens"]:
	#features[to["token"].lower()] = True
        if to["tag"] not in ["U","@","$"]:
            if to["tag"] in ["N","V","A","R"]:
                a,b = shorten(to["token"])
                features[b] = True
            else:
                features[to["token"].lower()] = True
	    features[wordShapeChris4(to["token"])]= True
    return features

def feature_regwords(tweet):
    features = {}
    #TODO case ile oynamayi unutma
    ttext= tweet["tweet"]
    tokens= WhitespaceTokenizer().tokenize(ttext)
    
    for to in tokens:
	features[to.lower()] = True
    
    return features

def bigram_word_feats(score_fn=BigramAssocMeasures.chi_sq, n=200):
    pos,neg,neu= parse_tweets(trainset)
    
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def feature_poswords(tweet):
    features = {}
    
    for to in tweet["ark_output"]["tokens"]:
	features[to["token"].lower()+"_"+to["tag"]] = True
    
    return features

def feature_posbigrams(tweet):
    features = {}
    
    tokenlist= []
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] != ",":
	    tokenlist.append(to["token"].lower()+"_"+to["tag"])
    
    bigrams = nltk.util.bigrams(tokenlist)
    features= dict([(bigram[0]+' '+bigram[1], True) for bigram in bigrams])
    
    return features

def feature_bigrams(tweet):
    features = {}
    tokenlist= []
    
    for to in tweet["ark_output"]["tokens"]:
	if to["tag"] not in [",","U","@","$"]:
	    #tokenlist.append(to["token"].lower())
            if to["tag"] in ["N","V","A","R"]:
                a,b = shorten(to["token"])
                features[b] = True
            else:
                features[to["token"].lower()] = True
    
    bigrams = nltk.util.bigrams(tokenlist)
    features= dict([(bigram[0]+' '+bigram[1], True) for bigram in bigrams])
    
    return features

def feature_regbigrams(tweet):
    features = {}
    tokenlist= []
    
    ttext= tweet["tweet"]
    tokens= WhitespaceTokenizer().tokenize(ttext)
    
    for to in tokens:
	tokenlist.append(to.lower())
    
    bigrams = nltk.util.bigrams(tokenlist)
    features= dict([(bigram[0]+' '+bigram[1], True) for bigram in bigrams])
    
    return features

#TODO not afinn
#TODO arzucan word list

def feature_bestwords(tweet):
    features = {}
    bestset=set(bestwords)
    
    
    for to in tweet["ark_output"]["tokens"]:
	dan1=wordShapeDan1(to["token"])
	chris4=wordShapeChris4(to["token"])
	
        if to["token"].lower() in bestset:
            #features[to["token"]] = True
            features[to["token"].lower()+"_best"] = True
	    #if dan1=="ALL-UPPER" or dan1=="MIXED-CASE":
	    #	features[chris4]= True
        else:
            a,b = shorten(to["token"])
            
            if b in bestset:
                features[a+"_best"]=True
                features[b+"_best"]=True
                #if dan1=="ALL-UPPER" or dan1=="MIXED-CASE":
		#    features[chris4]= True
    
    return features

def feature_posbestwords(tweet):
    features = {}
    bestset=set(bestposwords)
    	
    for to in tweet["ark_output"]["tokens"]:
        if (to["token"]+"_"+to["tag"]).lower() in bestset:
            #features[to["token"]] = True
            features[to["token"].lower()+"_best"+"_"+to["tag"]] = True
            #features[wordShapeChris4(to["token"])]= True
        else:
            #if to["tag"]=="#":
            #    to["token"]=to["token"][1:]
            
            a,b = shorten(to["token"])
            
            if b in bestset:
                features[a+"_best"+"_"+to["tag"]]=True
                features[b+"_best"+"_"+to["tag"]]=True
                #features[wordShapeChris4(to["token"])]= True
    
    return features

#def feature_freqwords(tweet):
#    features = {}
#    
#    freqset= set(freqwords)
#    
#    for to in tweet["ark_output"]["tokens"]:
#        #features[to["token"].lower()] = (to["token"].lower() in freqset)
#        if to["token"].lower() in freqset:
#            features[to["token"].lower()] = True
#
#    return features
#
#def feature_freqbigrams(tweet):
#    features = {}
#    
#    tokenlist= []
#    bestset= set(freqbigrams)
#    
#    for to in tweet["ark_output"]["tokens"]:
#        #tokenlist.append(to["token"])
#        tokenlist.append(to["token"].lower())
#    
#    bigram_finder = BigramCollocationFinder.from_words(tokenlist)
#    bigrams = nltk.util.bigrams(tokenlist)
#    
#    for bigram in bigrams:
#	w= bigram[0]+' '+bigram[1]
#	if w in bestset:
#	    features[w]=True
#    
#    return features

def feature_bestbigrams(tweet):
    features = {}
    
    tokenlist= []
    bestset= set(bestbigrams)
    
    #nottaglist= ["U","@","$","P","O",",","&"]
    nottaglist= ["U","@","$"]
    
    for to in tweet["ark_output"]["tokens"]:
        if to["tag"] not in nottaglist:
	#tokenlist.append(to["token"].lower())
            #if to["tag"]=="#":
            #    to["token"]=to["token"][1:]
	    if to["token"]!="":
		if "#"==to["token"][0] and len(to["token"])>1:
		    to["token"]=to["token"][1:]
		    
		a,b = shorten(to["token"])
		tokenlist.append(b)
    
    bigram_finder = BigramCollocationFinder.from_words(tokenlist)
    bigrams = nltk.util.bigrams(tokenlist)
    
    for bigram in bigrams:
	w= bigram[0]+' '+bigram[1]
	if w in bestset:
	    features[w]=True
            
        #features[wordShapeChris4(w)]= True
    
    return features

def feature_posbestbigrams(tweet):
    features = {}
    
    tokenlist= []
    bestset= set(bestposbigrams)
    
    nottaglist= ["U","@","$"]
    
    for to in tweet["ark_output"]["tokens"]:
        if to["tag"] not in nottaglist:
	#tokenlist.append(to["token"].lower())
            if to["token"]!="":
		if "#"==to["token"][0] and len(to["token"])>1:
		    to["token"]=to["token"][1:]
		
		a,b = shorten(to["token"])
		tokenlist.append((b+"_"+to["tag"]))
    
    bigram_finder = BigramCollocationFinder.from_words(tokenlist)
    bigrams = nltk.util.bigrams(tokenlist)
    
    for bigram in bigrams:
	w= bigram[0]+' '+bigram[1]
	if w in bestset:
	    features[w]=True
    
    return features
