from spacy.tokens import Doc, Token

from pathvecs.matchers.triples.triples import TripleMatcher
from pathvecs.matchers.triples.relative_pronouns import (
	RelativePronounMatcher)

if not Doc.has_extension('triples'):
    Doc.set_extension('triples', default=[])

if not Token.has_extension('verb_type'):
    Token.set_extension('verb_type', default=None)

if not Token.has_extension('antecedent'):
    Token.set_extension('antecedent', default=None)
