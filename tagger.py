"""Simple struct-like helper class for tagger objects"""

from cPickle import dump, load
from nltk.corpus import brown

import nltk
import random
import os.path

class Tagger:
   type = 'default'
   filename = 'gram_tagger.pkl'
   tagger = None

   def __init__(self, type = 'default', backoff = None):
      self.type = type

      if os.path.isfile(self.type + self.filename):
         self.load()
      else:
         if self.type == 'uni':
            self.tagger = nltk.UnigramTagger(brown.tagged_sents())
         elif self.type == 'bi':
            self.tagger = nltk.BigramTagger(brown.tagged_sents())
         elif self.type == 'tri':
            self.tagger = nltk.TrigramTagger(brown.tagged_sents())
         else:
            self.tagger = nltk.DefaultTagger('NN')

         self.dump()

   def dump(self):
      f = open(self.type + self.filename, 'wb')
      dump(self.tagger, f, -1)
      f.close()

   def load(self):
      f = open(self.type + self.filename, 'rb')
      self.tagger = load(f)
      f.close()
