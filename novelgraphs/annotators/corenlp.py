import json
import subprocess
import pandas as pd
from .annotator import Annotator


def _table_to_list(splitted_sent):
    with open('tokens.txt', 'w') as tokens_file:
        tokens_file.write('\n'.join([' '.join(s) for s in splitted_sent]))

def _corenlp_json(corenlp_path):
    with open('tokenstaggexs.txt', 'w') as tagged_tokens_file:
        subprocess.call(['java',
                         '-Xmx2g',
                         '-cp', corenlp_path + "*",
                         'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                         '-annotators',
                         'tokenize,ssplit,pos,lemma,ner,depparse,quote',
                         '-tokenize.whitespace',
                         '-ssplit.eolonly',
                         '-file', 'tokens.txt',
    #                      '-parse.originalDependencies',
                         '-outputFormat', 'json'],
                        stdout=tagged_tokens_file, stderr=tagged_tokens_file)


def _parse_json(table):
    with open('tokens.txt.json') as file:
        text = json.load(file)
    list_columns = ['Lemma', 'Pos', 'NER', 'DepParse', 'DepRel']
    for column in list_columns:
        table[column] = None
    sent_tok_index = pd.MultiIndex.from_arrays([table.SentenceID, table.TokenID])
    for sentence in text['sentences']:
#         print(sentence['index'])
        sentence_id = sentence['index']
        for token in sentence['tokens']:
            token_id = token['index'] - 1
            location = sent_tok_index.get_loc((sentence_id, token_id))
            lemma = token['lemma']
            table.loc[location, 'Lemma'] = lemma
            ner = token['ner']
            table.loc[location, 'NER'] = ner
            pos = token['pos']
            table.loc[location, 'Pos'] = pos
#             speaker = token.get('speaker')
#             table.loc[tok & sent, 'Speaker'] = speaker
        for token in sentence['collapsed-ccprocessed-dependencies']:
            token_id = token['dependent'] - 1
            location= sent_tok_index.get_loc((sentence_id, token_id))
            table.loc[location, 'DepParse'] = token['governor']-1
            table.loc[location, 'DepRel'] = token['dep']

class CoreNLP(Annotator):
    def __init__(self, corenlp_path="./stanford-corenlp-full-2015-12-09/"):
        Annotator.__init__(self)
        self._corenlp_path = corenlp_path

    def annotate(self, text):
        _table_to_list(text.tokens)
        _corenlp_json(self._corenlp_path)
        _parse_json(text.tags)
