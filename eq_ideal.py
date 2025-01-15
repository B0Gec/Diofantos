"""
This file tries to automate the translation from ideal to equation.
I.e., given output of MB algorithm, find the most appropriate equation automatically.
Also, take care of _linrec_ experiments.

Strategy:
    - sort generators of the ideal by complexity and bitsize. Bitsize of a polynomial expression is the sum of bitsizes of
     all summands. For equations of bitsize <= 20, sort by number of summands, otherwise by bitsize.
    - return top_n equations and filter by max_complexity and max_bitsize, output only if not too big numbers involved
    or number of summands.
    - Linrec: limit complexity to 20 and make an additional list of purely linear equations.
        - create 2 functions for automatic verification:
            1.) linear expression: convert easily to recursive linear/vector form for ground check. | -> id
            2.) implicit expression: function to verify it on the whole sequence. | -> non_id (and man_check)
    - TM-OEIS:
            3.) implicit to explicit: to predict next terms for TM-OEIS benchmark.
            - Run experiments for SINDy to check if it is better than TM-OEIS (fun if seen better than transformers).
"""



import re

from fontTools.ttLib.tables.ttProgram import instructions

from exact_ed import expr_eval, obs_eval, eq_order_explicit
from mb_wrap import cocoa_eval, pretty_to_cocoa


def bitsize_summand(summand: str):
    """Returns the sum of number of digits of the numerator and denomumerator,
    e.g. '+(-1200/4345)*n*a(n-2)(' \-> 4+4 = 8
    """

    # print('in bitsizef_summand')
    # summand = ['a(n)', '-2*a(n-1)', 'n^4', '+(-7/16875)*a(n-1)^4', '-93090916800*n^2*a(n-1)', 'tm2*a' ][5]
    # print(summand)
    coef = re.findall(r'^\+?\-?\(?\-?(\d+)/?(\d*)\)?', summand)
    print(f'{coef = }')
    if coef == []:
        #     # if re.findall(r'[a-zA-Z]', coef[0]) == []: return 0 else: raise ValueError('Variable have strange name or bug in code!!!.')
        bits = 1
    # elif:
    else:
        # return coef[0]
        nom, denom = coef[0]
        bits = len(nom) + len(denom)
        # print('coef', f'{str(coef): <40}, bits: {len(nom)} + {len(denom)} = {bits}', 'summand:', summand)

    if len(coef) > 1:
        raise ValueError('Strange error in bitsize_summand function!!!      ... input has more than one coefficient!!!')
    # print(coef)
    # print('return:', bits)
    # print('punchline')

    return bits


def bitsize(equation: list[str]):
    """Function determining the "bitsize" of an equation.
        e.g. ['(1200/4345)*n*a(n-2)', 'a(n-1)'] \-> (4+4 + 0)/2 = 4

    Args:
        - eq (list): list of strings, representing the equation, result of ideal_to_eqs function.

    Returns: int, representing the "bitsize" of the equation.
        I.e. bitsize([coefficient*monomial for summand in equation]) := sum([bitsize(summand) for summand in equation])/(#summands),
        where bitsize(coefficient) = (magnitude(nominator) + magnitude(denominator).

    """

    # print('in bitsizef')

    # print(bitsize_summand(equation[1]))
    bsize = sum([bitsize_summand(summand) for summand in equation])
    # print('eq:', equation)
    # print(f'returning bitsizef({equation}):\n', bsize)
    # for i in equation:
    #     print('  ', i, bitsize_summand(i))

    return bsize


