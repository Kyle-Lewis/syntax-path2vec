""" A matcher for syntactic path triples registered as a spaCy component.

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
from spacy.matcher import DependencyMatcher
from spacy.language import Language
from spacy.tokens import Doc, Token

import pathvecs.matchers.triples.patterns as patterns

@Language.factory('triple_matcher', default_config={'use_patterns': None})
def createTripleMatcherComponent(nlp, name, use_patterns):
    return TripleMatcher(nlp, use_patterns=use_patterns)


class TripleMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, use_patterns=None):

        # Create a matcher using our set of triple patterns
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)

        # Register token and doc extensions
        if not Doc.has_extension('triples'):
            Doc.set_extension('triples', default=[])

        if not Token.has_extension('verb_type'):
            Token.set_extension('verb_type', default=None)

        if use_patterns is not None:

            for pattern_key in use_patterns:
                pattern = patterns.get_pattern(pattern_key)
                self.matcher.add(pattern_key, [pattern], on_match=on_match)

        else:
            for pattern_key, pattern in patterns.get_all_patterns():
                self.matcher.add(pattern_key, [pattern], on_match=on_match)

    def __call__(self, doc):

        # Add the matched triples when the doc is processed
        self.matcher(doc)
        return doc


def on_match(_matcher, doc, i, matches):

    match_id, match_token_ids = matches[i]
    pattern_key = doc.vocab.strings[match_id]
    triples = patterns.get_all_triples(match_token_ids, pattern_key, doc)
    doc._.triples.extend(triples)
