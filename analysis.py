import nltk
import os
import pandas as pd

# TODO: make an output file for anything that we do
# TODO: figure out a stopwords file
# TODO: try out word embeddings for these text


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
                print('look it worked!')
            except:
                print('look an error!')
                print(fn)
        
        self.poem_lengths_in_tokens = [len(poem.raw_tokens) for poem in self.poems]
        self.all_tokens = [poem.raw_tokens for poem in self.poems]
        self.all_tokens = [item for sublist in self.all_tokens for item in sublist]
        self.corpus_fq = nltk.FreqDist(self.all_tokens)

        # self.poems = [Poem(fn, self.metadata) for fn in self.filenames]

    def write_output(self, to_write):
        """Write the results to a file so Amna can read it"""
        #terminal is always LTR. so, keep a sep output file as endpoint
        with open('output.txt', 'w') as outfile:
            outfile.write(str(to_write))

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
        with open('pun_stopwords.txt', 'r') as fin:
            self.stopwords = [line.strip() for line in fin.readlines()]
            # TODO: remove diacritical markings
        additions = ['آؤ'] 
        self.stopwords.extend(additions)
        self.stop_removed_tokens = [word for word in self.lower_tokens if word not in self.stopwords]

    def get_text(self):
        with open(self.relative_filename, 'r') as file_in:
            raw_text = file_in.read()
        return raw_text

def main():
    #This is all the stuff that will run if you type $ python analysis.py
    our_corpus = Corpus('corpus/')

    # poem_1 = Poem("corpus/poem1-ao-sayyo.txt",)
    # poem_2 = Poem("corpus/poem2-ik-nuqte.txt",)

    print('hello! this is the terminal version!')

    for poem in our_corpus.poems:
        print(poem.raw_tokens[0:9])
        print('=======')


# this allows you to import the classes as a module. it uses the special built-in variable __name__ set to the value "__main__" if the module is being run as the main program
if __name__ == "__main__":
    main()

# to work in the interpreter
# python
# >>> import analysis
# >>> our_corpus = analysis.Corpus('corpus/')
# >>> our_corpus.poems

# if something changes in the analysis file, save the file, then
# turn on terminal
# cd to right folder
# pipenv shell
# python3
# >>> import importlib
# >>> importlib.reload(analysis)
# >>> our_corpus = analysis.Corpus('corpus/')
