import os
import subprocess
import pandas as pd
from .annotator import Annotator


def _table_to_list(splitted_sent):
    with open('tokens.txt', 'w') as tokens_file:
        tokens_file.write('\n'.join([' '.join(s) for s in splitted_sent]))


def _corenlp_quote_annotate(corenlp_path, single_quotes, max_length):
    args_single_quotes = ['-quote.singleQuotes'] if single_quotes else []
    args_max_length = (['-quote.maxLength', str(max_length)]
                       if max_length is not None else [])
    path = os.path.dirname(os.path.realpath(__file__))
    with open('quotes.txt', 'w') as quotes_file:
        subprocess.call(['java',
                         '-Xmx2g',
                         '-cp', path + ":" + corenlp_path + "*",
                         'StanfordCoreNlpQuote',
                         '-tokenize.whitespace',
                         '-ssplit.eolonly',
                         '-file', 'tokens.txt'] +
                        args_max_length + args_single_quotes,
                        stdout=quotes_file)


class Quote(Annotator):
    def __init__(self, corenlp_path="./stanford-corenlp-full-2015-12-09/",
                 single_quotes=False, max_length=None):
        Annotator.__init__(self)
        self._corenlp_path = corenlp_path
        self._single_quotes = single_quotes
        self._max_length = max_length

    def annotate(self, text):
        _table_to_list(text.tokens)
        _corenlp_quote_annotate(self._corenlp_path, self._single_quotes,
                                self._max_length)
        quotation_ids = pd.read_csv(
            'quotes.txt', sep='\t', quoting=3,
            header=None, usecols=[1], squeeze=True)
        quotation_ids.replace(['null'], [None], inplace=True)
        text.tags['QuotationID'] = quotation_ids
