# bring in what we need
import hazm
import os


# gets the filenames
def all_files(folder_name):
    """given a directory, return the filenames in it"""
    # this makes an empty collection of texts
    texts = []
    for (root, _, files) in os.walk(folder_name):
        for fn in files:
            path = os.path.join(root, fn)
            texts.append(path)
    return texts

# reads in our texts
corpus_dir = 'corpus'
files = all_files(corpus_dir)
texts = []
for file in files:
    with open(file, 'r') as fin:
        texts.append(fin.read())

print(texts)

test = texts[0]

# lowercases and normalizes
normalizer = hazm.Normalizer()
normalized_test = normalizer.normalize(test)

# divides into sentences and then words
sents = hazm.sent_tokenize(normalized_test)
tokens = [hazm.word_tokenize(sent) for sent in sents]

# flat_tokens
tokens = [item for sublist in tokens for item in sublist]


stemmer = hazm.Stemmer()
lemmatizer = hazm.Lemmatizer()

stems = [stemmer.stem(token) for token in tokens]

print(stems)

# to set up / run in the future. 
# assuming that you have pipenv set up
# pipenv --python 3.11
# pipenv shell
# change to the right folder
# python filename

#### didn't test past here

# lemmatizer.lemmatize('می‌روم')
# 'رفت#رو'

# tagger = hazm.POSTagger(model='pos_tagger.model')
# tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
# [('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

# spacy_posTagger = SpacyPOSTagger(model_path = 'MODELPATH')
# spacy_posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
# [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

# posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = False)
# posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
# [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')] 

# chunker = Chunker(model='chunker.model')
# tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
# tree2brackets(chunker.parse(tagged))
# '[کتاب خواندن NP] [را POSTP] [دوست داریم VP]'

# spacy_chunker = hazm.SpacyChunker(model_path = 'model_path')
# tree = spacy_chunker.parse(sentence = [('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
# print(tree)


# word_embedding = WordEmbedding(model_type = 'fasttext', model_path = 'word2vec.bin')
# word_embedding.doesnt_match(['سلام' ,'درود' ,'خداحافظ' ,'پنجره'])
# 'پنجره'
# word_embedding.doesnt_match(['ساعت' ,'پلنگ' ,'شیر'])
# 'ساعت'

# parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
# parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))

# spacy_parser = SpacyDependencyParser(tagger=tagger, lemmatizer=lemmatizer)
# spacy_parser.parse_sents([word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟')])

# ner = HazmNER(model_path='ner/model-best')
# ner.predict_entity('حمله سایبری به سامانه سوخت در دولت سیزدهم برای بار دوم اتفاق افتاد، حادثه‌ای که در سال 1400 هم به وقوع پیوست اما رفع این مشکل بیش از یک هفته زمان برد، در حالی که آذر امسال پس از این حمله همه پمپ‌بنزین‌ها در کمتر از 24 ساعت فعالیت خود را از سر گرفتند.')
# ner.predict(
#     [
#       'ریو در ایران توسط شرکت سایپا از سال 1384 تا سال 1391 تولید شد',
#       'به جز ایالات متحده ، این خودرو در اروپا ، آمریکای جنوبی و آسیا هم فروش بالایی داشته است',
#       'این گاه شمار با قدمتی کمتر از دویست سال ، از جدیدترین گاه شمار های رایج به شمار می رود'
#       ]
# )