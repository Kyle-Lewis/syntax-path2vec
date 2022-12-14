# pylint: disable=line-too-long
import string

from pathvecs.utils.data import dates

def getSpanPatterns(key):
    """ Get matcher patterns """

    if key == 'nominals':
        return NOMINAL_SPAN_PATTERNS

    if key == 'modifiers':
        return MODIFIER_SPAN_PATTERNS

    if key == 'dates':
        return DATE_SPAN_PATTERNS

    raise KeyError("No span patterns found for key '{}'.".format(key))


nominal_dependencies = [
    "ROOT",
    "nsubj",
    "nsubjpass",
    "dobj",
    "pobj",
    "agent",
    "appos",
    "dative",
    "attr",
    "compound"
]

nominal_dependencies_b = [
    "ROOT",
    "nsubj",
    "nsubjpass",
    "dobj",
    "pobj",
    "agent",
    "appos",
    "dative",
    "attr"
]

hyphens = [
    '‐', # hyphen          | 2010
    '-', # hyphen-minus    | 002D
    '֊', # armenian hyphen | 1418
    '‑', # no break hyphen | 2011
    '﹣',# small hyphen minus | FE63
    # '‒', # figure dash     | 2012
    # '–', # en dash          | 2013
    # '—', # em dash          | 2014
    # '﹘',# small em dash    | FE58
    # '－'
]

a_noun = {"TAG": {"IN": ["NN", "NNS"]}}
optional_nth_adj = {
    "POS": "ADJ",
    "LEMMA": {"REGEX": r"[0-9]+(st|nd|rd|th)"},
    "OP": "?"
}

known_nominalized_verbs = []
optional_nomverb_noun = {"LEMMA": {"IN": known_nominalized_verbs}, "OP": "?"}

a_noun_not_amod = {
    "TAG": {"IN": ["NN", "NNS"]},
    "TEXT": {"NOT_IN": ["%"]},
    # "DEP": {"NOT_IN": ["amod"]},
    "_": {"matchers_left_text": {"NOT_IN": hyphens}}
}

one_or_more_nouns = {
    "TAG": {"IN": ["NN", "NNS"]},
    "TEXT": {"NOT_IN": ["%"]},
    "DEP": {"IN": nominal_dependencies},
    "OP": "+"
}

zero_or_more_nouns = {
    "TAG": {"IN": ["NN", "NNS"]},
    "TEXT": {"NOT_IN": ["%"]},
    "DEP": {"IN": nominal_dependencies},
    "OP": "*"
}

hyphen_by_tag = {"TAG": "HYPH", "SPACY": False}
hyphen_by_lem = {"LEMMA": {"IN": hyphens}, "SPACY": False}
comma = {"TAG": ","}

zero_or_more_propns = {"TAG": {"IN": ["NNP", "NNPS"]}, "OP": "*"}
one_or_more_propns = {"TAG": {"IN": ["NNP", "NNPS"]}, "OP": "+"}
one_or_more_nondate_propns = {"TAG": {"IN": ["NNP", "NNPS"]}, "TEXT": {"NOT_IN": dates.MONTH_STRINGS}, "OP": "+"}

any_until_space = {"SPACY": False, "_": {"matchers_right_text": {"NOT_IN": list(string.punctuation.replace('-', ''))}}, "OP": "*"}

nominal_number = {"TAG": "CD", "DEP": {"IN": nominal_dependencies}}
nominal_modifier = {""}
one_nominal = {"TAG": {"IN": ["NN", "NNS"]}, "DEP": {"IN": nominal_dependencies}}

NOMINAL_SPAN_PATTERNS = [

    # always respect date spans
    [{"_": {"matchers_is_date": True}, "OP": "+"}],

    ### Generally, contiguous common noun phrases of any length,

    # - can optionally begin with a numeral-abbreviated ordinal e.g., '1st'
    [optional_nth_adj, a_noun_not_amod, zero_or_more_nouns],

    # - otherwise, should not begin with a noun token that is acting as an adjective
    [a_noun_not_amod, zero_or_more_nouns],

    # - additionally, hyphen chained nominals
    [a_noun_not_amod, zero_or_more_nouns, hyphen_by_tag, any_until_space, {}],
    [a_noun_not_amod, zero_or_more_nouns, hyphen_by_lem, any_until_space, {}],

    # - As a special case, include leading numbers for fractions e.g., 'one-tenth'
    [{"TAG": "CD"}, hyphen_by_tag, one_nominal],
    [{"TAG": "CD"}, hyphen_by_lem, one_nominal],

    ### Generally, contiguous proper noun phrases of any length

    # - can optionally end with a common noun if it is a nominalized verb
    # - can optionally begin with a numeral-abbreviated ordinal e.g., '1st'
    [optional_nth_adj, one_or_more_propns, optional_nomverb_noun],

    # - can be separated by possessives *only* in the case of "Something's Day"
    [one_or_more_propns, {"TAG": "POS"}, {"TEXT": "Day"}],

    # - additionally, can be separated by a hyphen
    [optional_nth_adj, one_or_more_propns, hyphen_by_tag, one_or_more_propns],
    [optional_nth_adj, one_or_more_propns, hyphen_by_lem, one_or_more_propns],

    # - can be separated by non-English prepositions and contractions (de, del, la, al, etc.)
    [optional_nth_adj, one_or_more_propns, {"TAG": "FW"}, one_or_more_propns],

    # - additionally, can include numbers as parts of a proper noun span, so long as it isn't the first token
    [one_or_more_nondate_propns, {"TAG": "CD"}, zero_or_more_propns],

    # - can be lead by consecutive titlecased adjectives
    [{"POS": "ADJ", "IS_TITLE": True, "OP": "+"}, one_or_more_propns],

    ### Quotes

    # detect any quoted spans as long as there is one titlecase token present
    [{"TAG": "``"}, {"OP": "*"}, {"IS_TITLE": True}, {"OP": "*"}, {"TAG": "''"}],

    ## quantifiers
    [{"TAG": {"IN": ["NN", "NNS"]}, "LEMMA": {"IN": ['level', 'concentration']}}],

    # - Nominal numbers which are monetary values
    [{"TAG": "$", "OP": "?"}, {"TAG": "CD", "OP": "*"}, nominal_number],

    # - Nominal numbers which are percentages
    [{"TAG": "CD", "OP": "*"}, {"TEXT": "%", "DEP": {"IN": nominal_dependencies_b}}],

    ## PRONOUN
    # pronouns
    [{"TAG": {"IN": ["PRP", "PRP$"]}}]
]


