import numpy as np
import pandas as pd
from ProGED.equation_discoverer import EqDisco

# nrows = 100
# nrows = 94
# nrows = 90
nrows = 50
data = pd.read_csv('../oeis_selection.csv', nrows=nrows)
fibonacci_no = 45
fibonacci_id = f"A{fibonacci_no:0>6}"

# if nrows=50, dtype=int64:
# oeis = list(data[fibonacci_id])
# if nrows=100, dtype=object:
oeis = [int(term) for term in data[fibonacci_id]]
# print(f"{max(oeis):e}")
# oeis_old = [0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,
#  1597,2584,4181,6765,10946,17711,28657,46368,75025,
#  121393,196418,317811,514229,832040,1346269,
#  2178309,3524578,5702887,9227465,14930352,24157817,
#  39088169,63245986,102334155]
# oeis_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,
#  61,67,71,73,79,83,89,97,101,103,107,109,113,127,
#  131,137,139,149,151,157,163,167,173,179,181,191,
#  193,197,199,211,223,227,229,233,239,241,251,257,
#  263,269,271][:40+1]
# oeis = oeis_primes
fibs = np.array(oeis).reshape(-1, 1)
# print(type(fibs), fibs.dtype)
# print(fibs)
ts = np.array([i for i in range(len(oeis))]).reshape(-1, 1)
data = np.hstack((ts, fibs))

np.random.seed(0)
ED = EqDisco(data = data,
            task = None,
            target_variable_index = -1,
            variable_names=["n", "an"],
            sample_size = 10,
            verbosity = 0,
            generator = "grammar", 
            generator_template_name = "polynomial",
            generator_settings={"variables":["'n'"]},
            estimation_settings={"verbosity": 1, "task_type": "algebraic", "lower_upper_bounds": 
            # (-5, 5)} 
            # (-3, 3)} 
            (-4, 4)} 
            # (-10, 8)} # Last bound where it still finds.
            # (0, 1)}  
            # (0.4, 0.5)}  
            )
ED.generate_models()
ED.fit_models()
# print(ED.models)
print("\n\nFinal score:")
for m in ED.models:
    print(f"model: {str(m.get_full_expr()):<30}; error: {m.get_error():<15}")

phi = (1+5**(1/2))/2
psi = (1-5**(1/2))/2
c0 = 1/5**(1/2)
c1 = np.log(phi)
print(f"source m c0: {c0}", f"c1:{c1}")
# fib(n) = (phi**n - psi**n)/5**(1/2)
#         = floor(phi**n/5**(1/2) + 1/2)
#         = round(phi**n/5**(1/2))
#         = round( exp(log(phi)*n)/5**(1/2) )
#         = round( c0*exp(c1*n) )
#         = round( 0.447213596451458*exp(0.481211825004291*n) )

model = ED.models[5] 
# model = ED.models[15]  # primes
print(model, model.get_full_expr(), model.get_error(), ' -- = winner model')
res = model.evaluate(ts, *model.params)
res = [int(np.round(flo)) for flo in res]

print(res)
print(oeis)
counter = 1
error = 0
for i, j in zip(res, oeis):
    print(i,j, i-j, error, f"{j:e}")
    if counter == 40:
        print(f"this was {counter}th term")
    if counter == 50:
        print(f"this was {counter}th term")
    error += abs(i-j)
    counter += 1

print("total error:", error)
# nrows=95 returns error: 
#     <class 'TypeError'> with message: loop of ufunc does 
#     not support argument 0 of type float which has no callable exp method
