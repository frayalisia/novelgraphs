from .annotator import Annotator
import json
import os

def _count_first_person(table):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/json/say.json', 'r') as file:
        say = json.load(file)
    h3 = []
    h4 = []
    for s in table.index:
        if (table.Token.loc[s] == 'I' and table.Pos.loc[s] == 'PRP'):
            if (s+1 <= table.index.max() and (table.Lemma.loc[s+1] in say) and (table.loc[s+1, 'Pos'] in ['VBN', 'VBD'])):
                if table.DepParse.loc[s] == table.TokenID.loc[s+1]:
                    h3.append(table.Lemma.loc[s])
            elif (s-1 >= 0 and (table.Lemma.loc[s-1] in say) and (table.loc[s+1, 'Pos'] in ['VBN', 'VBD'])):
                if table.DepParse.loc[s] == table.TokenID.loc[s-1]:
                    h3.append(table.Lemma.loc[s])

    for s in table[table.Dialog != 1].index:
        if (table.Token.loc[s] == 'I' and table.Pos.loc[s] == 'PRP'):
            h4.append(table.Lemma.loc[s])

    print('Speaking I: ' + str(len(h3)))
    print('Like an ProNoun: ' + str(sum((table.Token == 'I') & (table.Pos == 'PRP'))))
    print('I without context: ' + str(len(h4)))
    print('Speaking I / I like PRP: ' + str((len(h3)) / (sum((table.Token == 'I') & (table.Pos == 'PRP')))))
    print('I without context / I like PRP: ' + str(len(h4)/(sum((table.Token == 'I') & (table.Pos == 'PRP')))))


class First_person(Annotator):
    def annotate(self, text):
        _count_first_person(text.tags)