###############################################################################
### MODIFIER PATTERNS #########################################################
###############################################################################

one_modifier = {"DEP": {"IN": ["amod", "nummod", "nmod"]}}
zero_or_more_modifiers = {"DEP": {"IN": ["amod", "nummod", "nmod"]}, "OP": "*"}

one_proper_modifier = {"DEP": {"IN": ["amod", "nummod", "nmod"]}, "IS_TITLE": True}
one_or_more_proper_modifiers = {"DEP": {"IN": ["amod", "nummod", "nmod"]}, "IS_TITLE": True, "OP": "+"}

optional_hyphen_by_tag = {"TAG": "HYPH", "OP": "?", "SPACY": False}
optional_hyphen_by_lem = {"LEMMA": {"IN": hyphens}, "OP": "?", "SPACY": False}

optional_nummod_time_old = {
    "TAG": "CD", "DEP": "nummod", "OP": "?",
    "_": {"matchers_right_text": {"IN": ['day', 'month', 'year']}}}

MODIFIER_SPAN_PATTERNS = [

    # always respect date spans
    [{"_": {"matchers_is_date": True}, "OP": "+"}],

    # single modifier
    [one_modifier],

    # modifier preceded by any number of compounds with optional currency symbol
    [{"TAG": "$", "OP": "?"}, {"TAG": "CD", "OP": "+"}, one_modifier],

    # continuous proper adjectives
    [one_or_more_proper_modifiers, optional_hyphen_by_tag, one_or_more_proper_modifiers],
    [one_or_more_proper_modifiers, optional_hyphen_by_lem, one_or_more_proper_modifiers],

    # child npadvmods, optionally joined by a hyphen
    # - In special cases, preceding nummods are included e.g., '3 year old'
    [optional_nummod_time_old, {"DEP": "npadvmod", "OP": "+"}, optional_hyphen_by_tag, one_modifier],
    [optional_nummod_time_old, {"DEP": "npadvmod", "OP": "+"}, optional_hyphen_by_lem, one_modifier],

    # child npadvmods, optionally joined by a hyphen, and optionally preceded by titlecased modifiers
    # "a (European Union-funded) something"
    [one_or_more_proper_modifiers, {"DEP": "npadvmod", "OP": "+"}, optional_hyphen_by_tag, one_modifier],
    [one_or_more_proper_modifiers, {"DEP": "npadvmod", "OP": "+"}, optional_hyphen_by_lem, one_modifier],

    # child advmods when joined by a hyphen
    # and optionally preceded by modifying numbers
    [optional_nummod_time_old, {"DEP": "advmod"}, hyphen_by_tag, one_modifier],
    [optional_nummod_time_old, {"DEP": "advmod"}, hyphen_by_lem, one_modifier],

    # modifier (typically verb pos) with a particle
    [one_modifier, {"TAG": "HYPH", "OP": "?"}, {"DEP": "prt"}],

    # hyphen chained modifiers
    [one_modifier, hyphen_by_tag, any_until_space, {}],
    [one_modifier, hyphen_by_lem, any_until_space, {}],
]


# Dates can behave both as nominals and as modifiers:
# Example:
#     nominal : "I saw you on July 14th"
#     modifier: "During the July 14th hearing"
#
# In order to prevent detection of nominal or modifying spans *within* dates,
# separate out their patterns so they can be detected & marked up-front. Then
# any pattern matcher can check for overlaps with dates regardless of role.
year = {
    "TEXT": {"REGEX": r"[1-2][0-9]{3}"}}
month = {
    "TEXT": {"REGEX": "|".join(dates.MONTH_STRINGS)}}
day = {
    "TEXT": {"REGEX": r"(((1[0-9])|(2[04-9])|30|([04-9]))th)|(2?2nd)|(2?3rd)|([2-3]?1st)|(((3[0-1])|([1-2]?[0-9])))"}}
era = {
    "TEXT": {"REGEX": r"([Aa](\.?)([D](\.?)|(d\.)))|([Bb](\.?)[Cc](\.?)[Ee]?(\.?))"}}
ancient_year = {
    "TEXT": {"REGEX": r"([0-9]{2})|([1-2]?[0-9]{3})"}}

DATE_SPAN_PATTERNS = [

    [ancient_year, era],

    [day, month, year],
    [day, month, comma, year],

    [month, day],
    [month, day, year],
    [month, day, comma, year],

    [month, day],
    [month, day, year],
    [month, day, comma, year],

    [month, year],
    [month, comma, year],

    [year],
]
