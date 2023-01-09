""" A pattern matcher to associate quantifiers with their objects.

This is meant to be used as a pre-processing step, marking quantifiers where
applicable on the spacy document such that later tasks can swap
in prepositional objects in place of the quantifier modifying them.


Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('map_quantifiers')

    doc = nlp("Alice drank some of the water.")
               0     1     2    3  4   5    6

    doc[2]._.quantifieds => [5]
"""

from spacy.matcher import DependencyMatcher
from spacy.language import Language
from spacy.tokens import Token

import pathvecs.matchers.quantifiers.patterns as patterns

@Language.factory('map_quantifiers')
def createQuantifiedObjectMatcherComponent(nlp, name):
    return QuantifiedObjectMatcher(nlp)

class QuantifiedObjectMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, use_patterns=None):

        # Create a matcher using the specified patterns, or all by default
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)

        # Register token extension
        if not Token.has_extension('quantifieds'):
            Token.set_extension('quantifieds', default=[])

        if use_patterns is not None:

            for key in use_patterns:
                pattern = patterns.get_pattern(key)
                self.matcher.add(key, [pattern], on_match=on_match)

        else:
            for key, pattern in patterns.get_all_patterns():
                self.matcher.add(key, [pattern], on_match=on_match)

    def __call__(self, doc):
        self.matcher(doc)
        return doc


def on_match(_matcher, doc, i, matches):

    _match_id, match_token_ids = matches[i]
    quantifier = doc[match_token_ids[0]]
    quantified_object = doc[match_token_ids[-1]]
    quantifier._.quantifieds.append(quantified_object)
