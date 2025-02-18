import os
import subprocess

# from ProGED_oeis.examples.oeis.csv_plot import verbosity
from cocoa_location import cocoa_location
import re

# def mb_oeis(points, )

def pretty_to_cocoa(linear_expr, order) -> str:
    """Convert equation from pretty to cocoa format.
    E.g. a(n-1) -> a_n_1.

    Primarely used for linear expressins for linear_to_vec
    Input:
        - linear_expr: str, linear equation in pretty format.
        - order: int, order of the equation.
    """

    bij = {f'a(n-{i})': f'a_n_{i}' for i in range(1, order+1)}
    bij.update({'a(n)': 'a_n'})
    for key in bij:
        linear_expr = linear_expr.replace(key, bij[key])
    # print(linear_expr)
    return linear_expr

# most common polynomial variables indeterminates:
vars_default = 'x, y, z, t, u, v, w, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t'.split(', ')
# # print(vars_lib)
def vars_str(dim, var_names='djus'):
    """
    Returns list of strings of variable names.

    Args:
        - dim: int, number of variables
        - var_names:
            - str, one of ['djus', 'num', 'oeis']
            - or list of strings, variable names, e.g. ['a_n', 'n', 'a_n_1']
    """
    vars_dict = {
        # 'djus': ",".join(vars_default[:dim]), # [the uss]ual suspects
        # 'num': ",".join([f'x_{i}' for i in range(dim)]),
        # 'oeis': ",".join([f'a_{{n-{i}}}' for i in range(dim)]),
        'djus': vars_default[:dim], # [the uss]ual suspects
        'num':  [f'x_{i}' for i in range(dim)],
        'oeis': [f'a_n_{i}' for i in range(dim)],
        }

    vars_dict = { key: ",".join(vars) for key, vars in vars_dict.items()}
    # print(vars_dict)
    vars_list =  vars_dict[var_names] if isinstance(var_names, str) else ",".join(var_names)
    if "{" in "".join(vars_list) or "}" in "".join(vars_list):
        raise ValueError('Variable names must not contain "{" or "}"!!')
    return vars_list


def mb(points: list, execute_cmd=False, var_names='djus', verbosity=0):
    """Runs 5 lines of cocoa code with given points and returns the ideal
        It makes sure the numper of variables is appropriate.
        Cocoa code:
            use P ::= QQ[x,y];
            ////y = x^2: success:
            Points := mat([[0, 0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81]]);
            I := IdealOfPoints(P, Points);
            I;

    Console command:
        echo "Points := ... IdealOfPoints;I;" | ./CocoAInterpter
    """

    CALL_SIZE_LIMIT=128000
    if len(f'{points}') > CALL_SIZE_LIMIT:
        # raise ValueError(f'cocoa_code is too long: {len(cocoa_code)} > {CALL_SIZE_LIMIT}!!')
        print(f'\ncocoa_code is probably too long!!!: {len(f"{points}") = } > {CALL_SIZE_LIMIT = }!!\n')

    dims = [len(p) for p in points]
    if len(set(dims)) != 1:
        raise ValueError('All points must have the same number of dimensions!!')
    dim = dims[0]
    # check type of points:
    if not all([isinstance(p, list) for p in points]) or not isinstance(points, list):
        raise ValueError('Points must be a list of lists!!')

    # [f"x_{i}" for i in range(dim)]
    # vars = ",".join([f"x_{i}" for i in range(dim)])
    # vars = vars_str(dim, 'djus')
    vars = vars_str(dim, var_names)
    if verbosity > 0:
        print('vars:', vars)
    # 1/0

    # points
    # use P ::= QQ[x,y];
    cocoa_code = f"use P ::= QQ[{vars}];"
    cocoa_code += f"Points := mat({points});"
    cocoa_code += "I := IdealOfPoints(P, Points);I;"
    if verbosity > 0:
        print('cocoa_code pretty printed:\n', cocoa_code.replace(';', ';\n'))
    # print('cocoa_code oneliner:\n', cocoa_code)

    # a) set location of cocoa file that will be executed by cocoa interpreter
    # print('Current linux bash location:')
    # print(os.getcwd())

    # b) execute cocoa file
    # command = f"cd ../{cocoa_location[2:]}; echo \"{cocoa_code}\" | ./CoCoAInterpreter"
    command = f"cd {cocoa_location}; echo \"{cocoa_code}\" | ./CoCoAInterpreter"

    if verbosity > 0:
        print(command)
        print()
    if execute_cmd:
        if verbosity > 0:
            print("Executing LINUX command for real...")
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        # b) extract output ignoring logo
        cocoa_res = re.findall(r'ideal.*\n', output.decode())
        if len(cocoa_res) == 0:
            print("Unexpected output, full output: \n", output.decode())
            raise ValueError('Unexpected output from CoCoAInterpreter!!')
        else:
            cocoa_res = cocoa_res[0][:-1]
            if verbosity > 0:
                print('output:', cocoa_res)

            first_generator = cocoa_res[6:].split(',')[0]
            # print('equation:\n', first_generator)
            return first_generator, cocoa_res
    print("NOT Executing LINUX command for real... just simulating command")
    raise ValueError('Not executing command for real!!')

    return


