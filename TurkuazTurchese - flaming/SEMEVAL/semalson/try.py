import en

print en.is_basic_emotion("anxious")
print en.is_persuasive("money")
print en.noun.is_emotion("anger")


print en.adjective.is_emotion("anxious", boolean=False)

print en.is_noun("comptuer")
print en.spelling.suggest("computer")[0]
print en.verb.is_emotion("love", boolean=False)
print en.verb.infinitive("announced")
print en.verb.infinitive("dont")
print en.is_verb("went")
a=en.verb.infinitive("dont")
print en.verb.is_emotion(a, boolean=False)
print en.is_noun("people")

print en.is_noun(en.noun.singular("adore"))
print en.noun.lexname("book")
print en.noun.lexname("music")
print en.noun.lexname("water")
print en.noun.lexname("fear")
print en.noun.lexname("love")
print en.noun.lexname("like")
print en.noun.lexname("hate")
print en.noun.lexname("overcome")
print en.adverb.lexname("actually")


print en.noun.synonyms("good")