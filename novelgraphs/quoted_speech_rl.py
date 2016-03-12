from annotator import Annotator

right_side_marks = ["``", '«', '„', '“', '‘']
left_side_marks = ["''", '»', '“', '”', '’']

def _quoted_speech_marks(table):
    '''Find instanses of quoted speech, if it starts with right_side_marks
    and ends with left_side_marks. Then add "Speech_mark" into the table'''
    table['Dialog'] = None

    for i in table.SentenceID.index:
        sent = table[table.SentenceID == i]
        for s in sent.index:
            if sent.loc[s, 'Token'] in right_side_marks:
                first = s
            elif sent.loc[s, 'Token'] in left_side_marks:
                second = s
                table.loc[first:second, 'Dialog'] = 'Speech_mark'

class Quoted_Speech_rl(Annotator):
    def annotate(self, text):
        _quoted_speech_marks(text.tags)
