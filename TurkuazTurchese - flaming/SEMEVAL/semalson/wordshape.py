from nltk.corpus import words
from nltk.stem import PorterStemmer
import en

greek = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "theta", "iota", "kappa", "lambda", "omicron", "rho", "sigma", "tau", "upsilon", "omega"]
known=set(words.words())

def wordShapeChris4(s,omitIfInBoundary=False,knownWords=None):
    ssize=len(s)
    
    if ssize < boundsize:
        return wordShapeChris4Short(s,knownWords)
    else:
        return wordShapeChris4Long(s,omitIfInBoundary,knownWords=None)

def danBigram(bigram):
    
    s=bigram.split(" ")
    
    r1= wordShapeDan1(s[0])
    r2= wordShapeDan1(s[1])
    
    if r1=="ALL-UPPER" or r1=="MIXED-CASE" or r2=="ALL-UPPER" or r2=="MIXED-CASE":
        return wordShapeChris4(bigram)
    else:
        return "OTHER" 

def wordShapeDan1(word):
    digit=True
    upper=True
    lower=True
    mixed=True
    
    for w in word:
        if not w.isdigit():
            digit=False
        if not w.islower():
            lower=False
        if not w.isupper():
            upper=False
        if ((w==word[0] and not w.isupper()) or (w!=word[0] and not w.islower())):
            mixed=False
            
    if digit:
        return "ALL-DIGITS"
    if upper:
        return "ALL-UPPER"
    if lower:
        return "ALL-LOWER"
    if mixed:
        return "MIXED-CASE"
    return "OTHER"

def chris4equivalenceClass(c):
    
    if c.isdigit():
        return 'd'
    elif c.islower():
        return 'x'
    elif c.isupper():
        return 'X'
    elif c==" ":
        return 's'
    elif c=="$":
        return "$"
    elif c=="+" or c=="=" or c=="<" or c==">":
        return "+"
    elif c=="|" or c=="/" or c=="\\":
        return "|"
    elif c=="(" or c=="[" or c=="{":
        return '('
    elif c==")" or c=="]" or c=="}":
        return ')'
    elif c=="'"or c=="\"":
        return "'"
    elif c=="%":
        return "%"
    elif c=="?":
        return "?"
    elif c=="!":
        return "!"
    elif c==".":
        return '.'
    elif c=="," or c==":" or c==";":
        return ","
    elif c=="_" or c=="-":
        return "_"
    elif c=="#":
        return "#"
    elif c=="@":
        return "@"
    else:
        return 'q'

#def chris4equivalenceClass(c):
#    
#    if c.isdigit():
#        return 'd'
#    elif c.islower():
#        return 'x'
#    elif c.isupper():
#        return 'X'
#    elif c==" ":
#        return 's'
#    elif c=="+" or c=="=" or c=="%" or c=="<" or c==">":
#        return "+"
#    elif c=="|" or c=="/" or c=="\\":
#        return "|"
#    elif c=="(" or c=="[" or c=="{":
#        return '('
#    elif c==")" or c=="]" or c=="}":
#        return ')'
#    elif c=="'"or c=="\"":
#        return "'"
#    elif c=="?":
#        return "?"
#    elif c=="!":
#        return "!"
#    elif c=="." or c=="," or c==":" or c==";" or c=="^":
#        return '.'
#    elif c=="_":
#        return "_"
#    elif c=="-":
#        return "-"
#    elif c=="#":
#        return "#"
#    else:
#        return 'q'

def wordShapeChris4Short(word,knownWords=None):
    wLen= len(word)
    sb=""
    nonLetters=False
    i=0
    while i<wLen:
        m=chris4equivalenceClass(word[i])
        for gr in greek:
            if word[i].startswith(gr,i):
                m='g'
                i= i+len(gr) -1
                break
        if m!='x' and m!= 'X':
            nonLetters=True
        
        sb= sb+m
        i=i+1
    
    #knownWords=set(words.words())
    if knownWords:
        if (not nonLetters) and (word in knownWords):
            sb=sb+'k'
    
    
    return sb

boundsize=2
def wordShapeChris4Long(s,omitIfInBoundary,knownWords=None):
    sb=""
    endSB=""
    boundSet=[]
    seenSet=[]
    nonLetters=False
    
    lenss=len(s)
    i=0
    
    while i<lenss:
        c=s[i]
        m=chris4equivalenceClass(c)
        iIncr=0
        for gr in greek:
            if s[i].startswith(gr,i):
                m='g'
                iIncr=len(gr)-1
                break
        if m!='x' and m!='X':
            nonLetters=True
        if i<boundsize:
            sb=sb+m
            boundSet.append(m)
        elif i<len(s)-boundsize:
            seenSet.append(m)
        else:
            boundSet.append(m)
            endSB=endSB+m
        
        i= i+ iIncr
        i= i+1
    
    for c in seenSet:
        if (not omitIfInBoundary) or (c not in boundSet):
            sb=sb+c
    sb=sb+endSB
    
    #knownWords=set(words.words())
    if knownWords:
        if (not nonLetters) and (s in knownWords):
            sb=sb+'k'
    
    
    return sb

import re
def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))

def shorten_pattern(p):
    res=""
    smini=p
    
    if len(p)==1:
        return p
    
    for r in list(repetitions(p)):
        if int(r[1])>1: # one char repeated
            smini=re.sub(r[0]+'+',r[0], smini)
        
    return smini

def shorten(s):
    import re
    s=s.lower()
    s=s.replace("\"","'") # replace quotes
    smini=s
    snew=s
    p=PorterStemmer()
    
    if (s in known):
        return s,s
    #elif (p.stem_word(s) in known):
    #    s=p.stem_word(s)
    #    return s,s
    else:
        for r in list(repetitions(s)):
            if int(r[1])>1: # one char repeated
                try:
                    smini=re.sub(r[0]+'+',r[0], smini)
                except:
                    smini=s
                snew=snew.replace(int(r[1])*r[0],"["+r[0]+"+]")
    
    return smini,snew

def split_uppercase(s):
    return re.sub(r'([a-z]*)([A-Z])',r'\1 \2',s)

#s="AAAAA nEWWW"
#s="pppppnnpn"
#s="AnneBakKralCiplak"
#print split_uppercase(s)
#print shorten_pattern(s)
#print shorten(s)
#print wordShapeDan1(s)
#print shorten(s)
#r1=wordShapeDan1(s)
#r2=wordShapeChris4Short(s)
#r3=wordShapeChris4Long(s,True)
#print r1,r2,r3