"""
Generate unstructions for llm.

number of examples: 24k * (175 + 180)* 2 = 8.4M
or: 24k * (20)* 2 = 1M
15

First iteration:
"""

import pandas as pd

from exact_ed import unpack_seq, unnan

TESTSET = False
# TESTSET = True

dir = 'preng/'

def linearLLM():
    """Generate linear LLM prompts - first round of experiments."""
    if TESTSET:
        test_csv = pd.read_csv(dir + 'linrec_and_dasco.csv', low_memory=False)
    else:
        train_csv = pd.read_csv(dir + 'linrec_without_dasco.csv', low_memory=False)
        # train_csv = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
        # train_csv = pd.read_csv('linrec_without_dasco.csv', low_memory=False, usecols=['A000051'])

    dataset_csv = test_csv if TESTSET else train_csv
    print(f'number of sequences in dataset: {len(dataset_csv.columns)}')


    def sequence_to_parts(seq, length=15):
        """Separate a sequence into parts/chunks of given length."""
        # seq = [i for i in range(100)]
        split = [seq[i:i+length] for i in range(0, len(seq), length) if len(seq[i:i+length]) == length]
        return split

    # print(sequence_to_parts([1,2,3,4,5,6, 7], 9))
    # 1/0

    def column_to_prompts(col_id, testset=TESTSET):
        """Convert a column of a dataframe to multiple prompts."""
        seq_matrix, coeffs_matrix, truth = unpack_seq(col_id, dataset_csv)
        seq = list(seq_matrix)
        truth = ['a_n = '] + [f'{str(coeff)}*a_{{n-{n + 1}}} + ' for n, coeff in enumerate(coeffs_matrix)]
        equation = ''.join(truth)[:-3]
        if testset:
            seq_parts15, seq_parts25 = [seq[:15]], [seq[:25]]
        else:
            seq_parts15 = sequence_to_parts(seq, 15)
            seq_parts25 = sequence_to_parts(seq, 25)
        file_content15 = ""
        file_content25 = ""
        backfile_content15 = ""
        backfile_content25 = ""
        for seq_part in seq_parts15:
            file_content15 += f"[INST] Could you give me a linear equation for the following number sequence: {','.join([str(i) for i in seq_part])} [/INST] [RESP] Certainly, the equation is the following: {equation} [/RESP]\n"
            backfile_content15 += f"[INST] Find me an example number sequence that fits the following equation: {equation} [/INST] [RESP] Off course, here is one example: {','.join([str(i) for i in seq_part])} [/RESP]\n"
        for seq_part in seq_parts25:
            file_content25 += f"[INST] Could you give me a linear equation for the following number sequence: {','.join([str(i) for i in seq_part])} [/INST] [RESP] Certainly, the equation is the following: {equation} [/RESP]\n"
            backfile_content25 += f"[INST] Find me an example number sequence that fits the following equation: {equation} [/INST] [RESP] Off course, here is one example: {','.join([str(i) for i in seq_part])} [/RESP]\n"
        return file_content15, file_content25, backfile_content15, backfile_content25

    example = "[INST] Could you give me a linear equation for the following number sequence: 0,0,1,2,4,7,12, ... [/INST] [RESP] Certainly, the equation is the following: a_n = 1*a_{n-1} + 1*a_{n-2} [/RESP]"


    # file1, file2, b1, b2 = column_to_prompts('A000004')
    file1, file2, b1, b2 = column_to_prompts('A000042')
    print(file2)
    print('this was 42')
    file1, file2, b1, b2 = column_to_prompts('A003555')
    print(file2)
    print('this was 3555')
    # 1/0

    def do_csv():
        """Convert a csv file to multiple prompts."""
        file15, file25 = "", ""
        backfile15, backfile25 = "", ""
        for n, i in enumerate(dataset_csv.columns[:]):
            print(n, i)
            f15, f25, bfile15, bfile25 = column_to_prompts(i)
            file15 += f15
            file25 += f25
            backfile15 += bfile15
            backfile25 += bfile25
        return file15, file25, backfile15, backfile25

    # WRITE_FILES = True
    WRITE_FILES = False
    # RUN = True
    RUN = False

    ### Write to files: ###
    if RUN:
        file15, file25, backfile15, backfile25 = do_csv()  # Actually generate the prompts.
        print(file15)
        print(file25)
        print(backfile15)
        print(backfile25)
        if WRITE_FILES:
            with open('test_15.txt', 'w') as f:
                f.write(file15)
            with open('test_25.txt', 'w') as f:
                f.write(file25)
            with open('test_inverse_15.txt', 'w') as f:
                f.write(backfile15)
            with open('test_inverse_25.txt', 'w') as f:
                f.write(backfile25)
            print('done writing files')

    print('done!')
    return

