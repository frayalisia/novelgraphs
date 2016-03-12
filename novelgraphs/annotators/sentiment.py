from .annotator import Annotator
import json
import pandas as pd

def _make_sentiment_column(table):
    with open('./json/senti.json', 'r') as file:
        senti = json.load(file)
    table['Sentiment'] = table.Lemma.apply(senti.get)

class Sentiment(Annotator):

    def annotate(self, text):
        _make_sentiment_column(text.tags)
