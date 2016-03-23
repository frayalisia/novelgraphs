from .annotator import Annotator

quotation_marks = ['"']
left_side_marks = ["``", '«', '„', '“', '‘']
right_side_marks = ["''", '»', '“', '”', '’']


def _ones_to_ids(table):
    cur_id = -1
    prev_tag = None
    for i in table.index:
        cur_tag = table.loc[i, 'QuotationID']
        if cur_tag is None:
            pass
        elif cur_tag == prev_tag:
            table.loc[i, 'QuotationID'] = cur_id
        else:
            cur_id += 1
            table.loc[i, 'QuotationID'] = cur_id
        prev_tag = cur_tag


def _quoted_speech_marks(table):
    '''Find instances of quoted speech, if it starts with left_side_marks
    and ends with right_side_marks, also find double quotes.
    Then add "Speech_mark" into the table'''
    table['QuotationID'] = None
    first, second = None, None

    for i in table.SentenceID.index:
        sent = table[table.SentenceID == i]
        for s in sent.index:
            if sent.loc[s, 'Token'] in left_side_marks:
                first = s
            elif sent.loc[s, 'Token'] in right_side_marks:
                second = s
                table.loc[first:second, 'QuotationID'] = 1
            elif sent.loc[s, 'Token'] in quotation_marks:
                if first is None:
                    first = s
                elif second is None:
                    second = s
                    table.loc[first:second, 'QuotationID'] = 1
                    first, second = None, None

class QuotedSpeech(Annotator):
    def annotate(self, text):
        _quoted_speech_marks(text.tags)
        _ones_to_ids(text.tags)