def cocoa_eval(cocoa_code: str, execute_cmd=False, verbosity=0, cluster=False):
    """Runs cocoa code and returns the result.
    Console command:
        echo "-(12312/243434)*2^3;" | ./CocoAInterpter
    """

    CALL_SIZE_LIMIT=129000
    if len(cocoa_code) > CALL_SIZE_LIMIT:
        # raise ValueError(f'cocoa_code is too long: {len(cocoa_code)} > {CALL_SIZE_LIMIT}!!')
        print(f'\ncocoa_code is probably too long!!!: {len(cocoa_code) = } > {CALL_SIZE_LIMIT = }!!\n')
    # command = f"cd ../{cocoa_location[2:]}; echo \"{cocoa_code}\" | ./CoCoAInterpreter"
    command = f"cd {cocoa_location}; echo \"{cocoa_code}\" | ./CoCoAInterpreter"
    if verbosity > 0:
        print('cocoa_code pretty printed:\n', cocoa_code.replace(';', ';\n'))

    if execute_cmd:
        if verbosity > 0:
            print()
            print(f"Executing LINUX command for real... {command*(verbosity>0)}")
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        if verbosity > 0:
            print(output.decode())

        # b) extract output ignoring logo
        cocoa_res = output.decode().split('indent(VersionInfo(), 2); -- for information about this version\n')[-1]
        if cocoa_res[-1] == '\n':
            cocoa_res = cocoa_res[:-1]
        # print('\n'*10, f'cocoa output:{cocoa_res}<--Till here')
        return cocoa_res
    print("NOT Executing LINUX command for real... just simulating command")
    raise ValueError('Not executing command for real!!')
    return


def mb_wrap_old(filename = 'runable.cocoa5', file_dir = 'julia/mb/'):

    # a) set location of cocoa file that will be executed by cocoa interpreter
    print('Current linux bash location:')
    print(os.getcwd())
    filename_loc = os.getcwd() + file_dir
    # filename = 'runable.cocoa5'
    filefull = filename_loc + filename
    print(' -=- exiting Python... '*20)


    # b) execute cocoa file
    # command = f"cd ../{cocoa_location[2:]}; ./CoCoAInterpreter {filefull}"
    command = f"cd {cocoa_location}; ./CoCoAInterpreter {filefull}"
    # print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    # print("Command output: \n", output.decode())

    # b) extract output ignoring logo
    cocoa_res = re.findall(r'ideal.*\n', output.decode())[0][:-1]
    print(cocoa_res)

    first_generator = cocoa_res[6:].split(',')[0]
    print(first_generator)


if __name__ == '__main__':
    print(cocoa_eval("-(12312/243434)*2^3;", execute_cmd=True))
    print(cocoa_eval("2 +-1;", execute_cmd=True))
    print(cocoa_eval("(0) -(1) -(1);", execute_cmd=True))
    # print(cocoa_eval("3 +2*-1;", execute_cmd=True))  # causes error
    print(mb([[0, 0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81]]))
    # print(mb([[0, 0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81]], execute_cmd=True))
    pass
