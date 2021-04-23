# -*- coding: utf-8 -*-

import numpy as np
from nltk import Nonterminal, PCFG

import sys

from ProGED.equation_discoverer import EqDisco
from ProGED.generators.grammar import GeneratorGrammar
from ProGED.generators.grammar_construction import grammar_from_template
from ProGED.generate import generate_models
from ProGED.model import Model
from ProGED.model_box import ModelBox
from ProGED.parameter_estimation import fit_models, hyperopt_fit
from hyperopt import hp

def test_grammar_general():
    np.random.seed(0)
    
    txtgram = "S -> S '+' F [0.2] | F [0.8] \n"
    txtgram += "F -> 'x' [0.5] | 'y' [0.5]"
    grammar = GeneratorGrammar(txtgram)
    
    sample = grammar.generate_one()
    assert sample[0] == ['y'] and sample[1] == 0.4 and sample[2] == '11'
    
    assert grammar.count_trees(Nonterminal("S"), 5) == 30
    assert grammar.count_coverage(Nonterminal("S"), 2) == 0.8
    
    assert "".join(grammar.code_to_expression('0101')[0]) == "x+y"
    
def test_grammar_templates():
    np.random.seed(0)
   
    templates_to_test = ["polynomial", "trigonometric", "polytrig", "simplerational", "rational", "universal"]
    variables = ["'x'", "'y'", "'z'"]
    p_vars = [0.3, 0.3, 0.4]
    codes = ["1101", "011", "02", "12", "0110001221101", "0202111211"]
    
    grammars = [grammar_from_template(template_name, {"variables": variables, "p_vars": p_vars}) for template_name in templates_to_test]
    for i in range(len(grammars)):
        assert grammars[i].generate_one()[2] == codes[i]
        
def test_generate_models():
    np.random.seed(0)
    generator = grammar_from_template("polynomial", {"variables":["'x'", "'y'"], "p_vars":[0.3,0.7]})
    symbols = {"x":['x', 'y'], "start":"S", "const":"C"}
    N = 3
    samples = ["C0*y", "C0*x*y**2", "C0*x**2 + C1"]
    
    models = generate_models(generator, symbols, strategy_settings = {"N":N})
    for i in range(len(models)):
        assert str(models[i]) == samples[i]
        
def test_model():
    grammar_str = "S -> 'c' '*' 'x' [1.0]"
    grammar = PCFG.fromstring(grammar_str)
    parse_tree_code = "0"
    expression_str = "c*x"
    probability = 1.0
    symbols_params = ["c"]
    symbols_variables = ["x"]
    
    model = Model(expr = expression_str, 
                  grammar = grammar, 
                  code = parse_tree_code, 
                  p = probability,
                  sym_params = symbols_params,
                  sym_vars = symbols_variables)

    assert str(model) == expression_str
    
    assert model.get_error() == 10**8
    
    result = {"x":[1.2], "fun":0.001}
    model.set_estimated(result)
    
    assert str(model.full_expr(*model.params)) == "1.2*x"
    
    X = np.reshape(np.linspace(0, 5, 2), (2, 1))
    y = model.evaluate(X, *model.params)

    assert isinstance(y, type(np.array([0])))
    assert sum((y - np.array([0, 6.0]))**2) < 1e-15
    
def test_model_box():
    grammar_str = "S -> 'c' '*' 'x' [0.5] | 'x' [0.5]"
    grammar = PCFG.fromstring(grammar_str)
    expr1_str = "x"
    expr2_str = "c*x"
    symbols = {"x":['x'], "const":"c", "start":"S"}
    
    models = ModelBox()
    models.add_model(expr1_str, symbols, grammar)
    assert len(models) == 1
    models.add_model(expr2_str, symbols, grammar, p=0.5, code="1")
    assert len(models) == 2
    assert str(models[1]) == str(models["c0*x"])
    assert str(models[1]) == "c0*x"
    assert models[1].p == 0.5
        
def test_parameter_estimation():
    np.random.seed(1)
    def f(x):
        return 2.0 * (x[:,0] + 0.3)
    X = np.linspace(-1, 1, 20).reshape(-1,1)
    Y = f(X).reshape(-1,1)
    data = np.hstack((X, Y))
    
    grammar = GeneratorGrammar("""S -> S '+' T [0.4] | T [0.6]
                              T -> 'C' [0.6] | T "*" V [0.4]
                              V -> 'x' [0.5] | 'y' [0.5]""")
    symbols = {"x":['x'], "start":"S", "const":"C"}
    N = 2
    
    models = generate_models(grammar, symbols, strategy_settings = {"N":N})
    models = fit_models(models, data, target_variable_index = -1, task_type="algebraic")
    
    assert np.abs(models[0].get_error() - 0.36) < 1e-6
    assert np.abs(models[1].get_error() - 1.4736842) < 1e-6

