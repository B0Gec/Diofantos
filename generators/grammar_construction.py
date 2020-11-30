# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 10:07:25 2020

@author: Jure
"""

import numpy as np
from generators.grammar import GeneratorGrammar
# from grammar import GeneratorGrammar

def grammar_from_template (template_name, grammar_parameters):
    if template_name in GRAMMAR_LIBRARY:
        grammar_str = GRAMMAR_LIBRARY[template_name](**grammar_parameters)
        return GeneratorGrammar(grammar_str)

def construct_right (right = "a", prob = 1):
    return right + " [" + str(prob) + "]"

def construct_production (left = "S", items = ["a"], probs=[1]):
    if not items:
        return ""
    else:
        return "\n" + left + " -> " + construct_right_distribution (items=items, probs=probs)

def construct_right_distribution (items=[], probs=[]):
    p = np.array(probs)/np.sum(probs)
    S = construct_right(right=items[0], prob=p[0])
    for i in range(1, len(items)):
        S += " | " + construct_right(right=items[i], prob=p[i])
    return S

def construct_grammar_trigonometric (probs1 = [0.8,0.2], probs2=[0.4,0.4,0.2], symbols = {"x":"'x'", "start":"S", "T1":"T1", "T2":"T2"}):
    items1 = ["'sin'", "'cos'", "'tan'"]
    grammar = construct_production(left=symbols["start"], items=[symbols["T1"]+"'('"+symbols["x"]+"')'",
                                                symbols["T1"]+" "+symbols["T2"]+"'('"+symbols["x"]+"')'"], probs=probs1)
    grammar += construct_production(left=symbols["T1"], items=items1, probs=probs2)
    grammar += construct_production(left=symbols["T2"], items=["'h'"], probs=[1])
    return grammar
    
def construct_grammar_function (functions=["'sin'", "'cos'"], probs=[0.5,0.5], symbols = {"x":"'x'", "start":"S", "A":"A1"}, string=True):
    grammar = construct_production(left=symbols["start"], items=[symbols["A"]+"'('"+symbols["x"]+"')'"], probs=[1])
    grammar += construct_production(left=symbols["A"], items=functions, probs=probs)
    return grammar
    
def construct_grammar_polytrig (p_more_terms=[0.7,0.15,0.15], p_higher_terms=0.5, p_vars = [0.5,0.3,0.2], variables = ["'x'", "'v'", "'a'", "'sin(C*x + C)'"]):
    grammar = construct_production(left="S", items=["'C' '+' S2"], probs=[1])
    grammar += construct_production(left="S2", items=["'C' '*' T '+' S2", "'C' '*' T", "'C'"], probs=p_more_terms)
    grammar += construct_production(left="T", items=["T '*' V", "V"], probs=[p_higher_terms, 1-p_higher_terms])
    grammar += construct_production(left="V", items=variables, probs=p_vars)
    return grammar

def construct_grammar_polynomial (p_S = [0.4, 0.6], p_T = [0.4, 0.6], p_vars = [1], p_R = [0.6, 0.4], p_F = [1],
                                  functions = ["'exp'"], variables = ["'x'"]):
    grammar = construct_production(left="S", items=["S '+' R", "R"], probs=p_S)
    grammar += construct_production(left="R", items=["T", "'C' '*' F '(' T ')'"], probs=p_R)
    grammar += construct_production(left="T", items=["T '*' V", "'C'"], probs=p_T)
    grammar += construct_production(left="F", items=functions, probs=p_F)
    grammar += construct_production(left="V", items=variables, probs=p_vars)
    return grammar

def construct_grammar_simplerational (p_S = [0.2, 0.8], p_P = [0.4, 0.3, 0.3], p_R = [0.4, 0.6], p_M = [0.4, 0.6], p_F = [1], p_V = [1],
                                      functions = ["'exp'"], variables = ["'x'"]):
    grammar = construct_production(left="S", items=["P '/' R", "P"], probs=p_S)
    grammar += construct_production(left="P", items=["P '+' 'C' '*' R", "'C' '*' R", "'C'"], probs=p_P)
    grammar += construct_production(left="R", items=["F '(' 'C' '*' M ')'", "M"], probs=p_R)
    grammar += construct_production(left="M", items=["M '*' V", "V"], probs=p_M)
    grammar += construct_production(left="F", items=functions, probs=p_F)
    grammar += construct_production(left="V", items=variables, probs=p_V)
    return grammar

def construct_grammar_rational (p_S = [0.4, 0.6], p_T = [0.4, 0.6], p_V = [1], p_R = [0.6, 0.4], p_F = [1],
                                  functions = ["'exp'"], variables = ["'x'"]):
    grammar = construct_production(left="S", items=["'(' E ')' '/' '(' E ')'"], probs=[1])
    grammar += construct_production(left="E", items=["E '+' R", "R"], probs=p_S)
    grammar += construct_production(left="R", items=["T", "'C' '*' F '(' T ')'"], probs=p_R)
    grammar += construct_production(left="T", items=["T '*' V", "'C'"], probs=p_T)
    grammar += construct_production(left="F", items=functions, probs=p_F)
    grammar += construct_production(left="V", items=variables, probs=p_V)
    return grammar

def construct_grammar_universal (p_sum=[0.2, 0.2, 0.6], p_mul = [0.2, 0.2, 0.6], p_rec = [0.2, 0.4, 0.4], 
                                 variables=["'x'", "'y'"], p_vars=[0.5,0.5],
                                 functions=["sin", "cos", "sqrt", "exp"], p_functs=[0.6, 0.1, 0.1, 0.1, 0.1]):
    #grammar = construct_production(left="S", items=["E '+' 'C'"], probs=[1])
    grammar = construct_production(left="S", items=["S '+' F", "S '-' F", "F"], probs=p_sum)
    grammar += construct_production(left="F", items=["F '*' T", "F '/' T", "T"], probs=p_mul)
    grammar += construct_production(left="T", items=["R", "'C'", "V"], probs=p_rec)
    grammar += construct_production(left="R", items=["'(' S ')'"] + ["'"+f+"(' S ')'" for f in functions], probs=p_functs)
    grammar += construct_production(left="V", items=variables, probs=p_vars)
    return grammar


GRAMMAR_LIBRARY = {
    "universal": construct_grammar_universal,
    "rational": construct_grammar_rational,
    "simplerational": construct_grammar_simplerational,
    "polytrig": construct_grammar_polytrig,
    "trigonometric": construct_grammar_trigonometric,
    "polynomial": construct_grammar_polynomial}

if __name__ == "__main__":
    print("--- grammar_construction.py test ---")
    np.random.seed(0)
    from nltk import PCFG
    # grammar = grammar_from_template("universal", {"variables":["'phi'", "'theta'", "'r'"], "p_vars":[0.2,0.4,0.4]})
    # grammar = grammar_from_template("trigonometric", {}) 
    # grammar = grammar_from_template("trigonometric", {"variables":["'phi'", "'theta'", "'r'"]})
    grammar = grammar_from_template("trigonometric", {"probs1":[0.8,0.2], "probs2":[0.4,0.4,0.2],
                                            "symbols": {"x":"'x'", "start":"S", "T1":"T1", "T2":"T2"}})
    print(grammar)
    for i in range(5):
        print(grammar.generate_one())
    print(construct_production("s",[],[]))