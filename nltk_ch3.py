import nltk, re, pprint
# from nltk.book import *
from nltk import word_tokenize

# ### to open a particular file from gutenberg, add url - in terminal:
from urllib import request
url = "http://www.gutenberg.org/cache/epub/301/pg301.txt" 
response = request.urlopen(url)
raw = response.read().decode('utf8')
print(len(raw))

# ### tokenize
#       tokens = word_tokenize(raw)
# ### NLTK Text
#       text = nltk.Text(tokens)

