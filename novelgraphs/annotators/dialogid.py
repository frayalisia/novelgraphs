from .annotator import Annotator

def _get_dialogies(table):
    sentences_with_speakers = list(set(table.loc[table.Dialog == 1, 'SentenceID']))

    dialogues = [[sentences_with_speakers[0], None]]
    for i in range(1, len(sentences_with_speakers)):
        if sentences_with_speakers[i]-sentences_with_speakers[i-1] <= 3:
            dialogues[-1][1] = sentences_with_speakers[i]
        else:
            dialogues.append([sentences_with_speakers[i], None])
    return dialogues

def _make_dialog_ids(table):
    table['DialogID'] = None
    dialogues = _get_dialogies(table)

    for id, dialog in enumerate(dialogues):
        if dialog[1] is not None:
            start = table[table.SentenceID == dialog[0]].index[0]
            end = table[table.SentenceID == dialog[1]].index[-1]
            table.loc[start:end, 'DialogID'] = id
        else:
            continue

class DialogID(Annotator):
    def annotate(self, text):
        _make_dialog_ids(text.tags)
