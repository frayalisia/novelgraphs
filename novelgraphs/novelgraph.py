import networkx as nx


def _weights2nx(weights, chars):
    return [(chars[pair[0]], chars[pair[1]], weight)
            for pair, weight in weights.items()
            if weight is not None]


class NovelGraph(object):
    def __init__(self, extractor, aggregator, character_weight=None):
        self.extractor = extractor
        self.aggregator = aggregator
        self.character_weight = character_weight

    def __call__(self, text):
        interactions = self.extractor(text)
        weights = self.aggregator(interactions, text)
        nx_weights = _weights2nx(weights, text.characters)
        graph = nx.Graph()
        graph.add_weighted_edges_from(nx_weights)
        node_weights = self._get_node_weights(text)
        self._add_node_weights(node_weights, graph, text)
        return graph

    def _get_node_weights(self, text):
        if self.character_weight is None:
            weights = [1.0] * len(text.characters)
        elif self.character_weight == 'frequency':
            occurencies = text.tags.groupby('NerNpID').CharacterID.first()
            counts = list(occurencies.value_counts().sort_index())
            if text.first_person:
                narrator_id = len(text.characters) - 1
                narrator_count = sum(text.tags.CharacterID == narrator_id)
                counts.append(narrator_count)
            frequencies = counts / sum(counts)
            weights = frequencies
        else:
            raise Exception('Unknown character_weight type')
        return weights

    def _add_node_weights(self, weights, graph, text):
        for char_id, char in enumerate(text.characters):
            if char in graph.nodes():
                graph.node[char]['weight'] = weights[char_id]
