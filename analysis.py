import nltk
import os
import pandas as pd
from collections import defaultdict
from Punjabi_Stemmer import PunjabiStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from bidi.algorithm import get_display
import arabic_reshaper




# TODO: try out word embeddings for these text
# TODO: lemmatize the texts


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
            self.poems.append(Poem(fn, self.metadata))

        self.poem_lengths_in_lines = [(poem.name,len(poem.flat_lines)) for poem in self.poems]
        # TODO: order the poems in some way
        self.poem_lengths_in_tokens = [len(poem.raw_tokens) for poem in self.poems]
        self.all_tokens = [poem.raw_tokens for poem in self.poems]
        self.stemmed_tokens = [poem.stemmed_tokens for poem in self.poems]
        self.all_tokens = [item for sublist in self.all_tokens for item in sublist]
        self.stemmed_tokens =  [item for sublist in self.stemmed_tokens for item in sublist]
        self.narrative_voices = [(poem.name, poem.narrative_voice) for poem in self.poems]
        self.nltk_corpus = nltk.Text(self.all_tokens)
        self.fq = nltk.FreqDist(self.all_tokens)
        self.stemmed_fq = nltk.FreqDist(self.stemmed_tokens)
        # read out all hapaxes for the corpus
        self.hapaxes = self.fq.hapaxes()
    
    def count_occurrences_by_poem(self,query):
        """give a word to query across the whole set of poems and return a list of all those word counts"""
        return [poem.fq[query] for poem in self.poems]

    def divide_corpus_by_length(self,length_limit):
        self.raw_corpus_subset = {'greater_than_' + str(length_limit) + '_lines': [], 'less_than_' + str(length_limit) + '_lines': []}
        for poem in self.poems:
            if poem.num_total_lines >= length_limit:
                self.raw_corpus_subset['greater_than_' + str(length_limit) + '_lines'].append(poem)
            else:
                self.raw_corpus_subset['less_than_' + str(length_limit) + '_lines'].append(poem)
        self.corpus_subset = {}
        for key in self.raw_corpus_subset.keys():
            self.corpus_subset[key] = Subset(self.raw_corpus_subset[key])
        self.corpus_subset_as_list = [Subset(self.raw_corpus_subset[key]) for key in self.raw_corpus_subset.keys()]
        self.query = length_limit

    def divide_corpus_by_metadata_query(self,query):
        """example usage:
        corpus.divide_corpus_by_metadata_query('narrative_voice')
        will create a new corpus attribute called corpus.corpus_subsets that divides the corpus into subsets based on your query
        """
        subsets = defaultdict(list)
        for poem in self.poems:
            value = getattr(poem, query)
            subsets[value].append(poem)

        self.raw_corpus_subset = dict(subsets)
        self.corpus_subset = {}
        for key in self.raw_corpus_subset.keys():
            self.corpus_subset[key] = Subset(self.raw_corpus_subset[key])
        self.corpus_subset_as_list = [Subset(self.raw_corpus_subset[key]) for key in self.raw_corpus_subset.keys()]
        self.query = query
    
    def count_word_by_subset(self, query):
        for key in self.corpus_subset.keys():
            print('=====')
            print(key)
            print(self.corpus_subset[key].fq[query])

    def concordance(self,token):
        for poem in self.poems:
            print(poem.name)
            poem.nltk_poem.concordance(token)
            print('======')

    def write_output(self, to_write):
        """Write the results to a file so Amna can read it"""
        #terminal is always LTR. so, keep a sep output file as endpoint
        with open('output.txt', 'w') as outfile:
            outfile.write(str(to_write))
        print('complete')

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

    def cluster(self):
        vectorizer = TfidfVectorizer()
        docs = [poem.raw_text for poem in self.poems]
        labels = [poem.name for poem in self.poems]
        tfidf_matrix = vectorizer.fit_transform(docs)
        X = vectorizer.fit_transform(docs)
        print(tfidf_matrix.toarray())
        similarity_matrix = cosine_similarity(tfidf_matrix)
        print(similarity_matrix)

        num_clusters = 4
        kmeans_model = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        clusters = kmeans_model.fit_predict(tfidf_matrix)

        print(clusters)

        X = X.toarray()
        # sns.scatterplot(x=X[:,0], y=X[:,5], hue=clusters, palette='rainbow')
        # plt.show()
        pca=PCA(n_components=2)
        reduced_X=pd.DataFrame(data=pca.fit_transform(X),columns=['PCA1','PCA2'])
        print(reduced_X.head())
        centers=pca.transform(kmeans_model.cluster_centers_)
        plt.figure(figsize=(7,5))
        # Scatter plot
        plt.scatter(reduced_X['PCA1'],reduced_X['PCA2'],c=kmeans_model.labels_)
        # plt.scatter(centers[:,0],centers[:,1],marker='x',s=100,c='red')
        for i,txt in enumerate(labels):
            plt.annotate(txt, (reduced_X['PCA1'][i], reduced_X['PCA2'][i]))
        plt.xlabel('PCA1')
        plt.ylabel('PCA2')
        plt.title('Poetry Cluster')
        plt.tight_layout()
        plt.show()

    def basic_graph(self,token_query):

        """graph a word count. assumes you have previously run a divide function to generate corpus subsets"""
        if hasattr(self, 'corpus_subset'):
            fig, ax = plt.subplots()

            metadata_keys = self.corpus_subset.keys()
            metadata_values = []
            for subset in self.corpus_subset_as_list:
                metadata_values.append(subset.fq[token_query])

            ax.bar(metadata_keys, metadata_values)

            # if we wanted colors
            # bar_labels = ['red', 'blue', '_red', 'orange']
            # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

            # ax.bar(metadata_keys, metadata_values, label=bar_labels[:len(metadata_keys)], color=bar_colors[:len(metadata_keys)])

            ax.set_ylabel("Counts")
            if type(self.query) == int:
                ax.set_xlabel("Corpus subdivided by token limit " + str(self.query))
            else:
                ax.set_xlabel("Corpus subdivided by " + self.query)
            ax.set_title('Counts of token ' + self.reshape_on_the_fly(token_query))
            # ax.legend(title='Counts of token' + token_query)

            plt.rcParams['font.family'] = 'Arial'
            plt.show()
        else:
            fig, ax = plt.subplots()

            poem_names = [self.reshape_on_the_fly(poem.name) for poem in self.poems]
            poem_counts = [poem.fq[token_query] for poem in self.poems]

            ax.bar(poem_names, poem_counts)

            # if we wanted colors
            # bar_labels = ['red', 'blue', '_red', 'orange']
            # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

            # ax.bar(metadata_keys, metadata_values, label=bar_labels[:len(metadata_keys)], color=bar_colors[:len(metadata_keys)])

            ax.set_ylabel("Counts")
            ax.set_xlabel("Poem name")
            ax.set_title('Counts of token ' + self.reshape_on_the_fly(token_query))
            # ax.legend(title='Counts of token' + token_query)
            plt.rcParams['font.family'] = 'Arial'
            plt.show()

    def reshape_on_the_fly(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        artext = get_display(reshaped_text)
        return artext

    def most_common_graph(self):
        """graph most common tokens"""
        if hasattr(self, 'corpus_subset'):
            fig, axs = plt.subplots(len(self.corpus_subset_as_list),sharey=True)
            fig.suptitle('Ten Most Common Tokens in Corpus Subdivided by ' + str(self.query))
            for index, subset in enumerate(self.corpus_subset_as_list):
                most_common_raw = subset.fq.most_common(10)
                most_common_tokens = [self.reshape_on_the_fly(token[0]) for token in most_common_raw]
                most_common_counts = [token[1] for token in most_common_raw]
                axs[index].bar(most_common_tokens, most_common_counts)
                axs[index].set_title(list(self.corpus_subset.keys())[index])
            fig.tight_layout()
            plt.rcParams['font.family'] = 'Arial'
            plt.show()
        else:
            fig, ax = plt.subplots()

            most_common_raw = self.fq.most_common(10)
            most_common_tokens = [self.reshape_on_the_fly(token[0]) for token in most_common_raw]
            most_common_counts = [token[1] for token in most_common_raw]

            ax.bar(most_common_tokens, most_common_counts)

            # if we wanted colors
            # bar_labels = ['red', 'blue', '_red', 'orange']
            # bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

            # ax.bar(metadata_keys, metadata_values, label=bar_labels[:len(metadata_keys)], color=bar_colors[:len(metadata_keys)])

            ax.set_title('Ten Most Common Tokens in Corpus')
            # ax.legend(title='Counts of token' + token_query)
            plt.rcParams['font.family'] = 'Arial'
            plt.show()

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
        self.poem_stanzas = self.raw_text.split('\n\n')
        self.poem_lines_as_stanzas = [stanza.splitlines() for stanza in self.poem_stanzas]
        self.flat_lines = [item for sublist in self.poem_lines_as_stanzas for item in sublist]
        self.raw_tokens = nltk.word_tokenize(self.raw_text)
        # TODO: not lowercasing, so do we need this?
        self.lower_tokens = [word.lower() for word in self.raw_tokens]
        #### stemming ####
        stemmer = PunjabiStemmer()
        self.stemmed_tokens = [stemmer.stem_word(word) for word in self.lower_tokens]
        #### stemming ####
        # TODO: find better stopwords list
        with open('pun_stopwords.txt', 'r') as fin:
            self.stopwords = [line.strip() for line in fin.readlines()]
            # TODO: remove diacritical markings
        additions = ['آؤ'] 
        self.stopwords.extend(additions)
        self.stop_removed_tokens = [word for word in self.lower_tokens if word not in self.stopwords]
        self.nltk_poem = nltk.Text(self.stop_removed_tokens)
        self.fq = nltk.FreqDist(self.stop_removed_tokens)
        # gives number of lines
        self.num_total_lines = len(self.flat_lines)
        # gives number of stanzas
        self.num_stanzas = len(self.poem_lines_as_stanzas)
        # length stats
        self.shortest_line = min(self.flat_lines, key=len)
        self.longest_line = max(self.flat_lines, key=len)
        # total number of tokens divided by total number of lines
        self.average_line_length = len(self.raw_tokens) / len(self.flat_lines)
        # total number of tokens divided by total number of stanzas
        self.average_stanza_length = len(self.raw_tokens) / len(self.poem_lines_as_stanzas)
        # length of each line in poem as a big list
        self.line_lengths_over_poem = [len(nltk.word_tokenize(line)) for line in self.flat_lines]
        # length of each line but preserving stanza structure
        self.line_lengths_preserving_stanzas = [[len(nltk.word_tokenize(line)) for line in stanza] for stanza in self.poem_lines_as_stanzas]

    def get_text(self):
        with open(self.relative_filename, 'r') as file_in:
            raw_text = file_in.read()
        return raw_text

class Subset(object):
    def __init__(self, poems):
        self.poems = poems
        self.poem_lengths_in_lines = [(poem.name,len(poem.flat_lines)) for poem in self.poems]
        # TODO: order the poems in some way
        self.poem_lengths_in_tokens = [len(poem.raw_tokens) for poem in self.poems]
        self.all_tokens = [poem.raw_tokens for poem in self.poems]
        self.all_tokens = [item for sublist in self.all_tokens for item in sublist]
        self.corpus_fq = nltk.FreqDist(self.all_tokens)
        self.narrative_voices = [(poem.name, poem.narrative_voice) for poem in self.poems]
        self.nltk_corpus = nltk.Text(self.all_tokens)
        self.fq = nltk.FreqDist(self.all_tokens)
        # read out all hapaxes for the corpus
        self.hapaxes = self.fq.hapaxes()
    

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

# if something changes in the analysis file, save the file, then ---only if youre in the same instance 
# turn on terminal
# cd to right folder
# pipenv shell
# python3
# >>> import importlib
# >>> importlib.reload(analysis)
# >>> our_corpus = analysis.Corpus('corpus/')
# >>> our_corpus.write_output(SOMETHING TO OUTPUT)
# as in 
# >>> our_corpus.write_output(our_corpus.fq.hapaxes())
# >>> our_corpus.write_output(our_corpus.poems[0])

# >>> our_corpus.corpus_concordance('دھاڑے')

# when using a subset corpus
# our_corpus.divide_corpus_by_length(15)
# our_corpus.corpus_subset['greater_than_15_lines'].narrative_voices
# our_corpus.corpus_subset['less_than_15_lines'].narrative_voices

# our_corpus.divide_corpus_by_metadata_query('narrative_voice')
# our_corpus.corpus_subset['u'].poems

# [poem.fq['میں'] for poem in our_corpus.corpus_subset['u'].poems]
# our_corpus.count_word_by_subset('میں')