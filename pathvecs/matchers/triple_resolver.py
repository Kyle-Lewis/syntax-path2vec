
from spacy.language import Language

@Language.factory('triple_resolver')
def createTripleMatcherComponent(nlp, name):
    return TripleResolver(nlp)


class TripleResolver:

    def __init__(self, nlp):
        pass

    def __call__(self, doc):
        """ Takes doc._.triples and creates doc._.resolved_triples

        Relative pronouns are swapped for their anticedents where possible

        Quantifiers are swapped for quantified objects where possible

        Permutations of triples are taken among conjoined tokens

            "Alice and Bob went to the park."
                    (Alice)-[go-to]->(park)
                (+) (Bob)-[go-to]->(park)

        """

        resolved_triples
        for t in doc._.triples:






