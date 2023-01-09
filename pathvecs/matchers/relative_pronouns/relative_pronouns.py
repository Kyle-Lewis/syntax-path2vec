""" A pattern matcher to associate relative pronouns with their antecedents.

This is meant to be used as a pre-processing step, marking up relative
pronouns where applicable on the spacy document such that later tasks
(frame matcher) can swap in antecedents in place of relative pronouns.


Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('map_relative_pronouns')

    doc = nlp("This is the girl whose notes I borrowed.")
               0    1  2   3    4     5     6 7

    > {4:3} (haven't decided on storage yet, doc vs token extension)
"""

from spacy.matcher import DependencyMatcher
from spacy.language import Language
from spacy.tokens import Token

import pathvecs.matchers.relative_pronouns.patterns as patterns

@Language.factory('map_relative_pronouns')
def createRelativePronounMatcherComponent(nlp, name):
    return RelativePronounMatcher(nlp)

class RelativePronounMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, use_patterns=None):

        # Create a matcher using the specified patterns, or all by default
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)

        # Register token extension
        if not Token.has_extension('antecedent'):
            Token.set_extension('antecedent', default=None)

        if use_patterns is not None:

            for pattern_key in use_patterns:
                pattern = patterns.get_pattern(pattern_key)
                self.matcher.add(pattern_key, [pattern], on_match=on_match)

        else:
            for pattern_key, pattern in patterns.get_all_patterns():
                self.matcher.add(pattern_key, [pattern], on_match=on_match)

    def __call__(self, doc):
        self.matcher(doc)
        return doc


def on_match(_matcher, doc, i, matches):

    _match_id, match_token_ids = matches[i]
    pronoun = doc[match_token_ids[0]]
    antecedent = doc[match_token_ids[-1]]
    pronoun._.antecedent = antecedent
