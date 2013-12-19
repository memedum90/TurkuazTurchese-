# -*- coding: utf-8 -*-

# Copyright (C) 2013 Federico Montori <fede.selmer@gmail.com>, Mehmet Durna <memdum@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import glob
import os
import math
import nltk

from collections import Counter

arraypost = {}
debbigrams = {}
debunigrams = {}
size_debate = {}
voc_debate = {}

lexicon_vs = []

# Grab all the files from the MPQA political debates corpus and collect them in a dictionary of dictionaries ready for Naive Bayes #UNUSED
def fill_debate_corpus():
    for folder in glob.glob(os.path.join('dicts/Political_debates_corpus/', '*')):
        name = folder.split("/")[-1]
        arraypost[name] = ""
        for filename in glob.glob(os.path.join(str(folder), '*')):
            with open(filename) as text:
                final = ("".join(c for c in text.read().split("\n")[-1] if c not in ('!','.',':',';',',','?','(',')','"','/','<url>'))).lower()
                arraypost[name] += ("* " + final)
        debunigrams[name] = nltk.word_tokenize(arraypost[name])
        size_debate[name] = len(debunigrams[name])
        debunigrams[name] = Counter(debunigrams[name])
        debbigrams[name] = Counter(nltk.bigrams(arraypost[name]))
        voc_debate[name] = len(debunigrams[name])

# This function creates a lexicon of agreement, disagreement and opinion expressions
def fill_vs_lexicon():
    with open('dicts/final_vs', 'r') as vs:
        txt = vs.read().split("////")
        for ind, cat in enumerate(txt):
            lexicon_vs.append(cat.split("\n"))
            while ("" in lexicon_vs[ind]):
                del lexicon_vs[ind][lexicon_vs[ind].index("")]
        
# Analyze the perplexity with the debate corpus and spit it out #UNUSED
def process_disagreement(unigrams, bigrams, topic):
    Cunigrams = Counter(unigrams)
    Cbigrams = Counter(bigrams)
    
    perplexity = 0
    for bg in Cbigrams:            
        perplexity += math.log((debunigrams[topic][bg[0]] + voc_debate[topic]) / (debbigrams[topic][bg] + 1))
    if perplexity == 0:
        return 0
    else:        
        return 9.0-(perplexity/len(Cunigrams))

# Analyze how many agreements/disagreements there are in the text
def process_vs(text):
    return float(sum(1 for c in lexicon_vs[1] if c in text)) - 0.75*float(sum(1 for c in lexicon_vs[0] if c in text)) + 0.25*float(sum(1 for c in lexicon_vs[2] if c in text))    