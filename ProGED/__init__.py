# -*- coding: utf-8 -*-

from model import Model
from model_box import ModelBox, symbolic_difference
from generators.grammar import GeneratorGrammar
from generators.grammar_construction import grammar_from_template
from parameter_estimation import fit_models
from task import EDTask
from equation_discoverer import EqDisco

__version__ = 0.6