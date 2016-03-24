import os
import subprocess
import pandas as pd
from .annotator import Annotator


quotation_marks = ['"']
left_side_marks = ["``", '«', '„', '“', '‘']
right_side_marks = ["''", '»', '“', '”', '’']


def _ones_to_ids(table):
    cur_id = -1
    prev_tag = None
    for i in table.index:
        cur_tag = table.loc[i, 'QuotationID']
        if cur_tag is None:
            pass
        elif cur_tag == prev_tag:
            table.loc[i, 'QuotationID'] = cur_id
        else:
            cur_id += 1
            table.loc[i, 'QuotationID'] = cur_id
        prev_tag = cur_tag


def _quote_annotate(table):
    '''Find instances of quoted speech, if it starts with left_side_marks
    and ends with right_side_marks, also find double quotes.
    Then add "Speech_mark" into the table'''
    table['QuotationID'] = None
    first, second = None, None

    for s in table.index[table.Token.isin(quotation_marks + left_side_marks +
                                          right_side_marks)]:
        if table.loc[s, 'Token'] in left_side_marks:
            first = s
        elif table.loc[s, 'Token'] in right_side_marks:
            second = s
            table.loc[first:second, 'QuotationID'] = 1
        elif table.loc[s, 'Token'] in quotation_marks:
            if first is None:
                first = s
            elif second is None:
                second = s
                table.loc[first:second, 'QuotationID'] = 1
                first, second = None, None

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
                 corenlp=False, single_quotes=False, max_length=None):
        Annotator.__init__(self)
        self._corenlp_path = corenlp_path
        self._corenlp = corenlp
        self._single_quotes = single_quotes
        self._max_length = max_length

    def annotate(self, text):
        if self._corenlp:
            _table_to_list(text.tokens)
            _corenlp_quote_annotate(self._corenlp_path, self._single_quotes,
                                    self._max_length)
            quotation_ids = pd.read_csv(
                'quotes.txt', sep='\t', quoting=3,
                header=None, usecols=[1], squeeze=True)
            quotation_ids.replace(['null'], [None], inplace=True)
            text.tags['QuotationID'] = quotation_ids
        else:
            _quote_annotate(text.tags)
            _ones_to_ids(text.tags)
