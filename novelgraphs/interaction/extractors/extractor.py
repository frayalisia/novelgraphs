from abc import ABCMeta, abstractmethod


class InteractionExtractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, text):
        pass
