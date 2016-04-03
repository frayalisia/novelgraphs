import networkx as nx


def _weights2nx(weights, chars):
    return [(chars[pair[0]], chars[pair[1]], weight)
            for pair, weight in weights.items()]


class NovelGraph(object):
    def __init__(self, extractor, aggregator):
        self.extractor = extractor
        self.aggregator = aggregator

    def __call__(self, text):
        interactions = self.extractor(text)
        weights = self.aggregator(interactions, text)
        nx_weights = _weights2nx(weights, text.characters)
        graph = nx.Graph()
        graph.add_weighted_edges_from(nx_weights)
        return graph
