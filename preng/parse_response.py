# """
# decode_sequence_function
# ========================
# Extract or synthesise a recursive integer-sequence generator from an
# LLM response.
#
# Usage
# -----
# func_src, func_name = decode_sequence_function(llm_response)
# print([globals()[func_name](n) for n in range(15)])   # first 15 terms
# """
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
    print(src)
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

    print(f'{best = }')
    # 1/0
    return None if best is None or best[0] == 0 else (best[0], best[2])


# ----------------------------------------------------------------------
# 2. Helper: build a Python function from a LaTeX-style recurrence
# ----------------------------------------------------------------------

# original:
# _LATEX_RE = re.compile(
#     r"""
#     (?P<lhs>[a-zA-Z])\s*\(n\)\s*=
#     (?P<rhs>[^,;\\]+?)            # right-hand expression (until comma or \text)
#     (?:
#         [,;]\s*(?:\\text\{)?\s*with[^\\]*?initial[^\\]*?values  # actually not needed I believe, could infer from question inits.
#         (?P<inits>.+)
#     )?
#     """,
#     re.VERBOSE | re.DOTALL,
# )

# # example = """ \boxed{a(n) = a(n-3) + a(n-5), \quad \text { with initial values} """
# _LATEX_RE = re.compile(
#     r"""
#      # (?P<lhs>[a-zA-Z])\s*\(n\)\s*=
#      (?P<lhs>[a-zA-Z])\s*\(n\)\s*=[^,;\\]+
#     # (?:
#     #     [,;]\s*(?:\\text\{)?\s*with[^\\]*?initial[^\\]*?values  # actually not needed I believe, could infer from question inits.
#     #     (?P<inits>.+)
#     # )?
#     """,
#     re.VERBOSE | re.DOTALL,
#     )
#
# _LATEX_RE = re.compile( r"(?P<lhs>[a-zA-Z])\s*\(n\)\s*=[^,;\\]+", re.VERBOSE | re.DOTALL, )

# _LATEX_RE = re.compile(
#     r"""
#      (?P<lhs>[a-zA-Z])\s*\(n\)\s*=
#      (?P<rhs>[^,;\\]+)
#      (?:
#          [,;]\s*(?:\\text\{)?\s*with[^\\]*?initial[^\\]*?values  # actually not needed I believe, could infer from question inits.
#          (?P<inits>.+)
#      )?
#     """,
#     re.VERBOSE | re.DOTALL,
#     )

_LATEX_RE = re.compile(
    r"""
     (?P<lhs>[a-zA-Z])\s*\(n\)\s*=
     (?P<rhs>[^,;.\n]+)
    """,
    # re.VERBOSE | re.DOTALL,
    re.VERBOSE,
    )

# _INIT_RE = re.compile(r"([a-zA-Z])\s*\(\s*(\d+)\s*\)\s*=\s*(-?\d+)")  # verjetno nepotrebno, zaradi init from question


def two_options(block: str):
    """try the last latex equation after 'final answer' and the last equation in the block before """

    # 1. Take response after "final answer"
    if 'final answer' in block.lower():
        blocks = block.lower().split('final answer')[-2:]
    options = []

    return


def _parse_latex_recurrence(block: str) -> Optional[List[Tuple[str, List[int], str]]]:
    """
    From something like
      a(n) = a(n-3) + a(n-5), \\text{ with initial values } a(0)=1, a(1)=0, ...
    return (sequence_variable, init_list, rhs_python_expr)
    """

    # print(block)
    # m = _LATEX_RE.search(block)
    ms = _LATEX_RE.findall(block)
    print(ms)
    # 1/0
    # if not ms:
    #     return None
    rhss = []
    for m in ms:
        # var = m.group("lhs")
        # rhs = m.group("rhs").strip()
        var = m[0]
        rhs = m[1].strip()
        print(f'var, rhs: {var, rhs}')

        # ---- RHS: turn 'a(n-3) + a(n-5)' ➜ 'seq(n-3) + seq(n-5)'
        # rhs = 'a(n-1) + (n-1) \cdot a(n-2)'
        rhs_py = re.sub(
            rf"{var}\s*\(\s*n\s*-\s*(\d+)\s*\)",
            r"seq(n-\1)",
            rhs.replace("^", "**"),  # handle powers
        )
        rhs_py = rhs_py.replace("\cdot", "*")  # handle powers

        # # ---- Initial values
        # init_matches = _INIT_RE.findall(block)
        # init_dict = {int(idx): int(val) for _, idx, val in init_matches}
        # if not init_dict:
        #     return None
        # max_idx = max(init_dict)
        # init = [init_dict.get(i, 0) for i in range(max_idx + 1)]

        # return var, init, rhs_py
        # print(f'var, rhs_py: {var, rhs_py}')
        # 1/0
        rhss.append((var, rhs_py))
    return rhss


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
    r"```(?:python)\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
# # print(re.findall( r"```(?:python)?.+\n(.*?)```", '```python \n 232323```'))
# print(re.findall( r"11(?:44)+", "1112311114444124462114456" ))
# # print(_CODE_BLOCK_RE.findall())
# # print(_CODE_BLOCK_RE.findall('```python\na=3\nb=4```'))
#
# text = "apple pie, apple tart"
# # pattern = r"(?:apple) (pie|tart)"
# pattern = r"apple (pie|tart)"
# pattern = r"(?P<word>\w+)\s+(?P=word)"
# # print(re.findall(pattern, 'ohmy there myhere there ohmy there', re.VERBOSE))
# print(re.findall(pattern, 'ohmy there myhere there ohmy there'))
# # print(re.findall(pattern, text))
# 1/0
# #

