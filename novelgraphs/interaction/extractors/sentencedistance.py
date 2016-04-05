from .extractor import InteractionExtractor


class SentenceDistance(InteractionExtractor):
    def __init__(self, distance=2):
        InteractionExtractor.__init__(self)
        self.distance = distance

    def __call__(self, text):
        table = text.tags
        indexes = table[table.CharacterID.notnull()].index
        interactions = []
        for i, number in enumerate(indexes):
            if (i + 1 < len(indexes) and table.loc[indexes[i + 1], 'SentenceID'] - table.loc[indexes[i], 'SentenceID'] <= self.distance):
                if table.loc[number, 'CharacterID'] != table.loc[indexes[i+1], 'CharacterID']:
                    characters = tuple(sorted(set([table.loc[number, 'CharacterID'], table.loc[indexes[i+1], 'CharacterID']])))
                    sent_numb_start = table.loc[indexes[i], 'SentenceID']
                    start = table[table.SentenceID == sent_numb_start].index[0]
                    sent_numb_end = table.loc[indexes[i + 1], 'SentenceID']
                    end = table[table.SentenceID == sent_numb_end].index[-1]
                    context = slice(start, end)
                    interactions.append([characters, context])
        return interactions
