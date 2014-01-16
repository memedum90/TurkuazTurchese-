
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
import time

from Semantic_Tagger import classifyTweet
from TT_prep import *
from TT_baseline import *
from TT_debate import *
from TT_politeness import *
from TT_scorer import *
from TT_SSWinitializer import *
from TT_TWgatherer import *

#GLOBAL VARIABLES

tm = time.time()
		
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

# Measurments used in feature evaluation
fla_upp = 0.0
nfla_upp = 0.0
tmp_upp = 0.0
fla_mrk = 0.0
nfla_mrk = 0.0
tmp_mrk = 0.0
fla_gsm = 0.0
nfla_gsm = 0.0
tmp_gsm = 0.0
fla_bsm = 0.0
nfla_bsm = 0.0
tmp_bsm = 0.0
fla_ins = 0.0
nfla_ins = 0.0
tmp_ins = 0.0
fla_dis = 0.0
nfla_dis = 0.0
tmp_dis = 0.0
fla_pol = 0.0
nfla_pol = 0.0
tmp_pol = 0.0

chkF = 0.0
chkN = 0.0

# Measurments used in final result evaluation
flamesnum = 0.0
flamesgsbs = 0.0
flamesgs = 0.0
noflamesnum = 0.0
noflamesgs = 0.0
noflamesgsbs = 0.0
flamesboh = 0.0
flamesbohbs = 0.0
noflamesboh = 0.0
noflamesbohbs = 0.0

universal_user_array = {}

def printhelp():
	sys.stdout.write("Insert an keyword or --no-tweet for analysis only.\nInsert --no-proc if you want only to retrieve tweets.\nInsert -q if you want the analysis on the keyword inserted.")

# Main flow
if __name__ == "__main__":
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
	
# 	# Mount the flaming corpus
# 	sys.stdout.write("Gathering and formatting TurkuazTurchese flaming corpus... ")
# 	fill_fl_corpus()
# 	sys.stdout.write("done!\n")
	
	# DEBATE CORPUS - Doesn't fit
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
	if '-q' in sys.argv and not (keyword == ''): # Read just for the designed one with the -q opt
		archive_list = readfromfile(keyword)
	else:
		archive_list = readfromall()
	sys.stdout.write("done!\n")
	
	# Clear output file content
	with open("output", 'w') as f: 
		f.seek(0)
		f.truncate()
				
		sys.stdout.write("Processing tweets one by one (output information in the output file)...\n\n")
		
		# Arrays where we gather respectively tweets and users in a same conversation.
		# we empty the arrays when the conversation is over and we pass the value to "passed" later
		actual = []
		actualU = []
		
		for idx, tweet in enumerate(archive_list):
			
			# Count smiley
			tweet['good'] = n_good_smile(tweet['text'])
			tweet['bad'] = n_bad_smile(tweet['text'])
			
			# Retrieve the original utf-8 codification on the text and eliminate hashtags and cite
			# Inside the function calls the slang translation before eliminating marks
			utftext = put_readable(tweet['text'].decode('utf-8'), slg)
			
			# Count uppercases and marks 
			tweet['uppercases'] = n_upper_chars(utftext)
			tweet['marks'] = n_marks_chars(utftext)

# 			tweet['uppercases'] /= (float(len(utftext)) + 0.000001)
# 			tweet['marks'] /= (float(len(utftext)) + 0.000001)
# 			
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
	
				# Process remaining features and save them into a dictionary
				tweet['rawvulgarity'] = process_vulgarity(tweet['text_processed_unigrams'], pwl)
				tweet['vulgarity'] = process_insults(tweet['text_processed_unigrams'], pwl)
				tweet['unpoliteness'] = process_politeness(tweet['text_processed_unigrams'], tweet['text_processed_bigrams'])
				tweet['disagreement'] = process_vs(utftext)
				tweet['fl_corpus'] = process_fl(tweet['text_processed_unigrams'], tweet['text_processed_bigrams'])
				tweet['polarity'] = 2 - tweet['polarity'] - 1
				
# 				polarity = classifyTweet(utftext)
# 				if polarity == 'positive':
# 					tweet['polarity'] = 1
# 				elif polarity == 'negative':
# 					tweet['polarity'] = -1
# 				else: tweet['polarity'] = 0
				
				# Partial sums of the feature evaluations
				tmp_upp += tweet['uppercases']
				tmp_mrk += tweet['marks']
				tmp_gsm += tweet['good']
				tmp_bsm += tweet['bad']
				tmp_ins += tweet['vulgarity']
				tmp_dis += tweet['disagreement']
				tmp_pol += tweet['polarity']
				
				actual.insert(0, tweet)
				actualU.append(tweet['username']) #actualU.insert(0, getTWUser(tweet))
				if tweet['rep'] == 0:
