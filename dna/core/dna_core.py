from dna.identity.identity_engine import (
    IdentityEngine
)

from dna.rules.rule_engine import (
    RuleEngine
)

from dna.evolution.evolution_engine import (
    EvolutionEngine
)

class DNACore:

    def __init__(self):

        self.identity = IdentityEngine()

        self.rules = RuleEngine()

        self.evolution = EvolutionEngine()

    def initialize(self):

        dna = (
            self.identity.load_identity()
        )

        dna["rules"] = (
            self.rules.load_rules()
        )

        evolved = (
            self.evolution.evolve(dna)
        )

        return evolved
