"""
decode_sequence_function
========================
Extract or synthesise a recursive integer-sequence generator from an
LLM response.

Usage
-----
func_src, func_name = decode_sequence_function(llm_response)
print([globals()[func_name](n) for n in range(15)])   # first 15 terms
"""
from __future__ import annotations

import ast
import re
import textwrap
from typing import Optional, Tuple, List


# ----------------------------------------------------------------------
# 1. Helper: find the *best* recursive fn inside a Python code snippet
# ----------------------------------------------------------------------
def _pick_recursive_function(src: str) -> Optional[str]:
    """
    Return the name of the top-level function that (a) is recursive and
    (b) returns something numeric.  Tie-break: the latest definition.
    """
    tree = ast.parse(src)
    best: Tuple[int, int, str] | None = None          # (score, idx, name)

    for idx, node in enumerate(tree.body):
        if not isinstance(node, ast.FunctionDef):
            continue
        name = node.name
        recursive, numeric = False, False

        class V(ast.NodeVisitor):
            def visit_Call(self, call):
                nonlocal recursive
                if isinstance(call.func, ast.Name) and call.func.id == name:
                    recursive = True
                self.generic_visit(call)

            def visit_Return(self, ret):
                nonlocal numeric
                v = ret.value
                if isinstance(v, ast.Constant) and isinstance(v.value, int):
                    numeric = True
                elif isinstance(v, (ast.BinOp, ast.UnaryOp)):
                    numeric = True
                self.generic_visit(ret)

        V().visit(node)
        score = (2 if recursive else 0) + (1 if numeric else 0)
        if best is None or (score, idx) > best[:2]:
            best = (score, idx, name)

    return None if best is None or best[0] == 0 else best[2]


# ----------------------------------------------------------------------
# 2. Helper: build a Python function from a LaTeX-style recurrence
# ----------------------------------------------------------------------
_LATEX_RE = re.compile(
    r"""
    (?P<lhs>[a-zA-Z])\s*\(n\)\s*=
    (?P<rhs>[^,;\\]+?)            # right-hand expression (until comma or \text)
    (?:
        [,;]\s*(?:\\text\{)?\s*with[^\\]*?initial[^\\]*?values
        (?P<inits>.+)
    )?
    """,
    re.VERBOSE | re.DOTALL,
)

_INIT_RE = re.compile(r"([a-zA-Z])\s*\(\s*(\d+)\s*\)\s*=\s*(-?\d+)")


def _parse_latex_recurrence(block: str) -> Optional[Tuple[str, List[int], str]]:
    """
    From something like
      a(n) = a(n-3) + a(n-5), \\text{ with initial values } a(0)=1, a(1)=0, ...
    return (sequence_variable, init_list, rhs_python_expr)
    """
    m = _LATEX_RE.search(block)
    if not m:
        return None
    var = m.group("lhs")
    rhs = m.group("rhs").strip()

    # ---- RHS: turn 'a(n-3) + a(n-5)' ➜ 'seq(n-3) + seq(n-5)'
    rhs_py = re.sub(
        rf"{var}\s*\(\s*n\s*-\s*(\d+)\s*\)",
        r"seq(n-\1)",
        rhs.replace("^", "**"),  # handle powers
    )

    # ---- Initial values
    init_matches = _INIT_RE.findall(block)
    init_dict = {int(idx): int(val) for _, idx, val in init_matches}
    if not init_dict:
        return None
    max_idx = max(init_dict)
    init = [init_dict.get(i, 0) for i in range(max_idx + 1)]

    return var, init, rhs_py


def _make_function_source(init: List[int], rhs_expr: str, name: str = "seq") -> str:
    """
    Craft a Python function that uses memoisation to realise the recurrence.
    """
    indent = " " * 4
    tpl = [
        f"from functools import lru_cache",
        "",
        f"@lru_cache(maxsize=None)",
        f"def {name}(n:int) -> int:",
        f"{indent}init = {init}",
        f"{indent}if n < len(init):",
        f"{indent*2}return init[n]",
        f"{indent}return {rhs_expr}",
        "",
    ]
    return "\n".join(tpl)


# ----------------------------------------------------------------------
# 3. Public API
# ----------------------------------------------------------------------
_CODE_BLOCK_RE = re.compile(
    r"```(?:python)?\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def decode_sequence_function(
    response: str, default_name: str = "seq"
) -> Tuple[str, str]:
    """
    Parameters
    ----------
    response : str
        Raw text returned by the LLM. May include:
          * Python code in ```python ... ``` fences
          * A LaTeX-formatted recurrence with initial values
    default_name : str, optional
        Fallback function name if we need to invent one (for LaTeX branch).

    Returns
    -------
    tuple
        (function_source_code:str, function_name:str)

    Raises
    ------
    ValueError
        If no suitable sequence function can be derived.
    """
    # ---- 1️⃣  Try to fish out a recursive Python function -----------------
    code_blocks = _CODE_BLOCK_RE.findall(response)
    for blk in code_blocks:
        fn = _pick_recursive_function(blk)
        if fn:
            # Make sure code string is dedented & runnable as-is
            source = textwrap.dedent(blk).rstrip() + "\n"
            return source, fn

    # ---- 2️⃣  Fall back to parsing a LaTeX recurrence ----------------------
    latex_match = _parse_latex_recurrence(response)
    if latex_match:
        _, init, rhs_py = latex_match
        print(f'{_ = }, {rhs_py = }')
        print(f'{init = }')
        src = _make_function_source(init, rhs_py, default_name)
        return src, default_name

    # ---- ❌  Nothing worked -------------------------------------------------
    raise ValueError("Could not locate a recursive sequence in the response.")


# ----------------------------------------------------------------------
# ⬇️  quick self-test  ------------------------------------------------------
if __name__ == "__main__":
    _latex_resp = r"""
    \boxed{a(n) = a(n-3) + a(n-5), \quad \text { with initial values}
    a(0)=1,\;a(1)=0,\;a(2)=0,\;a(3)=1,\;a(4)=0}
    """
    src, name = decode_sequence_function(_latex_resp)
    print(f'src:\n{src}')
    print(f'{name = }')
    # ns = {}
    # print("LaTeX demo:", [ns[name](i) for i in range(15)])
    1/0

    _py_resp = """
    Sure! Here is a generator:

    ```python
    def helper(k):           # not recursive
        return 1

    def is_square(x):
        s = int(x**0.5)
        return s*s == x

    def sequence(n):
        if n == 0:
            return 2
        prev = sequence(n-1)
        cand = prev + 1
        return cand + 1 if is_square(cand) else cand
    ```
    """
    src2, name2 = decode_sequence_function(_py_resp)
    ns2 = {}
    print("Python demo :", [ns2[name2](i) for i in range(15)])
