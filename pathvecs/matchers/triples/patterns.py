# pylint: disable=line-too-long
from spacy.tokens import Doc

# common patterns
nominal = {"POS": {"IN": ["NOUN", "PROPN", "PRON", "NUM"]}}
has_verb_tag = {"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]}}
has_being_lem = {"LEMMA": {"IN": ["be", "become", "remain"]}}


class Adjective:
    """
    Example:
        "The red dog." -> (red)-[adj]->(dog)
    """
    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {"DEP": "amod"}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'src', "REL_OP": "<", "RIGHT_ATTRS": {**nominal}},
    ]

    pattern_name = 'adjective'
    edge_fstring = 'adj'

    def fill(doc: Doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]

        edge = __class__.edge_fstring
        frame['edge'] = edge
        return frame


class Possessive:

    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {**nominal, "DEP": "poss"}, "CONJUNCTS": True},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'src', "REL_OP": "<", "RIGHT_ATTRS": {**nominal}, "CONJUNCTS": True},
    ]

    pattern_name = 'possessive'
    edge_fstring = 'poss'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring
        frame['edge'] = edge
        return frame


class Appositive:

    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {**nominal}, "CONJUNCTS": True},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'src', "REL_OP": ">", "RIGHT_ATTRS": {**nominal, "DEP": "appos"}, "CONJUNCTS": True},
    ]

    pattern_name = 'appositive'
    edge_fstring = 'appos'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring
        frame['edge'] = edge
        return frame


class CompoundA:


    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {'POS': 'PROPN', 'DEP': 'compound'}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'src', "REL_OP": "<", "RIGHT_ATTRS": {"POS": "NOUN"}}
    ]

    pattern_name = 'compound'
    edge_fstring = 'compound'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring
        frame['edge'] = edge
        return frame


class CompoundB:


    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {'POS': 'NOUN', 'DEP': 'compound'}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'src', "REL_OP": "<", "RIGHT_ATTRS": {"POS": "PROPN"}}
    ]

    pattern_name = 'compound'
    edge_fstring = 'compound'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring
        frame['edge'] = edge
        return frame



class NounPrepNoun:
    """
    Example:

        "A glass of water." ->
            (glass)-[of]->(water)
    """

    pattern = [
        {"RIGHT_ID": "src", "RIGHT_ATTRS": {**nominal}},
        {"RIGHT_ID": "prep", "LEFT_ID": "src", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": "dst", "LEFT_ID": "prep", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj"}}
    ]

    pattern_name = 'prep'
    edge_fstring = '{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            prep=doc[frame['prep']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class VerbDobjPobj:
    """
    Example:

        "Alice supported Bob with donations." ->
            (Bob)-[be-support-with]->(donations)
    """

    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag}},
        {"RIGHT_ID": "src", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "dobj"}},
        {"RIGHT_ID": "prep", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": "dst", "LEFT_ID": "prep", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj"}}
    ]

    pattern_name = 'verbed-prep'
    edge_fstring = 'be-{verb}-{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
            prep=doc[frame['prep']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class BeingVerb:
    """
    Example:

        "Bob is a person." ->
            (Bob)-[be]->(person)
    """


    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag, **has_being_lem}},
        {"RIGHT_ID": "src", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "dst", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "attr"}, "CONJUNCTS": True}
    ]


    pattern_name = 'being_verb'
    edge_fstring = '{verb}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class ActiveTransitiveVerb:
    """
    Example:

        "Bob is a person." ->
            (Bob)-[be]->(person)
    """

    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag}},
        {"RIGHT_ID": "src", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "dst", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "dobj"}, "CONJUNCTS": True}
    ]


    pattern_name = 'active_transitive_verb'
    edge_fstring = '{verb}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class ActiveTransitiveVerbConjuncts:

    pattern = [
        {"RIGHT_ID": "governor", "RIGHT_ATTRS": {**has_verb_tag}, "INCLUDE": False},
        {"RIGHT_ID": "src", "LEFT_ID": "governor", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "verb", "LEFT_ID": "governor", "REL_OP": ">>", "RIGHT_ATTRS": {**has_verb_tag, "DEP": "conj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "dst", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "dobj"}, "CONJUNCTS": True}
    ]

    pattern_name = 'active_transitive_verb_conjuncts'
    edge_fstring = '{verb}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class PassiveTransitiveVerb:

    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag}},
        {"RIGHT_ID": "agent_prep", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "agent"}, "INCLUDE": False},
        {"RIGHT_ID": "src", "LEFT_ID": "agent_prep", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "dst", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubjpass"}, "CONJUNCTS": True}
    ]

    pattern_name = 'passive_transitive_verb'
    edge_fstring = '{verb}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class PassiveTransitiveVerbConjuncts:

    pattern = [
        {"RIGHT_ID": "governor", "RIGHT_ATTRS": {**has_verb_tag}, "INCLUDE": False},
        {"RIGHT_ID": "verb", "LEFT_ID": "governor", "REL_OP": ">>", "RIGHT_ATTRS": {**has_verb_tag, "DEP": "conj"}, "CONJUNCTS": True},
        {"RIGHT_ID": "dst", "LEFT_ID": "governor", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubjpass"}, "CONJUNCTS": True},
        {"RIGHT_ID": "agent_prep", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "agent"}, "INCLUDE": False},
        {"RIGHT_ID": "src", "LEFT_ID": "agent_prep", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj"}, "CONJUNCTS": True}
    ]

    pattern_name = 'passive_transitive_verb_conjuncts'
    edge_fstring = '{verb}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class IntransitiveVerbPrep:

    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag}},
        {"RIGHT_ID": "src", "LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubj"}, "CONJUNCTS": True},
        {"RIGHT_ID": 'prep', "LEFT_ID": 'verb', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'prep', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj"}, "CONJUNCTS": True}
    ]

    pattern_name = 'intransitive_verb_prep'
    edge_fstring = '{verb}-{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            verb=doc[frame['verb']].lemma_.lower(),
            prep=doc[frame['prep']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class ApposNounPrep:

    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PROPN"]}}, "CONJUNCTS": True},
        {"RIGHT_ID": 'noun', "LEFT_ID": 'src', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "appos", "POS": "NOUN"}},
        {"RIGHT_ID": 'prep', "LEFT_ID": 'noun', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'prep', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj", "POS": {"IN": ["NOUN", "PROPN"]}}}
    ]

    pattern_name = 'appos_noun_prep'
    edge_fstring = 'appos_{noun}_{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            noun=doc[frame['noun']].lemma_.lower(),
            prep=doc[frame['prep']].lemma_.lower()
        )
        frame['edge'] = edge
        return frame