def ideal_to_eqs(ideal: str, max_complexity: int = 10, max_bitsize: int = 100, top_n: int = 10, verbosity=1) -> list:
    """
    Function to convert ideal to parsimony equations, which can be checked for correctness.

    Args:
        - ideal (list): list of generators produced by MB algorithm.

    Returns: list of equations, as candidates for equation discovery task.

    Filters:
        - max_complexity (int): Only equations with complexity <= max_complexity summands are outputed.
        - max_bitsize (int): Only equations with bitsize <= max_bitsize summands are outputed.
    """

    generators_string = ideal[6:-1]
    if verbosity >= 2:
        print('generators_string')
        print(generators_string)
        print(generators_string.replace(' ', ''))
    gens = [gen.strip(' ') for gen in generators_string.split(',')]

    eqs = []
    for gen in gens:
        if 'j' in gen:  # wtf!?
            raise ValueError('Repair split(\',  \'), since split from ideal to generator failed!!!.')
        # print(f'gen:{gen}')
        # summands = [i for i in gen.split(' ')]
        # summands = [j for j in [i.replace(' ', '') for i in summands] if j != '']  # clean-up empty strings.
        summands = gen.split(' ')


        if verbosity >=2:
            for sumand in summands:
                print('   ', sumand)
            print(len(summands))
        if len(summands) <= max_complexity and bitsize(summands) <= max_bitsize:  # filter equations by complexity
            eqs += [summands]

    # 1/0
    # eqs0 = sorted(eqs, key=lambda x: (bitsize(x), len(x)))[:top_n//2]
    eqs0 = sorted(eqs, key=lambda x: (len(x), bitsize(x)) if bitsize(x) <= 20 else (bitsize(x), len(x)))[:top_n]
    # x + y - z ... x + 100*y  now: 0 vs 3 (or updated 3 vs 4) or (updated 3 vs 2)
    # 10x + 34y - 5z ... 214x + 100*y  5 vs 6.  (3 vs 2)
    # eqs = eqs0 + [i for i in sorted(eqs, key=lambda x: (len(x), bitsize(x))) if i not in eqs0][:top_n//2]
    # eqs1 = [i for i in sorted(eqs, key=lambda x: (len(x), bitsize(x))) if i not in eqs0][:top_n//2]
    # eqs = eqs0 + eqs1
    eqs = eqs0

    if verbosity >= 1:
        for i, eq in enumerate(eqs):
            print(f'len(eq {i}): {len(eq)}, eq {i}: {eq}')

    human_readable_eqs = [' '.join(eq) for eq in eqs]
    # print('human_readable_eqs', human_readable_eqs)

    return eqs, human_readable_eqs

def is_linear(expr: str, allow_consts=False) -> bool:
    """Check if the OEIS recursive expression is linear without constant terms.
        Used by Linrec experiments for linear_to_vec function.
    """

    if '^' in expr:  # Power to > 1 indicates nonlinearity.
        return False
    else:  # Check if there are degree >= 2 terms.
        # noty = re.findall(r'^\+?-?\(?-?\d+/?\d*\)?\*?[^ ]+\*[^ ]+', expr)
        # noty = re.findall(r'[an][(n\-0-9)]*\*', expr) # this is enough here
        quads = re.findall(r'[an][(n\-0-9)]*\*[an][(n\-0-9)]*', expr)  # for linear including 'n'
        if quads:
            return False
        elif allow_consts:
            return True
        else:  # check if constant term is present
            # summands = [i for i in expr.split(' ')]
            # summands = [j for j in [i.replace(' ', '') for i in summands] if j != '']  # clean-up empty strings.
            summands = [i for i in expr.split(' ')]
            # print('summands:', summands)
            constants = sum([re.findall('^[^an*]*$', summand) for summand in summands], [])
            return len(constants) == 0


