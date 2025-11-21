from sympy import Add, Mul, Pow


def tokenize_generic(expr):
    if expr.is_Atom:
        return [str(expr)]

    tokens = []
    for arg in expr.args:
        tokens.extend(tokenize_generic(arg))

    # optionally insert operators depending on expr.func
    if isinstance(expr, Add):
        ops = ["+"] * (len(expr.args) - 1)
    elif isinstance(expr, Mul):
        ops = ["*"] * (len(expr.args) - 1)
    elif isinstance(expr, Pow):
        ops = ["^"]
    else:
        ops = []

    # interleave operands and operators
    out = []
    for a, op in zip(tokens, ops + [""]):
        out.append(a)
        if op:
            out.append(op)
    return out
