import nltk
import os
import pandas as pd

class Corpus(object):
    def __init__(self, corpus_folder):
        self.corpus_dir = corpus_folder
        self.filenames = self.all_files()
        # read in metadata file
        self.metadata = pd.read_csv('bs-metadata.csv')
        
        self.poems = []
        for fn in self.filenames:
            print('======')
            print(fn)
            try:
                self.poems.append(Poem(fn, self.metadata))
            except:
                print(fn)

        # self.poems = [Poem(fn, self.metadata) for fn in self.filenames]

    def all_files(self):
        """given a directory, return the filenames in it"""
        texts = []
        for (root, _, files) in os.walk(self.corpus_dir):
            for fn in files:
                if fn[0] == '.': # ignore dot files
                    pass
                else:
                    path = os.path.join(root, fn)
                    texts.append(path)
        return texts

class Poem(object):
    def __init__(self, fn, metadata):
        self.relative_filename = fn
        print(self.relative_filename[7:])
        # self.poem_metadata = metadata.loc[metadata['filename'] == self.fn]
        self.poem_metadata = metadata.loc[metadata['filename'] == self.relative_filename[7:]]
        print(self.poem_metadata)
        for item in self.poem_metadata:
            setattr(self, item, self.poem_metadata[item].iloc[0])
        self.raw_text = self.get_text()
        self.raw_tokens = nltk.word_tokenize(self.raw_text)
        # TODO: not lowercasing, so do we need this?
        self.lower_tokens = [word.lower() for word in self.raw_tokens]
        # TODO: find better stopwords list
        with open('ur_stopwords.txt', 'r') as fin:
            self.stopwords = [line.strip() for line in fin.readlines()]
            # TODO: remove diacritical markings
        additions = ['آؤ'] 
        self.stopwords.extend(additions)
        self.stop_removed_tokens = [word for word in self.lower_tokens if word not in self.stopwords]

    def get_text(self):
        with open(self.relative_filename, 'r') as file_in:
            raw_text = file_in.read()
        return raw_text

our_corpus = Corpus('corpus/')

# poem_1 = Poem("corpus/poem1-ao-sayyo.txt",)
# poem_2 = Poem("corpus/poem2-ik-nuqte.txt",)

for poem in our_corpus.poems:
    print(poem.raw_tokens[0:9])
    print('=======')

# print(poem_1.stop_removed_tokens)
# print('=========')
# print(poem_2.stop_removed_tokens)
# print('=========')
# print(poem_2.stopwords)
# print(our_corpus.poems)

# print(test_object.upper_name)
# print(test_object_2.name)