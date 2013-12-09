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

import re

# Function to count upper case letters in a string
def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())

# Function to count question and exclamation marks in a string
def n_marks_chars(string):
    return sum(1 for c in string if c in ('?','!'))

#Function to count good smileys in a string FIXME
def n_good_smile(string):
    return len(re.findall('(:|=|;|B)?-(\)+|D+|\*+|[pP]+)', string))

#Function to count bad smileys in a string FIXME
def n_bad_smile(string):
    return len(re.findall('(:|=)?-(\(+|\/)', string))

# Function to count the occurrences of vulgar words
def process_vulgarity(list_of_words, Dic):
    total = 0
    for word in list_of_words:
        if Dic.check(word):
            total += 1
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
        Tvlg += tw['vulgarity']
        Tump += tw['unpoliteness']
    return float(0.2*Tupp + 1.6*Tmrk - (idx*0.2)*8.0*Tgud + 0.4*Tbad + 3.0*Tvlg + 6.0*Tump) / float(2*len(conver))
