from spacy.tokens.token import Token

from pathvecs.matchers.spans.nominals import NominalSpanMatcher
from pathvecs.matchers.spans.modifiers import ModifierSpanMatcher

# Register all token extensions expected within this module

if not Token.has_extension('matchers_left_text'):
    get_left_text = lambda t: t.nbor(-1).text if t.i > 0 else ''
    Token.set_extension('matchers_left_text', getter=get_left_text)


if not Token.has_extension('matchers_right_text'):
    get_right_text = lambda t: t.nbor(1).text if t.i < len(t.doc) - 1 else ''
    Token.set_extension('matchers_right_text', getter=get_right_text)


if not Token.has_extension('matchers_is_date'):
    Token.set_extension('matchers_is_date', default=False)
