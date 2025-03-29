# def pretty_results(seq_name="fibonacci", is_direct=is_direct, order=order):
#     """Print results in prettier form."""
#     if seq_name =="fibonacci":
#         assert oeis == fibs
#     if seq_name=="fibonacci" and is_direct and order==0:  # i.e. direct fib
#         # is_fibonacci_direct = True
#         # if is_fibonacci_direct:
#         phi = (1+5**(1/2))/2
#         c0, c1 = 1/5**(1/2), np.log(phi)
#         print(f" m c0: {c0}", f"c1:{c1}")
#         model = ED.models[5]  # direct fib
#     elif seq_name=="fibonacci" and not is_direct and order != 0:  # i.e. rec fib
#         model = ED.models[-1]
#     elif seq_name=="primes" and not is_direct and order != 0:  # i.e. rec primes
#         model = ED.models[7]  # primes
#     else:    
#         model = ED.models[-1]  # in general to update
        
#     # an = model.lambdify()
#     an = model.lambdify(*np.round(model.params)) if order != 0 else model.lambdify(*model.params)
#     print("model:", model.get_full_expr())#, "[f(1), f(2), f(3)]:", an(1), an(2), an(3))

#     cache = oeis[:order]  # update this
#     # cache = list(oeis[:order])
#     for n in range(order, len(oeis)):
#         prepend = [n] if is_direct else []
#         append = cache[-order:] if (order != 0) else []
#         cache += [int(np.round(an(*(prepend+append))))]
#         # print(prepend, append, prepend + append, (prepend + append), cache, an)
#     res = cache
#     print(oeis)
#     print(res)
#     error = 0
#     for i, j in zip(res, oeis):
#         print(i,j, i-j, error)
#         error += abs(i-j)
#     print(error)
#     return
# # pretty_results(seq_name=seq_name, is_direct=is_direct, order=order)

# pickle.dump(eq_discos, open( "exact_models.p", "wb" ) )

