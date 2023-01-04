# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc
from spacy.language import Language

from pathvecs.matchers import TripleMatcher

params = [

##### being verbs with a nominal attr child
({
    'use_patterns': ['being_verb'],
    'description': "Being triples should be formed between the subject and "\
                   "nominal objects (attr) of a being / copular verb.",
    'words': ['California', 'is', 'a', 'state', '.'],
    'lemmas': ['California', 'be', 'a', 'state', '.'],
    'pos': ['PROPN', 'AUX', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'attr', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'be', 3)]
}),
({
    'use_patterns': ['being_verb'],
    'description': "Being triples should be formed for conjoined objects.",
    'words': ['Australia', 'is', 'a', 'country', 'and', 'a', 'continent', '.'],
    'lemmas': ['Australia', 'be', 'a', 'country', 'and', 'a', 'continent', '.'],
    'pos': ['PROPN', 'AUX', 'DET', 'NOUN', 'CCONJ', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'DT', 'NN', 'CC', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'attr', 'cc', 'det', 'conj', 'punct'],
    'heads': [1, 1, 3, 1, 3, 6, 3, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'be', 3),(0, 'be', 6)]
}),
({
    'use_patterns': ['being_verb'],
    'description': "Being triples should be formed for conjoined subjects.",
    'words': ['Europe', 'and', 'Asia', 'are', 'continents', '.'],
    'lemmas': ['Europe', 'and', 'Asia', 'be', 'continent', '.'],
    'pos': ['PROPN', 'CCONJ', 'PROPN', 'AUX', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'CC', 'NNP', 'VBP', 'NNS', '.'],
    'deps': ['nsubj', 'cc', 'conj', 'ROOT', 'attr', 'punct'],
    'heads': [3, 0, 0, 3, 3, 3],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'be', 4),(2, 'be', 4)]
}),

# ##### being verbs with attr child & predicate adjective

# ({
#     'description': "One being + adjective triple should be formed for verbs of "\
#                    "being with predicate adjectives present, rather than "\
#                    "separate being and adjective triples.",
#     'words': ['Alice', 'was', 'the', 'first', 'tester', '.'],
#     'lemmas': ['Alice', 'be', 'the', 'first', 'tester', '.'],
#     'pos': ['PROPN', 'AUX', 'DET', 'ADJ', 'NOUN', 'PUNCT'],
#     'tags': ['NNP', 'VBD', 'DT', 'JJ', 'NN', '.'],
#     'deps': ['nsubj', 'ROOT', 'det', 'amod', 'attr', 'punct'],
#     'heads': [1, 1, 4, 4, 1, 1],
#     'spaces': [' ', ' ', ' ', ' ', '', ''],
#     'gold_triples': [(0, 'be-first', 4)]

# }),

##### transitive verbs in the active voice

({
    'description': "Verb triples should be formed between the subject and "\
                   "object of active voice transitive verbs.",
    'words': ['Alice', 'threw', 'the', 'ball', '.'],
    'lemmas': ['Alice', 'throw', 'the', 'ball', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'throw', 3)]
}),
({
    'description': "One triple should be formed for each conjoined subject.",
    'words': ['Alice', 'and', 'Bob', 'threw', 'the', 'ball', '.'],
    'lemmas': ['Alice', 'and', 'Bob', 'throw', 'the', 'ball', '.'],
    'pos': ['PROPN', 'CCONJ', 'PROPN', 'VERB', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'CC', 'NNP', 'VBD', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'cc', 'conj', 'ROOT', 'det', 'dobj', 'punct'],
    'heads': [3, 0, 0, 3, 5, 3, 3],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'throw', 5),(2, 'throw', 5)]
}),
({
    'description': "One triple should be formed for each conjoined object.",
    'words': ['Alice', 'bought', 'pizza', 'and', 'chips', '.'],
    'lemmas': ['Alice', 'buy', 'pizza', 'and', 'chip', '.'],
    'pos': ['PROPN', 'VERB', 'NOUN', 'CCONJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'NN', 'CC', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'cc', 'conj', 'punct'],
    'heads': [1, 1, 1, 2, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'buy', 4),(0, 'buy', 2)]
}),
({
    'description': "One triple should be formed for each conjoined verb.",
    'words': ['Bob', 'buys', 'and', 'sells', 'lightbulbs', '.'],
    'lemmas': ['Bob', 'buy', 'and', 'sell', 'lightbulb', '.'],
    'pos': ['PROPN', 'VERB', 'CCONJ', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'CC', 'VBZ', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'cc', 'conj', 'dobj', 'punct'],
    'heads': [1, 1, 1, 1, 3, 1],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'buy', 4),(0, 'sell', 4)]
}),
({
    'description': "Seperate triples should be formed for conjoined verbs "\
                   "with distinct objects.",
    'words': ['Alice', 'sold', 'the', 'car', 'and', 'bought', 'a', 'truck', '.'],
    'lemmas': ['Alice', 'sell', 'the', 'car', 'and', 'buy', 'a', 'truck', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'NOUN', 'CCONJ', 'VERB', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'NN', 'CC', 'VBD', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'dobj', 'cc', 'conj', 'det', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1, 1, 7, 5, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'sell', 3), (0, 'buy', 7)],
}),