def replace_sqrt3(string: str, power=3) -> list:
    """findall() version for finding (expr)**(1/3) in string and extract the correct expression expr.

        E.g. 'a(n-1)**(1/3)' -> '[(a(n-1), **(1/3)]'
            '(3 +2*(1+n)^3 -a(n-2))**(1/3)' -> '[(3 +2*(1+n)^3 -a(n-2), **(1/3))]'

    Input:
        - string: str, OEIS recursive expression.
        - power: int, power of the root, to generalize from **(1/3) to **(1/power), e.g. **(1/4).
    """

    # print('inside replace_sqrt3')
    # string = '134*a(n-2) + FloorSqrt((3 +2*(1+n)^3 -a(n-2))**(1/3)) + 3*n^5 + 344 + (2+a(n-1))**(1/3) '
    # string = '134*a(n-2) + ((3 +2*(1+n)^3 -a(n-2))**(1/3)) + 3*n^5 + 344 + (2+a(n-1))**(1/3) '
    # string = '134*a(n-2) + ((3 +2*(1+n)^3 -an-242**(1/3)) + 3*n^5 + 344 + (2+a(n-1))**(1/3) '
    # print(string)
    splited = string.split(f'**(1/{power})')
    # print(splited)
    # 1/0
    def find_bracket(st: str) -> int:
        """3 +2*(1+n)^3 (2-a(n-2)) -> 9
        """
        # print(' inside find bracket')
        # print(st)
        st = st[::-1]
        # print(st)
        search = [len([i for i in st[:n] if i == ')']) - len([i for i in st[:n] if i == '(']) for n in range(1, len(st))]
        # print(search)
        return search.index(0)+1

    replacement = ''
    for i in splited[:-1]:
        # print(i)
        if i[-1] == ')':
            loc = -find_bracket(i)
            # print(f'{loc = }')
            # print(f'{i[loc:] = }')
            loc = loc-9 if i[loc-9:loc] in ['FloorSqrt', 'FloorRoot'] else loc
            # print(f'{loc = }')
            full_bracket = i[loc:]
            # print(f'{full_bracket = }')

            replacement += f"{i[:loc]}FloorRoot({i[loc:]}, {power})"
            # print(replacement)
        elif re.findall(r'\d', i[-1]):
            number = re.findall(r'\d+$', i)[0]
            loc = -len(number)
            replacement += f"{i[:loc]}FloorRoot({i[loc:]}, {power})"
            # print(replacement)
        else:
            raise ValueError('Unforseen combination of **(1/3) with other things! error in replace_sqrt3 function!!!  '
                             '   ... input has no closing bracket or digit at the end!!!')
    replacement += splited[-1]

    # print(f'{replacement = }')

    # 1/0

    return replacement

def sympy_to_cocoa(expr: str, order=100) -> str:
    """Convert sympy expression to cocoa expression for further processing.
        E.g. a(n - 1) - 2*a(n - 2) -> a(n-1) - 2*a(n-2)
             a(n-1)**2 -> a(n-1)^2
    """

    bij = {f'a(n - {i})': f'a(n-{i})' for i in range(1, order+1)}
    bij.update({f'a(n-{i})**(1/3)': f'FloorRoot(a(n-{i}),3)' for i in range(1, order+1)})
    bij.update({f'a(n-{i})**(1/4)': f'FloorRoot(a(n-{i}),4)' for i in range(1, order+1)})
    bij.update({f'n**(1/3)': f'FloorRoot(n,3)'})
    bij.update({f'n**(1/4)': f'FloorRoot(n,4)'})
    # print(bij)
    for key in bij:
        expr = expr.replace(key, bij[key])
    # for i in re.findall(r'([^()])', expr)
    # for i in re.findall(r'([^()])', expr)
    expr = expr.replace('sqrt', 'FloorSqrt')
    sqrt3 = False
    if "**(1/3)" in expr:
        sqrt3 = True
        print("**(1/3) is in expression!!!")
        print('expr:', expr)
    expr = replace_sqrt3(expr, power=3)
    expr = replace_sqrt3(expr, power=4)
    expr = expr.replace('**', '^')
    # print('expr:', expr)
    if sqrt3:
        print('replaced expr:', expr)
    return expr


def eq_to_explicit(expr: str, seq: list) -> list[str]:
    """The same as is_linear() - check if the OEIS  expression can be expressed explicitly, i.e. to calculate
    the next term.
        Used for experiments vs TM-OEIS.

    Input:
        - expr: str, OEIS recursive expression.
    Output:
        - list, nonempty if the expression is explicit, empty otherwise.

    To make it more robust this follows these steps:
        1.) Before it is executed, it is checked for linearity. If not, this function is called.
        2.) optimize order - order_optimize
          for now skipping the robust one:
            3.) Check if it contains only one term containing a(n). If so, it is explicit (divide by the rest).
        4.) Otherwise, situation is more complicated, use sympy's solve for \'a(n)\'.
    """

    # 1.)  This was supposed to happen before this function was called.

    # 2.) optimize order:
    expr = order_optimize(expr)

    # 4.) optimize order:
    from sympy.solvers import solve
    if "I" in expr:
        raise ValueError('Variable names might clash with imaginary unit "I" !!!')
    sympy_solutions = solve(expr, 'a(n)', quartics=False)  # to avoid Piecewise output like in: expr =' a(n)^4 +a(n) -n*a(n)^2 - n '
    # print('solutions:', sympy_solutions)
    non_imaginary = [rhs for solution in sympy_solutions if "I" not in (rhs:= sympy_to_cocoa(str(solution)))]
    # print('non_imaginary solutions:', non_imaginary)
    checked = [rhs for rhs in non_imaginary if check_explicit(rhs, seq)]
    explicits = [f'a(n) = {solution}' for solution in checked]
    # print(explicits)
    return explicits


