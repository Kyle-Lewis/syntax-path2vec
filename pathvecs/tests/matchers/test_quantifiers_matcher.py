# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc
from spacy.language import Language

from pathvecs.matchers import QuantifiedObjectMatcher


params = [
({
    'words': ['Bob', 'ate', 'one', 'of', 'the', 'cakes', '.'],
    'lemmas': ['Bob', 'eat', 'one', 'of', 'the', 'cake', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'IN', 'DT', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 1, 2, 5, 3, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_quantifieds': [(2, [5])],
}),
({
    'words': ['Bob', 'ate', 'one', 'of', 'the', 'cakes', '.'],
    'lemmas': ['Bob', 'eat', 'one', 'of', 'the', 'cake', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'IN', 'DT', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 1, 2, 5, 3, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_quantifieds': [(2, [5])],
}),
({
    'words': ['Alice', 'brought', 'some', 'of', 'her', 'pens', 'and', 'pencils', '.'],
    'lemmas': ['Alice', 'bring', 'some', 'of', 'her', 'pen', 'and', 'pencil', '.'],
    'pos': ['PROPN', 'VERB', 'PRON', 'ADP', 'PRON', 'NOUN', 'CCONJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'IN', 'PRP$', 'NNS', 'CC', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'prep', 'poss', 'pobj', 'cc', 'conj', 'punct'],
    'heads': [1, 1, 1, 2, 5, 3, 5, 5, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_quantifieds': [(2, [5, 7])]
})
]

@pytest.fixture
def matcher(en_vocab):
    nlp = Language(en_vocab)
    matcher = QuantifiedObjectMatcher(nlp)
    return matcher


def map_string(m, doc):
    print(m, doc)
    return "{} => {}".format(doc[m[0]], [doc[i] for i in m[1]])


def assert_mapping_in_mappings(mapping, gold_mappings, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    if mapping not in gold_mappings:
        expected_str = ', '.join(map_string(m, doc) for m in gold_mappings)
        failure_lines = [
            desc,
            "{:<10} {}".format("Given:", str(doc)),
            "{:<10} {}".format("Expected:", expected_str),
            "{:<10} {}".format("Found:", map_string(mapping, doc))
        ]
        pytest.fail("\n".join(failure_lines))


def assert_expected_num(found_mappings, gold_mappings, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    n_expected = len(gold_mappings)
    n_found = len(found_mappings)
    if n_found != n_expected:

        expected_str = ', '.join(map_string(m, doc) for m in gold_mappings)
        found_str = ', '.join(map_string(m, doc) for m in found_mappings)
        failure_lines = [
            desc,
            "{:<20} {}".format("Given:", str(doc)),
            "{:<20} {}".format("Expected {} mapped pronoun(s)".format(
                n_expected), expected_str),
            "{:<20} {}".format("Found {} mapped pronoun(s)".format(
                n_found), found_str)
        ]
        pytest.fail("\n".join(failure_lines))


@pytest.mark.parametrize("params", params)
def test_quantified_objects_matcher(params, matcher):
    """ Test that the quantifier matcher maps the expected quantified pairs """

    description = params.pop('description', '')
    gold_quantifieds = params.pop('gold_quantifieds')
    doc = Doc(matcher.matcher.vocab, **params)

    # Test the classes behavior as it will be called in a language pipeline
    doc = matcher(doc)
    mapped_quantifieds = []
    for t in doc:
        if t._.quantifieds:
            mapped_quantifieds.append((t.i, [q.i for q in t._.quantifieds]))

    for mapping in mapped_quantifieds:
        assert_mapping_in_mappings(mapping, gold_quantifieds, doc, description)

    assert_expected_num(
        mapped_quantifieds, gold_quantifieds, doc, description)
