""" Actually, it turns out that currently dont need such a tokenizer. """


import sympy as sp
from sympy.printing.precedence import precedence


def _tokenize(expr: sp.Basic, parent_prec=None):
    """
    Recursively tokenize a SymPy expression into a list of string tokens,
    using infix notation with explicit operators and parentheses when needed.

    Examples (up to SymPy's canonical reordering of terms/factors):
        x + y           -> ['x', '+', 'y']
        x - y           -> ['x', '-', 'y']
        x + y*z         -> ['x', '+', 'y', '*', 'z']
        (x + y)*z       -> ['z', '*', '(', 'x', '+', 'y', ')']
        (x + y)**2      -> ['(', 'x', '+', 'y', ')', '^', '2']
        -x              -> ['-', 'x']
        -x*y            -> ['-', 'x', '*', 'y']
        sin(x + y)      -> ['sin', '(', 'x', '+', 'y', ')']
    """
    expr_prec = precedence(expr)
    if parent_prec is None:
        parent_prec = expr_prec

    # --- Atoms: symbols and numbers ---
    if expr.is_Symbol:
        tokens = [expr.name]

    elif expr.is_Number:
        tokens = [str(expr)]

    # --- Addition (handle + and - nicely) ---
    elif expr.is_Add:
        tokens = []
        # Flatten additive terms
        args = list(sp.Add.make_args(expr))

        for i, arg in enumerate(args):
            if i == 0:
                # First term as-is
                tokens.extend(_tokenize(arg, expr_prec))
            else:
                sign = "+"
                arg_eff = arg

                # Numeric negative term: e.g., -2, -3*x, etc.
                if arg_eff.is_Number and arg_eff.is_real and arg_eff.is_negative:
                    sign = "-"
                    arg_eff = -arg_eff
                else:
                    coeff, rest = arg_eff.as_coeff_Mul()
                    if coeff.is_Number and coeff.is_negative:
                        sign = "-"
                        arg_eff = -arg_eff

                tokens.append(sign)
                tokens.extend(_tokenize(arg_eff, expr_prec))

    # --- Multiplication (handle unary minus) ---
    elif expr.is_Mul:
        coeff, factors = expr.as_coeff_mul()
        factors = list(factors)
        tokens = []

        # Numeric coefficient, if not 1
        if coeff != 1:
            # Treat -1 * f(...) as unary minus
            if coeff == -1 and factors:
                tokens.append("-")
            else:
                tokens.extend(_tokenize(coeff, expr_prec))

        for f in factors:
            if tokens:
                # Avoid "- * x" for unary minus; want "-x"
                if tokens[-1] != "-":
                    tokens.append("*")
            tokens.extend(_tokenize(f, expr_prec))

    # --- Power ---
    elif expr.is_Pow:
        base, exp = expr.as_base_exp()
        tokens = []
        tokens.extend(_tokenize(base, expr_prec))
        tokens.append("^")
        tokens.extend(_tokenize(exp, expr_prec))

    # --- Function call: f(a, b, ...) ---
    elif expr.is_Function:
        tokens = [expr.func.__name__, "("]
        for i, arg in enumerate(expr.args):
            if i > 0:
                tokens.append(",")
            tokens.extend(_tokenize(arg, precedence(arg)))
        tokens.append(")")

    # --- Fallback: just stringify ---
    else:
        tokens = [str(expr)]

    # Add parentheses if this subexpression has lower precedence than its parent
    if expr_prec < parent_prec:
        return ["("] + tokens + [")"]
    else:
        return tokens


def denumerate_tokens(tokens):
    """
    Replace enumerated constants like 'C0', 'C1', ... with 'C'.
    """
    out = []
    for t in tokens:
        if t.startswith('C') and t[1:].isdigit():
            out.append('C')
        else:
            out.append(t)
    return out

def tokenize_denumerate(expr):
    """
    Tokenize the expression and denumerate constants in one step.
    """
    tokens = _tokenize(expr)
    return denumerate_tokens(tokens)

def tokenize_expr(expr):
    """
    Public entry point: accepts either a SymPy expression or anything
    sympifiable (like a string or Python int/float).
    """
    expr = sp.sympify(expr)
    return _tokenize(expr, precedence(expr))



if __name__ == "__main__":
    from ProGED.model_box import ModelBox
    m = ModelBox()

    # ProGED's cannonic also fails (last time it did not?!)
    vars = ["x", "y", "z"]
    symbols = {"x": vars, "start": "S", "const": "C"}
    expr = '(C*z+C+C)/(C+C*z)'
    # expr = ['(' , 'C0', '*', 'z', '+', 'C1', '+', 'C2', ')', '/', '(', 'C3', '+', 'C4', '*', 'z', ')']
    # expr = ["x", "+", "y"]
    print(m.string_to_canonic_expression(expr, symbols))

    
