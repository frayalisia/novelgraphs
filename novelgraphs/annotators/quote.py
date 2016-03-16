import os
import subprocess
import pandas as pd
from .annotator import Annotator


def _table_to_list(splitted_sent):
    with open('tokens.txt', 'w') as tokens_file:
        tokens_file.write('\n'.join([' '.join(s) for s in splitted_sent]))


def _corenlp_quote_annotate(corenlp_path):
    path = os.path.dirname(os.path.realpath(__file__))
    with open('quotes.txt', 'w') as quotes_file:
        subprocess.call(['java',
                         '-Xmx2g',
                         '-cp', path + ":" + corenlp_path + "*",
                         'StanfordCoreNlpQuote',
                         'tokens.txt'],
                        stdout=quotes_file)


class Quote(Annotator):
    def __init__(self, corenlp_path="./stanford-corenlp-full-2015-12-09/"):
        Annotator.__init__(self)
        self._corenlp_path = corenlp_path

    def annotate(self, text):
        _table_to_list(text.tokens)
        _corenlp_quote_annotate(self._corenlp_path)
        text.tags['QuotationID'] = pd.read_csv('quotes.txt', sep='\t',
                                               header=None, usecols=[1])[1]
