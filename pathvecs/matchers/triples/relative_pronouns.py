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


@Language.factory('map_relative_pronouns')
def createRelativePronounMatcherComponent(nlp, name):
    return RelativePronounMatcher(nlp)

PATTERNS = {
    'relative_pronoun': [
        {"RIGHT_ID": 'pronoun', "RIGHT_ATTRS": {"LEMMA": {"IN": ['which', 'that', 'whom', 'who', 'whose']}}},
        {"RIGHT_ID": 'verb', "LEFT_ID": 'pronoun', "REL_OP": "<<", "RIGHT_ATTRS": {"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]}, "DEP": "relcl"}},
        {"RIGHT_ID": 'antecedent', "LEFT_ID": 'verb', "REL_OP": "<", "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PRON", "PROPN"]}}}
    ]
}

class RelativePronounMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp):

        # Create a matcher using our set of frame patterns
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)
        for key, pattern in PATTERNS.items():
            self.matcher.add(key, [pattern], on_match=mapRelativePronoun)

    def __call__(self, doc):
        self.matcher(doc)
        return doc


def mapRelativePronoun(_matcher, doc, i, matches):

    _match_id, match_token_ids = matches[i]
    pronoun = doc[match_token_ids[0]]
    antecedent = doc[match_token_ids[-1]]
    pronoun._.antecedent = antecedent