##### transitive verbs in the passive voice
({
    'description': "Verb triples should be formed between the passive subject "\
                   "and object of passive voice transitive verbs.",
    'words': ['The', 'company', 'was', 'bought', 'by', 'Bob', '.'],
    'lemmas': ['the', 'company', 'be', 'buy', 'by', 'Bob', '.'],
    'pos': ['DET', 'NOUN', 'AUX', 'VERB', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NN', 'VBD', 'VBN', 'IN', 'NNP', '.'],
    'deps': ['det', 'nsubjpass', 'auxpass', 'ROOT', 'agent', 'pobj', 'punct'],
    'heads': [1, 3, 3, 3, 3, 4, 3],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(5, 'buy', 1)]
}),
({
    'description': "One triple should be formed for each conjoined subject.",
    'words': ['The', 'company', 'was', 'bought', 'by', 'Alice', 'and', 'Bob', '.'],
    'lemmas': ['the', 'company', 'be', 'buy', 'by', 'Alice', 'and', 'Bob', '.'],
    'pos': ['DET', 'NOUN', 'AUX', 'VERB', 'ADP', 'PROPN', 'CCONJ', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NN', 'VBD', 'VBN', 'IN', 'NNP', 'CC', 'NNP', '.'],
    'deps': ['det', 'nsubjpass', 'auxpass', 'ROOT', 'agent', 'pobj', 'cc', 'conj', 'punct'],
    'heads': [1, 3, 3, 3, 3, 4, 5, 5, 3],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(5, 'buy', 1),(7, 'buy', 1)]
}),
({
    'description': "One triple should be formed for each conjoined object.",
    'words': ['The', 'company', 'and', 'property', 'were', 'sold', 'by', 'Charlie', '.'],
    'lemmas': ['the', 'company', 'and', 'property', 'be', 'sell', 'by', 'Charlie', '.'],
    'pos': ['DET', 'NOUN', 'CCONJ', 'NOUN', 'AUX', 'VERB', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NN', 'CC', 'NN', 'VBD', 'VBN', 'IN', 'NNP', '.'],
    'deps': ['det', 'nsubjpass', 'cc', 'conj', 'auxpass', 'ROOT', 'agent', 'pobj', 'punct'],
    'heads': [1, 5, 1, 1, 5, 5, 5, 6, 5],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(7, 'sell', 1),(7, 'sell', 3)]
}),
({
    'description': "One triple should be formed for each conjoined verb.",
    'words': ['The', 'company', 'was', 'bought', 'and', 'sold', 'by', 'a', 'fund', '.'],
    'lemmas': ['the', 'company', 'be', 'buy', 'and', 'sell', 'by', 'a', 'fund', '.'],
    'pos': ['DET', 'NOUN', 'AUX', 'VERB', 'CCONJ', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'NN', 'VBD', 'VBN', 'CC', 'VBN', 'IN', 'DT', 'NN', '.'],
    'deps': ['det', 'nsubjpass', 'auxpass', 'ROOT', 'cc', 'conj', 'agent', 'det', 'pobj', 'punct'],
    'heads': [1, 3, 3, 3, 3, 3, 5, 8, 6, 3],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(8, 'buy', 1),(8, 'sell', 1)]
}),

