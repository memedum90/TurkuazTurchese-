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
import re

# WEIGHTS
Wupp = 0.1 # Weight assigned to one uppercase
Wmrk = 2.0 # Weigth assigned to one question or exclamation mark
Wgud = -10 # Weigth assigned to one good smiley
Wbad = -0.5 # Weight assigned to one bad smiley
Wvlg = 4 # Weight assigned to one bad or risky word
Wump = 0.5 # Weight assigned to one politeness point



# Function to count upper case letters in a string
def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())

# Function to count question and exclamation/question marks in a string
def n_marks_chars(string):
    return sum(1 for c in string if c in ('?','!'))

#Function to count good smileys in a string FIXME
def n_good_smile(string):
    return len(re.findall(r'([:=;B]-?(\)+|D+|\*+|[pP]+))|(\b[lL]+[oO]+[lL]+\b)|[😍♥😘😜😭😂]', string))

#Function to count bad smileys in a string
def n_bad_smile(string):
    return len(re.findall('(:|=)-?(\(+|\/)', string))

# Function to count the occurrences of vulgar words or insults (vulgar word + 2nd person in a little distance)
def process_vulgarity(list_of_words, Dic):
    total = 0
    for word in list_of_words:
        if Dic.check(word):
            total += 1
    return total

def process_insults(list_of_words, Dic):
    pronouns = ["you","your","you're","you'll","you've"]
    intr = [list_of_words.index(val) for val in pronouns if val in list_of_words]
    total = 0.3 * len(intr)
    for idx, word in enumerate(list_of_words):
        if Dic.check(word):
            total += 0.3
            for i in intr:
                if abs(idx-i) < 3: 
                    total += 5
    return total

# Baseline function to compute the overall score of a conversation
def compute_baseline_score(conver):
    Tupp = 0
    Tmrk = 0
    Tgud = 0
    Tbad = 0
    Tvlg = 0
    Tump = 0
    for idx, tw in enumerate(conver):
        Tupp += tw['uppercases']
        Tmrk += tw['marks']
        Tgud += tw['good']
        Tbad += tw['bad']
        Tvlg += tw['rawvulgarity']
        Tump += tw['unpoliteness']
    return float(Wupp*Tupp + Wmrk*Tmrk + Wgud*Tgud + Wbad*Tbad + Wvlg*Tvlg ) / (len(conver))