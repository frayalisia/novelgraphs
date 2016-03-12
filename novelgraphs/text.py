import pickle
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize


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


class Text(object):
    def __init__(self, raw_text):
        self._raw_text = raw_text
        self.tokens = _split_into_words(self._raw_text)
        self.tags = _index_table(self.tokens)

    def to_pickle(self, filename):
        with open(filename, "wb") as out_file:
            pickle.dump(self, out_file)

    @staticmethod
    def from_pickle(filename):
        with open(filename, "rb") as in_file:
            return pickle.load(in_file)
