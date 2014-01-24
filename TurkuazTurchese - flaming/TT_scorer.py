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

import math
import nltk
import re

from collections import Counter

fl_size = 0
fl_voc = 0
fl_unigrams = []
fl_bigrams = []

with open('dicts/flaming.txt') as f:
    corp = f.read()
fl_unigrams.extend(nltk.word_tokenize(corp))
fl_size = len(fl_unigrams)
fl_bigrams = Counter(nltk.bigrams(corp))
fl_unigrams = Counter(fl_unigrams)
fl_voc = len(fl_unigrams)  

#
def process_fl(unigrams, bigrams):
    Cunigrams = Counter(unigrams)
    Cbigrams = Counter(bigrams)
    
    perplexity = 0
    for bg in Cbigrams:            
        perplexity += math.log(float(fl_unigrams[bg[0]] + fl_voc) / float(fl_bigrams[bg] + 1.0))
    
    return perplexity #FIXME



# WEIGHTS
SWupp = 0.1 # Weight assigned to one uppercase
SWmrk = 2.0 # Weigth assigned to one question or exclamation mark
SWgud = -10 # Weigth assigned to one good smiley
SWbad = -0.5 # Weight assigned to one bad smiley
SWvlg = 4 # Weight assigned to one bad or risky word
SWdis = 8 # Weight assigned to one disagreement point
SWpol = 2 # Weight assigned to one negativity point

# Final function to compute the overall score of a conversation
def compute_score(conver):
    STupp = 0.0
    STmrk = 0.0
    STgud = 0.0
    STbad = 0.0
    STvlg = 0.0
    STdis = 0.0
    STpol = 0.0
    for idx, tw in enumerate(conver):
        STupp += tw['uppercases']
        STmrk += tw['marks']
        STgud += tw['good']
        STbad += tw['bad']
        STvlg += tw['vulgarity']
        STdis += tw['disagreement']
        STpol += tw['polarity']
#     STupp /= len(conver)
#     STmrk /= len(conver)
#     STgud /= len(conver)
#     STbad /= len(conver)
#     STvlg /= len(conver)
#     STdis /= len(conver)
#     STpol /= len(conver)
    return float(SWupp*STupp + SWmrk*STmrk + SWgud*STgud + SWvlg*STvlg + SWbad*STbad + SWdis*STdis + STpol) / (len(conver))
#    return float(STvlg*3.512366452 + STdis*17.639133144 + STpol*2.035484006) - STgud*5
    
    
#     fneg=-0.025858589191
#     nneg=0.036421884865
#     fdis=0.110573805783
#     ndis=0.036421884865
#     fins=0.411572173623
#     nins=0.151582820365
#      
#     th=(fneg+nneg)/2.0+SWdis*(fdis+ndis)/2.0+SWvlg*(fins+nins)/2.0
#     return float(SWvlg*STvlg + SWdis*STdis + STpol)  - th
    