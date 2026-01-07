import os
import subprocess

import re


def oraj(data: list, execute_cmd=False, verbosity=0):
    """Runs 5 lines of cocoa code with given points and returns the ideal
        It makes sure the numper of variables is appropriate.
        Cocoa code:
            data = <given data>
            guess(data, OreAlgebra(ZZ['n'], 'Sn'))

    Console command:
        miniforge3/envs/sage/bin/sage -c "from ore_algebra import *;data = [0, 1, 1,2,3, 5, 8];print(guess(data, OreAlgebra(ZZ['n'], 'Sn')))"
    """

    # limit data length
    data = data[:200]

    CALL_SIZE_LIMIT=128000
    if len(f'{data}') > CALL_SIZE_LIMIT:
        # raise ValueError(f'cocoa_code is too long: {len(cocoa_code)} > {CALL_SIZE_LIMIT}!!')
        print(f'\nsage_code is probably too long!!!: {len(f"{data}") = } > {CALL_SIZE_LIMIT = }!!\n')

    sage_code = f"../miniforge3/envs/sage/bin/sage -c \"from ore_algebra import *;"
    sage_code += f"data = {data};print(guess(data, OreAlgebra(ZZ['n'], 'Sn')))\""


    # b) execute cocoa file
    command = sage_code

    if verbosity > 0:
        print(command)
        print()
    if execute_cmd:
        if verbosity > 0:
            print("Executing LINUX command for real...")
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        sage_res = output.decode()
        return sage_res
    print("NOT Executing LINUX command for real... just simulating command")
    raise ValueError('Not executing command for real!!')

    return


if __name__ == "__main__":

    # oraj([0, 1, 1, 2, 3, 5, 8])
    ans = oraj([0, 1, 1, 2, 3, 5, 8], execute_cmd=True)
    print(ans)
    ans = oraj([0, 1, 1, 2], execute_cmd=True)
    print(ans, len(ans))
    # print(len(ans))
