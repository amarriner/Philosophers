from cPickle import dump, load
from nltk.corpus import brown

import nltk
import random
import os.path

class Tagger:
   """Simple struct-like helper class for tagger objects; Uses the brown corpus from NLTK"""

   # String code for the type of tagger (unigram, bigram, etc).
   # Defaults to NN (always singular noun)
   type = 'default'

   # Suffix for the cache file name
   filename = 'gram_tagger.pkl'

   # The actual tagger object which is instantiated upon instantiation of this class
   tagger = None

   def __init__(self, type = 'default', backoff = None):
      self.type = type

      # If a cache file for this type of tagger already exists, just load it instead of creating a new one
      if os.path.isfile(self.type + self.filename):
         self.load()

      # Otherwise create a new tagger of the given type
      else:
         if self.type == 'uni':
            self.tagger = nltk.UnigramTagger(brown.tagged_sents())
         elif self.type == 'bi':
            self.tagger = nltk.BigramTagger(brown.tagged_sents())
         elif self.type == 'tri':
            self.tagger = nltk.TrigramTagger(brown.tagged_sents())
         else:
            self.tagger = nltk.DefaultTagger('NN')

         # Cache the tagger for next time
         self.dump()


   def dump(self):
      """Dumps the tagger to the filesystem to speed things up on future runs"""

      f = open(self.type + self.filename, 'wb')
      dump(self.tagger, f, -1)
      f.close()

   def load(self):
      """Read a tagger in from the filesystem if one has been cached"""

      f = open(self.type + self.filename, 'rb')
      self.tagger = load(f)
      f.close()
