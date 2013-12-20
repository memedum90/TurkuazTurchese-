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

import enchant

# Downloaded from https://bitbucket.org/spirit/guess_language
from guess_language import guess_language
# Downloaded from https://pypi.python.org/pypi/stemming/1.0#downloads
#from stemming.porter2 import stem

from TT_prep import *
from TT_baseline import *
from TT_debate import *
from TT_politeness import *
from TT_scorer import *
from TT_SSWinitializer import *
from TT_TWgatherer import *

def printhelp():
	sys.stdout.write("Insert an keyword or --no-tweet for analysis only.\nInsert --no-proc if you want only to retrieve tweets.\nInsert -q if you want the analysis on the keyword inserted.")
			
# Global list of tweets: every element is a dictionary
archive_list = []

#List of conversations and user in conversations flames or not
flames = []
noflames = []
flamesU = []
noflamesU = []

# Add as dictionary the English language plus the bad words
pwl = enchant.request_pwl_dict('dicts/bad-words.txt')
Dict = enchant.DictWithPWL('en_US', 'dicts/bad-words.txt')
slg = mount_slang_dict()

print "\n------------------------------------------------------------------------------------"
print "| WELCOME TO TURKUAZURCHESE, A TOOL TO FIND FLAMES AMONG CONVERSATIONS IN TWITTER! |"
print "------------------------------------------------------------------------------------"
print "             		by Federico Montori and Mehmet Durna\n\n"


# Check keyword
if (len(sys.argv) == 1) or ((sys.argv[-1][0] == "-") and ('--no-tweet' not in sys.argv)):
	printhelp()
	sys.exit()
	
keyword = sys.argv[-1]

if not '--no-tweet' in sys.argv:
	# Retrieve tweets
	sys.stdout.write("Gathering and formatting data from Twitter... ")
	sys.stdout.flush()
	gatherer(keyword)
	sys.stdout.write("done!\n")
	# If only gathering from twitter is selected
	if '--no-proc' in sys.argv:
		sys.stdout.write("You can find the data retrieved in the file %s.txt" % keyword)
		sys.exit()

# Mount the disagreement lexicon
sys.stdout.write("Gathering and formatting Disagreement lexicon... ")
fill_vs_lexicon()
sys.stdout.write("done!\n")

# Mount the politeness corpus
sys.stdout.write("Gathering and formatting Stanford politeness corpus... ")
fill_politeness_corpus()
sys.stdout.write("done!\n")

# Mount the debate corpus
# sys.stdout.write("Gathering and formatting Debate corpus... ")
# fill_debate_corpus()
# sys.stdout.write("done!\n")

# Open the csv files and add every line to the archive list
# for filename in glob.glob(os.path.join('twitter_archives/csv_processes/', 'process_*.csv')):
# 	with open(filename, 'rb') as csvfile: 
# 		archive = csv.DictReader(csvfile, dialect='excel')
# 		for csvrow in archive:
# 			archive_list.append(csvrow)
		
# Open the file where the selected data is stored and put it into a list
sys.stdout.write("Gathering data from tweet files... ")
if '-q' in sys.argv and not (keyword == ''):
	archive_list = readfromfile(keyword)
else:
	archive_list = readfromall()
sys.stdout.write("done!\n")

# Clear output file content
with open("output", 'w') as f: 
	f.seek(0)
	f.truncate()
			
	sys.stdout.write("Processing tweets one by one (output information in the output file)...\n\n")
	
	#Arrays where we gather respectively tweets and users in a same conversation.
	#we empty the arrays when the conversation is over and we pass the value to "passed"
	actual = []
	actualU = []
	
	for idx, tweet in enumerate(archive_list):
		
		# Count uppercases, smiley, exclamation marks and question marks
# 		tweet['uppercases'] = n_upper_chars(tweet['text'])
# 		tweet['marks'] = n_marks_chars(tweet['text'])
		tweet['good'] = n_good_smile(tweet['text'])
		tweet['bad'] = n_bad_smile(tweet['text'])
		
		# Retrieve the original utf-8 codification on the text and eliminate hashtags and cite
		# Inside the function calls the slang translation before eliminating marks
		utftext = put_readable(tweet['text'].decode('utf-8'), slg)
		
		tweet['uppercases'] = n_upper_chars(utftext)
		tweet['marks'] = n_marks_chars(utftext)
# 		tweet['good'] = n_good_smile(utftext)
# 		tweet['bad'] = n_bad_smile(utftext)
		
		# Remove useless punctuation and put everything in lower case
		utftext = lower_punct(utftext)
		
		# Guess the language of the text and eliminate everything that is not English
		tw_lang = guess_language(utftext)
		if not (tw_lang == 'en'):
			archive_list.remove(tweet)
			
		else:
			#tweet['text_processed_unigrams'] = nltk.word_tokenize(utftext)
			tweet['text_processed_unigrams'] = utftext.split()
			tweet['text_processed_bigrams'] = nltk.bigrams(tweet['text_processed_unigrams'])
	
			utftext = " ".join(word for word in spell_correct(tweet['text_processed_unigrams'], Dict))

			# Process vulgarity
			#tweet['vulgarity'] = process_vulgarity(tweet['text_processed_unigrams'], pwl)
			tweet['vulgarity'] = process_insults(tweet['text_processed_unigrams'], pwl)
			tweet['unpoliteness'] = process_politeness(tweet['text_processed_unigrams'], tweet['text_processed_bigrams'])
			tweet['disagreement'] = process_vs(utftext)
			#tweet['disagreement'] = process_disagreement(tweet['text_processed_unigrams'], tweet['text_processed_bigrams'], tweet['topic'])
			
			actual.insert(0, tweet)
			actualU.insert(0, getTWUser(tweet))
			if tweet['rep'] == 0:
				passed = actual
				passedU = Counter(actualU)
				actual = []
				actualU = []
				
				# decide if it's a flame or not and append user information to the SSW list
				checker = compute_baseline_score(passed)
				advanced_checker = compute_score(passed)
				
				# Add the user ids of the flame to a file "users" in single copy
# 					g.write("////")
				if advanced_checker > 5:
# 						g.write("F")
					flames.append(passed)
					for x in passedU:
						passedU[x] *= -1
# 						for x in passed:
# 							g.write("-"+x['user_id']) #XXX
				else:
#						g.write("N")
					noflames.append(passed)
# 						for x in passed:
# 							g.write("-"+x['user_id'])
				flamesU.append(passedU)


				f.write("<conversation baseline="+str(checker)+" TT="+str(advanced_checker)+">\n")
				for tw in passed:
					f.write(tw['username']+" ==> "+tw['text'].encode('utf-8')+"\n	"+"		<vulgarity: "+str(tw['vulgarity'])+"; unpoliteness: "+str(tw['unpoliteness'])+"; marks: "+str(tw['marks'])+"; uppercases: "+str(tw['uppercases'])+"; smileys: "+str(tw['good'])+"; disagreement: "+str(tw['disagreement'])+">\n")
				f.write("<\conversation>\n\n")
# 			f.write("Tweet #" + str(idx+1) + " english; vulgarity: "+str(tweet['vulgarity'])+"; unpoliteness: "+str(tweet['unpoliteness'])+"\n")
# 			f.write(tweet['text'].encode('utf-8')+'\n')
# 			f.write(utftext.encode('utf-8')+'\n') 
				
			print "Tweet "+str(idx+1)+" checked!"
	sys.stdout.write("done!\n")
	
	with open("almost_final", 'w') as g:
		g.write(str(flamesU))
		
sys.stdout.write("Now moving to the SNA...\n")
# SSW_init()