def order_optimize(expr: str) -> str:
    """Preprocess the expression (not containing the 'n' variable,) to minimize the recursion order.
        E.g. a(n-1) - 2*a(n-2) -> a(n) - 2*a(n-1)

    Useful for finding true vector for linear recursive equations of OEIS in Linrec data set.
        Careful! This function is not for general use:
            'a(n-2) - a(n-1) - n' \-> 'a(n-1) - a(n) - n' and not 'a(n) - a(n-1) - (n+1)'
    """

    min_order, max_order = eq_order_explicit(expr)
    # print(min_order, max_order)
    # print(expr)
    if not min_order in (None, 0):
        # a(n-1) -> a(n)
        expr = expr.replace(f'a(n-{min_order})', 'a(n)')
        # print('expr after a(n-1) -> a(n):', expr)
        # in the end: n-min -> n
        for i in range(min_order+1, max_order+1):
            # print('i:', i)
            expr = expr.replace(f'a(n-{i})', f'a(n-{i-min_order})')
            # print('expr after a(n-3) -> a(n-2):', expr)
    # print('expr after all:', expr)
    return expr


def linear_to_vec(linear_expr: str, verbosity=0, allow_constants=False) -> list:
    """Convert linear expression from mb to vector form.
    E.g. 'a(n) - a(n-1) - a(n-2)' -> [1, 1]

    Details:
        Expression is equalized to zero, and then a(n) is isolated and divided by its coefficient.
        the vector of coefficients in the rhs is returned.
    Input:
        - expression that was checked to be linear.
    """


    # head_tail = expr.split('a(n)')
    # if len(head_tail) != 1:
    # expr = 'a(n) -3 + 4*a(n-4) +a(n-2)'
    # expr = 'a(n) -3*a(n-2) +a(n-2)'
    # expr = 'a(n) -3*a(n-4) +a(n-2)'
    # expr = '+a(n) -3*a(n-2) +a(n-2)'
    # expr = '-2*a(n) -3*a(n-2) +a(n-2)'
    # expr = '3*a(n-3) -a(n) -3*a(n-2) +a(n-2)'
    # expr = '+(-7/16875)*a(n) +(-200704/15)*n^3 '
    # linear_expr = expr
    # linear_expr = expr
    # print('\nexpr:', linear_expr)

    expr = linear_expr
    # print(f'{expr = }')
    # is_sindy = True in [True for i in range(1, 22) if f'a(n - {i})' in expr]
    is_sindy = True
    is_sindy = False
    is_sindy = '=' in expr
    # print(is_sindy)
    if is_sindy:
    #     for i in range(1, 22):
    #         # print('i:', i)
    #         expr = expr.replace(f'a(n - {i})', f'a(n-{i})')
    #     expr = expr.replace('+ ', '+').replace('- ', '-')
        rhs_sindy = expr[expr.index('=')+2:]
    #     # print(f'{rhs_sindy = }')
    # linear_expr = expr

    # 1/0
    expr = order_optimize(linear_expr)
    if is_sindy:
        expr, old_expr = rhs_sindy, expr
    order = eq_order_explicit(expr)[1]
    if is_sindy:
        expr = old_expr
    # print(f'{expr = }')
    # expr = [j for j in [i.replace(' ', '') for i in summands] if j != '']  # clean-up empty strings.

    summands = [i for i in expr.split(' ')]
    summands = [j for j in [i.replace(' ', '') for i in summands] if j != '']  # clean-up empty strings.
    lhs = [summand for summand in summands if 'a(n)' in summand]
    rhss = [summand for summand in summands if 'a(n)' not in summand]
    if len(lhs) != 1:
        print('a(n) monomials:', lhs)
        raise ValueError('Strange error in linear_to_vec function!!!      '
                         '... linear expression has more than one \'a(n)\' (or not even one) monomials !!!'
                         f'\nThese are: {lhs}.')
    # print("lhs, rhs:", lhs, rhss)
    # print('summands', summands)
    coef = re.findall(r'^\+?([^an*]*)\*?a\(n\)', lhs[0])[0]
    cases = {'': '1', '+': '1', '-': '-1'}
    coef = cases[coef] if coef in list(cases.keys()) else coef
    # print('coef', coef)
    rhs = "".join(rhss)
    # print('rhs', rhs, len(rhs))
    if is_sindy:
        rhs = rhs_sindy
    rhs = pretty_to_cocoa(rhs, order) if len(rhs) != 0 else '0'
    if is_sindy:
        rhs_sindy = rhs
        divided = rhs
    else:
        # print('rhs', rhs, len(rhs))
        # 1/0

        vars = ",".join(['a_n'] + [f'a_n_{i}' for i in range(1, order+1)])
        # print(vars)
        # print(rhs, 'rhs')
        preamble = f'use P ::= QQ[{vars}];'
        divided = cocoa_eval(preamble + f'(-1)*({rhs})/({coef});', execute_cmd=True, verbosity=verbosity, cluster=False)
    if '/' in divided:
        if verbosity >= 1:
            print('linear solution has non-integer coefficients - never the case with ground truth', divided)
        return None
    else:
        vec = []
        rhs = divided
        # print(f'{rhs = }')
        if verbosity >= 1:
            print('rhs', rhs)
        if is_sindy:
            rhs = rhs_sindy
        summands = re.findall(r'(\+?(-?[^ an*]*)\*?a_n_(\d+))', rhs)
        # summands = re.findall(r'\+?(-?[^ an*]*)\*?(a_n_\d+)', rhs)[0]
        if allow_constants:
            true_summands = rhs.split(' ')
            # print(f'{true_summands = }')
            before = [summand for summand, _, __ in summands]
            # print(f'{before = }')
            consts = [summand for summand in true_summands if summand not in before]
            # print(f'{consts = }')
            if len(consts) > 1:
                raise ValueError(f'More than one constant term in linear expression!!!\n{consts = }')
            const = (consts + [0])[0]
            vec = [int(const)]
        if verbosity >= 1:
            print('summands:', summands)

        dicty = {order_: int(cases[coef] if coef in list(cases.keys()) else coef) for _, coef, order_ in summands}
        vec += [dicty.get(str(o), 0) for o in range(1, order+1)]
        # print(vec)
        # 1/0
        if verbosity >= 1:
            print('vec:', vec)
    return vec