# first round of experiments:
# linearLLM()


def prompt_test(seq_in, seq_pred, seq_id, eq):
    """Generate a prompt from sequence terms."""
    printout = ( f'[INST] Could you give me a recursive equation in a form of a Python code for the following number '
                 f'sequence: {str(seq_in)[1:-1].replace(" ", "")} [/INST]'
                 f'[RESP] The correct answer is: Certainly, Python code is the following: lambda a_n: {eq} and '
                 f'the next sequence terms are: {str(seq_pred)[1:-1].replace(" ", "")} '
                 f'while the OEIS ID is: {seq_id} [/RESP]\n')
    return printout

# print(prompt_test([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], 'A000001', 'a_n = a_{n-1} + a_{n-2}'))
# 1/0


def load_seq(seq_id, csv: pd.DataFrame, is_linrec=False):
    """Load a sequence from linrec/core csv file."""
    if is_linrec:
        seq_matrix, _coeffs_matrix, truth = unpack_seq(seq_id, csv)
        truth = truth.replace('\n', '')
        return list(seq_matrix), truth
    else:
        header = 0
        seq =  unnan(list(csv[seq_id][header:]))
        seq = list(seq)
        # print(seq)
        return seq, 'Unsaved equation'


def split_biggies(seq):
    """Select first low profile terms of a sequence.

    I.e., cut off all terms from the first with value > 10^10. 
    In worst case scenario we take at least 5 input sequence terms, regardless of the absolute value.
    """

    bools = [True if abs(i) <= 10**10 else False for i in seq]
    if False in bools:
        five_or_more = max(5, bools.index(False)) 
        return seq[:five_or_more]
    else:
        return seq

# print(filter_biggies([1, 21, 3, 4, 5, 6, 7, 8, 9, 10**10, 10**11]))
# 1/0

def csv_to_testset(filename, n_input=25, verbosity=0):
    """Convert a csv file to a test set in a form of a text of prompts."""

    file_content = ""
    csv = pd.read_csv(filename, low_memory=False)
    is_linrec = False
    if filename == 'linear_database_newbl.csv':
        is_linrec = True
    elif filename == 'cores_test.csv':
        is_linrec = False
    scale = 30000
    scale = 3
    for n, col_id in enumerate(csv.columns[:scale]):
        # print(n, col_id)
        seq, eq = load_seq(col_id, csv, is_linrec=is_linrec)
        seq = filter_biggies(seq[:n_input])
        row = prompt_test(seq)
        file_content += row + '\n'
        if verbosity > 0 and n % verbosity == 0:
            print(f'{n=}, {col_id=}, {seq=}')
            print(row)
    return file_content


# def do_linrec_n_input25():
def write_prompts(output_file, input_csv_filename='linear_database_newbl.csv', n_input=25, for_real=False, verbosity=0):
    """Create test_linrec25.txt file."""
    content = csv_to_testset(input_csv_filename, n_input=n_input, verbosity=verbosity)
    if for_real:
        with open(output_file, 'w') as f:
            f.write(content)
    else:
        print(content)
    return


if __name__ == '__main__':

    # First round of experiments: linear LLM.
    # linearLLM()

    # Second round: linrec and cores to prompts.
    print("\nInside main:")
    # linrec n_input=25:
    linrec_csv = 'linear_database_newbl.csv'
    # cores_csv = 'cores_test.csv'
    write_prompts('test_linrec25o.txt', input_csv_filename=linrec_csv, n_input=25, verbosity=1)
    # write_prompts('test_linrec25o.txt', input_csv_filename=linrec_csv, n_input=25, for_real=True, verbosity=100)
    # write_prompts('test_linrec15o.txt', input_csv_filename=linrec_csv, n_input=15, for_real=True, verbosity=500)
    # write_prompts('test_cores25o.txt', input_csv_filename=cores_csv, n_input=25, for_real=True, verbosity=100)
    # write_prompts('test_cores15o.txt', input_csv_filename=cores_csv, n_input=15, for_real=True, verbosity=100)


    pass
