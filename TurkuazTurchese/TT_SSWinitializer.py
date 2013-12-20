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

import sys
import time

from collections import Counter
from TT_TWgatherer import *

# List of Counters of user ids
raw_flamers = []
raw_noflamers = []

res_flamers = []

# This function extracts the user ids from the file and adds them to two lists of counters
# the lists are flames and non-flames and every user is a couple (id, number of replies)
def extract_from_file():
    with open("users", 'r') as userfile:
        rawtext = userfile.read().split("////")
        del rawtext[0]
        for users in rawtext:
            ulist = users.split("-")
            if ulist[0] == 'F':
                del ulist[0]
                raw_flamers.append(Counter(ulist))
            elif ulist[0] == 'N':
                del ulist[0]
                raw_noflamers.append(Counter(ulist))

# This function, given one of the lists and the condition (-1:flame, 1:not a flame) gets all
# the informations from every user and finally stores everything in a list (total) of lists (conversations)
# of dictionaries (informations about every user).
def append_flamer(flamer_list, cond):
    for cv in flamer_list:
        conversation = []
        for flamer in cv.keys():
            user = getUserAll(flamer)
            user['weight'] = cv[flamer] * cond
            conversation.append(user)
            #time.sleep(5) #To avoid twitter rate limit
        res_flamers.append(conversation)

def SSW_init():
        
    print "\n------------------------------------------------------------------------------------"
    print "| WELCOME TO TURKUAZURCHESE, A TOOL TO FIND FLAMES AMONG CONVERSATIONS IN TWITTER! |"
    print "------------------------------------------------------------------------------------"
    print "                     by Federico Montori and Mehmet Durna"
    print "                     Social Network Analysis\n\n"
    
    # If the program is called with the -e option it includes the extraction from twitterS
    if '-e' in sys.argv:
        sys.stdout.write("Extracting users from file...")
        extract_from_file()
        sys.stdout.write("done!\n")
        
        sys.stdout.write("Extracting flamers from twitter... \n")    
        append_flamer(raw_flamers, -1)
        sys.stdout.write("\nExtracting non-flamers from twitter... \n")
        append_flamer(raw_noflamers, 1)
        sys.stdout.write("\n... done!\n")
        
        with open("almost_final", 'w') as fn:
            fn.write(str(res_flamers))
    
    
    # TEST
#     ciao = getUserAll('14662354')
#     print ciao
    with open("almost_final", 'r') as f:
        rawtxt = eval(f.read())
    
    print rawtxt
    
    with open("sciocco", 'w') as f:        
        for tuple in rawtxt:
            for user in tuple.keys():
                weight = tuple[user]
                sioc_user = "<sioc:UserAccount rdf:about=\"https://www.twitter.com/" + user[0] + "\" rdfs:label=\"Cloud\">"
                for user2 in tuple.keys():
                    if not user2 == user:
                        sioc_user += "<tt:hasFlamed><sioc:UserAccount rdf:about=\"https://www.twitter.com/" + user2[0] + "\" rdfs:label=\"Cloud\"></sioc:UserAccount></tt:hasFlamed>"
                sioc_user += "</sioc:UserAccount>"
                f.write(sioc_user)   
    return 0


SSW_init()