def check_implicit(mb_eq: str, seq: list[int]) -> bool:
    """ I checked that I have not yet implemented this function in exact_ed.py or check_quick.py.
    Although check_eq_man has similar implementation I implemented it from the scratch with hope
    of more efficiency by using Cocoa.

    E.g. 'a(n) - a(n-2) - 1*a(n-1)^1', [0, 1, 1, 2, 3, 5] -> True
    """


    order = eq_order_explicit(mb_eq)[1]
    print('order:', order)
    wanted_zeros = []
    for n in range(order, len(seq)):
        till_now = seq[:n+1]
        print('n', n, 'till_now', till_now)
        evaled = expr_eval(mb_eq, till_now)
        print('n', n, 'till_now', till_now, f'evaled: {evaled}')
        wanted_zeros.append(evaled)
    print(wanted_zeros)
    non_zeros = [i for i in wanted_zeros if i != '0']
    vanishes = len(non_zeros) == 0
    return vanishes, wanted_zeros

def check_implicit_batch(mb_eq: str, seq: list[int], verbosity=0) -> bool:
    """Alternative to check_implicit, which sends list of instructions to Cocoa which
     performs them in whole batch to compensate for signal sending overhead.
     """

    if verbosity >= 1:
        print('inside check_implicit_batch')
    exe_calls = list_evals(mb_eq, seq)
    if verbosity >= 2:
        print('exe_calls:', exe_calls)
    # ['123 -23424 -456', '344554 -34 +223']

    # CoCoa code:
    # li := [-0, -0, -120 + 20 + 100, 1 - 1];
    # min(li) = max(li) and max(li) = 0;

    # CALL_SIZE_LIMIT=131500
    # CALL_SIZE_LIMIT=131000  # 131129 is too big, but 129823 is OK.
    CALL_SIZE_LIMIT=129000
    def prepare_batches(exe_calls: list[str], call_size_limit=CALL_SIZE_LIMIT) -> list[str]:  # 1311 and 133 too big, but 131 is ok
        calls = []
        full_call = ""
        for call in exe_calls:
            # print('len(full_call):', len(full_call))
            if len(call) > call_size_limit:
                print('TOO LARGE NUMBERS. Cutting ourselves some slack here, ignoring all further terms.')
                if full_call != "":
                    calls.append(full_call)
                break
            if len(full_call) + len(call) > call_size_limit:
                calls.append(full_call)
                full_call = call
            else:
                full_call += " " + call
        if full_call != "":
            calls.append(full_call)

        wrapped_calls = [f'li := [{call.replace(";", ",")[:-1]}]; min(li) = max(li) and max(li) = 0;' for call in calls]
        return wrapped_calls
    cocoa_codes = prepare_batches(exe_calls)

    # print(exe_calls)
    if verbosity >= 1:
        print("cocoa_codes:")
        for code in cocoa_codes:
            print(code)
    # print(len(" ".join(exe_calls)))
    # cocoa_code = f'li := [{" ".join(exe_calls).replace(";", ",")[:-1]}]; min(li) = max(li) and max(li) = 0;'
    # print(len(cocoa_code))

    # if verbosity >= 1:
    #     print('cocoa_code:', cocoa_code)
    # cocoa_res = cocoa_eval(cocoa_code, execute_cmd=True, verbosity=0)
    # print('len of code', len(cocoa_code))
    # print('lens of cocoa codes:')
    # print([len(cocoa_code) for cocoa_code in cocoa_codes])

    executes = [cocoa_eval(cocoa_code, execute_cmd=True, verbosity=0) for cocoa_code in prepare_batches(exe_calls)]
    if verbosity >= 2:
        print('executes:', executes)
    res_dict = {'true': True, 'false': False}
    full_output = "".join(executes)
    if 'ERROR: Division by zero' in full_output:
        return False
    elif "--> ERROR: Value must be non-negative\n--> [CoCoALib] FloorSqrt(N)" in full_output:
        # print('Catched non negative FloorSqrt(N) error!!!')
        return False
    elif "--> ERROR: Expecting type INT" in full_output:
        return False

    anss = [res_dict[ans] for ans in executes]
    if verbosity >= 2:
        print('anss:', anss)
    # 1/0
    # cocoa_res = cocoa_eval(cocoa_code, execute_cmd=True, verbosity=0)
    # if verbosity >= 1:
    #     print(cocoa_res, len(cocoa_res), type(cocoa_res))
    # is_check = res_dict[cocoa_res]
    is_check = not (False in anss)
    # print(is_check)
    # 1/0

    return is_check