def test_parameter_estimation_2D():
    np.random.seed(0)
    def f(x):
        return 2.0 * (x[:,0]*x[:,1] + 0.3)
    
    r = np.linspace(-1, 1, 4)
    X = np.array([[[x,y] for x in r] for y in r]).reshape(-1,2)
    Y = f(X).reshape(-1,1)
    data = np.hstack((X, Y))
    
    grammar = GeneratorGrammar("""S -> S '+' T [0.4] | T [0.6]
                              T -> 'C' [0.6] | T "*" V [0.4]
                              V -> 'x' [0.5] | 'y' [0.5]""")
    symbols = {"x":['x', 'y'], "start":"S", "const":"C"}
    N = 2
    
    models = generate_models(grammar, symbols, strategy_settings = {"N":N})
    models = fit_models(models, data, target_variable_index = -1, task_type="algebraic")
    
    assert np.abs(models[0].get_error() - 0.36) < 1e-6
    assert np.abs(models[1].get_error() - 1.5945679) < 1e-6

# Prepare dataODE for multiple tests:
B = -2.56; a = 0.4; ts = np.linspace(0.45, 0.87, 1000)
ys = (ts+B)*np.exp(a*ts); xs = np.exp(a*ts)
dataODE = np.hstack((ts.reshape(-1, 1), xs.reshape(-1, 1), ys.reshape(-1, 1)))

def test_parameter_estimation_ODE():
    grammar = GeneratorGrammar("""S -> S '+' T [0.4] | T [0.6]
                                T -> V [0.6] | 'C' "*" V [0.4]
                                V -> 'x' [0.5] | 'y' [0.5]""")
    symbols = {"x":['y', 'x'], "start":"S", "const":"C"}
    np.random.seed(2)
    models = generate_models(grammar, symbols, strategy_settings={"N":5})
    models = fit_models(models, dataODE, target_variable_index=-1, time_index=0, task_type="differential")

    # print("\n", models, "\n\nFinal score:")
    # for m in models:
    #     print(f"model: {str(m.get_full_expr()):<30}; error: {m.get_error():<15}")
    def assert_line(models, i, expr, error, tol=1e-9, n=100):
        assert str(models[i].get_full_expr())[:n] == expr[:n]
        assert abs(models[i].get_error() - error) < tol
    assert_line(models, 0, "y", 0.6248459649904826)
    assert_line(models, 1, "x", 0.058235586316492984)
    assert_line(models, 2, "x + 0.400257928405516*y", 2.1252303778422445e-09, n=8)
    return

def test_equation_discoverer():
    np.random.seed(0)
    def f(x):
        return 2.0 * (x[:,0] + 0.3)
	
    X = np.linspace(-1, 1, 20).reshape(-1,1)
    Y = f(X).reshape(-1,1)
    data = np.hstack((X,Y))
        
    ED = EqDisco(data = data,
                 task = None,
                 target_variable_index = -1,
                 sample_size = 2,
                 verbosity = 1)
    
    ED.generate_models()
    ED.fit_models()
    
    #print(ED.models[0].get_error())
    assert np.abs(ED.models[0].get_error() - 0.72842105) < 1e-6
    assert np.abs(ED.models[1].get_error() - 0.59163899) < 1e-6
    
def test_equation_discoverer_ODE():
    np.random.seed(20)
    ED = EqDisco(data = dataODE,
                 task = None,
                 task_type = "differential",
                 time_index = 0,
                 target_variable_index = -1,
                 variable_names=["t", "x", "y"],
                 sample_size = 2,
                 verbosity = 1)
    ED.generate_models()
    ED.fit_models()

    def assert_line(models, i, expr, error, tol=1e-9, n=100):
        assert str(models[i].get_full_expr())[:n] == expr[:n]
        assert abs(models[i].get_error() - error) < tol
    assert_line(ED.models, 0, "y", 0.058235586316492984)
    assert_line(ED.models, 1, "0.4002359511712702*x + y", 2.1263385622753895e-09, n=6)
    return

def test_equation_discoverer_hyperopt():
# def ntest_equation_discoverer_hyperopt():
    np.random.seed(20)
    ED = EqDisco(data = dataODE,
                 task = None,
                 task_type = "differential",
                 time_index = 0,
                 target_variable_index = -1,
                 variable_names=["t", "x", "y"],
                 sample_size = 2,
                 verbosity = 1)
    ED.generate_models()
    ED.fit_models(
        estimation_settings={
            "optimizer": hyperopt_fit,
            "hyperopt_space_fn": hp.qnormal,
            "hyperopt_space_args": (0.4, 0.5, 1/1000),
        }
    )

    print("\n", ED.models, "\n\nFinal score:")
    for m in ED.models:
        print(f"model: {str(m.get_full_expr()):<30}; error: {m.get_error():<15}")
    def assert_line(models, i, expr, error, tol=1e-9, n=100):
        assert str(ED.models[i].get_full_expr())[:n] == expr[:n]
        assert abs(ED.models[i].get_error() - error) < tol
    assert_line(ED.models, 0, "y", 0.058235586316492984)
    assert_line(ED.models, 1, "0.401*x + y", 2.2989386082698416e-07, n=6)
    # Final score:
# model: y                             ; error: 0.058235586316492984
# model: 0.401*x + y                   ; error: 2.2989386082698416e-07


    return

# test_equation_discoverer_hyperopt()



# if __name__ == "__main__":
#     test_grammar_general()
#     test_grammar_templates()
#     test_generate_models()
#     test_model()
#     test_model_box()
#     test_parameter_estimation()
#     test_parameter_estimation_2D()    
#     test_equation_discoverer()
#     test_parameter_estimation_ODE()
#     test_equation_discoverer_ODE()