class PossNounAppos:

    pattern = [
        {"RIGHT_ID": 'noun', "RIGHT_ATTRS": {"POS": "NOUN"}, "CONJUNCTS": True},
        {"RIGHT_ID": 'src', "LEFT_ID": 'noun', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "poss", "POS": {"IN": ["NOUN", "PROPN"]}}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'noun', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "appos", "POS": {"IN": ["NOUN", "PROPN"]}}},
    ]

    pattern_name = 'poss_noun_appos'
    edge_fstring = 'poss_{noun}_appos'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            noun=doc[frame['noun']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


class PossNounPrep:

    pattern = [
        {"RIGHT_ID": 'noun', "RIGHT_ATTRS": {**nominal}, "CONJUNCTS": True},
        {"RIGHT_ID": 'src', "LEFT_ID": 'noun', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "poss", "POS": {"IN": ["NOUN", "PROPN"]}}},
        {"RIGHT_ID": 'prep', "LEFT_ID": 'noun', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'prep', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj", "POS": {"IN": ["NOUN", "PROPN"]}}}
    ]

    pattern_name = 'poss_noun_prep'
    edge_fstring = 'poss_{noun}_{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            noun=doc[frame['noun']].lemma_.lower(),
            prep=doc[frame['prep']].lemma_.lower()
        )
        frame['edge'] = edge
        return frame


class BeingNounPrep:

    pattern = [
        {"RIGHT_ID": "verb", "RIGHT_ATTRS": {**has_verb_tag, **has_being_lem}},
        {"RIGHT_ID": "src", "LEFT_ID": "verb",  "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "nsubj", "POS": {"IN": ["NOUN", "PROPN"]}}, "CONJUNCTS": True},
        {"RIGHT_ID": 'noun', "LEFT_ID": 'verb', "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "attr", **nominal}, "CONJUNCTS": True},
        {"RIGHT_ID": "prep", "LEFT_ID": "noun", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "prep"}},
        {"RIGHT_ID": "dst", "LEFT_ID": "prep", "REL_OP": ">", "RIGHT_ATTRS": {"DEP": "pobj", "POS": {"IN": ["NOUN", "PROPN"]}}}
    ]

    pattern_name = 'be_noun_prep'
    edge_fstring = 'be_{noun}_{prep}'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            noun=doc[frame['noun']].lemma_.lower(),
            prep=doc[frame['prep']].lemma_.lower()
        )
        frame['edge'] = edge
        return frame


class CompoundNounCompound:

    # "CNN reporter Bob Lastname"
    # (CNN)-[compound_reporter_compound]->(Bob Lastname)

    pattern = [
        {"RIGHT_ID": 'src', "RIGHT_ATTRS": {'POS': 'PROPN', 'DEP': 'compound'}},
        {"RIGHT_ID": 'noun', "LEFT_ID": 'src', "REL_OP": "<", "RIGHT_ATTRS": {"DEP": "compound", "POS": "NOUN"}},
        {"RIGHT_ID": 'dst', "LEFT_ID": 'noun', "REL_OP": "<", "RIGHT_ATTRS": {"POS": "PROPN"}}
    ]

    pattern_name = 'compound_noun_compound'
    edge_fstring = 'compound_{noun}_compound'

    def fill(doc, match):

        frame = {'type': __class__.pattern_name}
        pattern = __class__.pattern

        for token_index in range(len(match)):

            if pattern[token_index].get("INCLUDE", True):

                role = pattern[token_index]["RIGHT_ID"]
                frame[role] = match[token_index]


        edge = __class__.edge_fstring.format(
            noun=doc[frame['noun']].lemma_.lower(),
        )
        frame['edge'] = edge
        return frame


TRIPLE_PATTERNS = {}
for p in [
    # Adjective,
    # Possessive,
    # Appositive,
    # CompoundA,
    # CompoundB,
    NounPrepNoun,
    # BeingVerb,
    # ActiveTransitiveVerb,
    # ActiveTransitiveVerbConjuncts,
    # PassiveTransitiveVerb,
    # PassiveTransitiveVerbConjuncts,
    IntransitiveVerbPrep,
    ApposNounPrep,
    BeingNounPrep,
    CompoundNounCompound,
    PossNounAppos,
    PossNounPrep,
]:
    if p.pattern_name in TRIPLE_PATTERNS:
        TRIPLE_PATTERNS[p.pattern_name].append(p)
    else:
        TRIPLE_PATTERNS[p.pattern_name] = [p]

def get_triple_patterns():
    return TRIPLE_PATTERNS
