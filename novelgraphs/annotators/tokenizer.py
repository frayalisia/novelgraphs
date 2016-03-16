import subprocess
import json
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
from .annotator import Annotator


def _tokenize_corenlp(text, corenlp_path):
    with open('text.txt', 'w') as in_file:
        in_file.write(text)
    with open('info.txt', 'w') as info_file:
        subprocess.call(['java',
                         '-Xmx2g',
                         '-cp', corenlp_path + "*",
                         'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                         '-annotators',
                         'tokenize,ssplit',
                         '-file', 'text.txt',
                         '-outputFormat', 'json'],
                        stdout=info_file, stderr=info_file)
    with open('text.txt.json', 'r') as out_file:
        tokenized = json.load(out_file)
    return [[token['originalText'].replace(' ', '')
             for token in sentence['tokens']]
            for sentence in tokenized['sentences']]


def _flatten(list_of_lists):
    return [elem for inner_list in list_of_lists for elem in inner_list]


def _split_into_sentences(text):
    sentence = [i.strip() for i in sent_tokenize(text)]
    new_sentence = [sentence[0]]
    for s in sentence[1:]:
        if s[0].islower():
            new_sentence[-1] += " " + s
        else:
            new_sentence.append(s)
    return new_sentence


def _split_into_words(text):
    sentence = _split_into_sentences(text)
    return [word_tokenize(s) for s in sentence]


def _index_table(split_sent):
    lengths = [len(s) for s in split_sent]
    sentence_id = _flatten([[i] * length for i, length in enumerate(lengths)])
    token_id = _flatten([list(range(length)) for length in lengths])
    tokens = _flatten(split_sent)
    return pd.DataFrame({'SentenceID' : sentence_id, 'TokenID' : token_id, 'Token' : tokens},
                        columns=['SentenceID', 'TokenID', 'Token'])


class Tokenizer(Annotator):
    def __init__(self, backend='corenlp',
                 corenlp_path="./stanford-corenlp-full-2015-12-09/"):
        Annotator.__init__(self)
        self._backend = backend
        self._corenlp_path = corenlp_path

    def annotate(self, text):
        if self._backend == 'corenlp':
            text.tokens = _tokenize_corenlp(text._raw_text, self._corenlp_path)
        elif self._backend == 'nltk':
            text.tokens = _split_into_words(text._raw_text)
        else:
            raise Exception('Unknown tokenizer backend')
        text.tags = _index_table(text.tokens)
