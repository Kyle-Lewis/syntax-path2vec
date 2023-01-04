# pylint: disable=line-too-long

import pytest
from spacy.tokens import Doc, Span
from spacy.language import Language

from pathvecs.matchers import NominalSpanMatcher

params = [
({
    'description': 'Single token singular common nouns should be detected as spans',
    'words': ['The', 'dog', 'barked', '.'],
    'lemmas': ['the', 'dog', 'bark', '.'],
    'pos': ['DET', 'NOUN', 'VERB', 'PUNCT'],
    'tags': ['DT', 'NN', 'VBD', '.'],
    'deps': ['det', 'nsubj', 'ROOT', 'punct'],
    'heads': [1, 2, 2, 2],
    'gold_spans': [(1, 2)]
}),
({
    'description': 'Single token plural common nouns should be detected as spans',
    'words': ['The', 'dogs', 'barked', '.'],
    'lemmas': ['the', 'dog', 'bark', '.'],
    'pos': ['DET', 'NOUN', 'VERB', 'PUNCT'],
    'tags': ['DT', 'NNS', 'VBD', '.'],
    'deps': ['det', 'nsubj', 'ROOT', 'punct'],
    'heads': [1, 2, 2, 2],
    'gold_spans': [(1, 2)],
}),
({
    'description': 'Adjectival modifiers should *not* be added to noun phrase spans',
    'words': ['The', 'black', 'dog', 'barked', '.'],
    'lemmas': ['the', 'black', 'dog', 'bark', '.'],
    'pos': ['DET', 'ADJ', 'NOUN', 'VERB', 'PUNCT'],
    'tags': ['DT', 'JJ', 'NN', 'VBD', '.'],
    'deps': ['det', 'amod', 'nsubj', 'ROOT', 'punct'],
    'heads': [2, 2, 3, 3, 3],
    'gold_spans': [(2, 3)],
}),
({
    'description': 'Multi token common noun phrases should be greedily detected without overlaps',
    'words': ['The', 'police', 'dog', 'barked', '.'],
    'lemmas': ['the', 'police', 'dog', 'bark', '.'],
    'pos': ['DET', 'NOUN', 'NOUN', 'VERB', 'PUNCT'],
    'tags': ['DT', 'NN', 'NN', 'VBD', '.'],
    'deps': ['det', 'compound', 'nsubj', 'ROOT', 'punct'],
    'heads': [2, 2, 3, 3, 3],
    'gold_spans': [(1, 3)]
}),
({
    'description': 'Single token proper nouns should be detected as spans',
    'words': ['Alice', 'cheered', '.'],
    'lemmas': ['Alice', 'cheer', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT'],
    'tags': ['NNP', 'VBD', '.'],
    'deps': ['nsubj', 'ROOT', 'punct'],
    'heads': [1, 1, 1],
    'gold_spans': [(0, 1)],
}),
({
    'description': 'Multi token proper noun phrases should be greedily detected without overlaps',
    'words': ['New', 'York', 'is', 'great', '.'],
    'lemmas': ['New', 'York', 'be', 'great', '.'],
    'pos': ['PROPN', 'PROPN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['NNP', 'NNP', 'VBZ', 'JJ', '.'],
    'deps': ['compound', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 2, 2, 2, 2],
    'gold_spans': [(0, 2)],
}),
({
    'description': "Proper adjectives should be added to proper noun spans",
    'words': ['Silly', 'Symphonies', 'was', 'great', '.'],
    'lemmas': ['silly', 'Symphonies', 'be', 'great', '.'],
    'pos': ['ADJ', 'PROPN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['JJ', 'NNPS', 'VBD', 'JJ', '.'],
    'deps': ['amod', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 2, 2, 2, 2],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 2)]
}),

##### compounds with nominalized verbs
## compounds between mixed noun types should indicate separate entity spans
({
    'description': 'Compound phrases with a nominalized verb at their head should be detected as one span',
    'words': ['Trees', 'are', 'O2', 'producers', '.'],
    'lemmas': ['tree', 'be', 'O2', 'producer', '.'],
    'pos': ['NOUN', 'AUX', 'PROPN', 'NOUN', 'PUNCT'],
    'tags': ['NNS', 'VBP', 'NNP', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'compound', 'attr', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'gold_spans': [(2, 4),(0, 1)],
}),
({
    'description': "Multi token common noun phrases should be greedily "
        "detected without overlaps, and the presence of a nominalized verb "
        "should not change this",
    'words': ['Trees', 'are', 'oxygen', 'producers', '.'],
    'lemmas': ['tree', 'be', 'oxygen', 'producer', '.'],
    'pos': ['NOUN', 'AUX', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNS', 'VBP', 'NN', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'compound', 'attr', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'gold_spans': [(2, 4),(0, 1)],
}),

##### compounds with quantifiers
({
    'description': 'As an exception to the contiguously matched case rule, a small set of quantifier nouns should be detected as separate spans',
    'words': ['That', 'increased', 'protein', 'levels', '.'],
    'lemmas': ['that', 'increase', 'protein', 'level', '.'],
    'pos': ['DET', 'VERB', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'VBN', 'NN', 'NNS', '.'],
    'deps': ['det', 'amod', 'compound', 'ROOT', 'punct'],
    'heads': [3, 3, 3, 3, 3],
    'gold_spans': [(2, 3), (3, 4)],
}),

##### phrases around possessives
({
    'description': 'Common nouns divided by possessives should be detected as separate spans',
    'words': ['The', 'dog', "'s", 'collar', 'is', 'grey', '.'],
    'lemmas': ['the', 'dog', "'s", 'collar', 'be', 'grey', '.'],
    'pos': ['DET', 'NOUN', 'PART', 'NOUN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['DT', 'NN', 'POS', 'NN', 'VBZ', 'JJ', '.'],
    'deps': ['det', 'poss', 'case', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 3, 1, 4, 4, 4, 4],
    'gold_spans': [(1, 2),(3, 4)],
}),
({
    'description': 'Proper nouns divided by possessives should be detected as separate spans',
    'words': ['Brazil', "'s", 'Health', 'Ministry', '.'],
    'lemmas': ['Brazil', "'s", 'Health', 'Ministry', '.'],
    'pos': ['PROPN', 'PART', 'PROPN', 'PROPN', 'PUNCT'],
    'tags': ['NNP', 'POS', 'NNP', 'NNP', '.'],
    'deps': ['poss', 'case', 'compound', 'ROOT', 'punct'],
    'heads': [3, 0, 3, 3, 3],
    'gold_spans': [(0, 1), (2, 4)],
}),
({
    'description': 'Proper nouns divided by possessives are typically detected as separate spans, but make an exception for the special case of "\'s Day"',
    'words': ['Saint', 'Patrick', "'s", 'Day', 'was', 'fun', '.'],
    'lemmas': ['Saint', 'Patrick', "'s", 'Day', 'be', 'fun', '.'],
    'pos': ['PROPN', 'PROPN', 'PART', 'PROPN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['NNP', 'NNP', 'POS', 'NNP', 'VBD', 'JJ', '.'],
    'deps': ['compound', 'poss', 'case', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 3, 1, 4, 4, 4, 4],
    'gold_spans': [(0, 4)],
}),
({
    'description': 'Mixed noun classes divided by possessives should be detected as separate spans',
    'words': ['Bob', "'s", 'dog', 'is', 'grey', '.'],
    'lemmas': ['Bob', "'s", 'dog', 'be', 'grey', '.'],
    'pos': ['PROPN', 'PART', 'NOUN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['NNP', 'POS', 'NN', 'VBZ', 'JJ', '.'],
    'deps': ['poss', 'case', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [2, 0, 3, 3, 3, 3],
    'gold_spans': [(0, 1),(2, 3)],
}),
({
    'description': 'Mixed noun classes divided by possessives should be detected as separate spans',
    'words': ['That', 'kid', "'s", 'Tesla', 'is', 'sneaky', '.'],
    'lemmas': ['that', 'kid', "'s", 'Tesla', 'be', 'sneaky', '.'],
    'pos': ['DET', 'NOUN', 'PART', 'PROPN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['DT', 'NN', 'POS', 'NNP', 'VBZ', 'JJ', '.'],
    'deps': ['det', 'poss', 'case', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 3, 1, 4, 4, 4, 4],
    'gold_spans': [(1, 2),(3, 4)],
}),
({
    'description': 'Possessive pronouns are detected as separate spans',
    'words': ['His', 'cat', 'is', 'grey', '.'],
    'lemmas': ['his', 'cat', 'be', 'grey', '.'],
    'pos': ['PRON', 'NOUN', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['PRP$', 'NN', 'VBZ', 'JJ', '.'],
    'deps': ['poss', 'nsubj', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 2, 2, 2, 2],
    'gold_spans': [(0, 1),(1, 2)],
}),

##### pronouns
({
    'description': 'Human pronouns are detected as spans',
    'words': ['Then', 'she', 'won', '!'],
    'lemmas': ['then', 'she', 'win', '!'],
    'pos': ['ADV', 'PRON', 'VERB', 'PUNCT'],
    'tags': ['RB', 'PRP', 'VBD', '.'],
    'deps': ['advmod', 'nsubj', 'ROOT', 'punct'],
    'heads': [2, 2, 2, 2],
    'gold_spans': [(1, 2)],
}),
({
    'description': 'Non-human pronouns are detected as spans',
    'words': ['Then', 'it', 'sank', '.'],
    'lemmas': ['then', 'it', 'sink', '.'],
    'pos': ['ADV', 'PRON', 'VERB', 'PUNCT'],
    'tags': ['RB', 'PRP', 'VBD', '.'],
    'deps': ['advmod', 'nsubj', 'ROOT', 'punct'],
    'heads': [2, 2, 2, 2],
    'gold_spans': [(1, 2)],
}),

##### parentheticals
({
    'description': 'Would-be contiguous proper noun spans divided by parentheticals are detected as separate spans',
    'words': ['General', 'Electric', '(', 'GE', ')', 'is', 'great', '.'],
    'lemmas': ['General', 'Electric', '(', 'GE', ')', 'be', 'great', '.'],
    'pos': ['PROPN', 'PROPN', 'PUNCT', 'PROPN', 'PUNCT', 'AUX', 'ADJ', 'PUNCT'],
    'tags': ['NNP', 'NNP', '-LRB-', 'NNP', '-RRB-', 'VBZ', 'JJ', '.'],
    'deps': ['compound', 'nsubj', 'punct', 'appos', 'punct', 'ROOT', 'acomp', 'punct'],
    'heads': [1, 5, 1, 1, 1, 5, 5, 5],
    'gold_spans': [(0, 2),(3, 4)],
}),
({
    'description': 'Would-be contiguous common noun spans divided by parentheticals are detected as separate spans',
    'words': ['dog', '(', 'canus', ')'],
    'lemmas': ['dog', '(', 'canus', ')'],
    'pos': ['NOUN', 'PUNCT', 'NOUN', 'PUNCT'],
    'tags': ['NN', '-LRB-', 'NN', '-RRB-'],
    'deps': ['ROOT', 'punct', 'appos', 'punct'],
    'heads': [0, 0, 0, 0],
    'gold_spans': [(0, 1),(2, 3)],
}),

##### non-english prepositions in proper nouns
({
    'description': "Would-be contiguous proper noun spans divided by a foreign language prepositions should be detected as single spans.",
    'words': ['Banca', 'Nazionale', 'del', 'Lavoro', '.'],
    'lemmas': ['Banca', 'Nazionale', 'del', 'Lavoro', '.'],
    'pos': ['PROPN', 'PROPN', 'X', 'PROPN', 'PUNCT'],
    'tags': ['NNP', 'NNP', 'FW', 'NNP', '.'],
    'deps': ['compound', 'nmod', 'compound', 'ROOT', 'punct'],
    'heads': [3, 3, 3, 3, 3],
    'spaces': [' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 4)]
}),

##### quotations
({
    'description': 'Quotes that are speech acts should *not* be detected as spans',
    'words': ['Bob', 'asked', "'", 'has', 'anybody', 'seen', 'Alice', '?', "'", '.'],
    'lemmas': ['Bob', 'ask', "'", 'have', 'anybody', 'see', 'Alice', '?', "'", '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'AUX', 'PRON', 'VERB', 'PROPN', 'PUNCT', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'VBZ', 'NN', 'VBN', 'NNP', '.', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'aux', 'nsubj', 'ccomp', 'dobj', 'punct', 'punct', 'punct'],
    'heads': [1, 1, 1, 5, 5, 1, 5, 5, 5, 1],
    'spaces': [' ', ' ', '', ' ', ' ', ' ', '', '', '', ''],
    'gold_spans': [(0, 1), (4, 5), (6, 7)],
}),
({
    'description': 'Title cased spans in quotes are detected as (unquoted) spans',
    'words': ['Alice', 'wrote', '"', 'Mountain', 'Climbing', '"', '.'],
    'lemmas': ['Alice', 'write', '"', 'Mountain', 'Climbing', '"', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'PROPN', 'PROPN', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'NNP', 'NNP', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'compound', 'dobj', 'punct', 'punct'],
    'heads': [1, 1, 1, 4, 1, 1, 1],
    'gold_spans': [(3, 5),(0, 1)],
}),
({
    'description': 'Quoted span detection is independant of the quote characters used',
    'words': ['Alice', 'wrote', '“', 'Mountain', 'Climbing', '”', '.'],
    'lemmas': ['Alice', 'write', '"', 'Mountain', 'Climbing', '"', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'PROPN', 'PROPN', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'NNP', 'NNP', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'compound', 'dobj', 'punct', 'punct'],
    'heads': [1, 1, 1, 4, 1, 1, 1],
    'gold_spans': [(3, 5),(0, 1)],
}),
({
    'description': 'Partially title cased spans in quotes are detected as (unquoted) spans',
    'words': ['Alice', 'wrote', '"', 'Climbing', 'into', 'the', 'Mountains', '"', '.'],
    'lemmas': ['Alice', 'write', '"', 'climb', 'into', 'the', 'Mountains', '"', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'VERB', 'ADP', 'DET', 'PROPN', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'VBG', 'IN', 'DT', 'NNPS', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'xcomp', 'prep', 'det', 'pobj', 'punct', 'punct'],
    'heads': [1, 1, 1, 1, 3, 6, 4, 3, 1],
    'gold_spans': [(3, 7),(0, 1)]
}),
({
    'description': 'When a quoted span is detected, no nested spans of any class of noun should be allowed (common & proper nouns)',
    'words': ['Bob', 'wrote', '"', 'Mountains', 'with', 'snow', '"', '.'],
    'lemmas': ['Bob', 'write', '"', 'Mountains', 'with', 'snow', '"', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'PROPN', 'ADP', 'NOUN', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'NNPS', 'IN', 'NN', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'dobj', 'prep', 'pobj', 'punct', 'punct'],
    'heads': [1, 1, 1, 1, 3, 4, 1, 1],
    'gold_spans': [(3, 6),(0, 1)]
}),
({
    'description': 'When a quoted span is detected, no nested spans of any class of noun should be allowed (pronouns)',
    'words': ['Alice', 'published', '"', 'We', 'Want', 'Answers', '!', '"', '.'],
    'lemmas': ['Alice', 'publish', '"', 'we', 'want', 'answer', '!', '"', '.'],
    'pos': ['PROPN', 'VERB', 'PUNCT', 'PRON', 'VERB', 'NOUN', 'PUNCT', 'PUNCT', 'PUNCT'],
    'tags': ['NNP', 'VBD', '``', 'PRP', 'VBP', 'NNS', '.', "''", '.'],
    'deps': ['nsubj', 'ROOT', 'punct', 'nsubj', 'ccomp', 'dobj', 'punct', 'punct', 'punct'],
    'heads': [1, 1, 4, 4, 1, 4, 4, 1, 1],
    'gold_spans': [(3, 7),(0, 1)],
}),

##### hyphenation
({
    'description': 'Common noun phrases divided by hyphens are detected as single spans',
    'words': ['The', 'city', '-', 'state', 'of', 'Carthage', '.'],
    'lemmas': ['the', 'city', '-', 'state', 'of', 'Carthage', '.'],
    'pos': ['DET', 'NOUN', 'PUNCT', 'NOUN', 'ADP', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NN', 'HYPH', 'NN', 'IN', 'NNP', '.'],
    'deps': ['det', 'compound', 'punct', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [3, 3, 3, 3, 3, 4, 3],
    'spaces': [' ', '', '', ' ', ' ', '', ''],
    'gold_spans': [(1, 4),(5, 6)]
}),
({
    'description': 'Nominal phrases divided by multiple hyphens are detected as single spans',
    'words': ['Alice', "'s", 'son', '-', 'in', '-', 'law', 'is', 'Bob', '.'],
    'lemmas': ['Alice', "'s", 'son', '-', 'in', '-', 'law', 'be', 'Bob', '.'],
    'pos': ['PROPN', 'PART', 'NOUN', 'PUNCT', 'ADP', 'PUNCT', 'NOUN', 'AUX', 'PROPN', 'PUNCT'],
    'tags': ['NNP', 'POS', 'NN', 'HYPH', 'IN', 'HYPH', 'NN', 'VBZ', 'NNP', '.'],
    'deps': ['poss', 'case', 'nsubj', 'punct', 'prep', 'punct', 'pobj', 'ROOT', 'attr', 'punct'],
    'heads': [2, 0, 7, 2, 2, 4, 4, 7, 7, 7],
    'spaces': ['', ' ', '', '', '', '', ' ', ' ', '', ''],
    'gold_spans': [(2, 7),(0, 1),(8, 9)]
}),
({
    'description': 'Proper noun phrases divided by hyphens are detected as single spans',
    'words': ['Anwar', 'al', '-', 'Awlaki', '.'],
    'lemmas': ['Anwar', 'al', '-', 'Awlaki', '.'],
    'pos': ['PROPN', 'PROPN', 'PUNCT', 'PROPN', 'PUNCT'],
    'tags': ['NNP', 'NNP', 'HYPH', 'NNP', '.'],
    'deps': ['compound', 'compound', 'punct', 'ROOT', 'punct'],
    'heads': [3, 3, 3, 3, 3],
    'spaces': [' ', '', '', '', ''],
    'gold_spans': [(0, 4)],
}),
({
    'description': 'Hyphen joined phrases are detected despite a lack of \'HYPH\' tags, which are inconsistent for characters like em-dash',
    'words': ['The', 'stop', 'at', 'North', 'Street', '–', 'Washington', 'Heights', '.'],
    'lemmas': ['the', 'stop', 'at', 'North', 'Street', '–', 'Washington', 'Heights', '.'],
    'pos': ['DET', 'NOUN', 'ADP', 'PROPN', 'PROPN', 'PUNCT', 'PROPN', 'PROPN', 'PUNCT'],
    'tags': ['DT', 'NN', 'IN', 'NNP', 'NNP', ':', 'NNP', 'NNP', '.'],
    'deps': ['det', 'ROOT', 'prep', 'compound', 'pobj', 'punct', 'compound', 'appos', 'punct'],
    'heads': [1, 1, 1, 4, 2, 1, 7, 1, 1],
    'spaces': [' ', ' ', ' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(3, 8),(1, 2)],
}),
# ({
#     'description': 'Abbreviated ordinals are included in the spans for hyphen joined phrases',
#     'words': ['The', 'stop', 'at', '168th', 'Street', '–', 'Washington', 'Heights', '.'],
#     'lemmas': ['the', 'stop', 'at', '168th', 'Street', '–', 'Washington', 'Heights', '.'],
#     'pos': ['DET', 'NOUN', 'ADP', 'ADJ', 'PROPN', 'PUNCT', 'PROPN', 'PROPN', 'PUNCT'],
#     'tags': ['DT', 'NN', 'IN', 'JJ', 'NNP', ':', 'NNP', 'NNP', '.'],
#     'deps': ['det', 'ROOT', 'prep', 'amod', 'pobj', 'punct', 'compound', 'appos', 'punct'],
#     'heads': [1, 1, 1, 4, 2, 1, 7, 1, 1],
#     'spaces': [' ', ' ', ' ', ' ', '', '', ' ', '', ''],
#     'gold_spans': [(3, 8),(1, 2)],
# }),
({
    'description': "The rightmost noun of a hyphenated modifier span should not be included in the head nouns span.",
    'words': ['Alice', 'prefers', 'live', '-', 'action', 'movies', '.'],
    'lemmas': ['Alice', 'prefer', 'live', '-', 'action', 'movie', '.'],
    'pos': ['PROPN', 'VERB', 'ADJ', 'PUNCT', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBZ', 'JJ', 'HYPH', 'NN', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'amod', 'punct', 'compound', 'dobj', 'punct'],
    'heads': [1, 1, 4, 4, 5, 1, 1],
    'spaces': [' ', ' ', '', '', ' ', '', ''],
    'gold_spans': [(5, 6),(0, 1)]
}),

##### number hyphenation
# NOTE (Kyle)
# I've decided on these rules for compound ~modifying nouns with hyphenation for now.
# I think they tend to act as modifiers, which means the relationships below
# would be picked up as adjective edges, as opposed to compound edges.
# This is somewhat arbitrary
#
# "18-year history"  -> mod(18-year)     nom(history)
# "third-party apps" -> mod(third-party) nom(apps)
# "full-page adds"   -> mod(full-page)   nom(adds)
#
# With a special case for hyphenated fractions as nominals:
# "one-tenth [of]"   -> nom(one-tenth)

({
    'description': 'Fractions',
    'words': ['Bob', 'ate', 'one', '-', 'tenth', 'of', 'the', 'apples', '.'],
    'lemmas': ['Bob', 'eat', 'one', '-', 'tenth', 'of', 'the', 'apple', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'PUNCT', 'NOUN', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'HYPH', 'NN', 'IN', 'DT', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'nummod', 'punct', 'dobj', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 4, 4, 1, 4, 7, 5, 1],
    'spaces': [' ', ' ', '', '', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1),(2, 5),(7, 8)],
}),

##### punctuation
({
    'description': 'Would-be contiguous proper noun spans ending in a comma '\
                   'separated abbreviation should be detected as single spans.',
    'words': ['Bob', 'founded', 'Bob', 'Technologies', ',', 'Inc.'],
    'lemmas': ['Bob', 'found', 'Bob', 'Technologies', ',', 'Inc.'],
    'pos': ['PROPN', 'VERB', 'PROPN', 'PROPN', 'PUNCT', 'PROPN'],
    'tags': ['NNP', 'VBD', 'NNP', 'NNP', ',', 'NNP'],
    'deps': ['nsubj', 'ROOT', 'compound', 'dobj', 'punct', 'appos'],
    'heads': [1, 1, 3, 1, 3, 3],
    'spaces': [' ', ' ', ' ', '', ' ', ''],
    'gold_spans': [(2, 6),(0, 1)]
}),

##### numbers
# Generally, numbers modifying nouns should not be picked up in noun phrases
# and are instead picked up as modifier spans.
# However, there are a few exceptions where they should be detected.

({
    'description': 'Generally, numbers modifying nouns should not be picked up in noun phrase spans',
    'words': ['Alice', 'bought', '3', 'apples', '.'],
    'lemmas': ['Alice', 'buy', '3', 'apple', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'nummod', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'gold_spans': [(0, 1),(3, 4)],
}),
({
    'description': 'Modifying numeral-abbreviated ordinal numbers are included in common noun phrase spans.',
    'words': ['Alice', 'won', '1st', 'place', '.'],
    'lemmas': ['Alice', 'win', '1st', 'place', '.'],
    'pos': ['PROPN', 'VERB', 'ADJ', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'JJ', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'amod', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'gold_spans': [(0, 1),(2, 4)],
}),
({
    'description': 'Modifying numeral-abbreviated ordinal numbers are included in proper noun phrase spans.',
    'words': ['They', 'fought', 'in', 'the', '1st', 'World', 'War', '.'],
    'lemmas': ['they', 'fight', 'in', 'the', '1st', 'World', 'War', '.'],
    'pos': ['PRON', 'VERB', 'ADP', 'DET', 'ADJ', 'PROPN', 'PROPN', 'PUNCT'],
    'tags': ['PRP', 'VBD', 'IN', 'DT', 'JJ', 'NNP', 'NNP', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'det', 'amod', 'compound', 'pobj', 'punct'],
    'heads': [1, 1, 1, 6, 6, 6, 2, 1],
    'gold_spans': [(4, 7),(0, 1)],
}),

({
    'description': "Numbers should be detected as nominal spans if they are subjects, objects, or prepositional objects.",
    'words': ['Bob', 'bought', '2', 'of', 'the', 'apples', '.'],
    'lemmas': ['Bob', 'buy', '2', 'of', 'the', 'apple', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'IN', 'DT', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 1, 2, 5, 3, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1),(2, 3),(5, 6)]
}),
({
    'description': "Numbers should be detected as nominal spans if they are subjects, objects, or prepositional objects.",
    'words': ['Of', 'all', 'the', 'witnesses', ',', 'three', 'remembered', 'the', 'details', '.'],
    'lemmas': ['of', 'all', 'the', 'witness', ',', 'three', 'remember', 'the', 'detail', '.'],
    'pos': ['ADP', 'DET', 'DET', 'NOUN', 'PUNCT', 'NUM', 'VERB', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['IN', 'PDT', 'DT', 'NNS', ',', 'CD', 'VBD', 'DT', 'NNS', '.'],
    'deps': ['prep', 'predet', 'det', 'pobj', 'punct', 'nsubj', 'ROOT', 'det', 'dobj', 'punct'],
    'heads': [6, 3, 3, 0, 6, 6, 6, 8, 6, 6],
    'spaces': [' ', ' ', ' ', '', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(3, 4),(5, 6),(8, 9)]
}),
({
    'description': "Numbers should be detected as nominal spans if they are subjects, objects, or prepositional objects.",
    'words': ['Alice', 'got', '2', 'out', 'of', '3', '.'],
    'lemmas': ['Alice', 'get', '2', 'out', 'of', '3', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'ADP', 'ADP', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'IN', 'IN', 'CD', '.'],
    'deps': ['nsubj', 'ROOT', 'dobj', 'prep', 'prep', 'pobj', 'punct'],
    'heads': [1, 1, 1, 1, 3, 4, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1),(2, 3), (5, 6)]
}),

({
    'description': "If detected as a nominal span, numbers should include currency markers.",
    'words': ['Alice', 'has', '$', '3', '.'],
    'lemmas': ['Alice', 'have', '$', '3', '.'],
    'pos': ['PROPN', 'VERB', 'SYM', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBZ', '$', 'CD', '.'],
    'deps': ['nsubj', 'ROOT', 'nmod', 'dobj', 'punct'],
    'heads': [1, 1, 3, 1, 1],
    'spaces': [' ', ' ', '', '', ''],
    'gold_spans': [(0, 1), (2, 4)],
}),
({
    'description': "If detected as a nominal span, numbers should include multi token currency words.",
    'words': ['Bob', 'lost', '£', '330', 'million', '.'],
    'lemmas': ['Bob', 'lose', '£', '330', 'million', '.'],
    'pos': ['PROPN', 'VERB', 'SYM', 'NUM', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', '$', 'CD', 'CD', '.'],
    'deps': ['nsubj', 'ROOT', 'quantmod', 'compound', 'dobj', 'punct'],
    'heads': [1, 1, 4, 4, 1, 1],
    'spaces': [' ', ' ', '', ' ', '', ''],
    'gold_spans': [(0, 1), (2, 5)]
}),
({
    'description': "Numbers should be included as spans for percentages.",
    'words': ['Alice', 'wrote', '50', '%', 'of', 'the', 'tests', '.'],
    'lemmas': ['Alice', 'write', '50', '%', 'of', 'the', 'test', '.'],
    'pos': ['PROPN', 'VERB', 'NUM', 'NOUN', 'ADP', 'DET', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'CD', 'NN', 'IN', 'DT', 'NNS', '.'],
    'deps': ['nsubj', 'ROOT', 'nummod', 'dobj', 'prep', 'det', 'pobj', 'punct'],
    'heads': [1, 1, 3, 1, 3, 6, 4, 1],
    'spaces': [' ', ' ', '', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1),(2, 4),(6, 7)]
}),
({
    'description': "The percent sign should not be included in a nominal (unless it is the head token)",
    'words': ['A', '32', '%', 'rate', 'increase', '.'],
    'lemmas': ['a', '32', '%', 'rate', 'increase', '.'],
    'pos': ['DET', 'NUM', 'NOUN', 'NOUN', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'CD', 'NN', 'NN', 'NN', '.'],
    'deps': ['det', 'nummod', 'compound', 'compound', 'ROOT', 'punct'],
    'heads': [4, 2, 4, 4, 4, 4],
    'spaces': [' ', '', ' ', ' ', '', ''],
    'gold_spans': [(3, 5)]
}),
({
    'description': 'Numbers should be included in proper noun spans when they are not leftmost.',
    'words': ['The', 'album', 'made', 'it', 'to', 'Billboard', 'Hot', '100', '.'],
    'lemmas': ['the', 'album', 'make', 'it', 'to', 'Billboard', 'Hot', '100', '.'],
    'pos': ['DET', 'NOUN', 'VERB', 'PRON', 'ADP', 'PROPN', 'PROPN', 'NUM', 'PUNCT'],
    'tags': ['DT', 'NN', 'VBD', 'PRP', 'IN', 'NNP', 'NNP', 'CD', '.'],
    'deps': ['det', 'nsubj', 'ROOT', 'dobj', 'prep', 'compound', 'pobj', 'nummod', 'punct'],
    'heads': [1, 2, 2, 2, 2, 6, 4, 6, 2],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(5, 8),(1, 2),(3, 4)]
}),

##### Numbers and dates
({
    'description': "Numbers should be included as parts of date spans with token(s) denoting era, such as 'A.D.'",
    'words': ['They', 'met', 'in', '327', 'B.C.'],
    'lemmas': ['they', 'meet', 'in', '327', 'B.C.'],
    'pos': ['PRON', 'VERB', 'ADP', 'NUM', 'PROPN'],
    'tags': ['PRP', 'VBD', 'IN', 'CD', 'NNP'],
    'deps': ['nsubj', 'ROOT', 'prep', 'nummod', 'pobj'],
    'heads': [1, 1, 1, 4, 2],
    'gold_spans': [(3, 5), (0, 1)],
}),
({
    'description': "Numbers should be detected if they represent a date in YYYY form.",
    'words': ['Bob', 'was', 'born', 'in', '1995', '.'],
    'lemmas': ['Bob', 'be', 'bear', 'in', '1995', '.'],
    'pos': ['PROPN', 'AUX', 'VERB', 'ADP', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'VBN', 'IN', 'CD', '.'],
    'deps': ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [2, 2, 2, 2, 3, 2],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1), (4, 5)]
}),
({
    'description': 'Nominal dates should be detected in DD Month YYYY form.',
    'words': ['Alice', 'was', 'born', 'on', '18', 'May', '2022', '.'],
    'lemmas': ['Alice', 'be', 'bear', 'on', '18', 'May', '2022', '.'],
    'pos': ['PROPN', 'AUX', 'VERB', 'ADP', 'NUM', 'PROPN', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'VBN', 'IN', 'CD', 'NNP', 'CD', '.'],
    'deps': ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'nummod', 'pobj', 'nummod', 'punct'],
    'heads': [2, 2, 2, 2, 5, 3, 5, 2],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 7),(0, 1)]
}),
({
    'description': 'Nominal dates should be detected in Month DD YYYY form.',
    'words': ['Bob', 'was', 'born', 'on', 'June', '16', '2022', '.'],
    'lemmas': ['Bob', 'be', 'bear', 'on', 'June', '16', '2022', '.'],
    'pos': ['PROPN', 'AUX', 'VERB', 'ADP', 'PROPN', 'NUM', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'VBN', 'IN', 'NNP', 'CD', 'CD', '.'],
    'deps': ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'pobj', 'nummod', 'nummod', 'punct'],
    'heads': [2, 2, 2, 2, 3, 4, 4, 2],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 7),(0, 1)]
}),
({
    'description': 'Dates should still be detected when st/nd/rd/th shorthands are present.',
    'words': ['Bob', 'was', 'born', 'on', 'June', '16th', '2022', '.'],
    'lemmas': ['Bob', 'be', 'bear', 'on', 'June', '16th', '2022', '.'],
    'pos': ['PROPN', 'AUX', 'VERB', 'ADP', 'PROPN', 'NOUN', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'VBN', 'IN', 'NNP', 'NN', 'CD', '.'],
    'deps': ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'compound', 'pobj', 'nummod', 'punct'],
    'heads': [2, 2, 2, 2, 5, 3, 5, 2],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(4, 7),(0, 1)]
}),
({
    'description': "Dates should be detected when broken by a comma.",
    'words': ['Bob', 'was', 'born', 'on', 'June', '16', ',', '2022', '.'],
    'lemmas': ['Bob', 'be', 'bear', 'on', 'June', '16', ',', '2022', '.'],
    'pos': ['PROPN', 'AUX', 'VERB', 'ADP', 'PROPN', 'NUM', 'PUNCT', 'NUM', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'VBN', 'IN', 'NNP', 'CD', ',', 'CD', '.'],
    'deps': ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'pobj', 'nummod', 'punct', 'nummod', 'punct'],
    'heads': [2, 2, 2, 2, 3, 4, 4, 4, 2],
    'spaces': [' ', ' ', ' ', ' ', ' ', '', ' ', '', ''],
    'gold_spans': [(4, 8),(0, 1)]
}),
({
    'description': "Years modifying nouns should not be included as part of the noun's span.",
    'words': ['A', '2014', 'ad', 'for', 'toothpaste', '.'],
    'lemmas': ['a', '2014', 'ad', 'for', 'toothpaste', '.'],
    'pos': ['DET', 'NUM', 'NOUN', 'ADP', 'NOUN', 'PUNCT'],
    'tags': ['DT', 'CD', 'NN', 'IN', 'NN', '.'],
    'deps': ['det', 'nummod', 'ROOT', 'prep', 'pobj', 'punct'],
    'heads': [2, 2, 2, 2, 3, 2],
    'spaces': [' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(2, 3), (4, 5)]
}),
({
    'description': "Proper nouns as parts of dates modifying a noun should not be included as part of the noun's span",
    'words': ['Bob', 'claimed', 'in', 'his', 'December', '2002', 'interview', '.'],
    'lemmas': ['Bob', 'claim', 'in', 'his', 'December', '2002', 'interview', '.'],
    'pos': ['PROPN', 'VERB', 'ADP', 'PRON', 'PROPN', 'NUM', 'NOUN', 'PUNCT'],
    'tags': ['NNP', 'VBD', 'IN', 'PRP$', 'NNP', 'CD', 'NN', '.'],
    'deps': ['nsubj', 'ROOT', 'prep', 'poss', 'nmod', 'nummod', 'pobj', 'punct'],
    'heads': [1, 1, 1, 6, 6, 4, 2, 1],
    'spaces': [' ', ' ', ' ', ' ', ' ', ' ', '', ''],
    'gold_spans': [(0, 1),(3, 4),(6, 7)]
})
]


@pytest.fixture
def matcher(en_vocab):
    nlp = Language(en_vocab)
    matcher = NominalSpanMatcher(nlp)
    return matcher


def assertSpanInSpans(span, spans, desc):
    """ Assertion helper, makes test failures readable. """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    span_as_tuple = (span.start, span.end)
    spans_as_tuples = [(s.start, s.end) for s in spans]

    doc = span.doc
    if span_as_tuple not in spans_as_tuples:
        failure_lines = [
            desc,
            "{:<10} {}".format("Given:", str(doc)),
            "{:<10} {}".format("Expected:", spans),
            "{:<10} {}".format("Found:", span)
        ]
        pytest.fail("\n".join(failure_lines))


@pytest.mark.parametrize("params", params)
def testNominalSpanMatcher(params, matcher):
    """ Test that the nominal matcher gets the correct spans for each doc """

    description = params.pop('description')
    gold_span_tuples = params.pop('gold_spans')
    doc = Doc(matcher.matcher.vocab, **params)
    gold_spans = [Span(doc, *gs) for gs in gold_span_tuples]

    # Test the classes behavior as it will be called in a language pipeline
    doc = matcher(doc)

    for span in doc.spans[matcher.key]:
        assertSpanInSpans(span, gold_spans, description)

    assert len(gold_spans) == len(doc.spans[matcher.key]), description
