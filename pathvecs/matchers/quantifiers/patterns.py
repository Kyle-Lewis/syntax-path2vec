from typing import List

QUANTIFIERS = [
    'all',
    'another',
    'any',
    'anything',
    'both',
    'each',
    'either',
    'enough',
    'every',
    'few',
    'half',
    'lot',
    'many',
    'most',
    'much',
    'neither',
    'no',
    'none',
    'nothing',
    'one',
    'plenty',
    'plenty',
    'scores',
    'series',
    'set',
    'several',
    'some',
    'something',
    'string',
    'thing',
    'things',
    'whatever',

    # Not exactly quantifiers, pattern still applies
    'variety',
    'kind',
    'level',
    'number',
    'amount',
    'portion',
    'proportion',
    'concentration',
    'ratio',
    'frequency',
    '%',
    'percent',
    'percentage',

    # cardinal forms of numbers
    'tenth', 'tenths',
    'ten', 'tens',
    'dozen', 'dozens',
    'hundredth', 'hundredths',
    'hundred', 'hundreds',
    'thousandth', 'thousandths',
    'thousand', 'thousands',
    'millionth', 'millionths',
    'million', 'millions',
    'billionth', 'billionths',
    'billion', 'billions'
]

QUANTIFIER_OF_PATTERNS = {

    # Rule to match common quantifier words with the entity they quantify in
    # "quantity of" prepositional phrases. The purpose is to replace
    # quantifiers with the entities they reference in triples, which should be
    # more informative.
    #
    # "Bob ate most of the pizza."
    # (Bob)-[eat]->(most)  -replace->  (Bob)-[eat]->(pizza)
    'quantifier': {
        'pattern': [
            {
                "RIGHT_ID": 'quantifier',
                "RIGHT_ATTRS": {"LEMMA": {"IN": QUANTIFIERS}}
            },
            {
                "RIGHT_ID": 'of',
                "LEFT_ID": 'quantifier',
                "REL_OP": ">",
                "RIGHT_ATTRS": {"LEMMA": "of", "DEP": "prep"}
            },
            {
                "RIGHT_ID": 'object',
                "LEFT_ID": 'of',
                "REL_OP": ">",
                "RIGHT_ATTRS": {
                    "POS": {"IN": ["NOUN", "PRON", "PROPN"]},
                    "DEP": "pobj"
                }
            }
        ]
    }
}


def get_pattern(key: str) -> dict:
    """ Get pattern data by key """
    return QUANTIFIER_OF_PATTERNS[key]['pattern']


def get_all_patterns() -> List[dict]:
    """ Get all pattern data """
    for pattern_name, pattern_data in QUANTIFIER_OF_PATTERNS.items():
        yield pattern_name, pattern_data['pattern']
