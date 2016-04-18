import pandas as pd

from .aggregator import InteractionAggregator


class Sentiment(InteractionAggregator):
    def cumulative_weight(self, context):
        return self._text.tags.loc[context, 'Sentiment'].mean()

    def reduce(self, weights):
        mean = pd.Series(weights).mean()
        return mean if not pd.isnull(mean) else None
