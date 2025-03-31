### get the text in
import nltk
from nltk.corpus import stopwords

text_name = 'amna-project/corpus/poem1-ao-sayyo.txt'
print(text_name)
# ### parse the text
with open(text_name, 'r') as file_in:
    raw_text = file_in.read()
print(raw_text)
# ### from the one big file break it into poems


# ### clean and sanitize it

raw_tokens = nltk.word_tokenize(raw_text)

lower_tokens = [word.lower() for word in raw_tokens]
stopwords = nltk.corpus.stopwords.words('english')
stop_removed_tokens = [word for word in lower_tokens if word not in stopwords]

print(raw_tokens)
print(stop_removed_tokens)

# ### process it

nltk.text.Text(raw_tokens)

# ### analyze it

# ### show off the kinds of things you can do

# ### talk through how we might approach some of the questions and what problems it raises