"""
Extracts the

Example:

    "A glass of water." ->
        (glass)-[of]->(water)
"""

import itertools
from typing import List, NamedTuple

from spacy.tokens import Doc


# common matcher attributes
nominal_attrs = {"POS": {"IN": ["NOUN", "PROPN", "PRON", "NUM"]}}
verb_attrs = {"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]}}
be_attrs = {"LEMMA": {"IN": ["be", "become", "remain"]}}


class Triple(NamedTuple):
    src: int
    edge: str
    dst: int


TRIPLE_PATTERNS = {

    # syntactic path between a nominal head and its prepositional object
    "prep": {
        "name": "prep",
        "edge_fstring": "{}",
        "src_rule_index": 0,
        "dst_rule_index": 2,
        "edge_rule_indices": [1],
        "pattern": [
            {
                "RIGHT_ID": "src",
                "RIGHT_ATTRS": {**nominal_attrs}
            },
            {
                "RIGHT_ID": "prep",
                "LEFT_ID": "src",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "prep"}
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "prep",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj"}
            }
        ],
    },

    # syntactic path between the subject of and the nominative which
    # completes a copular verb (restricted to be, become, remain)
    "being_verb": {
        "name": "being_verb",
        "edge_fstring": "{}",
        "src_rule_index": 1,
        "dst_rule_index": 2,
        "edge_rule_indices": [0],
        "pattern": [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {**verb_attrs, **be_attrs}
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "attr"},
            }
        ]

    },

    # syntactic paths between the subject(s) and object(s) of transitive
    # verbs in the active voice. Captures conjuncts of the subject and / or
    # object which can be permuted, but leaves the responsability of matching
    # conjoined verbs to another pattern
    #   "Alice ate cookies." -> (Alice)-[eat]->(cookies)
    "active_transitive_verb": {
        "name": "active_transitive_verb",
        "edge_fstring": "{}",
        "src_rule_index": 1,
        "dst_rule_index": 2,
        "edge_rule_indices": [0],
        "pattern": [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {**verb_attrs}
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "dobj"},
            }
        ]

    },

    # syntactic paths between the subject(s) and object(s) of transitive
    # verbs in the active voice, where this pattern captures conjunct verbs
    "active_transitive_verb_conjuncts": {
        "name": "active_transitive_verb",
        "edge_fstring": "{}",
        "src_rule_index": 1,
        "dst_rule_index": 3,
        "edge_rule_indices": [2],
        "pattern": [
            {
                "RIGHT_ID": "governor",
                "RIGHT_ATTRS": {**verb_attrs},
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "governor",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
            },
            {
                "RIGHT_ID": "verb",
                "LEFT_ID": "governor",
                "REL_OP": ">>",
                "RIGHT_ATTRS": {**verb_attrs, "DEP": "conj"}
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "dobj"},
            }
        ]
    },

    # syntactic path between the "subject" (pobj of agent 'by') and
    # "object" (passive subject) of a transitive verb in the passive voice
    "passive_transitive_verb": {
        "name": "passive_transitive_verb",
        "edge_fstring": "{}",
        "src_rule_index": 2,
        "dst_rule_index": 3,
        "edge_rule_indices": [0],
        "pattern": [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {**verb_attrs}
            },
            {
                "RIGHT_ID": "agent_prep",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "agent"},
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "agent_prep",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj"},
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubjpass"},
            }
        ]
    },

    # syntactic path between the "subject" (pobj of agent 'by') and
    # "object" (passive subject) of a transitive verb in the passive voice
    # where this pattern captures conjunct verbs
    "passive_transitive_verb_conjuncts": {
        "name": "passive_transitive_verb_conjuncts",
        "edge_fstring": "{}",
        "src_rule_index": 4,
        "dst_rule_index": 2,
        "edge_rule_indices": [1],
        "pattern": [
            {
                "RIGHT_ID": "governor",
                "RIGHT_ATTRS": {**verb_attrs},
            },
            {
                "RIGHT_ID": "verb",
                "LEFT_ID": "governor",
                "REL_OP": ">>",
                "RIGHT_ATTRS": {**verb_attrs, "DEP": "conj"},
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "governor",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubjpass"},
            },
            {
                "RIGHT_ID": "agent_prep",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "agent"},
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "agent_prep",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj"},
            }
        ]
    },

    # MULTI HOP

    # syntactic path between the subject of an intransitive verb
    # and the prepositional object of that verb if present
    "intransitive_verb_prep": {
        "name": "intransitive_verb_prep",
        "edge_fstring" : "{}-{}",
        "src_rule_index": 1,
        "dst_rule_index": 3,
        "edge_rule_indices": [0, 2],
        "pattern" : [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {**verb_attrs}
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
            },
            {
                "RIGHT_ID": 'prep',
                "LEFT_ID": 'verb',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "prep"}
            },
            {
                "RIGHT_ID": 'dst',
                "LEFT_ID": 'prep',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj"},
            }
        ]
    },

    # syntactic path between the head of an appositive, and the prepositional
    # object of the appositive child.
    # "Paris, the capital of France" -> (Paris)-[appos_capital_of]->(France)
    "appos_noun_prep": {
        "name": "appos_noun_prep",
        "edge_fstring" : "appos_{}_{}",
        "src_rule_index": 0,
        "dst_rule_index": 3,
        "edge_rule_indices": [1, 2],
        "pattern": [
            {
                "RIGHT_ID": 'src',
                "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PROPN"]}},
            },
            {
                "RIGHT_ID": 'noun',
                "LEFT_ID": 'src',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "appos", "POS": "NOUN"}
            },
            {
                "RIGHT_ID": 'prep',
                "LEFT_ID": 'noun',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "prep"}
            },
            {
                "RIGHT_ID": 'dst',
                "LEFT_ID": 'prep',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj", "POS": {"IN": ["NOUN", "PROPN"]}}
            }
        ]
    },

    # syntactic path between the subject of a being verb to the prepositional
    # child of the attribute which completes it.
    # "Alice is the queen of France" -> (Alice)-[be_queen_of]->(France)
    "be_noun_prep": {
        "name": "be_noun_prep",
        "edge_fstring" : "be_{}_{}",
        "src_rule_index": 1,
        "dst_rule_index": 4,
        "edge_rule_indices": [2, 3],
        "pattern": [
            {
                "RIGHT_ID": "verb",
                "RIGHT_ATTRS": {**verb_attrs, **be_attrs}
            },
            {
                "RIGHT_ID": "src",
                "LEFT_ID": "verb",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "nsubj"},
                "POS": {"IN": ["NOUN", "PROPN"]},
            },
            {
                "RIGHT_ID": 'noun',
                "LEFT_ID": 'verb',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "attr", "POS": "NOUN"}
            },
            {
                "RIGHT_ID": "prep",
                "LEFT_ID": "noun",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "prep"},
            },
            {
                "RIGHT_ID": "dst",
                "LEFT_ID": "prep",
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj", "POS": {"IN": ["NOUN", "PROPN"]}}
            }
        ]
    },

    # "Alice's book, 'Poetry By Alice'"
    "poss_noun_appos": {
        "edge_fstring" : "poss_{}_appos",
        "src_rule_index": 1,
        "dst_rule_index": 2,
        "edge_rule_indices": [0],
        "pattern": [
            {
                "RIGHT_ID": 'noun',
                "RIGHT_ATTRS": {"POS": "NOUN"},
            },
            {
                "RIGHT_ID": 'src',
                "LEFT_ID": 'noun',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "poss", "POS": {"IN": ["NOUN", "PROPN"]}}
            },
            {
                "RIGHT_ID": 'dst',
                "LEFT_ID": 'noun',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "appos", "POS": {"IN": ["NOUN", "PROPN"]}}
            },
        ]
    },

    # "Alice's book about poetry"
    "poss_noun_prep": {
        "edge_fstring" : "poss_{}_{}",
        "src_rule_index": 1,
        "dst_rule_index": 3,
        "edge_rule_indices": [0, 2],
        "pattern": [
            {
                "RIGHT_ID": 'noun',
                "RIGHT_ATTRS": {**nominal_attrs},
            },
            {
                "RIGHT_ID": 'src',
                "LEFT_ID": 'noun',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "poss", **nominal_attrs}
            },
            {
                "RIGHT_ID": 'prep',
                "LEFT_ID": 'noun',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "prep"},
            },
            {
                "RIGHT_ID": 'dst',
                "LEFT_ID": 'prep',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"DEP": "pobj", **nominal_attrs}
            }
        ]
    },

    # # "Alice wrote a book about poetry"
    # "transitive_verb_noun_prep": {},

    # # "Alice wrote in a notebook from Japan."
    # "intransitive_verb_prep_noun_prep": {},
}

