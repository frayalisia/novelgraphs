from .annotator import Annotator

quotation_marks = ['"']
right_side_marks = ["``", '«', '„', '“', '‘']
left_side_marks = ["''", '»', '“', '”', '’']

def _quoted_speech_marks(table):
    '''Find instanses of quoted speech, if it starts with right_side_marks
    and ends with left_side_marks, also find double quotes.
    Then add "Speech_mark" into the table'''
    table['Dialog'] = None
    first, second = None, None

    for i in table.SentenceID.index:
        sent = table[table.SentenceID == i]
        for s in sent.index:
            if sent.loc[s, 'Token'] in right_side_marks:
                first = s
            elif sent.loc[s, 'Token'] in left_side_marks:
                second = s
                table.loc[first:second, 'Dialog'] = 1
            elif sent.loc[s, 'Token'] in quotation_marks:
                if first is None:
                    first = s
                elif second is None:
                    second = s
                    table.loc[first:second, 'Dialog'] = 1
                    first, second = None, None

class Quoted_Speech(Annotator):
    def annotate(self, text):
        _quoted_speech_marks(text.tags)