##### intransitive verbs with prepositional objects
({
    'description': "iverb-prep triples should be formed between the subject "\
                   "of intransitive verbs and the prepositional object of "\
                   "child prepositions of those verbs.",
    'words': ['Joe', 'jumped', 'from', 'the', 'chair', '.'],
    'lemmas': ['Joe', 'jump', 'from', 'the', 'chair', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'IN', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 1, 4, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'jump-from', 4)]
}),
({
    'description': "One triple should be formed for each conjoined subject.",
    'words': ['Jack', 'and', 'Jill', 'ran', 'up', 'the', 'hill', '.'],
    'lemmas': ['Jack', 'and', 'Jill', 'run', 'up', 'the', 'hill', '.'],
    'pos': ['PROPN', 'CCONJ', 'PROPN', 'VERB', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'CC', 'NNP', 'VBD', 'IN', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'cc', 'conj', 'ROOT', 'prep', 'det', 'pobj', 'punct'],
    'heads': [3, 0, 0, 3, 3, 6, 4, 3],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'run-up', 6),(2, 'run-up', 6)]
}),
({
    'description': "One triple should be formed for each conjoined object.",
    'words': ['Jack', 'rolled', 'through', 'the', 'grass', 'and', 'the', 'dirt', '.'],
    'lemmas': ['Jack', 'roll', 'through', 'the', 'grass', 'and', 'the', 'dirt', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'DET', 'NOUN', 'CCONJ', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'IN', 'DT', 'NN', 'CC', 'DT', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'pobj', 'cc', 'det', 'conj', 'punct'],
    'heads': [1, 1, 1, 4, 2, 4, 7, 4, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'roll-through', 4),(0, 'roll-through', 7)]
}),

