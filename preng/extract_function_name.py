import ast
from typing import Optional


def extract_function_name(code: str) -> Optional[str]:
    """
    Inspect a Python source string and guess which *top-level* function
    is generating an integer sequence.

    Heuristics (ordered by importance):
    1. Recursion   – the function calls itself
    2. Numeric-ish – it returns an int literal or an arithmetic expression
    3. Tie-break   – choose the last-defined candidate

    Parameters
    ----------
    code : str
        The Python source code to inspect.

    Returns
    -------
    Optional[str]
        The chosen function's name, or None if no function is found.
    """
    tree = ast.parse(code)
    candidates = []
    # print(tree)
    # print(tree.body)
    # 1/0

    # look only at *module-level* defs
    for idx, node in enumerate(tree.body):
        # print(idx, node)
        if not isinstance(node, ast.FunctionDef):
            continue

        name = node.name
        # print(name)
        # print(node.func)
        # print(node.func.id)
        # print('id')
        recursive = False
        returns_numeric = False

        class Analyzer(ast.NodeVisitor):
            def visit_Call(self, call_node):
                nonlocal recursive
                # self-call  → recursion
                if isinstance(call_node.func, ast.Name) and call_node.func.id == name:
                    recursive = True
                self.generic_visit(call_node)

            def visit_Return(self, ret_node):
                nonlocal returns_numeric
                v = ret_node.value
                # int literal  e.g. 0, 1, 42
                if isinstance(v, ast.Constant) and isinstance(v.value, int):
                    returns_numeric = True
                # arithmetic expression  e.g. a + 1, candidate + 1
                elif isinstance(v, ast.BinOp):
                    returns_numeric = True
                self.generic_visit(ret_node)
    #
        Analyzer().visit(node)
        score = (2 if recursive else 0) + (1 if returns_numeric else 0)
        candidates.append((score, idx, name))

    # candidates = [('perf', 2, 'dsddstndstndstn'), ( 'sq', 4, [3455])]
    # print(candidates)
    if not candidates:
        return None

    # pick the highest-scoring; on ties choose the *latest* definition
    # print('max', max(candidates, key=lambda t: (t[0], t[1])))
    # print('max', max(candidates, key=lambda t: (t[0], t[1]))[2])
    # print( max(candidates, key=lambda t: (t[0], t[1])))
    return max(candidates, key=lambda t: (t[0], t[1]))[2]



# -------------------------  demo  -------------------------
if __name__ == "__main__":
    sample_code = """
def is_perfect_square(x):
    s = int(x ** 0.5)
    return s * s == x

def calculate_sequence(n):
    if n == 0:
        return 2
    prev = calculate_sequence(n - 1)
    candidate = prev + 1
    if is_perfect_square(candidate):
        return candidate + 1
    else:
        return candidate
"""

    print(extract_function_name(sample_code))      # → calculate_sequence
