from .annotator import Annotator
import json
import pandas as pd
import os

def _make_sentiment_column(table):
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + '/json/senti.json', 'r') as file:
        senti = json.load(file)
    table['Sentiment'] = table.Lemma.apply(senti.get)

class Sentiment(Annotator):

    def annotate(self, text):
        _make_sentiment_column(text.tags)
