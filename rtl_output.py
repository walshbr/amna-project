# if spacy
# import spacy
# opening lines are the same
#how to creat'Text': spacy is library name. '.blank' creates blank pipeline. then doc=nlp creates 'text'
#nlp=spacy.blank('ur')
#doc=nlp(raw_text)

import nltk
file_path="corpus/poem1-ao-sayyo.txt"

with open(file_path,'r') as infile:
    raw_text=infile.read()


tokens=nltk.word_tokenize(raw_text)

#terminal is always LTR. so, keep a sep output file as endpoint
with open('poem1-tokenized.txt', 'w') as outfile:
    outfile.write(str(tokens))

# pos tagging --requires downloading things
#  outfile.write(str(nltk.pos_tag(tokens,lang='ur')))