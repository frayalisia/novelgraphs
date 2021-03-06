from .extractor import InteractionExtractor


class TokenDistance(InteractionExtractor):
    def __init__(self, distance=15):
        InteractionExtractor.__init__(self)
        self.distance = distance

    def __call__(self, text):
        indexes = text.tags[text.tags.CharacterID.notnull()].index
        interactions = []
        for i, number in enumerate(indexes):
            # print(i, number)
            if i + 1 < len(indexes) and indexes[i + 1] - indexes[i] <= self.distance:
                if text.tags.loc[number, 'CharacterID'] != text.tags.loc[indexes[i+1], 'CharacterID']:
                    characters = tuple(sorted(set([text.tags.loc[number, 'CharacterID'], text.tags.loc[indexes[i+1], 'CharacterID']])))
                    context = slice(number, indexes[i+1])
                    interactions.append([characters, context])
        return interactions
