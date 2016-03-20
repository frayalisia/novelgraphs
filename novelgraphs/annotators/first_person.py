from .annotator import Annotator

I_RATIO_THRESHOLD = 0.4

def _count_first_person(table):
    withoutcontext = sum((table.Dialog != 1) & (table.Token == 'I') & (table.Pos == 'PRP'))
    total = sum((table.Token == 'I') & (table.Pos == 'PRP'))
    return withoutcontext / total > I_RATIO_THRESHOLD

class FirstPerson(Annotator):
    def annotate(self, text):
        text.first_person = _count_first_person(text.tags)
