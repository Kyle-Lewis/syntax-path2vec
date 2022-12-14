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

from pathvecs.matchers.triples.patterns import get_triple_patterns
# from triples.matchers.relative_pronouns import (RelativePronounMatcher)

@Language.factory('triple_matcher')
def createTripleMatcherComponent(nlp, name):
    return TripleMatcher(nlp)

FRAME_PATTERNS = get_triple_patterns()

class TripleMatcher:
    """ A spacy DependencyMatcher object wrapped as a pipeline component

    Attributes:
        matcher: A spacy.Matcher component with patterns loaded on init
    """

    def __init__(self, nlp, patterns=None):

        # Create a matcher using our set of triple patterns
        self.matcher = DependencyMatcher(nlp.vocab, validate=True)

        if patterns is not None:
            for pattern_name in patterns:
                pattern_classes = FRAME_PATTERNS[pattern_name]
                patterns = [klass.pattern for klass in pattern_classes]
                self.matcher.add(pattern_name, patterns, on_match=addTriple)
        else:
            for pattern_name, pattern_classes in FRAME_PATTERNS.items():
                patterns = [klass.pattern for klass in pattern_classes]
                self.matcher.add(pattern_name, patterns, on_match=addTriple)

    def __call__(self, doc):

        # Add the matched triples when the doc is processed
        self.matcher(doc)
        return doc


pattern_to_verb_type = {
    'being_verb': 'being',
    'active_transitive_verb': 'transitive',
    'active_transitive_verb_conjuncts': 'transitive',
    'passive_transitive_verb': 'transitive',
    'passive_transitive_verb_conjuncts': 'transitive',
    'intransitive_verb_prep': 'intransitive',
}

def addTriple(_matcher, doc, i, matches):

    match_id, match_token_ids = matches[i]
    pattern_name = doc.vocab.strings[match_id]
    pattern_class = FRAME_PATTERNS[pattern_name][0]
    pattern = pattern_class.pattern

    verb_type = pattern_to_verb_type.get(pattern_name, None)

    if verb_type is not None:
        verb_token = doc[match_token_ids[0]]

        if verb_token._.verb_type is not None:
            return

        verb_token._.verb_type = verb_type

    # Build up combinations of conjunct triples
    conjunct_matches = [[ti] for ti in match_token_ids]
    for tidx in range(len(match_token_ids)):
        if pattern[tidx].get('CONJUNCTS', False):
            for conjunct in doc[match_token_ids[tidx]].conjuncts:
                conjunct_matches[tidx].append(conjunct.i)

    # Use each pattern class's fill() method to generate the triple
    conjunct_matches = itertools.product(*conjunct_matches)
    for match in conjunct_matches:
        triple = pattern_class.fill(doc, match)
        doc._.triples.append(triple)
