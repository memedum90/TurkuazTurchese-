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

import rdfextras
import sys
import uuid

from collections import Counter
from rdflib.graph import Graph
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
    
    with open('SNA/social_graph.rdf', 'w') as f:
        
        #f.write("<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" xmlns:sioc=\"http://rdfs.org/sioc/ns#\" xmlns:foaf=\"http://xmlns.com/foaf/0.1/\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\" xmlns:xs=\"http://www.w3.org/2000/10/XMLSchema#\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns=\"http://www.w3.org/2000/10/XMLSchema#\" xml:base=\"http://ns.inria.fr/semsna/2009/06/21/voc\">")
        f.write("<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\" xmlns:xs=\"http://www.w3.org/2000/10/XMLSchema#\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns=\"http://www.w3.org/2000/10/XMLSchema#\" xml:base=\"http://www.fedemontori.eu/ns#\" xmlns:tto=\"http://www.fedemontori.eu/ns#\" xmlns:sioc=\"http://rdfs.org/sioc/ns#\" xmlns:foaf=\"http://xmlns.com/foaf/0.1/\"> <owl:Ontology rdf:about=\"http://www.fedemontori.eu\"> <dc:title xml:lang=\"en\"> TurkuazTurkese core ontology </dc:title> <owl:versionInfo> Revision: 1.2 </owl:versionInfo> <dc:description xml:lang=\"en\"> TurkuazTurcheseOnto is an extension of sioc used to represent concepts like flaming and non-flaming conversation (so weighted relationships) </dc:description> </owl:Ontology> <!-- top concepts --> <owl:Class rdf:ID=\"Conversation\"> <rdfs:subClassOf rdf:resource=\"sioc:Forum\"/> <label xml:lang=\"en\"> TTO conversation </label> <comment xml:lang=\"en\"> A class that represents a conversation among more people. </comment> </owl:Class> <owl:ObjectProperty rdf:ID=\"hasConversation\"> <range rdf:resource=\"#Conversation\"/> <label xml:lang=\"en\"> has Conversation </label> <comment xml:lang=\"en\"> Links personally an user to a conversation, let's say from his point of view. </comment> </owl:ObjectProperty> <owl:ObjectProperty rdf:ID=\"hasCorrespondant\"> <range rdf:resource=\"#UserAccount\"/> <label xml:lang=\"en\"> has Correspondant user </label> <comment xml:lang=\"en\"> link a conversation with its correspondants </comment> </owl:ObjectProperty>")
              
        for tple in rawtxt:
            for user in tple.keys():
                weight = tple[user]
                if weight > 0: fl = "noflame"
                else: fl = "flame"
                uid = str(uuid.uuid4())
                sioc_user = "<sioc:UserAccount rdf:about=\"https://www.twitter.com/" + user[0] + "\" rdfs:label=\"Cloud\">"
                sioc_user += "<tto:hasRelationship rdf:resource=\"http://www.fedemontori.eu/#" + uid + "\"/>"
                for user2 in tple.keys():
                    if not user2 == user:
                        sioc_user += "<foaf:knows rdf:resource=\"https://www.twitter.com/" + user2[0] + "\"/>"
                sioc_user += "</sioc:UserAccount> <tto:Relationship rdf:about=\"http://www.fedemontori.eu/#" + uid + "\" flame=\"" + fl + "\"> <tto:value rdf:datatype=\"http://www.w3.org/2001/XMLSchema#int\">" + str(abs(weight)) + "</tto:value>"
                for user2 in tple.keys():
                    if not user2 == user:
                        sioc_user += "<tto:hasCorrespondant rdf:resource=\"https://www.twitter.com/" + user2[0] + "\" />"
                sioc_user += "</tto:Relationship>"
                
                
                f.write(sioc_user)

#         for tple in rawtxt:
#             for user in tple.keys():
#                 weight = tple[user]
#                 sioc_user = "<sioc:UserAccount rdf:about=\"https://www.twitter.com/" + user[0] + "\" rdfs:label=\"Cloud\">"
#                 for user2 in tple.keys():
#                     if not user2 == user:
#                         sioc_user += "<foaf:knows rdf:resource=\"https://www.twitter.com/" + user2[0] + "\" value=\"" + str(weight) + "\"/>"
#                 sioc_user += "</sioc:UserAccount>"
#                 f.write(sioc_user)
                
        f.write("</rdf:RDF>")

    # Activate the rdf plugin on the variable graph
    rdfgraph = Graph()
    rdfextras.registerplugins() # so we can Graph.query()
    rdfgraph.parse('SNA/social_graph.rdf')
    
    with open('SNA/social_graph.rdf', 'w') as sgr: 
        sgr.write(rdfgraph.serialize(format='pretty-xml'))
     
    alltuples = rdfgraph.query("SELECT ?s ?w ?o ?f WHERE { ?s tto:hasRelationship ?r . ?r tto:value ?w . ?r ns1:flame ?f . ?r tto:hasCorrespondant ?o }")
    # result = rdfgraph.query("SELECT ?o WHERE { <https://www.twitter.com/ArkanKurd> <http://ns.inria.fr/semsna/2009/06/21/value> ?o } ")
    # result = rdfgraph.query("SELECT ?y WHERE { ?x $path ?y }")# . FILTER match($path, foaf:knows) }")# FILTER (pathLength($path) >= 1 && pathLength($path) <= 2)") 
     
    for res in alltuples:
        print res
    print len(alltuples)


if __name__ == "__main__":
    SSW_init()