def list_evals(mb_eq: str, seq: list[int]) -> list:
    """Alternative to check_implicit, which returns list of evaluations of the equation on the sequence.
    List it intended to be sent to CoCoA for further processing.

    Idea:
        - I hypothesize, check_implicit takes too much time because it sends evaluation to CoCoA for each term.
        - To solve this, I will send all evaluations at once to CoCoA and ask to return list of evaluations.
    """

    order = eq_order_explicit(mb_eq)[1]
    # print('order:', order)
    exprs_to_eval = []
    for n in range(order, len(seq)):
        till_now = seq[:n+1]
        # print('n', n, 'till_now', till_now)
        evaled, to_eval = expr_eval(mb_eq, till_now, execute_cmd=False)
        # print('n', n, 'till_now', till_now, f'evaled: {evaled}', 'to_eval:', to_eval)
        exprs_to_eval.append(to_eval)
    # print(exprs_to_eval)
    return exprs_to_eval
    # return


def check_explicit(rhs: str, seq: list[int], verbosity=0) -> bool:
    """Alternative to check_implicit, which sends list of instructions to Cocoa which
     performs them in whole batch to compensate for signal sending overhead.

     Input:
        - rhs: str, OEIS recursive expression, where a(n) is asummed to be on lhs. I.e. a(n) = rhs.
    """

    # print('inside check_explicit')
    # print('rhs:', rhs, f'{seq = }')

    if 'a(n)' in rhs:
        raise ValueError('The expression should not contain a(n) on the left hand side!!!')

    implicit = f'{rhs} -a(n)'
    # print(implicit)
    # print(a)
    # 1/0
    return check_implicit_batch(implicit, seq, verbosity=verbosity)


