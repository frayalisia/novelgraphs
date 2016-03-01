from annotator import Annotator
import json

def _make_animacy_mark(table):
    with open('./json/animacy.json', 'r') as file:
        animacy = json.load(file)
    table['Animacy'] = table.Lemma.apply(lambda x: True if x in animacy else None)

def _make_gender_mark(token):
    with open('./json/male.json', 'r') as file:
        male = json.load(file)
    with open('./json/female.json', 'r') as file:
        female = json.load(file)

    if token in male:
        return 'Male'
    elif token in female:
        return 'Female'
    else:
        return None

def _get_gender(table):
    table['Gender'] = table.Lemma.apply(_make_gender_mark)

class AnimGender(Annotator):

    def annotate(self, text):
        _make_animacy_mark(text.tags)
        _get_gender(text.tags)
