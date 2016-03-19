from .annotator import Annotator
import json
import os

def _get_singular_or_plural(token):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/json/sg.json', 'r') as file:
        sg = json.load(file)
    with open(path + '/json/pl.json', 'r') as file:
        pl = json.load(file)

    if token in sg:
        return 'sg'
    elif token in pl:
        return 'pl'
    else:
        return None

def _get_grammatical_numb(table):
    table['Grammatical_number'] = table.Lemma.apply(_get_singular_or_plural)

class Grammatical_number(Annotator):
    def annotate(self, text):
        _get_grammatical_numb(text.tags)
