from abc import ABCMeta, abstractmethod
from collections import defaultdict
from itertools import combinations
import numpy as np


class InteractionAggregator(object):
    __metaclass__ = ABCMeta

    def __call__(self, interactions, text):
        self._text = text
        pair_weight_list = defaultdict(list)

        for chars, context in interactions:
            cum_weight = self.cumulative_weight(context)
            pair_weight = self.distribute(cum_weight, chars)
            for pair, weight in pair_weight:
                pair_weight_list[pair].append(weight)

        return {pair : self.reduce(weights)
                for pair, weights in pair_weight_list.items()}

    @abstractmethod
    def cumulative_weight(self, context):
        pass

    def distribute(self, cum_weight, characters):
        pairs = list(combinations(sorted(characters), 2))
        weight = cum_weight / len(pairs)
        return [[pair, weight] for pair in pairs]

    def reduce(self, weights):
        return np.mean(weights)