def predict_with_explicit(mb_rhs: str, train_seq: list[int], n_pred: int, verbosity=0) -> list[int]:
    """Alternative to check_explicit, instead of checking the equation,
    just predicts the next term terms.

    Intended for TM-OEIS benchmark, since every rhs will get us some predicted terms.

    Disadvantages: EXTREMELY SLOWER than check_explicit or check_implicit_batch, since it
    sends plenty of commands to CoCoA.
    """

    if 'a(n)' in mb_rhs:
        raise ValueError('The expression should not contain a(n) on the left hand side!!!')

    mb_eq = mb_rhs
    if verbosity >= 1:
        print(f'{mb_eq = }')
    order = eq_order_explicit(mb_eq)[1]
    if verbosity >= 1:
        print('order:', order)
    wanted_zeros = train_seq.copy()
    for n in range(n_pred):
        # print(f'{wanted_zeros = }')
        till_now = wanted_zeros + [None]
        # print('n', n, 'till_now', till_now)
        rational = expr_eval(mb_eq, till_now)[0]
        if 'ERROR: Division by zero' in rational:
            return wanted_zeros
        elif "--> ERROR: Value must be non-negative\n--> [CoCoALib] FloorSqrt(N)" in rational:
            return wanted_zeros

        # 1/0
        # evaled = int(cocoa_eval(f'floor({rational});', execute_cmd=True))
        evaled = int(cocoa_eval(f'round({rational});', execute_cmd=True))
        # evaled = int(rational) if '/' not in rational else [round(int(i) / int(j)) for i, j in [tuple(rational.split('/'))]][0]
        # print('n', n, 'till_now', till_now, f'evaled: {evaled}')
        if verbosity >= 1:
            print('n', n, 'till_now', till_now, f'evaled: {evaled}')
        wanted_zeros.append(evaled)
    if verbosity >= 1:
        print(wanted_zeros)
    return wanted_zeros


# maybe for TM-OEIS:
# def implicit_to_explicit(linear_eq):
#     return


