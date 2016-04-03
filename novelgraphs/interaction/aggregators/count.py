import numpy as np
from .aggregator import InteractionAggregator


class Count(InteractionAggregator):
    def cumulative_weight(self, context):
        return 1.0

    def reduce(self, weights):
        return np.sum(weights)
