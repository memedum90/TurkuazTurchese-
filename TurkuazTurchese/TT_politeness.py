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

import csv
import glob
import math
import nltk
import os
import sys

from collections import Counter
from TT_prep import *

corpus = []
organized_corpus = []
uni_corpus = []
bi_corpus = []
voc_corpus = []
size_corpus = []

# With this function we split the corpus in bigrams and unigrams and we divide it into level categories
def fill_politeness_corpus():
    for i in range (0, 5):
        organized_corpus.append("")
    
    # Open the csv files and add every line to the archive list
    for filename in glob.glob(os.path.join('dicts/Stanford_politeness_corpus/', '*.annotated.csv')):
        with open(filename, 'rb') as csvfile: 
            raw_corpus = csv.DictReader(csvfile, dialect='excel')
            for csvrow in raw_corpus:
                corpus.append(csvrow)
    # Populate the dicts
    for post in corpus:
        # We will have 5 categories of unpoliteness (0: very polite, 4: very unpolite)
        av_pol = (int(post['Score1']) + int(post['Score2']) + int(post['Score3']) + int(post['Score4']) + int(post['Score5'])) / 25
        organized_corpus[(av_pol + 1) * (-1)] += lower_punct(post['Request']) + " * "
    for category in range(0, 5):
        uni_corpus.append(nltk.word_tokenize(organized_corpus[category]))
        size_corpus.append(len(uni_corpus[category]))
        bi_corpus.append(Counter(nltk.bigrams(uni_corpus[category])))
        uni_corpus[category] = (Counter(uni_corpus[category]))
        voc_corpus.append(len(uni_corpus[category]))
        
# Function to calculate the politeness with bigrams of a tweet
def process_politeness(unigrams, bigrams):
        Cunigrams = Counter(unigrams)
        Cbigrams = Counter(bigrams)
        
        perplexity = [0.0,0.0,0.0,0.0,0.0]
        
        for bg in Cbigrams:            
            for c in range (0, 5):
                perplexity[c] += math.log(float(uni_corpus[c][bg[0]] + voc_corpus[c]) / float(bi_corpus[c][bg] + 1.0))
#         for ug in Cunigrams:            
#             for c in range (0, 5):
#                 perplexity[c] += math.log(float(size_corpus[c] + voc_corpus[c]) / float(uni_corpus[c][ug] + 1.0))       
        return perplexity.index(min(perplexity)) + 1