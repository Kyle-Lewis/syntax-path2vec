""" A pattern matcher to associate quantifiers with their objects.

This is meant to be used as a pre-processing step, marking quantifiers where
applicable on the spacy document such that later tasks (frame matcher) can swap
in prepositional objects in place of the quantifier modifying them.


Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('map_quantifiers')

    doc = nlp("Alice drank some of the water.")
               0     1     2    3  4   5    6

    doc[2]
"""

from spacy.matcher import DependencyMatcher
from spacy.language import Language

QUANTIFIERS = [
    'all',
    'another',
    'any',
    'anything',
    'both',
    'each',
    'either',
    'enough',
    'every',
    'few',
    'half',
    'lot',
    'many',
    'most',
    'much',
    'neither',
    'no',
    'none',
    'nothing',
    'one',
    'plenty',
    'plenty',
    'scores',
    'series',
    'set',
    'several',
    'some',
    'something',
    'string',
    'thing',
    'things',
    'whatever',

    # Not quantifiers but still words for which we want to make the substitution
    'variety', 'varities',
    'kind', 'kinds',
    'level', 'levels',
    'number', 'numbers',
    'amount', 'amounts',
    'portion', 'portions',
    'proportion', 'proportions',
    'concentration', 'concentrations',
    'ratio', 'ratios',
    'frequency', 'frequencies',
    '%',
    'percent', 'percents',
    'percentage', 'percentages',
    'which', 'who', 'whom'

    # cardinal forms of numbers
    'tenth', 'tenths',
    'ten', 'tens',
    'dozen', 'dozens',
    'hundredth', 'hundredths',
    'hundred', 'hundreds',
    'thousandth', 'thousandths',
    'thousand', 'thousands',
    'millionth', 'millionths',
    'million', 'millions',
    'billionth', 'billionths',
    'billion', 'billions'
]

@Language.factory('map_quantifiers')
def createQuantifiedObjectMatcherComponent(nlp, name):
    return QuantifiedObjectMatcher(nlp)

PATTERNS = {
    'relative_pronoun': [
        {"RIGHT_ID": 'quantifier', "RIGHT_ATTRS": {"LEMMA": {"IN": QUANTIFIERS}}},
        {"RIGHT_ID": 'of', "LEFT_ID": 'quantifier', "REL_OP": ">", "RIGHT_ATTRS": {"LEMMA": "of", "DEP": "prep"}},
        {"RIGHT_ID": 'object', "LEFT_ID": 'verb', "REL_OP": ">", "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PRON", "PROPN"]}, "DEP": "pobj"}}
    ]
}

class QuantifiedObjectMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp):

        # Create a matcher using our set of frame patterns
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)
        for key, pattern in PATTERNS.items():
            self.matcher.add(key, [pattern], on_match=mapQuantifiedObject)

    def __call__(self, doc):
        self.matcher(doc)
        return doc


def mapQuantifiedObject(_matcher, doc, i, matches):

    _match_id, match_token_ids = matches[i]
    quantifier = doc[match_token_ids[0]]
    quantified_object = doc[match_token_ids[-1]]
    quantifier._.quantified_objects.append(quantified_object)
