from typing import List

verb_attrs = {"TAG": {"IN": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]}}

RELATIVE_PRONOUN_PATTERNS = {
    'nominal_antecedent': {
        'pattern': [
            {
                "RIGHT_ID": 'pronoun',
                "RIGHT_ATTRS":
                {"LEMMA": {"IN": ['which', 'that', 'whom', 'who', 'whose']}}
            },
            {
                "RIGHT_ID": 'verb',
                "LEFT_ID": 'pronoun',
                "REL_OP": "<<",
                "RIGHT_ATTRS": {**verb_attrs, "DEP": "relcl"}},
            {
                "RIGHT_ID": 'antecedent',
                "LEFT_ID": 'verb',
                "REL_OP": "<",
                "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PRON", "PROPN"]}}
            }
        ]
    }
}


def get_pattern(key: str) -> dict:
    """ Get pattern data by key """
    return RELATIVE_PRONOUN_PATTERNS[key]['pattern']


def get_all_patterns() -> List[dict]:
    """ Get all pattern data """
    for pattern_name, pattern_data in RELATIVE_PRONOUN_PATTERNS.items():
        yield pattern_name, pattern_data['pattern']
