from collections import defaultdict, Counter
import networkx as nx
from .annotator import Annotator


def _flatten(list_of_lists):
    return [elem for inner_list in list_of_lists for elem in inner_list]


def _get_np_groups(tags):
    condition = (~tags.NerNpID.isnull()) & (tags.NER == 'PERSON')
    return tags.loc[condition].groupby('NerNpID').Lemma


def _get_name_phrases(np_groups):
    return list(set(tuple(group.values) for _, group in np_groups))


def _build_graph(compound_name_phrases):
    compound_nps_dict = defaultdict(set)
    for np in compound_name_phrases:
        lemmas = set(np)
        for lemma in lemmas:
            compound_nps_dict[lemma].update(lemmas - {lemma})
    return nx.Graph(compound_nps_dict)


def _find_character_cliques(name_phrases):
    simple_nps = [np for np in name_phrases if len(np) == 1]
    compound_nps = [np for np in name_phrases if len(np) > 1]

    compound_nps_graph = _build_graph(compound_nps)
    cliques = list(nx.find_cliques(compound_nps_graph))

    clique_lemmas = set(_flatten(cliques))
    cliques += [list(np) for np in simple_nps if np[0] not in clique_lemmas]
    return cliques


def _lemma_to_nps_dict(name_phrases):
    lemma_to_nps = defaultdict(set)
    for np in name_phrases:
        for lemma in np:
            lemma_to_nps[lemma].add(np)
    return dict(lemma_to_nps)


def _find_unique_lemmas(cliques):
    clique_counts = Counter(_flatten(cliques))
    return {lemma for lemma, counts in clique_counts.items() if counts == 1}


def _short_representations(cliques, name_phrases):
    lemma_to_nps = _lemma_to_nps_dict(name_phrases)
    unambiguous_lemmas = _find_unique_lemmas(cliques)
    
    short_repr = [None] * len(cliques)
    for clique_id, clique in enumerate(cliques):
        representations = set()
        for lemma in set(clique) & unambiguous_lemmas:
            for np in lemma_to_nps[lemma]:
                representations.add(np)
        if not representations:
            possible_nps = [lemma_to_nps[lemma] for lemma in set(clique)]
            representations = set.intersection(*possible_nps)
        short_repr[clique_id] = min(representations, key=len)
    return short_repr


def _lemma_to_clique_ids_dict(cliques):
    lemma_to_clique_ids = defaultdict(set)
    for clique_id, clique in enumerate(cliques):
        for lemma in clique:
            lemma_to_clique_ids[lemma].add(clique_id)
    return dict(lemma_to_clique_ids)


def _np_to_clique_ids_dict(name_phrases, cliques):
    lemma_to_clique_ids = _lemma_to_clique_ids_dict(cliques)

    def get_clique_ids(name_phrase):
        possible_cliques = [lemma_to_clique_ids[lemma] for lemma in name_phrase]
        return set.intersection(*possible_cliques)

    return {np : get_clique_ids(np) for np in name_phrases}


def _ambiguous_nps_in_clique_dict(np_to_clique_ids):
    ambiguous_nps_in_clique = defaultdict(set)
    for np, clique_ids in np_to_clique_ids.items():
        if len(clique_ids) > 1:
            for clique_id in clique_ids:
                ambiguous_nps_in_clique[clique_id].add(np)
    return dict(ambiguous_nps_in_clique)


def _add_character_ids(tags, np_groups, name_phrases, cliques):
    tags['CharacterID'] = None

    np_to_clique_ids = _np_to_clique_ids_dict(name_phrases, cliques)
    ambiguous_nps_in_clique = _ambiguous_nps_in_clique_dict(np_to_clique_ids)
    ambiguous_nps = {}
    if ambiguous_nps_in_clique:
        ambiguous_nps = set.union(*ambiguous_nps_in_clique.values())
    last = defaultdict(int)
    for _, group in np_groups:
        name_phrase = tuple(group.values)
        # TODO: remove assert statement
        assert (name_phrase not in ambiguous_nps) == (len(np_to_clique_ids[name_phrase]) == 1)
        if name_phrase in ambiguous_nps:
            clique_id = last[name_phrase]
        else:
            # Idiom to assign the only element of
            # np_to_clique_ids[name_phrase] set to clique_id.
            (clique_id,) = np_to_clique_ids[name_phrase]
            for np in ambiguous_nps_in_clique.get(clique_id, []):
                last[np] = clique_id
        tags.loc[list(group.index), 'CharacterID'] = clique_id


class Character(Annotator):
    def annotate(self, text):
        np_groups = _get_np_groups(text.tags)
        name_phrases = _get_name_phrases(np_groups)
        character_cliques = _find_character_cliques(name_phrases)
        text.characters = _short_representations(character_cliques, name_phrases)
        _add_character_ids(text.tags, np_groups, name_phrases, character_cliques)
