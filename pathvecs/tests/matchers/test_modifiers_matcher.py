# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from pathvecs.matchers import ModifierSpanMatcher

params = [

##### adjectives
({
    'description': 'Single token adjectival modifiers should be detected as spans.',
    'words': ['The', 'big', 'dog', '.'],
    'lemmas': ['the', 'big', 'dog', '.'],
    'pos': ['DET', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'JJ', 'NN', '.'],
    'deps': ['det', 'amod', 'ROOT', 'punct'],
    'heads': [2, 2, 2, 2],
    'gold_spans': [(1, 2)],
}),
({
    'description': "Consecutive adjectival modifiers should be detected as separate spans.",
    'words': ['The', 'great', 'big', 'red', 'dog', '.'],
    'lemmas': ['the', 'great', 'big', 'red', 'dog', '.'],
    'pos': ['DET', 'ADJ', 'ADJ', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'JJ', 'JJ', 'JJ', 'NN', '.'],
    'deps': ['det', 'amod', 'amod', 'amod', 'ROOT', 'punct'],
    'heads': [4, 4, 4, 4, 4, 4],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(1, 2),(2, 3),(3, 4)]
}),

##### proper adjectives
({
    'description': "Single token proper adjectives should be detected as modifier spans.",
    'words': ['Bob', 'loves', 'Indian', 'food', '.'],
    'lemmas': ['Bob', 'love', 'indian', 'food', '.'],
    'pos': ['PROPN', 'VERB', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'JJ', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'amod', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_spans': [(2, 3)]
}),
({
    'description': "Multi token proper adjectives should be detected as single modifier spans.",
    'words': ['They', 'met', 'at', 'the', 'West', 'African', 'consulate', '.'],
    'lemmas': ['they', 'meet', 'at', 'the', 'west', 'african', 'consulate', '.'],
    'pos': ['PRON', 'VERB', 'ADP', 'DET', 'ADJ', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['PRP', 'VBD', 'IN', 'DT', 'JJ', 'JJ', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'amod', 'amod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 6, 5, 6, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 6)]
}),
({
    'description': "Hyphenated multi token proper adjectives should be detected as single modifier spans.",
    'words': ['Bob', 'studies', 'Afro', '-', 'American', 'religion', '.'],
    'lemmas': ['Bob', 'study', 'Afro', '-', 'american', 'religion', '.'],
    'pos': ['PROPN', 'VERB', 'PROPN', 'PUNCT', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'NNP', 'HYPH', 'JJ', 'NN', '.'],
    'deps': ['compound', 'ROOT', 'amod', 'punct', 'amod', 'dobj', 'punct'],
    'heads': [1, 1, 4, 4, 5, 1, 1],
    'spaces': [' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(2, 5)]
}),

##### advmods & npadvmods
({
    'description': "Hyphenated NP adverb modifiers are included in the spans for their parent modifier.",
    'words': ['The', 'flea', '-', 'bitten', 'dog', '.'],
    'lemmas': ['the', 'flea', '-', 'bite', 'dog', '.'],
    'pos': ['DET', 'NOUN', 'PUNCT', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'NN', 'HYPH', 'VBN', 'NN', '.'],
    'deps': ['det', 'npadvmod', 'punct', 'amod', 'ROOT', 'punct'],
    'heads': [4, 3, 3, 4, 4, 4],
    'spaces': [' ', '', '', ' ', '', ''],
    'gold_spans': [(1, 4)]
}),
({
    'description': "Modifiers to the left of npadvmod spans should generally be detected as separate modifying spans.",
    'words': ['5', 'gold', '-', 'plated', 'rings', '.'],
    'lemmas': ['5', 'gold', '-', 'plate', 'ring', '.'],
    'pos': ['NUM', 'NOUN', 'PUNCT', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['CD', 'NN', 'HYPH', 'VBN', 'NNS', '.'],
    'deps': ['nummod', 'npadvmod', 'punct', 'amod', 'ROOT', 'punct'],
    'heads': [4, 3, 3, 4, 4, 4],
    'spaces': [' ', '', '', ' ', '', ''],
    'gold_spans': [(0, 1), (1, 4)]
}),
({
    'description': "The '# year old' pattern should be detected as one modifying span.",
    'words': ['The', '2', 'year', 'old', 'dog', '.'],
    'lemmas': ['the', '2', 'year', 'old', 'dog', '.'],
    'pos': ['DET', 'NUM', 'NOUN', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'CD', 'NN', 'JJ', 'NN', '.'],
    'deps': ['det', 'nummod', 'npadvmod', 'amod', 'ROOT', 'punct'],
    'heads': [4, 2, 3, 4, 4, 4],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(1, 4)]
}),
({
    'description': "Hyphen-joined adverb modifiers are included in the spans for their parent modifier.",
    'words': ['We', 'are', 'an', 'online', '-', 'only', 'marketplace', '.'],
    'lemmas': ['we', 'be', 'an', 'online', '-', 'only', 'marketplace', '.'],
    'pos': ['PRON', 'AUX', 'DET', 'ADV', 'PUNCT', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['PRP', 'VBP', 'DT', 'RB', 'HYPH', 'JJ', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'advmod', 'punct', 'amod', 'attr', 'punct'],
    'heads': [1, 1, 6, 5, 5, 6, 1, 1],
    'spaces': [' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),
({
    'description': "Multi token proper nouns should be detected as parts of modifier spans when used as npadvmod.",
    'words': ['Bob', 'works', 'at', 'a', 'European', 'Union', '-', 'funded', 'startup', '.'],
    'lemmas': ['Bob', 'work', 'at', 'a', 'European', 'Union', '-', 'fund', 'startup', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'DET', 'PROPN', 'PROPN', 'PUNCT', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'IN', 'DT', 'NNP', 'NNP', 'HYPH', 'VBN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'amod', 'npadvmod', 'punct', 'amod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 8, 8, 7, 7, 8, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(4, 8)]
}),
({
    'description': "Multi token nouns should be detected as parts of modifier spans when used as npadvmod",
    'words': ['Bob', 'works', 'at', 'a', 'sports', 'game', '-', 'based', 'startup', '.'],
    'lemmas': ['Bob', 'work', 'at', 'a', 'sport', 'game', '-', 'base', 'startup', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'DET', 'NOUN', 'NOUN', 'PUNCT', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'IN', 'DT', 'NNS', 'NN', 'HYPH', 'VBN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'npadvmod', 'npadvmod', 'punct', 'amod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 8, 7, 7, 7, 8, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(4, 8)]
}),

##### hyphenation
({
    'description': "Modifiers proceded by a hyphen should include the full hyphenation in their span.",
    'words': ['Alice', 'got', 'a', 'long', '-', 'term', 'loan', '.'],
    'lemmas': ['Alice', 'get', 'a', 'long', '-', 'term', 'loan', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'ADJ', 'PUNCT', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', 'JJ', 'HYPH', 'NN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'amod', 'punct', 'compound', 'dobj', 'punct'],
    'heads': [1, 1, 6, 5, 5, 6, 1, 1],
    'spaces': [' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),
({
    'description': "Modifiers proceded by a hyphen should include the full hyphenation in their span.",
    'words': ['Bob', 'drank', 'his', 'mid', '-', 'afternoon', 'cup', 'of', 'tea', '.'],
    'lemmas': ['Bob', 'drink', 'his', 'mid', '-', 'afternoon', 'cup', 'of', 'tea', '.'],
    'pos': ['PROPN', 'VERB', 'PRON', 'ADJ', 'ADJ', 'ADJ', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'PRP$', 'JJ', 'JJ', 'JJ', 'NN', 'IN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'poss', 'amod', 'amod', 'compound', 'dobj', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 6, 6, 6, 6, 1, 6, 7, 1],
    'spaces': [' ', ' ', ' ', '', '', ' ', ' ', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),
({
    'description': "Modifiers followed by particles should be detected as single spans.",
    'words': ['Bob', 'has', 'an', 'opt', '-', 'out', 'configuration', '.'],
    'lemmas': ['Bob', 'have', 'an', 'opt', '-', 'out', 'configuration', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'VERB', 'PUNCT', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'DT', 'VB', 'HYPH', 'NN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'amod', 'punct', 'prt', 'dobj', 'punct'],
    'heads': [1, 1, 6, 6, 3, 3, 1, 1],
    'spaces': [' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),
({
    'description': "Modifiers chained by hyphens should be detected as single spans.",
    'words': ['Alice', 'is', 'a', 'non', '-', 'subscribed', 'user', '.'],
    'lemmas': ['Alice', 'be', 'a', 'non', '-', 'subscribe', 'user', '.'],
    'pos': ['PROPN', 'AUX', 'DET', 'ADJ', 'ADJ', 'VERB', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'DT', 'JJ', 'JJ', 'VBN', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'amod', 'amod', 'amod', 'attr', 'punct'],
    'heads': [1, 1, 6, 6, 6, 6, 1, 1],
    'spaces': [' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),
({
    'description': "Modifiers proceded by consecutive hyphens should include the full hyphenation in their span.",
    'words': ['Alice', 'makes', 'farm', '-', 'to', '-', 'table', 'meals', '.'],
    'lemmas': ['Alice', 'make', 'farm', '-', 'to', '-', 'table', 'meal', '.'],
    'pos': ['PROPN', 'VERB', 'NOUN', 'PUNCT', 'ADP', 'PUNCT', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'NN', 'HYPH', 'IN', 'HYPH', 'NN', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'nmod', 'punct', 'prep', 'punct', 'pobj', 'dobj', 'punct'],
    'heads': [1, 1, 7, 2, 2, 4, 4, 1, 1],
    'spaces': [' ', ' ', '', '', '', '', ' ', '', ''],
    'gold_spans': [(2, 7)]
}),

##### numbers
({
    'description': "Multi token nummod children should be detected as single spans.",
    'words': ['Bob', 'got', '40', 'thousand', 'dollars', '.'],
    'lemmas': ['Bob', 'get', '40', 'thousand', 'dollar', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'NUM', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'CD', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'compound', 'nummod', 'dobj', 'punct'],
    'heads': [1, 1, 3, 4, 1, 1],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(2, 4)]
}),
({
    'description': "Currency symbols should be included in nummod spans.",
    'words': ['Alice', 'got', 'a', '$', '40', 'million', 'bonus', '.'],
    'lemmas': ['Alice', 'get', 'a', '$', '40', 'million', 'bonus', '.'],
    'pos': ['PROPN', 'VERB', 'DET', 'SYM', 'NUM', 'NUM', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'DT', '$', 'CD', 'CD', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'det', 'quantmod', 'compound', 'nummod', 'dobj', 'punct'],
    'heads': [1, 1, 6, 5, 5, 6, 1, 1],
    'spaces': [' ', ' ', ' ', '', ' ', ' ', '', ''],
    'gold_spans': [(3, 6)]
}),

##### dates as modifiers
({
    'description': "No modifiers should be detected within *nominal* date spans.",
    'words': ['On', 'March', '18', ',', '2011', ',', 'Bob', 'went', 'to', 'work', '.'],
    'lemmas': ['on', 'March', '18', ',', '2011', ',', 'Bob', 'go', 'to', 'work', '.'],
    'pos': ['ADP', 'PROPN', 'NUM', 'PUNCT', 'NUM', 'PUNCT', 'PROPN', 'VERB', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['IN', 'NNP', 'CD', ',', 'CD', ',', 'NNP', 'VBD', 'IN', 'NN', '.'],
    'deps': ['prep', 'pobj', 'nummod', 'punct', 'nummod', 'punct', 'nsubj', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [7, 0, 1, 1, 1, 7, 7, 7, 7, 8, 7],
    'spaces': [' ', ' ', '', ' ', '', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': []
}),
({
    'description': "",
    'words': ['On', '1', 'May', '2013', '.'],
    'lemmas': ['on', '1', 'May', '2013', '.'],
    'pos': ['ADP', 'NUM', 'PROPN', 'NUM', 'PUNCT'],
    'tags': ['IN', 'CD', 'NNP', 'CD', '.'],
    'deps': ['ROOT', 'nummod', 'pobj', 'nummod', 'punct'],
    'heads': [0, 2, 0, 2, 0],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_spans': []
}),
({
    'description': "Years used as modifiers should be detected as modifier spans.",
    'words': ['A', '2014', 'ad', 'for', 'toothpaste', '.'],
    'lemmas': ['a', '2014', 'ad', 'for', 'toothpaste', '.'],
    'pos': ['DET', 'NUM', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'CD', 'NN', 'IN', 'NN', '.'],
    'deps': ['det', 'nummod', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [2, 2, 2, 2, 3, 2],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(1, 2)]
}),
({
    'description': "Multi token dates (month + year) used as modifiers should be detected as single modifier spans.",
    'words': ['Bob', 'claimed', 'in', 'his', 'December', '2002', 'interview', '.'],
    'lemmas': ['Bob', 'claim', 'in', 'his', 'December', '2002', 'interview', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'PRON', 'PROPN', 'NUM', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'IN', 'PRP$', 'NNP', 'CD', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'poss', 'nmod', 'nummod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 6, 6, 4, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 6)]
}),
({
    'description': "Multi token dates (month + day) used as modifiers should be detected as single modifier spans.",
    'words': ['Alice', 'partied', 'on', 'her', 'March', '30th', 'anniversery', '.'],
    'lemmas': ['Alice', 'partie', 'on', 'her', 'March', '30th', 'anniversery', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'PRON', 'PROPN', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'IN', 'PRP$', 'NNP', 'JJ', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'poss', 'nmod', 'amod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 6, 6, 6, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 6)]
})
]

@pytest.fixture
def matcher(en_vocab):
    nlp = Language(en_vocab)
    matcher = ModifierSpanMatcher(nlp)
    return matcher


def assertSpanInSpans(span, spans, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    span_as_tuple = (span.start, span.end)
    spans_as_tuples = [(s.start, s.end) for s in spans]

    doc = span.doc
    if span_as_tuple not in spans_as_tuples:
        failure_lines = [
            desc,
            "{:<10} {}".format("Given:", str(doc)),
            "{:<10} {}".format("Expected:", spans),
            "{:<10} {}".format("Found:", span)
        ]
        pytest.fail("\n".join(failure_lines))


@pytest.mark.parametrize("params", params)
def testModifierSpanMatcher(params, matcher):
    """ Test that the modifier matcher gets the correct spans for each doc """

    description = params.pop('description')
    gold_span_tuples = params.pop('gold_spans')
    doc = Doc(matcher.matcher.vocab, **params)
    gold_spans = [Span(doc, *gs) for gs in gold_span_tuples]

    # Test the classes behavior as it will be called in a language pipeline
    doc = matcher(doc)

    for span in doc.spans[matcher.key]:
        assertSpanInSpans(span, gold_spans, description)

    helper = '\n'.join([description, str(doc)])
    assert len(gold_spans) == len(doc.spans[matcher.key]), helper
