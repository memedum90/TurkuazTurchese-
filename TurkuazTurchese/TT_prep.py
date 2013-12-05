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

from nltk.metrics import edit_distance

#Function to remove punctuation and put everything in lowercase
def lower_punct(string):
	string = re.sub('\. |\.\n', ' * ', string)
	string = re.sub('&amp', '&', string)
	return ("".join(c for c in string if c not in ('!','.',':',';',',','?','(',')','"','/','<url>'))).lower()
	# string = (" * " + re.sub('[0-9]+', 'QQQ', string)) NUMBERS / APOSTROPHES
	
# Function to mount the slang dictionary
def mount_slang_dict():
	with open('dicts/slang-dict', 'r') as slang:
		slang = slang.read().split("\n")
		del slang[-1]
	slg = {}
	for couple in slang:
		slg[couple.split(" - ")[0]] = couple.split(" - ")[1]
	return slg

#Fuction to remove hashtags, retweet symbols and links from a string
def put_readable(string, slg):
	res = ""
	for x in string.split(" "):
		if x:
			x = slang_translate(x, slg)
			if not ((x[0] == "#") or (x[0] == "@") or ("http://" in x)):
				res += (x + " ")
	return res

# Slang correction
def slang_translate(word, slg):
	if word in slg.keys():
		word = slg[word]
	return word

# Function to correct spell errors FIXME
def spell_correct(unigrams, Dict):
	for raword in unigrams:	
		if not (raword == "" or (raword[0] == '@' or raword[0] == '#')):
		
			#Type error
			suggestions = Dict.suggest(raword)
			if suggestions and not Dict.check(raword):
				if edit_distance(suggestions[0], raword) < 2:
					raword = suggestions[0]
	return unigrams