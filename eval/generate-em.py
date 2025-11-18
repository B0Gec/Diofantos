import numpy as np
import pandas as pd

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc

# look in ProGED/testing_constants for accessing constants inside of models.

grammar = gc.grammar_from_template("universal_oeis", {})
grammar = gc.grammar_from_template("universal_oeis", {})
print(grammar)
print(grammar.generate_one())
for i in range(5):
    print(grammar.generate_one())


