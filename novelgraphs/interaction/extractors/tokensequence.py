from .extractor import InteractionExtractor
import json
import os

class TokenSequence(InteractionExtractor):
    def __call__(self, text):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(cur_dir, os.pardir, os.pardir, 'annotators')
        with open(path + '/json/say.json') as file:
            say = json.load(file)

        interactions = []
        table = text.tags
        for i in table.index:
            if table.loc[i, 'CharacterID'] is not None:
                if ((table.loc[i+2, 'CharacterID'] is not None) &
                    ((table.loc[i+1, 'Pos'] in ['VBD', 'VBN', 'VBP']) or
                    (table.loc[i+1, 'Lemma'] in say))):
                    sent_numb = table.loc[i, 'SentenceID']
                    context = slice(table[table.SentenceID == sent_numb].index[0],
                                    table[table.SentenceID == sent_numb].index[-1])
                    characters = tuple(sorted([table.loc[i, 'CharacterID'], table.loc[i+2, 'CharacterID']]))
                    interactions.append([characters, context])
        return interactions
