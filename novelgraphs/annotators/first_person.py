from .annotator import Annotator
import json
import os

def _count_first_person(table):
    h4 = []
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/json/say.json', 'r') as file:
        say = json.load(file)

    for s in table[table.Dialog != 1].index:
        if (table.Token.loc[s] == 'I' and table.Pos.loc[s] == 'PRP'):
            h4.append(table.Lemma.loc[s])

    if len(h4) / (sum((table.Token == 'I') & (table.Pos == 'PRP'))) < 0.3:
        return True

class FirstPerson(Annotator):
    def annotate(self, text):
        text.first_person = _count_first_person(text.tags)
