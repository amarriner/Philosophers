#!/home/amarriner/.virtualenvs/philosopher/bin/python

"""Script to parse quotes from wikiquotes and do silly things to them"""
from bs4 import BeautifulSoup

import nltk
import os
import requests
import sys

"""This is the URL to get quotes from"""
BASE_URL = 'http://en.wikiquote.org/wiki/Locke'

"""Sets up a unigram tagger via the NLTK library"""
import tagger as T
unigram = T.Tagger('uni')

def main():
   """Main entry point"""
   result = requests.get(BASE_URL)
   soup = BeautifulSoup(result.text)

   for sib in soup.find_all(id='Quotes')[0].parent.next_siblings:
      if sib.name == 'h2':
         break

      if sib.name == 'ul':
         sib.ul.extract()
         tokens = nltk.word_tokenize(sib.text)
         print '-----------------------------------------------------------------------------------------------'
         print unigram.tagger.tag(tokens)

if __name__ == '__main__':
   sys.exit(main())
