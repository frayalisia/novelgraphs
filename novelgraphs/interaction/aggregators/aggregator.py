from abc import ABCMeta, abstractmethod


class InteractionAggregator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, interactions, text):
        pass
