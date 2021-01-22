# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:43:01 2020

@author: Jure
"""

import numpy as np
# import sympy as sp
# from nltk import PCFG

# from model import Model
# from model_box import ModelBox
from generate import generate_models
from parameter_estimation import fit_models
from generators.base_generator import BaseExpressionGenerator
# from generators.grammar import GeneratorGrammar
from generators.grammar_construction import grammar_from_template
from task import EDTask

GENERATOR_LIBRARY = {"grammar": grammar_from_template}

class EqDisco:
    def __init__ (self, task = None,  dataX = None, dataY = None, variable_names = None, output_variable = None,
                  variable_probabilities = None, success_threshold = 1e-8, task_type = "algebraic",
                  generator = "grammar", generator_template_name = "universal", generator_settings = {},
                  strategy = "monte-carlo", strategy_settings = None, sample_size = 10,
                  verbosity = 1):        
        
        if not task:
            if isinstance(dataX, type(None)) or isinstance(dataY, type(None)):
                raise TypeError ("Missing inputs. Either task object or data required.")
            else:
                if not variable_names:
                    variable_names = [chr(97+i) for i in range(dataX.shape[-1])]
                if not output_variable:
                    output_variable = "f"
                if not variable_probabilities:
                    variable_probabilities = [1/len(variable_names)]*len(variable_names)
                self.task = EDTask(dataX, dataY, variable_names, output_variable, success_threshold, task_type)
        elif isinstance(task, EDTask):
            self.task = task
        else:
            raise TypeError ("Missing task information!")
            
        generator_settings.update({"variables":self.task.symbols["x"], "p_vars": variable_probabilities})
        if isinstance(generator, BaseExpressionGenerator):
            self.generator = generator
        elif isinstance(generator, str):
            if generator in GENERATOR_LIBRARY:
                self.generator = GENERATOR_LIBRARY[generator](generator_template_name, 
                                                              generator_settings)
            else:
                raise KeyError("Generator name not found. Supported generators:\n" + str(list(GENERATOR_LIBRARY.keys())))
        else:
            raise TypeError ("Invalid generator specification. Expected: class that inherits from "\
                             "generators.base_generator.BaseExpressionGenerator or string, corresponding to template name.\n"\
                             "Input: " + str(type(generator)))
            
        self.strategy = strategy
        if not strategy_settings:
            self.strategy_settings = {"N": sample_size}
        else:
            self.strategy_settings = strategy_settings
        
        self.models = None
        self.solution = None
        
        self.verbosity = verbosity
        
        
    def generate_models (self, strategy_settings = None):
        if not strategy_settings:
            strategy_settings = self.strategy_settings
        self.models = generate_models(self.generator, self.task.symbols, self.strategy, strategy_settings, verbosity=self.verbosity)
        return self.models
    
    def fit_models (self, pool_map = map):
        self.models = fit_models(self.models, self.task.dataX, self.task.dataY, pool_map = pool_map, verbosity=self.verbosity)
        return self.models
        
    
if __name__ == "__main__":
    print("--- equation_discoverer.py test --- ")
    np.random.seed(4)
    
    def f(x):
        return 2.0 * (x + 0.3)
	
    X = np.linspace(-1, 1, 20)
    Y = f(X)
    X = X.reshape(-1,1)
    Y = Y.reshape(-1,1)
        
    ED = EqDisco(dataX = X,
                 dataY = Y,
                 sample_size = 5,
                 verbosity = 1)
    
    print(ED.generate_models())
    print(ED.fit_models())
