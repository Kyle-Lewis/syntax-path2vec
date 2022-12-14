# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc
from spacy.language import Language

from pathvecs.matchers import TripleMatcher

params = [

##### adjectival modifiers

({
    'description': "Match adjective triples",
    'words': ['The', 'red', 'dog'],
    'lemmas': ['the', 'red', 'dog'],
    'pos': ['DET', 'ADJ', 'NOUN'],
    'tags': ['DT', 'JJ', 'NN'],
    'deps': ['det', 'amod', 'ROOT'],
    'heads': [2, 2, 2],
    'spaces': [' ', ' ', ''],
    'gold_triples': [(1, 'adj', 2)]
}),
({
    'description': "Match multiple adjective triples where multiple modifiers "\
                   "are present.",
    'words': ['The', 'large', 'silly', 'dog'],
    'lemmas': ['the', 'large', 'silly', 'dog'],
    'pos': ['DET', 'ADJ', 'ADJ', 'NOUN'],
    'tags': ['DT', 'JJ', 'JJ', 'NN'],
    'deps': ['det', 'amod', 'amod', 'ROOT'],
    'heads': [3, 3, 3, 3],
    'spaces': [' ', ' ', ' ', ''],
    'gold_triples': [(1, 'adj', 3), (2, 'adj', 3)]
}),

##### possessive modifiers

({
    'description': "Match possessive triples",
    'words': ['Alice', "'s", 'dog'],
    'lemmas': ['Alice', "'s", 'dog'],
    'pos': ['PROPN', 'PART', 'NOUN'],
    'tags': ['NNP', 'POS', 'NN'],
    'deps': ['poss', 'case', 'ROOT'],
    'heads': [2, 0, 2],
    'spaces': ['', ' ', ''],
    'gold_triples': [(0, 'poss', 2)]
}),
({
    'description': "Match multiple possessives with conjugated possessions.",
    'words': ['Bob', "'s", 'items', 'and', 'possessions', '.'],
    'lemmas': ['Bob', "'s", 'item', 'and', 'possession', '.'],
    'pos': ['PROPN', 'PART', 'NOUN', 'CCONJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'POS', 'NNS', 'CC', 'NNS', '.'],
    'deps': ['poss', 'case', 'ROOT', 'cc', 'conj', 'punct'],
    'heads': [2, 0, 2, 2, 2, 2],
    'spaces': ['', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'poss', 2),(0, 'poss', 4)]
}),

##### appositive modifiers
({
    'description': "Match appositive triples",
    'words': ['Alice', ',', 'the', 'tester', '.'],
    'lemmas': ['Alice', ',', 'the', 'tester', '.'],
    'pos': ['PROPN', 'PUNCT', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', ',', 'DT', 'NN', '.'],
    'deps': ['ROOT', 'punct', 'det', 'appos', 'punct'],
    'heads': [0, 0, 3, 0, 0],
    'spaces': ['', ' ', ' ', '', ''],
    'gold_triples': [(0, 'appos', 3)]
}),

({
    'description': "Match appositive triples for conjugated appositive modifiers",
    'words': ['Bob', ',', 'the', 'founder', 'and', 'CEO'],
    'lemmas': ['Bob', ',', 'the', 'founder', 'and', 'ceo'],
    'pos': ['PROPN', 'PUNCT', 'DET', 'NOUN', 'CCONJ', 'NOUN'],
    'tags': ['NNP', ',', 'DT', 'NN', 'CC', 'NN'],
    'deps': ['ROOT', 'punct', 'det', 'appos', 'cc', 'conj'],
    'heads': [0, 0, 3, 0, 3, 3],
    'spaces': ['', ' ', ' ', ' ', ' ', ''],
    'gold_triples': [(0, 'appos', 3),(0, 'appos', 5)]
}),

({
    'description': "Match appositive triples for conjugated appositive heads",
    'words': ['Alice', 'and', 'Bob', ',', 'the', 'test', 'cases', '.'],
    'lemmas': ['Alice', 'and', 'Bob', ',', 'the', 'test', 'case', '.'],
    'pos': ['PROPN', 'CCONJ', 'PROPN', 'PUNCT', 'DET', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'CC', 'NNP', ',', 'DT', 'NN', 'NNS', '.'],
    'deps': ['ROOT', 'cc', 'conj', 'punct', 'det', 'compound', 'appos', 'punct'],
    'heads': [0, 0, 0, 0, 6, 6, 0, 0],
    'spaces': [' ', ' ', '', ' ', ' ', ' ', '', ''],
    'gold_triples': [(0, 'appos', 6), (2, 'appos', 6)],
}),

##### compound modifiers
({
    'description': "Compound triples should be formed between compound "\
                   "modifiers of head nouns with mixed parts of speech.",
    'words': ['Microsoft', 'executive', '.'],
    'lemmas': ['Microsoft', 'executive', '.'],
    'pos': ['PROPN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'NN', '.'],
    'deps': ['compound', 'ROOT', 'punct'],
    'heads': [1, 1, 1],
    'spaces': [' ', '', ''],
    'gold_triples': [(0, 'compound', 1)]
}),
({
    'description': "Compound triples should not be formed between compound "\
                   "modifiers of head nouns with matching parts of speech.",
    'words': ['ice', 'cream', '.'],
    'lemmas': ['ice', 'cream', '.'],
    'pos': ['NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NN', 'NN', '.'],
    'deps': ['compound', 'ROOT', 'punct'],
    'heads': [1, 1, 1],
    'spaces': [' ', '', ''],
    'gold_triples': []
}),

##### being verbs with a nominal attr child
({
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
    'description': "prep triples should only modify the noun if the dependency "\
                   "parse says so.",
    'words': ['Alice', 'took', 'a', 'cup', 'of', 'sugar', '.'],
    'lemmas': ['Alice', 'take', 'a', 'cup', 'of', 'sugar', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'NN', 'IN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'dobj', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 3, 1, 3, 4, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_triples': [],

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
})
]

@pytest.fixture
def matcher(en_vocab):
    nlp = Language(en_vocab)
    matcher = TripleMatcher(nlp)
    return matcher


def tripleString(triple, doc):
    return "({})-[{}]->({})".format(
            doc[triple['src']],
            triple['edge'],
            doc[triple['dst']])


def assertFrameInFrames(triple, triples, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    comparison_keys = ['src', 'edge', 'dst']
    triple = {k: v for k, v in triple.items() if k in comparison_keys}
    if triple not in triples:
        failure_lines = [
            desc,
            "{:<10} {}".format("Given:", str(doc)),
            "{:<10} {}".format("Expected:", ', '.join(tripleString(f, doc) for f in triples)),
            "{:<10} {}".format("Found:", tripleString(triple, doc))
        ]
        pytest.fail("\n".join(failure_lines))


def assertExpectedNumberOfTriples(gold_triples, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    if len(gold_triples) != len(doc._.triples):

        failure_lines = [
            desc,
            "{:<20} {}".format("Given:", str(doc)),
            "{:<20} {}".format(
                "Expected {} triples".format(len(gold_triples)),
                ", ".join(tripleString(f, doc) for f in gold_triples)),
            "{:<20} {}".format(
                "Found {} triples".format(len(doc._.triples)),
                ", ".join(tripleString(f, doc) for f in doc._.triples))
        ]
        pytest.fail("\n".join(failure_lines))


@pytest.mark.parametrize("params", params)
def testNominalSpanMatcher(params, matcher):
    """ Test that the nominal matcher gets the correct spans for each doc """

    description = params.pop('description')
    gold_triples = params.pop('gold_triples')
    gold_triples = [{'src': f[0], 'edge': f[1], 'dst': f[2]}
                   for f in gold_triples]
    doc = Doc(matcher.matcher.vocab, **params)

    # Test the classes behavior as it will be called in a language pipeline
    doc = matcher(doc)

    assertExpectedNumberOfTriples(gold_triples, doc, description)

    for triple in doc._.triples:
        assertFrameInFrames(triple, gold_triples, doc, description)

