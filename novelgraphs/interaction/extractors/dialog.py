from .extractor import InteractionExtractor

class Dialog(InteractionExtractor):
    def __call__(self, text):
        interactions = []
        for _, group in text.tags.groupby('DialogID'):
            characters = tuple(sorted(set(group.CharacterID) - {None}))
            if len(characters) >= 2:
                start = group.index[0]
                end = group.index[-1]
                context = slice(start, end)
                interactions.append([characters, context])
        return interactions
