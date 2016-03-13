import pickle
from novelgraphs.annotators import Tokenizer


class Text(object):
    def __init__(self, raw_text, tokenizer='corenlp',
                 corenlp_path="./stanford-corenlp-full-2015-12-09/"):
        self._raw_text = raw_text
        if tokenizer is not None:
            Tokenizer(backend=tokenizer,
                      corenlp_path=corenlp_path).annotate(self)

    def to_pickle(self, filename):
        with open(filename, "wb") as out_file:
            pickle.dump(self, out_file)

    @staticmethod
    def from_pickle(filename):
        with open(filename, "rb") as in_file:
            return pickle.load(in_file)
