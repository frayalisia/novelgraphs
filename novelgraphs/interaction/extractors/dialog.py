from .extractor import InteractionExtractor


class Dialog(InteractionExtractor):
    def __call__(self, text):
        interactions = []
        table = text.tags
        ids = [n for el in [[table[table.QuotationID == i].index[0],
                table[table.QuotationID == i].index[-1]] for i in
                range(table.QuotationID.max())] for n in el]

        dialog_ids = [[0,ids[0]]] + [ids[1:-1][i:i+2] for i in range(0,
                        len(ids[1:-1]), 2)] + [[ids[-1], table.index.max()]]
        dialog_ids = [slice(i[0], i[1]) for i in dialog_ids]

        for context in dialog_ids:
        # print(context)
            if len(set(table[table.CharacterID.notnull()].loc[context, 'CharacterID'])) > 1:
                characters = tuple(sorted(set(table[table.CharacterID.notnull()].loc[context, 'CharacterID'])))
                # print(character)
                interactions.append([characters, context])
        return interactions
