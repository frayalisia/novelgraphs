from abc import ABCMeta, abstractmethod


class Annotator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def annotate(self, text):
        pass
