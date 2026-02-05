import os
import subprocess

import re


def oraj(data: list, execute_cmd=False, is_berlekamp=False, verbosity=0):
    """Runs equation guessing via ore_algebra or alternatively berlekamp_massey algorithm.

    Console command:
        miniforge3/envs/sage/bin/sage -c "from ore_algebra import *;data = [0, 1, 1,2,3, 5, 8];print(guess(data, OreAlgebra(ZZ['n'], 'Sn')))"
            or (in case of using berlekamp_massey):
        miniforge3/envs/sage/bin/sage -c "from sage.matrix.berlekamp_massey import berlekamp_massey;data = [0, 1, 1,2,3, 5, 8];berlekamp_massey(data)"
    """

    # limit data length
    data = data[:200]
    if is_berlekamp == True:
        if len(data) % 2 != 0:
            data = data[:-1]

    CALL_SIZE_LIMIT=128000
    if len(f'{data}') > CALL_SIZE_LIMIT:
        # raise ValueError(f'cocoa_code is too long: {len(cocoa_code)} > {CALL_SIZE_LIMIT}!!')
        print(f'\nsage_code is probably too long!!!: {len(f"{data}") = } > {CALL_SIZE_LIMIT = }!!\n')

    sage_code = f"../miniforge3/envs/sage/bin/sage -c \"from ore_algebra import *;"
    sage_code += f"data = {data};print(guess(data, OreAlgebra(ZZ['n'], 'Sn')))\""
    if is_berlekamp == True:
        berlekamp_massey_code = "../miniforge3/envs/sage/bin/sage -c "
        berlekamp_massey_code += "\"from sage.matrix.berlekamp_massey import berlekamp_massey;\n"
        berlekamp_massey_code += f"data = {data};\npoly = berlekamp_massey(data);\nprint(poly)\""

    if is_berlekamp == "fricas":
        fricas_code = "echo \"1+2\" | fricas -nosman"
        fricas_code = f"echo \"guessPRec({data})\" | fricas -nosman"

    # b) execute cocoa file
    command = sage_code
    if is_berlekamp == True:
        command = berlekamp_massey_code
    elif is_berlekamp == "fricas":
        command = fricas_code

    if verbosity > 0:
        print(command)
        print()
    if execute_cmd:
        if verbosity > 0:
            print("Executing LINUX command for real...")
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        bash_res = output.decode()
        return bash_res
    print("NOT Executing LINUX command for real... just simulating command")
    raise ValueError('Not executing command for real!!')

    return


if __name__ == "__main__":

    ORAJ = False
    ORAJ = True
    if ORAJ:
        seq = [0, 1, 1, 2, 3, 5, 8]
        # oraj([0, 1, 1, 2, 3, 5, 8])
        # ans = oraj([0, 1, 1, 2, 3, 5, 8], execute_cmd=True, is_berlekamp=True)
        # ans = oraj([0, 1, 1, 2, 3, 5, 8], execute_cmd=False, is_berlekamp=True, verbosity=1)

        # ans = oraj([13424224, 1, 1, 2, 3, 5, 8,13, 1, 2], execute_cmd=True, is_berlekamp=True, verbosity=1)
        # seq = [13424224, 1, 1, 2, 3, 5, 8, 13, 1, 2]
        # ans = oraj(seq, execute_cmd=False, is_berlekamp='fricas', verbosity=1)
        ans = oraj(seq, execute_cmd=True, is_berlekamp='fricas', verbosity=1)
        # ans = oraj([13424224, 1, 1, 2, 3, 5, 8,13, 1, 2], execute_cmd=True, is_berlekamp='fricas', verbosity=1)
        print(ans)
        # ans = oraj([0, 1, 1, 2], execute_cmd=True)
        # print(ans, len(ans))
        # # print(len(ans))

    # results analysis
    ANALYZE = False
    # ANALYZE = True
    if ANALYZE:
        import os
        # indir = 'ore_algebra0'
        indir = 'berlk-messay0/444571'
        indir = 'berlk-messay0/447940'
        files = sorted(os.listdir(f'./results/{indir}'))
        print(files)
        for file in files[:160]:
            if file[-3:] == 'out':
                with open(f"./results/{indir}/{file}", 'r') as f:
                    # print(f.read())
                    eq, is_disco = re.findall('eq = \'(.*)\'.+\nis Disco: (\w+)', f.read())[0]
                    if is_disco == 'True':
                        # print(f'{file}:', eq)
                        # print(f'{file}:', eq.strip('\\n'))
                        eq = eq[:-2] if eq[-2:] == '\\n' else eq
                        print(f'{file}:', eq[:100])