# 					twn = float(len(actual))
					twn = 1
					passed = actual
					passedU = Counter(actualU)
					actual = []
					actualU = []
					
					# FIXME Decide if it's a flame or not and append user information to the SSW list
					checker = compute_baseline_score(passed) - 3.0
					advanced_checker = compute_score(passed) - 3.0
				
					# Stuff for evaluation part (only if we have the field flame in the last tweet of the conv)
					if tweet['flame'] == 1:
						flamesnum += 1.0
						
						# Store all the features 
						fla_upp += tmp_upp/twn
						fla_mrk += tmp_mrk/twn
						fla_gsm += tmp_gsm/twn
						fla_bsm += tmp_bsm/twn
						fla_ins += tmp_ins/twn
						fla_dis += tmp_dis/twn
						fla_pol += tmp_pol/twn
						chkF += advanced_checker 
						
						if checker >= 0:
							flamesgsbs += 1.0
						if advanced_checker >= 0:
							flamesgs += 1.0	
					else:
						noflamesnum += 1.0
						
						#Store all the features
						nfla_upp += tmp_upp/twn
						nfla_mrk += tmp_mrk/twn
						nfla_gsm += tmp_gsm/twn
						nfla_bsm += tmp_bsm/twn
						nfla_ins += tmp_ins/twn
						nfla_dis += tmp_dis/twn
						nfla_pol += tmp_pol/twn		
						chkN += advanced_checker
						
						if checker < 0:
							noflamesgsbs += 1.0
						if advanced_checker < 0:
							noflamesgs += 1.0
					if checker < 0:
						noflamesbohbs += 1.0
					else: 
						flamesbohbs += 1.0
					if advanced_checker < 0:
						noflamesboh += 1.0
						denote = 0
					else: 
						flamesboh += 1.0
						denote = 1
					
					# Insert conversation users in the universal list
					for user in passedU:
						for user2 in passedU:
							if not user == user2:
								if user not in universal_user_array.keys():
									universal_user_array[user] = []
								universal_user_array[user].append((passedU[user],denote,user2))
					
	
					# Zero to all the temp features
					tmp_upp = 0.0
					tmp_mrk = 0.0
					tmp_gsm = 0.0
					tmp_bsm = 0.0
					tmp_ins = 0.0
					tmp_dis	= 0.0
					tmp_pol = 0.0
	
				# Stuff for SSW part
					if advanced_checker >= 0:
	# 						g.write("F")
						flames.append(passed)
				#		for x in passedU:
				#			passedU[x] *= -1
	# 						for x in passed:
	# 							g.write("-"+x['user_id']) #XXX
					else:
	#						g.write("N")
						noflames.append(passed)
	# 						for x in passed:
	# 							g.write("-"+x['user_id'])
				#	flamesU.append(passedU)
	
					# Spit out the output
					f.write("<conversation baseline="+str(checker)+" TT="+str(advanced_checker)+">  "+str(tweet['flame'])+"\n")
					for tw in passed:
						f.write(tw['username']+" ==> "+tw['text'].encode('utf-8')+"\n	"+"		<vulgarity: "+str(tw['rawvulgarity'])+"/"+str(tw['vulgarity'])+"; unpoliteness: "+str(tw['unpoliteness'])+"; marks: "+str(tw['marks'])+"; uppercases: "+str(tw['uppercases'])+"; smileys: "+str(tw['good'])+"; disagreement: "+str(tw['disagreement'])+"; pplxity: "+str(tw['fl_corpus'])+">\n")
					f.write("<\conversation>\n\n")
					
				print "Tweet "+str(idx+1)+" checked!"
		sys.stdout.write("done! Computed in " + str(time.time() - tm) + " seconds.\n\n")
		
# 		with open("almost_final", 'w') as g:
# 			g.write(str(flamesU))

	print "Uppercases: flaming " + str(fla_upp/flamesnum) + " nonflaming " + str(nfla_upp/noflamesnum) + "."
	print "Marks: flaming " + str(fla_mrk/flamesnum) + " nonflaming " + str(nfla_mrk/noflamesnum) + "."
	print "Good Smileys: flaming " + str(fla_gsm/flamesnum) + " nonflaming " + str(nfla_gsm/noflamesnum) + "."
	print "Bad Smileys: flaming " + str(fla_bsm/flamesnum) + " nonflaming " + str(nfla_bsm/noflamesnum) + "."
	print "Insults: flaming " + str(fla_ins/flamesnum) + " nonflaming " + str(nfla_ins/noflamesnum) + "."
	print "Disagreement: flaming " + str(fla_dis/flamesnum) + " nonflaming " + str(nfla_dis/noflamesnum) + "."
	print "Negativity flaming " + str(fla_pol/flamesnum) + " nonflaming " + str(nfla_dis/noflamesnum) + ".\n"
	print "in toto flaming " + str(chkF/flamesnum) + " nonflaming " + str(chkN/noflamesnum) + ".\n"
	print "Baseline Precision: "+str(flamesgsbs/flamesbohbs)+"/"+str(noflamesgsbs/noflamesbohbs)+" Recall: "+str(flamesgsbs/flamesnum)+"/"+str(noflamesgsbs/noflamesnum) + "."
	print "Our Precision: "+str(flamesgs/flamesboh)+"/"+str(noflamesgs/noflamesboh)+" Recall: "+str(flamesgs/flamesnum)+"/"+str(noflamesgs/noflamesnum) + ".\n"
	
	# TODO substitute keys with sets
	sys.stdout.write("Elaborating output on file... ")
	with open('raw_users','w') as g:
		g.write(str(universal_user_array))
	sys.stdout.write("done!\n") 
			
	sys.stdout.write("Now moving to the SNA...\n\n")
#SSW_init()