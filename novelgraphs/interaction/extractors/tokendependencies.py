from .extractor import InteractionExtractor
import json
import os

class TokenDependencies(InteractionExtractor):
    def __call__(self, text):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(cur_dir, os.pardir, os.pardir, 'annotators')
        with open(path + '/json/say.json') as file:
            say = json.load(file)

        interactions = []
        table = text.tags
        for _, sentence in table.groupby('SentenceID'):
            for i in sentence.index:
                if (sentence.loc[i, 'Pos'] in ['VBD', 'VBN', 'VBP'] or sentence.loc[i, 'Lemma'] in say):
                    left = sentence.loc[:i-1]
                    left_el = left[sentence.CharacterID.notnull()].index
                    right = sentence.loc[i:]
                    right_el = right[sentence.CharacterID.notnull()].index
                    for e in left_el:
                        if sentence.loc[e, 'DepParse'] == sentence.loc[i, 'TokenID']:
                            for r in right_el:
                                if sentence.loc[r, 'DepParse'] == sentence.loc[i, 'TokenID']:
                                    characters = tuple(sorted(set([sentence.loc[e, 'CharacterID'], sentence.loc[r, 'CharacterID']])))
                                    context = slice(sentence.index[0], sentence.index[-1])
                                    interactions.append([characters, context])
        return interactions
