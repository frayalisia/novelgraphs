from .annotator import Annotator


class Pipeline(Annotator):
    def __init__(self, annotators):
        Annotator.__init__(self)
        self._annotators = list(annotators)

    def annotate(self, text):
        for ann in self._annotators:
            ann.annotate(text)
