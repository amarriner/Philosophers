#!/home/amarriner/.virtualenvs/philosopher/bin/python

"""Script to parse quotes from wikiquotes and do silly things to them"""
from bs4 import BeautifulSoup

import json
import keys
import nltk
import os
import random
import requests
import sys

# This is the URL to get quotes from
BASE_URL = 'http://en.wikiquote.org/wiki/Locke'

# Wordnik API URL
WORDNIK_URL = 'http://api.wordnik.com:80/v4/words.json/randomWords?limit=1000&hasDictionaryDef=true&includePartOfSpeech=<POS>&minCorpusCount=5&maxCorpusCount=-1&minDictionaryCount=5&maxDictionaryCount=-1&minLength=2&maxLength=10&api_key=' + keys.wordnik_api_key

# Percent chance to replace a given part of speech in a quote
REPLACEMENT_CHANCE = 50

# Sets up a unigram tagger via the NLTK library
import tagger as T
unigram = T.Tagger('uni')

# Dicts for parts of speech based on NLTK tags (nltk.help.brown_tagset(TAG))
POS =  {
        'adjective'   : None,
        'noun'        : None, 
        'noun-plural' : None,
        'proper-noun' : None,
        'verb'        : None,
       }
TAGS = {
        'JJ'          : 'adjective',   # adjective
        'NN'          : 'noun',        # noun, singular, common
        'NNS'         : 'noun-plural', # noun, plural, common
        'NP'          : 'proper-noun', # noun, singular, proper
        'VBZ'         : 'verb'         # verb, present tense, 3rd person singular
       }
WORDS = {}

def get_parts_of_speech():
   """Set up structures to be able to pull random words from later; gets lists of words from Wordnik"""

   # Loop through the TAGS dict, pulling random words from Wordnik for the given part of speech
   # Some tags may use the same Wordnik part of speech
   for tag in TAGS.keys():

      # Get a list from Wordnik for this part of speech if we haven't already
      if POS[TAGS[tag]] == None:
         result = requests.get(WORDNIK_URL.replace('<POS>', TAGS[tag]))
         POS[TAGS[tag]] = json.loads(result.content)

      # Associate the wordlist with the tag
      WORDS[tag] = POS[TAGS[tag]]


def get_quote():
   """Retrieve the wikiquote page and parse it"""

   # Grab the raw HTML from wikiquote and send it through BeautifulSoup to make it more easily parseable
   result = requests.get(BASE_URL)
   soup = BeautifulSoup(result.text)

   # These wiki pages are structured in a certain way and we rely on that. If they're adjusted this could break
   # The assumption is that there's a "Quotes" heading that we look for first and then we look for all the UL
   # tags at the same level until we reach the next H2 (sub-heading)
   lis = []
   for sib in soup.find_all(id='Quotes')[0].parent.next_siblings:
      if sib.name == 'h2':
         break

      if sib.name == 'ul':
         # This is probably not the best way to do this as some other wiki pages may be structured differently
         # For the John Locke page, we strip out the UL children inside a given LI
         sib.ul.extract()
         lis.append(sib.text)

   # Return the text of a a random LI we've found
   return random.choice(lis)


def process_quote(q):
   """Parses the quote for parts of speech and replaces some of them"""

   quote = ''

   # Tokenize from the NLTK library will split text into an array of logical language tokens (words, punctuation, etc)
   tokens = nltk.word_tokenize(q)

   # The unigram tagger will attempt to tag each token with a part of speech. I haven't been able to get a bigram
   # tagger to work correctly yet so this will have to suffice for now. Unigram taggers generally take the highest
   # probability part of speech for a given token. As opposed to a bigram (or even trigram) tagger which takes 
   # surrounding words and context into account
   for (word, tag) in unigram.tagger.tag(tokens):
      if tag == None:
         tag = 'None'

      # If the tag for this token exists in the dicts we set up earlier and the percentage chance to replace
      # succeeds, replace the current token with a word from the Wordnik API call for that part of speech
      if tag in WORDS.keys() and random.choice(range(1,100)) < REPLACEMENT_CHANCE:
         quote = quote + ' ~' + random.choice(WORDS[tag])['word'] + '~'
      else:
         quote = quote + ' ' + word

   return quote


def main():
   """Main entry point"""

   # Set up parts of speech dicts
   get_parts_of_speech()

   # Get a quote from wikiquote
   quote = get_quote()

   # Transform the quote
   print process_quote(quote)


if __name__ == '__main__':
   sys.exit(main())
