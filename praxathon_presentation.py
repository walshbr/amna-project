import nltk

### get the text in

text_name = 'yj_may22.txt'

### parse the text
with open(text_name, 'r') as file_in:
    raw_text = file_in.read()
    
### from the one big file break it into pieces if necessary.


### clean and sanitize it

raw_tokens = nltk.word_tokenize(raw_text)
lower_tokens = [word.lower() for word in raw_tokens]
stopwords = nltk.corpus.stopwords.words('english')
stop_removed_tokens = [word for word in lower_tokens if word not in stopwords]

### process it

print(nltk.text.Text(raw_tokens))

### analyze it

### show off the kinds of things you can do

### talk through how we might approach some of the questions and what problems it raises