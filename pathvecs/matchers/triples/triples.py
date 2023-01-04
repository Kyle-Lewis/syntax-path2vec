""" A pattern matcher for syntactic relationship triples registered as a spaCy pipe component.

Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('triple_matcher')

    doc = nlp("Alice went to the store.")
    print(doc._.triples[0])

    >
    {
        'type': 'intransitive_prep',
        'src': 0,
        'edge': 'go_to',
        'dst': 4
    }

    # where:
    doc[0] -> "Alice"
    doc[4] -> "store"
"""
import itertools

from spacy.matcher import DependencyMatcher
from spacy.language import Language

import pathvecs.matchers.triples.triple_patterns as tp
# from triples.matchers.relative_pronouns import (RelativePronounMatcher)

@Language.factory('triple_matcher')
def createTripleMatcherComponent(nlp, name):
    return TripleMatcher(nlp)


class TripleMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, use_patterns=None):

        # Create a matcher using our set of triple patterns
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)

        if use_patterns is not None:

            for pattern_key in use_patterns:
                pattern = tp.get_pattern(pattern_key)
                self.matcher.add(pattern_key, [pattern], on_match=add_triple)

        else:
            for pattern_key, pattern in tp.get_all_patterns():
                self.matcher.add(pattern_key, [pattern], on_match=add_triple)

    def __call__(self, doc):

        # Add the matched triples when the doc is processed
        self.matcher(doc)
        return doc


def add_triple(_matcher, doc, i, matches):

    match_id, match_token_ids = matches[i]
    pattern_key = doc.vocab.strings[match_id]
    triples = tp.get_all_triples(match_token_ids, pattern_key, doc)
    doc._.triples.extend(triples)
