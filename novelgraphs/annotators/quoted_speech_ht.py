dfrom .annotator import Annotator

quotation_marks = ["``", '«', '„', '“', '‘', '"', "'", "''", '»', '“', '”', '’', '—']
right_side_marks = ["``", '«', '„', '“', '‘']
left_side_marks = ["''", '»', '“', '”', '’']

def _qspeech(token):
    '''Checking the instances of speech'''
    if token in quotation_marks:
        return True
    else:
        return False

def _qspeech_ht(token):
    '''Marking heads and tails in speech'''
    if token in left_side_marks:
        return "TAIL"
    elif token in right_side_marks:
        return "HEAD"
    else:
        return None

def _add_speech_marks(table):
    table['Qspeech'] = table.Token.apply(_qspeech)
    table['QspeechHT'] = table.Token.apply(_qspeech_ht)


class Quoted_Speech_ht(Annotator):
    def annotate(self, text):
        _add_speech_marks(text.tags)
