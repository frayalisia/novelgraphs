import pickle


class Text(object):
    def __init__(self, raw_text):
        self._raw_text = raw_text

    def to_pickle(self, filename):
        with open(filename, "wb") as out_file:
            pickle.dump(self, out_file)

    @staticmethod
    def from_pickle(filename):
        with open(filename, "rb") as in_file:
            return pickle.load(in_file)
