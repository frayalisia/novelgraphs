from .aggregator import InteractionAggregator


class Sentiment(InteractionAggregator):
    def cumulative_weight(self, context):
        return self._text.tags.loc[context, 'Sentiment'].mean()