def get_pattern(key: str) -> dict:
    """ Get pattern data by key """
    return TRIPLE_PATTERNS[key]['pattern']


def get_all_patterns() -> List[dict]:
    """ Get all pattern data """
    for pattern_name, pattern_data in TRIPLE_PATTERNS.items():
        yield pattern_name, pattern_data['pattern']


def get_all_triples(match: List[int], key: str, doc: Doc) -> List[Triple]:
    """ Get all the triples for a match, accounting for possible conjuncts

    Args:
        match: List of token ids for a pattern match
        key: The pattern key for the pattern that was matched
        doc: The spacy doc where the match was found

    Returns:
        triples: List of all triples
    """
    allowed_conjuncts = ['src', 'dst']

    pattern = TRIPLE_PATTERNS[key]['pattern']

    # Build up combinations of conjunct triples
    conjunct_matches = [[ti] for ti in match]

    for rule_index, token_index in enumerate(match):
        if pattern[rule_index]['RIGHT_ID'] in allowed_conjuncts:
            for conjunct in doc[token_index].conjuncts:
                conjunct_matches[rule_index].append(conjunct.i)

    triples = []
    conjunct_matches = itertools.product(*conjunct_matches)
    for conj_match in conjunct_matches:
        triples.append(get_triple(conj_match, key, doc))

    return triples


def get_triple(match: List[int], key: str, doc: Doc) -> Triple:
    """
    Args:
        match: List of token ids for a pattern match
        key: The pattern key for the pattern that was matched
        doc: The spacy doc where the match was found

    Returns:
        triple: A filled in Triple namedtuple for the match
    """

    data = TRIPLE_PATTERNS[key]
    src_token_index = match[data['src_rule_index']]
    dst_token_index = match[data['dst_rule_index']]

    edge_tokens = [doc[match[i]] for i in data['edge_rule_indices']]
    edge_fargs = [t.lemma_.lower() for t in edge_tokens]
    edge_name = data['edge_fstring'].format(*edge_fargs)

    return Triple(src_token_index, edge_name, dst_token_index)


def get_pattern_verb_type(key: str):
    """ Get the verb type for the provided pattern key"""
    pass
