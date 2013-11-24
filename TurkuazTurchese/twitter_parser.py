#! /usr/bin/env python
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
#
# This program allows you to collect data from the reuters21578 training
# corpus and store it into 5 different files in the Training_Corpus 
# folder accordind to one of the 5 main topics

#import codecs
import csv
import enchant
#import glob
import nltk
#import os
import re
#import sys

# Downloaded from https://bitbucket.org/spirit/guess_language
from guess_language import guess_language
from nltk.metrics import edit_distance
# Downloaded from https://pypi.python.org/pypi/stemming/1.0#downloads
#from stemming.porter2 import stem

# Function to mount the slang dictionary
def mount_slang_dict():
	with open('dicts/slang-dict', 'r') as slang:
		slang = slang.read().split("\n")
		del slang[-1]
	slg = {}
	for couple in slang:
		slg[couple.split(" - ")[0]] = couple.split(" - ")[1]
	return slg

# Function to count uppercase letters in a string
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

# Function to correct spell errors FIXME
def spell_correct(raword):
	if not (raword == "" or (raword[0] == '@' or raword[0] == '#')):
		# Slang correction
		if raword in slg.keys():
			raword = slg[raword]
		
		#Type error
		suggestions = Dict.suggest(raword)
		if suggestions and not Dict.check(raword):
			if edit_distance(suggestions[0], raword) < 2:
				return suggestions[0]
	return raword

# Global list of tweets: every element is a dictionary
archive_list = []

# Add as dictionary the english language plus the bad words
pwl = enchant.request_pwl_dict('dicts/bad-words.txt')
#Dict = enchant.Dict('en_US')
Dict = enchant.DictWithPWL('en_US', 'dicts/bad-words.txt')
slg = mount_slang_dict()

# Open the csv file and add every line to the archive list
with open('twitter_archives/csv_processes/process_414_justinbieber.csv', 'rb') as csvfile:
	archive = csv.DictReader(csvfile, dialect='excel')
	for csvrow in archive:
		archive_list.append(csvrow)
		
# Clear output file content
with open("output", 'w') as f:
	f.seek(0)
	f.truncate()
	
	for idx, tweet in enumerate(archive_list):
		
		# Retrieve the original utf-8 codification on the text
		utftext = tweet[' text'].decode('utf-8')
		
		# Count uppercases, smiley, exclamation marks and question marks
		tweet[' uppercases'] = n_upper_chars(utftext)
		tweet[' marks'] = n_marks_chars(utftext)
		tweet[' good'] = n_good_smile(utftext)
		tweet[' bad'] = n_bad_smile(utftext)
		
		# Remove useless punctuation and put everything in lower case FIXME
		utftext = re.sub('\. |\.\n', ' * ', utftext)
		utftext = re.sub('&amp', '&', utftext)
		utftext = ("".join(c for c in utftext if c not in ('!','.',':',';',',','?','(',')','"',"'",'/'))).lower()
		# utftext = (" * " + re.sub('[0-9]+', 'QQQ', utftext)) NUMBERS
		
		# Guess the language of the text and eliminate everything that is not English
		tw_lang = guess_language(utftext)
		#tw_lang = tweet[' user_lang']
		if not (tw_lang == 'en'):
			archive_list.remove(tweet)
	
		wordbyword = utftext.split(" ")
		del wordbyword[0]
		utftext = " ".join([ spell_correct(word) for word in wordbyword if isinstance(word, unicode)])
			
		tweet[' text_processed_unigrams'] = nltk.word_tokenize(utftext)
		tweet[' text_processed_bigrams'] = nltk.bigrams(tweet[' text_processed_unigrams'])
	
		f.write("Tweet #" + str(idx) + ": detected " + str(tw_lang) + " language\n")
		f.write(tweet[' text'].encode('utf-8')+'\n')
		f.write(utftext.encode('utf-8')+'\n')
		print str(idx) + str(tweet)
		
# WE STILL DON'T USE STEMMING
# WE SHALL FIRST CORRECT SLANG, THE PUNCT, THEN TYPE