import os
import collections
import re

from Punjabi_Stemmer import PunjabiStemmer

# Now you can simply initialize the stemmer without specifying file paths
stemmer = PunjabiStemmer()

text = "بھجدا بھجدی بھجدے  بھجیاں بھجنی بھجنے بھجاندا بھجاندی"
stemmed_text = stemmer.stem_text(text)
print(f"Original: {text}\nStemmed: {stemmed_text}")



