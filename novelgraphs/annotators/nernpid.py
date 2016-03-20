from .annotator import Annotator

# зависимость от NER

def _add_nercorenlp_id(text):
    text['NerNpID'] = None
    cur_id = -1
    for s in text.SentenceID.unique():
        sentence = text.loc[text.SentenceID == s]
        prev_tag = None
        for i in sentence.index:
            cur_tag = text.loc[i, 'NER']
            if cur_tag == 'O':
                pass
            elif cur_tag == prev_tag:
                text.loc[i, 'NerNpID'] = cur_id
            else:
                cur_id += 1
                text.loc[i, 'NerNpID'] = cur_id
            prev_tag = cur_tag

def _fix_ner(table):
    bugs = table.Lemma.isin(['(', ')', 'xi', 'viii', 'iii', 'vi', 'ii', '-', '“',
                                '”', '’s', '"', '—', '‘'])
    table.loc[bugs, 'NER'] = 'O'

class NerNpID(Annotator):
    def annotate(self, text):
        _fix_ner(text.tags)
        _add_nercorenlp_id(text.tags)
