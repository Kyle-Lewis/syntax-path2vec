""" A pattern matcher for nominal spans registered as a spaCy pipe component.

Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('modifier_spans')

    doc = nlp("The big red dog barked.")
    print(doc.spans['modifiers'])

    > [big, red]
"""

from spacy.matcher import Matcher
from spacy.language import Language
from spacy.util import filter_spans

from pathvecs.matchers.spans.patterns import getSpanPatterns
from pathvecs.matchers.utils import getInboundDependencies

@Language.factory('modifier_spans')
def createNominalMatcherComponent(nlp, name):
    return ModifierSpanMatcher(nlp)


class ModifierSpanMatcher:
    """ A spacy Matcher object wrapped as a pipeline component

    Attributes:
        key: Where the matched spans will be saved to (doc.spans[key])
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, key='modifiers'):

        self.key = key

        # Create a matcher using our set of nominal span patterns
        patterns = getSpanPatterns('modifiers')
        self.matcher = Matcher(nlp.vocab, validate=True)
        self.matcher.add(key, patterns, on_match=addSpan)

        # Create a matcher using our set of date span patterns
        date_patterns = getSpanPatterns('dates')
        self.date_matcher = Matcher(nlp.vocab, validate=True)
        self.date_matcher.add(key, date_patterns, on_match=tagDateSpan)

    def __call__(self, doc):

        doc.spans[self.key] = []

        # Tag date spans up front so they are respected
        self.date_matcher(doc)

        # Add the matched spans when the doc is processed
        self.matcher(doc)

        doc.spans[self.key] = filter_spans(doc.spans[self.key])
        return doc


modifier_deps = set(['amod', 'nummod', 'nmod', 'compound'])

def addSpan(_matcher, doc, i, matches):
    """ Callback to run on pattern matches. """

    match_id, start, end = matches[i]
    match_key = doc.vocab.strings[match_id]

    span = doc[start:end]

    # logic for date spans
    if any(token._.matchers_is_date for token in span):

        # Dont consider any span that only partially overlaps with a date
        if start > 0 and doc[start-1]._.matchers_is_date:
            return

        if end < len(doc) and doc[end]._.matchers_is_date:
            return

        # Otherwise, only add dates behaving as modifiers
        if not any(d in modifier_deps for d in getInboundDependencies(span)):
            return

    doc.spans[match_key].append(span)


def tagDateSpan(_matcher, doc, i, matches):
    """ Callback to tag date matches for later use. """

    _match_id, start, end = matches[i]
    for token in doc[start:end]:
        token._.matchers_is_date = True
