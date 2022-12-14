""" A pattern matcher for nominal spans registered as a spaCy pipe component.

Typical usage example:

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('nominal_spans')

    doc = nlp("Alice saw Bob Lastname at the park.")
    print(doc.spans['nominals'])

    > [Alice, Bob Lastname, park]
"""

from spacy.matcher import Matcher
from spacy.language import Language
from spacy.util import filter_spans

from pathvecs.matchers.spans.patterns import getSpanPatterns
from pathvecs.matchers.utils import getInboundDependencies

@Language.factory('nominal_spans')
def createNominalMatcherComponent(nlp, name):
    return NominalSpanMatcher(nlp)


class NominalSpanMatcher:
    """ A spacy Matcher object wrapped as a pipeline component

    Attributes:
        key: Where the matched spans will be saved to (doc.spans[key])
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, key='nominals'):

        self.key = key

        # Create a matcher using our set of nominal span patterns
        patterns = getSpanPatterns('nominals')
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


# Lemmas which always indicate speech, e.g., 'write' is not included because
#   Bob wrote "hey Alice, how's it goin?"
#   Bob wrote "The Book about Alice".

SPEECH_VERB_LEMMAS = ['say', 'tell', 'assert', 'state', 'confess',
    'claim', 'express', 'admit', 'ask']


nominal_deps = set([
    'nsubj', 'nsubjpass', 'dobj', 'pobj', 'agent', 'appos', 'dative'])

def addSpan(_matcher, doc, i, matches):
    """ Callback to run on pattern matches. """

    match_id, start, end = matches[i]
    match_key = doc.vocab.strings[match_id]
    length = end - start

    # special treatment cases for quoted spans
    if doc[start].tag_ == "``" and doc[end - 1].tag_ == "''":

        # If we are adding the quoted span, remove the quotes
        start += 1
        end -= 1


        num_titlecase = 0
        for t in doc[start:end]:

            if t.text.istitle():
                num_titlecase += 1

            # *dont* detect quoted spans that are speech
            if t.head.pos_ == 'VERB' and t.head.lemma_ in SPEECH_VERB_LEMMAS:
                return

            # avoid going from the start, to the end of a second quotation
            if t.tag_ in ["''", "``"]:
                return

        # Require a good amount of titlecasing to allow big spans
        total = end - start
        if num_titlecase / (total) < 0.5 and total > 5:
            return

    # TODO factor data
    # special treatment case for compound quantifiers as heads
    elif length > 1 and all(t.tag_ in ['NN', 'NNS'] for t in doc[start:end-1]):
        if doc[end - 1].lemma_ in ['level', 'concentration']:
            end -= 1

    span = doc[start:end]

    # logic for date spans
    if any(token._.matchers_is_date for token in span):

        # Dont consider any span that only partially overlaps with a date
        if start > 0 and doc[start-1]._.matchers_is_date:
            return

        if end < len(doc) and doc[end]._.matchers_is_date:
            return

        # Otherwise, only add dates behaving as nominals
        if not any(d in nominal_deps for d in getInboundDependencies(span)):
            return

    doc.spans[match_key].append(span)


def tagDateSpan(_matcher, doc, i, matches):
    """ Callback to tag date matches for later use. """

    _match_id, start, end = matches[i]
    for token in doc[start:end]:
        token._.matchers_is_date = True