##### prepositions
({
    'use_patterns': ['prep'],
    'description': "prep triples should be formed for standalone NPs with PP "\
                   "modifiers.",
    'words': ['A', 'cup', 'of', 'sugar', '.'],
    'lemmas': ['a', 'cup', 'of', 'sugar', '.'],
    'pos': ['DET', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'NN', 'IN', 'NN', '.'],
    'deps': ['det', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 1, 2, 1],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_triples': [(1, 'of', 3)]
}),
({
    'use_patterns': ['prep'],
    'description': "prep triples should only modify the noun if the dependency "\
                   "parse says so.",
    'words': ['Alice', 'took', 'a', 'cup', 'of', 'sugar', '.'],
    'lemmas': ['Alice', 'take', 'a', 'cup', 'of', 'sugar', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'NN', 'IN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'dobj', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 3, 1, 3, 4, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(3, 'of', 5)],

}),

##### verb-noun-prep-noun, dobj-pobj edge
({
    'description': "verbed-prep triples should be formed between direct objects "\
                   "and prepositional objects when the preposition is parsed "\
                   "as modifying the same parent verb.",
    'words' : ['Alice', 'supported', 'Bob', 'with', 'donations', '.'],
    'lemmas' : ['Alice', 'support', 'Bob', 'with', 'donation', '.'],
    'pos' : ['PROPN', 'VERB', 'PROPN', 'ADP', 'NOUN', 'PUNCT'],
    'tags' : ['NNP', 'VBD', 'NNP', 'IN', 'NNS', '.'],
    'deps' : ['nsubj', 'ROOT', 'dobj', 'prep', 'pobj', 'punct'],
    'heads' : [1, 1, 1, 1, 3, 1],
    'spaces' : [' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(2, 'be-support-with', 4)]
}),

##### appos_noun_prep
({
    'description': "appos noun prep",
    'words': ['Paris', ',', 'the', 'capital', 'of', 'France', '.'],
    'lemmas': ['Paris', ',', 'the', 'capital', 'of', 'France', '.'],
    'pos': ['PROPN', 'PUNCT', 'DET', 'NOUN', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['NNP', ',', 'DT', 'NN', 'IN', 'NNP', '.'],
    'deps': ['ROOT', 'punct', 'det', 'appos', 'prep', 'pobj', 'punct'],
    'heads': [0, 0, 3, 0, 3, 4, 0],
    'spaces': ['', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'appos_capital_of', 5), (3, 'of', 5)]
}),
({
    'description': "appos noun prep, with conjoined subjects",
    'words': ['Alice', 'and', 'Bob', ',', 'rulers', 'of', 'Testland'],
    'lemmas': ['Alice', 'and', 'Bob', ',', 'ruler', 'of', 'Testland'],
    'pos': ['PROPN', 'CCONJ', 'PROPN', 'PUNCT', 'NOUN', 'ADP', 'PROPN'],
    'tags': ['NNP', 'CC', 'NNP', ',', 'NNS', 'IN', 'NNP'],
    'deps': ['ROOT', 'cc', 'conj', 'punct', 'appos', 'prep', 'pobj'],
    'heads': [0, 0, 0, 0, 0, 4, 5],
    'spaces': [' ', ' ', '', ' ', ' ', ' ', ''],
    'gold_triples': [(0, 'appos_ruler_of', 6),
                     (2, 'appos_ruler_of', 6),
                     (4, 'of', 6)]
}),

##### be_noun_prep
({
    'description': "be noun prep pattern",
    'use_patterns': ['be_noun_prep'],
    'words': ['Alice', 'is', 'the', 'king', 'of', 'France', '.'],
    'lemmas': ['Alice', 'be', 'the', 'king', 'of', 'France', '.'],
    'pos': ['PROPN', 'AUX', 'DET', 'NOUN', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'DT', 'NN', 'IN', 'NNP', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'attr', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 3, 1, 3, 4, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'be_king_of', 5)]
}),
({
    'description': "be noun prep, conjoined subjects.",
    'use_patterns': ['be_noun_prep'],
    'words': ['The', 'U.S.', 'and', 'Canada', 'are', 'countries', 'in', 'NATO', '.'],
    'lemmas': ['the', 'U.S.', 'and', 'Canada', 'be', 'country', 'in', 'NATO', '.'],
    'pos': ['DET', 'PROPN', 'CCONJ', 'PROPN', 'AUX', 'NOUN', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NNP', 'CC', 'NNP', 'VBP', 'NNS', 'IN', 'NNP', '.'],
    'deps': ['det', 'nsubj', 'cc', 'conj', 'ROOT', 'attr', 'prep', 'pobj', 'punct'],
    'heads': [1, 4, 1, 1, 4, 4, 5, 6, 4],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [(1, 'be_country_in', 7), (3, 'be_country_in', 7)]
})
]


def triple_string(t, doc):
    return "({})-[{}]->({})".format(doc[t[0]], t[1], doc[t[2]])


def assert_triple_matches_gold(triple, triples, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    # comparison_keys = ['src', 'edge', 'dst']
    # triple = {k: v for k, v in triple.items() if k in comparison_keys}
    if triple not in triples:
        failure_lines = [
            desc,
            "{:>20} {}".format("Given:", str(doc)),
            "{:>20} {}".format("Expected:", ', '.join(triple_string(t, doc) for t in triples)),
            "{:>20} {}".format("Found:", triple_string(triple, doc))
        ]
        pytest.fail("\n".join(failure_lines))


def assert_count_matches_gold(gold_triples, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    if len(gold_triples) != len(doc._.triples):

        failure_lines = [
            desc,
            "{:>20}  {}".format("Given:", str(doc)),
            "{:>20}  {}".format(
                "Expected {}:".format(len(gold_triples)),
                ", ".join(triple_string(t, doc) for t in gold_triples)),
            "{:>20}  {}".format(
                "Found {}:".format(len(doc._.triples)),
                ", ".join(triple_string(t, doc) for t in doc._.triples))
        ]
        pytest.fail("\n".join(failure_lines))


@pytest.mark.parametrize("params", params)
def test_triple_matcher(params, en_vocab):
    """ Test that the triple matcher gets the correct triples for each doc """

    use_patterns = params.pop('use_patterns', None)
    description = params.pop('description')
    gold_triples = params.pop('gold_triples')
    # gold_triples = [{'src': t[0], 'edge': t[1], 'dst': t[2]}
    #                for t in gold_triples]

    # Remaining params are spaCy Doc data
    nlp = Language(en_vocab)
    matcher = TripleMatcher(nlp, use_patterns=use_patterns)
    doc = Doc(matcher.matcher.vocab, **params)

    doc = matcher(doc)

    assert_count_matches_gold(gold_triples, doc, description)

    for triple in doc._.triples:
        assert_triple_matches_gold(triple, gold_triples, doc, description)
