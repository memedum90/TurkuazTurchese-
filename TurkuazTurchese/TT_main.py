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

# TODO
# 

import enchant
import nltk
import sys

# Downloaded from https://bitbucket.org/spirit/guess_language
from guess_language import guess_language
# Downloaded from https://pypi.python.org/pypi/stemming/1.0#downloads
#from stemming.porter2 import stem

from TT_prep import *
from TT_baseline import *
from TT_politeness import *
			
# Global list of tweets: every element is a dictionary
archive_list = []

# Add as dictionary the english language plus the bad words
pwl = enchant.request_pwl_dict('dicts/bad-words.txt')
Dict = enchant.DictWithPWL('en_US', 'dicts/bad-words.txt')
slg = mount_slang_dict()


print "\n------------------------------------------------------------------------------------"
print "| WELCOME TO TURKUAZURCHESE, A TOOL TO FIND FLAMES AMONG CONVERSATIONS IN TWITTER! |"
print "------------------------------------------------------------------------------------"
print "             		by Federico Montori and Mehmet Durna\n\n"


# Mount the politeness corpus
sys.stdout.write("Gathering and formatting Stanford politeness corpus... ")
fill_politeness_corpus()
sys.stdout.write("done!\n")

# TEST
#sys.exit()

# Open the csv files and add every line to the archive list
for filename in glob.glob(os.path.join('twitter_archives/csv_processes/', 'process_*.csv')):
	with open(filename, 'rb') as csvfile: 
		archive = csv.DictReader(csvfile, dialect='excel')
		for csvrow in archive:
			archive_list.append(csvrow)
		
# Clear output file content
with open("output", 'w') as f:
	f.seek(0)
	f.truncate()
	
	sys.stdout.write("Processing tweets one by one (output information in the output file)...\n\n")
	
	for idx, tweet in enumerate(archive_list):
		
		# Retrieve the original utf-8 codification on the text and eliminate hashtags and cite
		# Inside the function calls the slang translation before eliminating marks
		utftext = put_readable(tweet[' text'].decode('utf-8'), slg)
		
		# Count uppercases, smiley, exclamation marks and question marks
		tweet[' uppercases'] = n_upper_chars(utftext)
		tweet[' marks'] = n_marks_chars(utftext)
		tweet[' good'] = n_good_smile(utftext)
		tweet[' bad'] = n_bad_smile(utftext)
		
		# Remove useless punctuation and put everything in lower case
		utftext = lower_punct(utftext)
		
		# Guess the language of the text and eliminate everything that is not English
		tw_lang = guess_language(utftext)
		if not (tw_lang == 'en'):
			archive_list.remove(tweet)
			
		else:
			#tweet[' text_processed_unigrams'] = nltk.word_tokenize(utftext)
			tweet[' text_processed_unigrams'] = utftext.split()
			tweet[' text_processed_bigrams'] = nltk.bigrams(tweet[' text_processed_unigrams'])
	
			utftext = " ".join(word for word in spell_correct(tweet[' text_processed_unigrams'], Dict))

			# Process vulgarity
			tweet[' vulgarity'] = process_vulgarity(tweet[' text_processed_unigrams'], pwl)
			tweet[' politeness'] = process_politeness(tweet[' text_processed_unigrams'], tweet[' text_processed_bigrams'])
			
			f.write("Tweet #" + str(idx+1) + " english; vulgarity: "+str(tweet[' vulgarity'])+"; politeness: "+str(tweet[' politeness'])+"\n")
			f.write(tweet[' text'].encode('utf-8')+'\n')
			f.write(utftext.encode('utf-8')+'\n') 
			
		print "Tweet "+str(idx+1)+" checked!"
		
	sys.stdout.write("done!\n")	