if __name__ == '__main__':
    outpt = 'a_n*a_n_1 +a_n*a_n_2 -a_n_1*a_n_3 -a_n_2*a_n_3 -3*a_n +3*a_n_3'
    outpt = 'a_n_1 * a_n_2 + a_n_1 * a_n_3 - a_n_2 * a_n_4 - a_n_3 * a_n_4 - 3 * a_n_1 + 3 * a_n_4'
    outpt = 'a_n * a_n_1 + a_n * a_n_2 + a_n_1 * a_n_2 - 3 * a_n - 3 * a_n_1 - 3 * a_n_2 + 7'

    # print(external_prettyprint(outpt, sol_ref= ['a(n-1)', 'a(n-2)', 'a(n-3)', 'a(n-4)', 'a(n-5)']))
    # 1/0

    import pandas as pd

    from mb_oeis import one_mb
    # import matplotlib.pyplot as plt
    # from mavi_oeis import anform

    eq = """
        0.01⋅a(n) - 0.004⋅a(n - 3) - 0.02⋅a(n - 1) + 0.02 = 0
        """
    # print(anform(eq, 0.01))
    # 1/0

    seq_id = 'A000045'
    seq_id = 'A000079'
    csv_filename = 'cores_test.csv'
    N_OF_TERMS_LOAD = 10 ** 5
    N_OF_TERMS_LOAD = 20
    # N_OF_TERMS_LOAD = 10
    # N_OF_TERMS_LOAD = 2
    csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:N_OF_TERMS_LOAD]

    from IPython.display import display, display_latex
    from exact_ed import unnan, eq_order_explicit

    seq, coeffs, truth = (unnan(csv[seq_id]), None, None)
    print(seq)
    # 1/0

    # # seq = sindy_hidden[d_max_lib - 1]
    # # print(n_of_terms, seq)
    # seq = seq[:N_OF_TERMS_LOAD]
    # print(seq)
    # # 1/0


    print('before onemb')
    res = one_mb(seq, order=1, n_more_terms=10, execute=True, library='n', n_of_terms=200)
    print(res)
    # 1/0
    ideal = res[2]

    print('po res')
    print(ideal)
    eqs, heqs = ideal_to_eqs(ideal, max_complexity=16, max_bitsize=100, top_n=10, verbosity=0)
    # eqs = ideal_to_eqs(ideal, complexity=16, top_n=10, verbosity=2)
    # for eq in eqs:
    #     print(f'  len(eq): {len(eq)}, bitsize: {bitsize(eq)}, bitsizes {[bitsize_summand(summand) for summand in eq]}, \neq: {eq}')


    print('eqs:', eqs, 'human eqs:', heqs)
    # 1/0

    expr = 'a(n) -a(n-1) -a(n-2)'
    # expr = ' -a(n-1) -a(n-2)'
    # expr = ' a(n-1) +a(n-2)'
    # expr = 'n + n^2 - n^3'
    # expr = 'a(n-6)*a(n+14) - a(n-2)'
    # expr = 'a(n-6) +a(n-14) -a(n-2)'
    # expr = 'a(n) +13*n -34'
    # expr =   '+(-7/16875)*a(n-1)^4 +(-200704/15)*n^3 '
    # expr =   '+(-7/16875)*a(n-1)*a(n-2) +(-200704/15)*n*a(n)'

    print('eqs:', len(eqs))
    bitsize_ = bitsize(eqs[1])
    print(bitsize_)
    print(f"{bitsize_summand('(-7/16875') = }")
    print(f"{bitsize_summand('-716875*a(n-2)') = }")
    print(f"{bitsize_summand('-a(n-2)') = }")
    print(f"{bitsize_summand('+a(n-2)') = }")

    seq = [0, 1, 1, 2, 3, 5]
    print(expr, seq)
    order = eq_order_explicit(expr)
    print('eq_order:', order)
    # is_check = check_implicit(expr, seq)
    # print('check_implicit:', is_check)
    is_linear_ = is_linear(expr)
    print('is_linear_:', is_linear_)

    print()
    is_explicit_ = eq_to_explicit(expr, seq)
    print(f'{is_explicit_ = }')

    # 1/0
    from sympy.solvers import solve
    from sympy import symbols

    # x, y, a_n = symbols('x y, a(n)')

    # print(solve(y + y**3 - x ** 2 - 1, y))
    # print(solve('y + y**2 - x ** 2 - 1', x))
    print(solve('a(n-2) + y + y**2 - x ** 2 - 1 +(-7/115)*a(n) ', 'a(n)'))

    print(check_explicit('1*a(n-1) +1*a(n-2)', seq))

    # 1/0
    print()
    expr = 'a(n-1) +a(n-2)'
    print(predict_with_explicit(expr, seq[:3], 10))

    # 1/0
    order_optimized = order_optimize(expr)
    print('order_optimized:', order_optimized)

    expr = 'a(n) -a(n-1) -a(n-2)'
    print()
    print('ablated expr:', expr)
    vector = linear_to_vec(expr, verbosity=0, allow_constants=True)
    print('vector:', vector)

    expr = 'a(n)*a(n-1) -a(n-1)^2 -a(n)*a(n-2) +a(n-1)*a(n-2) -a(n) +a(n-2) +1'
    # expr = 'a(n) -a(n-1) -1'
    seq = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3]
    print('expr:', expr, 'seq:', seq)
    print(check_implicit_batch(expr, seq))
    1/0

    print('\n ------ after eqs ------')
    for eq in eqs:
        print(eq)
    # 1/0
    print('after error')

    # increasing_mb(seq_id, csv, max_order=2, n_more_terms=10, library='n', n_of_terms=2000)