def decode_sequence_function( response: str, inits: List[int], default_name: str = "latex_seq" ) -> Tuple[str, str]:
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

    print('here I stand')
    # ---- 1️⃣  Try to fish out a recursive Python function -----------------
    print(f'response:\n{response}')
    code_blocks = _CODE_BLOCK_RE.findall(response)
    # print('code_blocks exist:')
    print(f'{code_blocks = }')
    # 1/0

    best_block: Tuple[int, int, str, str] | None = None          # (score, idx, name)

    for idx, blk in enumerate(code_blocks):
        # print(f'blk:\n{blk}')
        dedented = textwrap.dedent(blk)
        picked_fn = _pick_recursive_function(dedented)
        if picked_fn is not None:
            score, fn = picked_fn

        # print(f'fn: {fn}')
        # print(f' ----- ------ ------ ----- ')
        # if fn:
            # Make sure code string is dedented & runnable as-is
            # print(blk)
            # print(textwrap.dedent(blk))
            # print(f' ----- ------ ------ ----- ')
            source = textwrap.dedent(blk).rstrip() + "\n"
            # return source, fn
#     score = (2 if recursive else 0) + (1 if numeric else 0)
            if best_block is None or (score, idx) > best_block[:2]:
                best_block = (score, idx, source, fn)


    # return None if best_block is None or best_block[0] == 0 else (best_block[2], best_block[3])
    if not (best_block is None or best_block[0] == 0):
        return (best_block[2], best_block[3])


    print('Seems no Python code was found!')
    # ---- 2️⃣  Fall back to parsing a LaTeX recurrence ----------------------
    print('Started parsing latex equation, if any.')

    # my Plan/idea:
    # convert all equations to recursive Python functions and concatenate them into python block code.
    # Then run _pick_function on this block to pick function that makes the most sense.

    latex_matches = _parse_latex_recurrence(response)
    print(f'{latex_matches = }')
    # 1/0
    latex_fn_codes = []
    for i, latex_match in enumerate(latex_matches):
        _, rhs_py = latex_match
        print(f'{_ = }, {rhs_py = }')
        print(f'{inits = }')
        fn_name = f'{default_name}_{i}'
        src = _make_function_source(inits, rhs_py, fn_name)
        print(f'src:\n{src}')
        latex_fn_codes.append((src, fn_name))

    # 1/0
    print(f'{latex_fn_codes = }')
    code_block = '\n'.join([code for code, fn_name in latex_fn_codes])
    print(f'code_block:\n{code_block}')
    print(f'\n-- End of: code_block:\n')
    print()
    answer = _pick_recursive_function(code_block)  # None | score, fn_name
    print(f'{answer = }')
    if answer is not None:
        return code_block, answer[1]


    print('Unfortunately, NO LATEX equation as well as no PYTHON CODE was successfully parsed into recursive function/equation.')
    # ---- ❌  Nothing worked -------------------------------------------------
    raise ValueError("Could not locate a recursive sequence in the response.")





# needless:
# # ----------------------------------------------------------------------
# # ⬇️  quick self-test  ------------------------------------------------------
if __name__ == "__main__":
    _latex_resp = r"""
    \boxed{a(n) = a(n-3) + a(n-5), \quad \text { with initial values}
    a(0)=1,\;a(1)=0,\;a(2)=0,\;a(3)=1,\;a(4)=0}
    """
    # src, name = decode_sequence_function(_latex_resp, [1,1,1,1,1])
    # # No need to check order(latex_eq), since we can asume a(0), ..., a(25) from question.
    # # raise ValueError('programmer: Take care of order(latex_eq) to insert inits of appropriate length!!!')
    # print(f'src:\n{src}')
    # print(f'{name = }')
    # # 1/0
#     ns = {}
#     print("LaTeX demo:", [ns[name](i) for i in range(15)])


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
    _py_resp = " a(0) = 1,\n a(2) = 1, \n a(n) = a(n-1), dstst dstndstn\ndstndstn\ndstnst a(n) = 2*n final answer a(n) = a(n-1) + a(n-2)"  # not yet covered
    _py_resp = " a(0) = 1,\n a(2) = 1, \n a(n) = a(n-1), dstst dstndstn\ndstndstn\ndstnst a(n) = 2*n \n final answer a(n) = a(n-1) + a(n-2)"
    # _py_resp = " a(n) = a(n-1) + (n-1) \cdot a(n-2)"
    # _py_resp = " a(n) = a(n-1) + (n-1) \cdot a(n-2). final answer a(n) = a(n-1) + a(n-2)"
    src2, name2 = decode_sequence_function(_py_resp, [1,1,1,1,1,1,1])
    print(src2)
    print(name2)

# src2, name2 = _pick_recursive_function(_py_resp)
    # print(f'{src2 = }')
    # print(f'{name2 = }')
#     ns2 = {}
#     print("Python demo :", [ns2[name2](i) for i in range(15)])
#     re.compile()
