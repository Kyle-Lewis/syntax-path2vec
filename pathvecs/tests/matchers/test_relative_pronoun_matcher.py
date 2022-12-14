# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc
from spacy.language import Language

from pathvecs.matchers import RelativePronounMatcher

params = [
({
    'description': "Relative pronoun subjects of AUX verbs.",
    'words': ['Alice', ',', 'who', 'was', 'friends', 'with', 'Bob', '.'],
    'lemmas': ['Alice', ',', 'who', 'be', 'friend', 'with', 'Bob', '.'],
    'pos': ['PROPN', 'PUNCT', 'PRON', 'AUX', 'NOUN', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['NNP', ',', 'WP', 'VBD', 'NNS', 'IN', 'NNP', '.'],
    'deps': ['ROOT', 'punct', 'nsubj', 'relcl', 'attr', 'prep', 'pobj', 'punct'],
    'heads': [0, 0, 3, 0, 3, 4, 5, 0],
    'spaces': ['', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_antecedents': [(2, 0)],
}),
({
    'description': "Map relative pronouns through inverted clauses.",
    'words': ['Alice', ',', 'whom', 'I', 'was', 'familiar', 'with', '.'],
    'lemmas': ['Alice', ',', 'whom', 'I', 'be', 'familiar', 'with', '.'],
    'pos': ['PROPN', 'PUNCT', 'PRON', 'PRON', 'AUX', 'ADJ', 'ADP', 'PUNCT'],
    'tags': ['NNP', ',', 'WP', 'PRP', 'VBD', 'JJ', 'IN', '.'],
    'deps': ['ROOT', 'punct', 'pobj', 'nsubj', 'relcl', 'acomp', 'prep', 'punct'],
    'heads': [0, 0, 6, 4, 0, 4, 5, 0],
    'spaces': ['', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_antecedents': [(2, 0)],
}),
({
    'description': "Map relative pronouns which are the objects of verbs",
    'words': ['The', 'book', 'that', 'Bob', 'read', '.'],
    'lemmas': ['the', 'book', 'that', 'Bob', 'read', '.'],
    'pos': ['DET', 'NOUN', 'PRON', 'PROPN', 'VERB', 'PUNCT'],
    'tags': ['DT', 'NN', 'WDT', 'NNP', 'VBD', '.'],
    'deps': ['det', 'ROOT', 'dobj', 'nsubj', 'relcl', 'punct'],
    'heads': [1, 1, 4, 4, 1, 1],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_antecedents': [(2, 1)],
}),
({
    'description': "Map all relative pronouns which are present.",
    'words': ['Alice', ',', 'who', 'wrote', 'the', 'book', ',', 'and', 'Bob', ',', 'who', 'published', 'it', '.'],
    'lemmas': ['Alice', ',', 'who', 'write', 'the', 'book', ',', 'and', 'Bob', ',', 'who', 'publish', 'it', '.'],
    'pos': ['PROPN', 'PUNCT', 'PRON', 'VERB', 'DET', 'NOUN', 'PUNCT', 'CCONJ', 'PROPN', 'PUNCT', 'PRON', 'VERB', 'PRON', 'PUNCT'],
    'tags': ['NNP', ',', 'WP', 'VBD', 'DT', 'NN', ',', 'CC', 'NNP', ',', 'WP', 'VBD', 'PRP', '.'],
    'deps': ['ROOT', 'punct', 'nsubj', 'relcl', 'det', 'dobj', 'punct', 'cc', 'conj', 'punct', 'nsubj', 'relcl', 'dobj', 'punct'],
    'heads': [0, 0, 3, 0, 5, 3, 0, 0, 0, 8, 11, 8, 11, 0],
    'spaces': ['', ' ', ' ', ' ', ' ', '', ' ', ' ', '', ' ', ' ', ' ', '', ''],
    'gold_antecedents': [(2, 0), (10, 8)],
})
]

@pytest.fixture
def matcher(en_vocab):
    nlp = Language(en_vocab)
    matcher = RelativePronounMatcher(nlp)
    return matcher


def mapString(mapping, doc):
    return "{} => {}".format(doc[mapping[0]], doc[mapping[1]])


def assertMappingInMappings(mapping, gold_mappings, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable

    if mapping not in gold_mappings:
        expected_str = ', '.join(mapString(m, doc) for m in gold_mappings)
        failure_lines = [
            desc,
            "{:<10} {}".format("Given:", str(doc)),
            "{:<10} {}".format("Expected:", expected_str),
            "{:<10} {}".format("Found:", mapString(mapping, doc))
        ]
        pytest.fail("\n".join(failure_lines))


def assertExpectedNumberOfMappings(found_mappings, gold_mappings, doc, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    n_expected = len(gold_mappings)
    n_found = len(found_mappings)
    if n_found != n_expected:

        expected_str = ', '.join(mapString(m, doc) for m in gold_mappings)
        found_str = ', '.join(mapString(m, doc) for m in found_mappings)
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
def testNominalSpanMatcher(params, matcher):
    """ Test that the nominal matcher gets the correct spans for each doc """

    description = params.pop('description')
    gold_antecedents = params.pop('gold_antecedents')
    doc = Doc(matcher.matcher.vocab, **params)

    # Test the classes behavior as it will be called in a language pipeline
    doc = matcher(doc)
    mapped_antecedents = []
    for t in doc:
        if t._.antecedent:
            mapped_antecedents.append((t.i, t._.antecedent.i))


    for mapping in mapped_antecedents:
        assertMappingInMappings(mapping, gold_antecedents, doc, description)

    assertExpectedNumberOfMappings(
        mapped_antecedents, gold_antecedents, doc, description)
