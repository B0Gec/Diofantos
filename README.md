**Pro**babilistic **G**rammar-based **E**quation **D**iscovery

ProGED discovers physical laws in data, expressed in the form of equations. 
A probabilistic context-free grammar (PCFG) is used to generate candidate equations. 
Their optimal values of their parameters are estimated and their perfomance evaluated.
The output of ProGED is a list of equations, ordered according to the likelihood that they represent the best model for the data.

# Features
- algebraic equations
- 1st order ordinary differential equations
- construct a grammar from a template or write a custom grammar
- intuitive and flexible paramterization of parsimony principle

Details in https://arxiv.org/abs/2012.00428.

# Dependencies
- numpy
- scipy
- sympy
- NLTK

# Setup
You can install the package directly from the git repository:
```
pip install git+https://github.com/brencej/ProGED.
```

# Usage guide and examples
## Simple use
First, generate data for a simple 1-dimensional problem:
```
import numpy as np

def f(x):
    return 2.0 * (x + 0.3)
	
X = np.linspace(-1, 1, 20)
Y = f(X)
```
ProGED provides an interface for common usage through the class EqDisco:
```
from ProGED import EqDisco

ED = EqDisco(dataX = X,
             dataY = Y,
             sample_size = 5,
             verbosity = 1)
```
The algorithm has two steps: generating the models and fiting the models:
```
print(ED.generate_models())
print(ED.fit_models())
```




