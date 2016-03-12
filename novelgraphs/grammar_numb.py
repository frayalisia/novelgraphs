from annotator import Annotator
import json

def _get_singular_or_plural(token):
    with open('./json/sg.json', 'r') as file:
        sg = json.load(file)
    with open('./json/pl.json', 'r') as file:
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
