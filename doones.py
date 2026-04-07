"""Run exact_ed on specific sequence with slurm arrays.
"""

import os
import sys
import time

# import numpy as np  # not really since diophantine
import sympy as sp
import pandas as pd
import argparse

# from ProGED_oeis.examples.oeis.proles_new import n_of_terms_ed
# import random  # for performing diofant grid


# needs (listed so far) doones,: exact_ed, diophantine_solver, linear_database_full.csv, buglist.py, oei.sh, runoei.sh, blacklist, unsuccessful.py, task2job

# if os.getcwd()[-11:] == 'ProGED_oeis':
#     from ProGED.examples.oeis.scraping.downloading.download import bfile2list
from exact_ed import exact_ed, increasing_eed, timer, check_eq_man, check_truth, check_eq_dasco, unnan, unpack_seq, solution_vs_truth, solution2str



import warnings


warnings.simplefilter("ignore")
# # warnings.filterwarnings("ignore", category=UserWarning, message='UserWarning: Sparsity parameter is too big (0.9) and eliminated all coefficients')
# # warnings.filterwarnings("ignore", message='UserWarning: Sparsity parameter is too big (0.9) and eliminated all coefficients')
# warnings.filterwarnings("ignore")

# from task2job import task2job
# else:
#     from exact_ed import exact_ed, timer

EXECUTE_REAL = False
EXECUTE_REAL = True


OEISformer = True
OEISformer = False
if OEISformer:
    from loadtrans import dict_csv, dasco_dict, csv_input
    N_INPUT = 15
    N_INPUT = 25
    print(f'OEISformer: True, n_input: {N_INPUT}, special input database used.')

ORE_ALGEBRA = False  # default settings
ORE_ALGEBRA = True  # testing guessing from gfun

METHOD = 'Diofantos'
METHOD = 'SINDy'
# METHOD = 'Mavi'
# METHOD = 'MB'
SINDy = True if METHOD in ('SINDy', 'Mavi') else False
# SINDy = False
SINDy_default = True
if SINDy:
    # from sindy_oeis import sindy, preprocess, heuristic, sindy_grid, one_results
    from sindy_oeis import preprocess

if METHOD == 'SINDy':
    from sindy_oeis import sindy, preprocess, heuristic, sindy_grid, one_results

if METHOD == 'Mavi':
    raise ValueError('Mavi not researching ATM!')
    sys.path.append('../monomial-agnostic-vanishing-ideal')
    from mavi.vanishing_ideal import VanishingIdeal
    # from mavi_oeis import one_results
    # from mavi_oeis import domavi

if METHOD == 'MB':
    MAX_BITSIZE = 30
    MAX_BITSIZE = 50
    # sys.path.append('../monomial-agnostic-vanishing-ideal')
    # from mb_wrap import mb
    from mb_oeis import increasing_mb


INCREASING_EED = True
# print("IDEA: max ORDER for GRAMMAR = floor(DATASET ROWS (LEN(SEQ)))/2)-1")

##############################
# Quick usage is with flags:
#  --seq_only=A000045 --sample_size=3 # (Fibonacci with 3 models fitted)
# search for flags with: flags_dict
###############

# False positives (linear equation does not hold (manual check fails), or empty or noncomplete lists of coeffs (e.k. >200 coefficients))
from blacklist import no_truth, false_truth
# mini_false_truth += ['A053833', 'A055649', 'A044941',]  # some of false_truth manually checked
# mini_no_truth ['A025858', 'A025858', 'A246175', 'A025924', 'A356621', ]  # some of no_true manually checked
blacklist = no_truth + false_truth
# blacklist = no_truth
# A026471

# remnants = ['00191', '00193', '00194', '00200', '00209', '00210', '00946', '01218', '01691', '01692', '01693', '01713', '01714', '01715', '01716', '01717', '01718', '01719', '01720', '01721', '01722', '01723', '01724', '01725', '01726', '01727', '01728', '01729', '01730', '01731', '01733', '01734', '01736', '01743', '01744', '01745', '01747', '01748', '01749', '01750', '01752', '01754', '01756', '01758', '01760', '01761', '01762', '01763', '01764', '01765', '01766', '01767', '01768', '01769', '02176', '02179', '02180', '02184', '02187', '02192', ]
remnants = [191, 193, 194, 200, 209, 210, ]
REMNANTS = True
REMNANTS = False

# successful_only = True
# if successful_only:
#     from successful import successful_list


# MODE = 'black_check'  # try only unsuccessful
MODE = 'doone'
# MODE = 'diofant grid'
if MODE == 'black_check':
    blacklist = no_truth

N_OF_TERMS_LOAD = 100000
N_OF_TERMS_LOAD = 20
N_OF_TERMS_LOAD = 200

N_MORE_TERMS = 10  # original
# N_MORE_TERMS = 30
# N_MORE_TERMS = 40
# N_MORE_TERMS = 60
# N_MORE_TERMS = 70

VERBOSITY = 2  # dev scena
# VERBOSITY = 1  # run scenario
# VERBOSITY = 3  # dev scenario

DEBUG = True
DEBUG = False

# BUGLIST ignores blacklisting (runs also blacklisted) !!!!!
# BUGLIST = True
BUGLIST = False
BUGLIST_BLACKLISTING = True
# BUGLIST ignores blacklisted sequences !!!!!

CORELIST = True  # have to scrape core sequences!  # also for OEISformer
CORELIST = False
if BUGLIST:
    from buglist import buglist
REAL_WORLD_BENCH = True

GROUND_TRUTH = True
GROUND_TRUTH = False

# if not DEBUG and BUGLIST:
#     print("\nWarning!!!!! buglist is used outside debug mode!!")
#     print("Warning!!!!! buglist is used outside debug mode!!")
#     print("Warning!!!!! buglist is used outside debug mode!!\n")

# only libraries allowed:
# LIBRARY = 'lin'
library = 'n' if CORELIST else 'non'
d_max = 3 if CORELIST else 1

# # mavi testing:
# d_max = 1
# d_max = 2
# # library = 'non'


# LIBRARY = 'nlin'
# LIBRARY = 'quad'
# # LIBRARY = 'nquad'
# LIBRARY = 'cub'
# LIBRARY = 'ncub'
# LIBRARIES = ['n', 'lin', 'nlin', 'quad', 'nquad', 'cub', 'ncub']
# LIBRARIES = ['lin', 'nlin', 'quad', 'nquad', 'cub', 'ncub']
# LIBRARIES = ['lin', 'nlin']
# LIBRARIES = ['nlin']
# LIBRARIES = ['ncub']
# LIBRARIES = ['nquad']
# LIBRARIES = LIBRARIES[plus:plus+1]
# LIBRARIES = ['lin', 'nlin', 'quad', 'nquad', 'ncub']
# LIBRARIES = LIBRARY
# library = LIBRARIES[0]

# mavi settings:
ROUND_OFF = 1e-05
ROUND_OFF = 1e-04
DIVISOR = 1.0

if not CORELIST:
    MAX_ORDER = 20  # We care only for recursive equations with max 20 terms or order.
    # MAX_ORDER = 12
    GROUND_TRUTH = True
    START_ORDER = 1
else:
    MAX_ORDER = 1
    # MAX_ORDER = 2
    # MAX_ORDER = 4
    # # MAX_ORDER = 5
    MAX_ORDER = 10
    MAX_ORDER = 20
    # MAX_ORDER = 5
    # MAX_ORDER = 2  # mavi
    GROUND_TRUTH = False
    START_ORDER = 0
# START_ORDER = 3
# if DEBUG:
#     MAX_ORDER = 5  # We care only for recursive equations with max 20 terms or order.

# mavi:
# MAX_ORDER = 1  # mavi
if OEISformer and METHOD == 'MB':
    MAX_ORDER = 20

# THRESHOLD = 0.2  # For sindy - masking threshold.
THRESHOLD = 0.1  # For sindy - masking threshold.
# THRESHOLD = 0.08  # For sindy - masking threshold.
# THRESHOLD = 0.05  # For sindy - masking threshold.
# THRESHOLD = 0.0001  # For sindy - masking threshold.
# THRESHOLD = 0.00000001  # For sindy - masking threshold.

# SEQ_LEN_SINDY = 30
# SEQ_LEN_SINDY = 70
# SEQ_LEN_SINDY = 4

# N_OF_TERMS_ED = 200 # before mavi
N_OF_TERMS_ED = 200  # MB
# N_OF_TERMS_ED = 20  # mavi
# N_OF_TERMS_ED = 7  # mavi
# N_OF_TERMS_ED = 14  # mavi
# N_OF_TERMS_ED = 11  # mavi good simple for a142
# N_OF_TERMS_ED = 9  # mavi good simple
# N_OF_TERMS_ED = 3  # mavi
# N_OF_TERMS_ED = 5  # mavi
TASK_ID = 0
TASK_ID = 8
TASK_ID = 10
TASK_ID = 14  # fibo at cores
# # TASK_ID = 17
# TASK_ID = 32
# TASK_ID = 111
# TASK_ID = 112
# TASK_ID = 187
# TASK_ID = 5365  # A026471
# TASK_ID = 191  # A026471
# TASK_ID = 2000
# unsucc [11221, 27122, 27123]
# TASK_ID = 11221
# TASK_ID = 26
# TASK_ID = 2
# TASK_ID = 7
# TASK_ID = 9  # fibo linrec
TASK_ID = 959
TASK_ID = 158
TASK_ID = 369
TASK_ID = 463
TASK_ID = 479
TASK_ID = 1151
TASK_ID = 23808
# first 200  order 5 non_manuals: ['00158', '00369', '00463', '00479'] 4
TASK_ID = 26  # fibo in TM-OEIS
# TASK_ID = 25
# TASK_ID = 4
# TASK_ID = 5
# TASK_ID = 22
# TASK_ID = 138  # FloatRoot instead of FloorRoot
TASK_ID = 601  # dividing too big numbers in predict_with_emplicit
TASK_ID = 145
# TASK_ID = 255
TASK_ID = 26
# TASK_ID = 51
# TASK_ID = 1367
TASK_ID = 11100
TASK_ID = 14
TASK_ID = 9
TASK_ID = 10
TASK_ID = 112
TASK_ID = 116
TASK_ID = 111
TASK_ID = 100
TASK_ID = 97
TASK_ID = 9


JOB_ID = "000000"
# SEQ_ID = (True, 'A153593')
# SEQ_ID = (True, 'A053833')
# SEQ_ID = (True, 'A055649')
# SEQ_ID = (True, 'A044941')
# SEQ_ID = (True, 'A153593')
# SEQ_ID = (True, 'A026471')
# SEQ_ID = (True, 'A001306')
# SEQ_ID = (True, 'A001343')
# SEQ_ID = (True, 'A008685')
# SEQ_ID = (True, 'A013833')
SEQ_ID = (True, 'A000045')
# SEQ_ID = (False, 'A000045')
# SEQ_ID = (True, 'A000043')  # core
# SEQ_ID = (True, 'A000187')
# ['A056457', 'A212593', 'A212594']

# SEQ_ID = (True, 'A056457')
# SEQ_ID = (True, 'A029378')
# SEQ_ID = (True, 'A000042')
# SEQ_ID = (True, 'A000004')
# SEQ_ID = (True, 'A000008')
# SEQ_ID = (True, 'A000027')
# SEQ_ID = (True, 'A000034')
# SEQ_ID = (True, 'A000012')
# SEQ_ID = (True, 'A000392')
SEQ_ID = (True, 'A000045')
SEQ_ID = (False, 'A000045')
# non_manuals =  ['23167_A169198.txt', '23917_A170320.txt', '03322_A016835.txt', '24141_A170544.txt', '24240_A170643.txt', '24001_A170404.txt', '24014_A170417.txt', '23207_A169238.txt', '22912_A168943.txt', '03330_A016844.txt', '23872_A170275.txt', '22983_A169014.txt', '24006_A170409.txt', '24211_A170614.txt', '15737_A105944.txt', '24053_A170456.txt', '23488_A169519.txt', '23306_A169337.txt', '22856_A168887.txt', '23049_A169080.txt', '23980_A170383.txt', '23742_A170145.txt', '23109_A169140.txt', '06659_A035798.txt', '23860_A170263.txt', '23800_A170203.txt', '23649_A170052.txt', '23219_A169250.txt', '23682_A170085.txt', '06706_A035871.txt', '23720_A170123.txt', '31181_A279282.txt', '23382_A169413.txt', '24034_A170437.txt', '24192_A170595.txt']
# SEQ_ID = (True, 'A169198')
# SEQ_ID = (True, 'A024347')
# SEQ_ID = (True, 'A010034')
# # SEQ_ID = (True, 'A000518')  # not in cores?
# cores:
# SEQ_ID = (True, 'A055512')
# SEQ_ID = (False, 'A000032')
# SEQ_ID = (True, 'A000032')
SEQ_ID = (True, 'A000045')
SEQ_ID = (True, 'A000085')
# SEQ_ID = (True, 'A000578')
# SEQ_ID = (True, 'A002620')
# SEQ_ID = (True, 'A000032')
# SEQ_ID = (False, 'A000290')
SEQ_ID = (True, 'A000290')
# SEQ_ID = (True, 'A000124')  #cores

# not cores or linrec:
SEQ_ID = (True, 'A025938')
# # debug and sindy and buglist
SEQ_ID = (True, 'A074515')
SEQ_ID = (True, 'A074517')
SEQ_ID = (True, 'A091881')
# SEQ_ID = (True, 'A000009')  # cores
# first 100 non_manuals: ['00003_A000009.txt', '00012_A000041.txt', '00013_A000043.txt', '00021_A000085.txt', '00023_A000105.txt', '00028_A000123.txt', '00029_A000124.txt', '00039_A000217.txt', '00046_A000290.txt', '00047_A000292.txt', '00051_A000326.txt', '00052_A000330.txt', '00056_A000578.txt', '00058_A000593.txt', '00065_A000793.txt', '00073_A001034.txt', '00078_A001065.txt', '00082_A001157.txt', '00107_A002322.txt', '00108_A002378.txt', '00114_A002620.txt', '00121_A004011.txt', '00135_A006530.txt', '00136_A006882.txt', '00149_A025487.txt']
SEQ_ID = (True, 'A003082')  # linrec

# SEQ_ID = (True, 'A000041') # in cores

# not in cores:
# SEQ_ID = (True, 'A168838')
# SEQ_ID = (True, 'A000044')  # mb fails, order 13
# SEQ_ID = (True, 'A000073')
# SEQ_ID = (True, 'A000078')
# SEQ_ID = (True, 'A000100')

SEQ_ID = (True, 'A005588')  # cores
# SEQ_ID = (True, 'A000004')  # not in cores
SEQ_ID = (True, 'A000045')

# # cores: 2*10 + 10 = 30 terms  # cores with low number of terms: a58, a1699, a2658?, a6894
# # no problems for them with this setting
# # SEQ_ID = (True, 'A002658')
# # SEQ_ID = (True, 'A000058')
# # SEQ_ID = (True, 'A001699')
# # SEQ_ID = (True, 'A006894')
# # SEQ_ID = (True, 'A000396')
# SEQ_ID = (True, 'A190528')
# SEQ_ID = (True, 'A204419')
# SEQ_ID = (True, 'A135982')
# SEQ_ID = (True, 'A275639')
# SEQ_ID = (True, 'A304583')
# SEQ_ID = (True, 'A017847')  # linrec order 7 reconstructed!
# # SEQ_ID = (True, 'A051793')  # -2*-1 ali +-1 za a(n) -2*a(n-5) +a(n-1)
# SEQ_ID = (True, 'A014025')  # linrec order 8 one nonzero term NOT reconstructed!
# SEQ_ID = (True, 'A104237')
# SEQ_ID = (True, 'A000962')
#     # (103, 'A000962'), (104, 'A000963'), (105, 'A000964'), (152, 'A001110'), (201, 'A001520'), (202, 'A001526'), (203, 'A001533'), (204, 'A001534'), (205, 'A001535'), (206, 'A001536')]
# SEQ_ID = (True, 'A000959')
# SEQ_ID = (True, 'A000129')  # linrec order 8 one nonzero term NOT reconstructed!
# SEQ_ID = (False, 'A000158')

# if DEBUG:
#     SEQ_ID = (True, 'A000045')

# TARGETED_CORES = ['A02', 'a32', 'a35', 'a45', 'a58', 'a79', 'a85', 'a108', 'a124', # a129, a142, a166, a169, a204, a217, a225, a244, a262, a290, a292, a302, a312, a326, a330, a578, a583, a984, a1003, a1006, a1045, a1057, a1147, a1333, a1405, a1519, a1700, a1764, a1906, a2275, a2378, a2426, a2530, a2531, a2620, a2658, a4526, a5408, a5811, a5843, a6318, a6882, a6894, ]


# first 100 non_manuals: ['04132_A025938.txt', '09906_A074515.txt', '09908_A074517.txt', '11571_A091881.txt', '11572_A091883.txt', '11827_A094944.txt', '11939_A097068.txt', '13516_A114480.txt', '13922_A120465.txt', '13939_A120689.txt']

# DIOFANT_GRID = False

# ('00193', 'A001310')  # ('00194', 'A001312'), ('00200', 'A001343'), ('00209', 'A001364'), ('00210', 'A001365'), ('00946', 'A007273'), ('01218', 'A008685'), ('01691', 'A011616'), ('01692', 'A011617')]
# [('00184', 'A001299'), ('00185', 'A001300'), ('00186', 'A001301'), ('00187', 'A001302'), ('00195', 'A001313'), ('00196', 'A001314'), ('00198', 'A001319'), ('00222', 'A001492'), ('00347', 'A002015'), ('00769', 'A005813')] 1921

# first 35 ed_fails: ['06210_A029378.txt', '06742_A036137.txt', '05957_A029125.txt', '06205_A029373.txt', '09668_A042836.txt', '09003_A042094.txt', '32687_A302763.txt', '06193_A029361.txt', '06183_A029351.txt', '00466_A003404.txt', '08819_A041879.txt', '06656_A035744.txt', '12087_A069956.txt', '09388_A042531.txt', '09333_A042471.txt', '23374_A169405.txt', '06223_A029391.txt', '00615_A004460.txt', '09022_A042113.txt', '08979_A042069.txt', '06082_A029250.txt', '07630_A040529.txt', '08772_A041825.txt', '09559_A042719.txt', '06650_A035738.txt', '23102_A169133.txt', '06053_A029221.txt', '09606_A042770.txt', '08419_A041396.txt', '23780_A170183.txt', '06208_A029376.txt', '05243_A025894.txt', '02116_A014040.txt', '18404_A133854.txt', '05987_A029155.txt']

# EXPERIMENT_ID
timestamp = time.strftime("%Hh%Mm%Ss-%dd%m-%Y", time.localtime())
EXPERIMENT_ID = timestamp

parser = argparse.ArgumentParser()
parser.add_argument("--job_id", type=str, default=JOB_ID)
parser.add_argument("--task_id", type=int, default=TASK_ID)
parser.add_argument("--lib", type=str, default=library)
parser.add_argument("-ss", type=int, default=-1)
parser.add_argument("-to", type=int, default=-1)
parser.add_argument("--order", type=int, default=MAX_ORDER)
parser.add_argument("--deg", type=int, default=d_max)
parser.add_argument("--threshold", type=int, default=THRESHOLD)
# parser.add_argument("--seq_len", type=int, default=SEQ_LEN_SINDY)
parser.add_argument("--paral", type=int, default=2)
parser.add_argument("--verb", type=int, default=VERBOSITY)
parser.add_argument("--n_of_terms", type=int, default=N_OF_TERMS_ED)
parser.add_argument("--n_more_terms", type=int, default=N_MORE_TERMS)
parser.add_argument("--exper_id", type=str, default=EXPERIMENT_ID)
parser.add_argument("--divisor", type=float, default=DIVISOR)
parser.add_argument("--roundoff", type=float, default=ROUND_OFF)
# parser.add_argument("--diogrid", type=str, default=DIOFANT_GRID)
args = parser.parse_args()

n_more_terms = args.n_more_terms
job_id = args.job_id
task_id = args.task_id
library = args.lib
# libraries = args.lib.split(',') if args.lib is not None else LIBRARIES
# if library is None:
#     library = libraries

# print('libraries', libraries)
# 1/0

# print('task_id', task_id)
# task_id = remnants[task_id]
# diofant_grid = True if args.diogrid == "True" else False

max_order = args.order
d_max = args.deg
threshold = args.threshold
# seq_len = args.seq_len
PARALLEL = args.paral
VERBOSITY = args.verb if not DEBUG else 2
experiment_id = args.exper_id

n_of_terms_ed = args.n_of_terms

# N_OF_TERMS_ED = 2*max_order  # Use only first n_of_terms_ed of the given sequence.
# N_OF_TERMS_ED = None

divisor = args.divisor
round_off = args.roundoff

flags_dict = {argument.split("=")[0]: argument.split("=")[1]
              for argument in sys.argv[1:] if len(argument.split("=")) > 1}
# n_of_terms_ed = 50
# n_of_terms_ed = int(flags_dict.get("--n_of_terms", n_of_terms_ed))


# from proged times:
has_titles = 1
#
# # for linear database:
# # mabye slow:
now = time.perf_counter()
# # a bit faster maybe:
# csv_filename = 'linear_database_full.csv'
# csv_filename = 'linear_database_clean2.csv'
csv_filename = 'linear_database_newbl.csv'

if CORELIST:
    blacklist = []
    # from core_nice_nomore import cores
    # csv_filename = 'cores.csv'
    csv_filename = 'cores_test.csv'
    # Explained cores, how I got them: back at the time they were scraped.
    # specs: only first 100 terms, 150 sequences
    # i think I will redowmnload them, because I have a better way to do it now.

# print(os.getcwd())
if os.getcwd()[-11:] == 'ProGED_oeis':
    # csv_filename = 'ProGED_oeis/examples/oeis/' + csv_filename
    # print(os.getcwd())
    pass
# except ValueError as error:
#     print(error.__repr__()[:1000], type(error))

fail = False
fail = (BUGLIST and task_id >= len(buglist)) or fail
# fail = (CORELIST and task_id >= len(cores)) or fail

# 1/0

csv = pd.read_csv(csv_filename, low_memory=False, nrows=0)
if OEISformer:
    CORELIST = False
    dic, csv_zerows = dict_csv()
    csv = csv_zerows
n_of_seqs = len(list(csv.columns))
# print(csv.columns[:100])
print(n_of_seqs)
# 1/0

# if diofant_grid:
#     task_id = random.randint(0, n_of_seqs)

fail = (not BUGLIST and task_id >= n_of_seqs) or fail
if not fail:
    if BUGLIST_BLACKLISTING:
        fail = list(csv.columns)[task_id] in blacklist or fail
    else:
        fail = (not BUGLIST and list(csv.columns)[task_id] in blacklist) or fail
    seq_id = list(csv.columns)[task_id] if not SEQ_ID[0] or not DEBUG else SEQ_ID[1]
    #above line can in DEBUG mode cause task_id to differ from corresponding seq_id
    # print('seq_id', seq_id)
    # print('seq_id', BUGLIST)
    if BUGLIST:
        if isinstance(buglist[task_id], str):
            seq_id = buglist[task_id]
        else:
            seq_id = buglist[task_id][1]
            task_id = int(buglist[task_id][0])
    # if CORELIST:
    #     seq_id = cores[task_id]
    # if DEBUG:
    print(TASK_ID, task_id, seq_id, " ... TASK ID, task_id, seq_id")

    # b. set output folder and check is file for this task already exists
    sep = os.path.sep
    out_dir_base = f"results{sep}"
    # out_dir = out_dir_base + f"{experiment_id}{sep}{job_id}{sep}"
    out_dir = out_dir_base + f"{experiment_id}{sep}"
    # print('seq_id', seq_id)

    if not DEBUG and not experiment_id == timestamp:
        os.makedirs(out_dir, exist_ok=True)
    out_fname = out_dir + f"{task_id:0>5}_{seq_id}.txt"
    fail = fail or os.path.isfile(out_fname)

if fail:
    print('ED was not performed since task_id surpassed our list or target sequence is on blacklist or '
          'the task was already performed in the past.')
else:
    print()
    settings_memo = (f'\nCORELIST: {CORELIST}, METHOD: {METHOD}, SINDy: {SINDy} (True also in case of MAVI), '
                     f'GROUND_TRUTH: {GROUND_TRUTH}, SINDy_default: {SINDy_default}, DEBUG: {DEBUG}, OEISformer: {OEISformer}')
    settings_memo += f'\nn_of_terms_ed: {n_of_terms_ed}, N_OF_TERMS_ED: {N_OF_TERMS_ED}'
    settings_memo += f'\nLibrary: {library}, max_order {max_order}, max_degree: {d_max}, threshold: {threshold}, '
    if METHOD == 'MB':
        settings_memo += f'\nn_more_terms: {n_more_terms}'
    print(settings_memo)
    # print('CORELIST', CORELIST, 'SINDy', SINDy, 'GROUND_TRUTH', GROUND_TRUTH)
    # print('Library:', library, 'max_order', max_order, 'threshold:', threshold)
    # csv = pd.read_csv(csv_filename, low_memory=False, nrows=0)
    # print(csv.columns[:100])
    if not OEISformer:
        csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:N_OF_TERMS_LOAD]
    else:
        csv = csv_input(seq_id, N_INPUT, dic)
    # nans are checked by every function separately since exact_ed needs also ground truth

    csv.head()
    # now = timer(now, 'loading csv')
    # csv = csv.astype('int64')
    # print("csv", csv)
    # csv = csv.astype('float')
    terms_count, seqs_count = csv.shape


    # Run eq. disco. on all oeis sequences:
    start = time.perf_counter()
    now = start


    # with open('relevant_seqs.txt', 'r') as file:  # Use.
    #     # file.read('Hi there!')
    #     text = file.read()
    #
    # saved_seqs = re.findall(r'A\d{6}', text)

    # print('seq_id bef print_res', seq_id)

    def print_results(results, verbosity=2):

        if verbosity>=1:
            print("\n\n\n -->> The results are the following:  <<-- \n\n\n")
        if verbosity>=2:
            for (seq_id, eq, truth, x, is_reconst, is_check) in results:
                # if eq == 'EXACT_ED ERROR':
                #
                # else:
                print(seq_id, ': ', eq)
                print('truth:    ', truth)
                print('\"Check against website ground truth\":    ', is_reconst)
                # print('\"Manual check if equation is correct\":    ', is_check[0])
                print('\"Manual check if equation is correct\":    ', is_check)
                # if not is_check[0]:
                #     print('\" recorst vs truth\":    ', is_check[1].row_join(sp.zeros(is_check[1].rows, 1)).row_join(is_check[2]), '\n')
                print()

        if verbosity>=1:
            print(f"\n\n\n -->> The summary of the results untill now ({len(results)} sequences) are the following:  <<-- \n\n\n")

            false_positives = [seq_id for seq_id, eq, truth, x, is_reconst, is_check in results if not is_check]
            non_ground_truth = [seq_id for seq_id, eq, truth, x, is_reconst, is_check in results if not is_reconst]
            no_discovery = [seq_id for seq_id, eq, truth, x, is_reconst, is_check in results if x==[]]
            # ids = [seq_id for seq_id, eq, truth in results if eq == 'EXACT_ED ERROR']


            print('Number of false positives in exact ED:', len(false_positives))
            if verbosity >= 2:
                print('False positives:', false_positives)
            else:
                print('first 20 False positives:', false_positives[:20])
            print('Number of different sequences:', len(non_ground_truth))
            if verbosity >= 2:
                print('Different sequences:', non_ground_truth)
            else:
                print('first 20 Different sequences:', non_ground_truth[:20])
            print('Number of sequence without any equation found:', len(no_discovery))
            if verbosity >= 2:
                print('Sequences without any equation found:', no_discovery)
            else:
                print('first 20 Sequences without any equation found:', no_discovery[:20])

            # print('Number of false positives in exact ED:', len(ids))
            # print('False positives:', ids)

            print("Running equation discovery for all oeis sequences, "
                  "with these settings:\n"
                  f"=>> number of terms in every sequence saved in csv = {terms_count}\n"
                  # f"=>> nof_eqs = {nof_eqs}\n"
                  f"=>> number of all considered sequences = {n_of_seqs}\n"
                  # f"=>> list of considered sequences = {selection}\n"
                  f"=>> max order = {max_order}\n"
                  )
            timer(now=start, text=f"While total time consumed by now")
        return 0

    SUMMARY_FREQUENCY = 20
    SUMMARY_FREQUENCY = 1000  # cluster for real
    # SUMMARY_FREQUENCY = 5
    INCREASING_FREQS = [2**i for i in range(SUMMARY_FREQUENCY) if 2**i <= SUMMARY_FREQUENCY]



    results = []

    # print('seq_id', seq_id)

    def doone(task_id: int, seq_id: str, linear: bool, now=now):
        if VERBOSITY>=2:
            print()
        output_string = "\n"
        max_order_ = max_order
        print('Attempting doone for', seq_id)
        non_linears = []

        eqs_explicit = []
        # try:
        if ORE_ALGEBRA:
            from ore_alg import oraj
            seq, coeffs, truth = unpack_seq(seq_id, csv) if GROUND_TRUTH else (unnan(csv[seq_id]), None, None)
            # seq = unnan(csv[seq_id])
            print(seq)
            # 1/0
            # eq = oraj(seq, True, 1)
            eq = oraj(seq, True, is_berlekamp='fricas')
            print(f'\n\n{eq = }', '\nis Disco:', 'True' if eq else 'False', '\n\n\nExiting after running sage code with zero division:')
            return [eq] + ['' for _ in range(10)]
            # 1/0
        elif SINDy:
            print('Attempting SINDy (or Mavi) for', seq_id)
            # if GROUND_TRUTH:
            # print(csv, seq_id)
            # print(csv[seq_id])
            seq, coeffs, truth = unpack_seq(seq_id, csv) if GROUND_TRUTH else (unnan(csv[seq_id]), None, None)

            # seq = seq[:40, :]
            # library = libraries[0]
            # seqs, pre_fail = preprocess(seq, library=library)
            preseqs = [preprocess(seq, degree)[0] for degree in range(1, d_max+1)]
            # seq_len = len(seq)
            if False:
                if pre_fail:
                    output_string += f'Only huge terms in the sequence!!!\n\n'
                    x = []
            else:

                # lib
                # x, sol_ref, eq = sindy_grid(seq, seq_id, csv, coeffs, max_order_, library='n')
                # init = (x, (sol_ref, ('n', 0) ), eq, coeffs, truth, False if x == [] else True)

                # START_ORDER = 1
                # START_ORDER = 0
                # START_ORDER = 6
                # START_ORDER = 13
                # libraries = [1, 2, 3]  # poly degrees (look increasind_eed)
                # libraries = [1,]  # poly degrees (look increasind_eed)
                # libraries = [3]  # poly degrees (look increasind_eed)

                # print('before')
                if METHOD == 'Mavi':
                    print('Attempting Mavi for', seq_id)
                    # one_results = mavi_one_result
                    # x, (sol_ref, deg_used, order_used), eq, _, _ = mavi_one_result(one_results, seq_id, csv, d_max, max_order_)

                    # library = 'n'  # mavi always uses linear dataset
                    d_max_lib = 1  # create linear dataset
                    d_max_mavi = d_max
                    # d_max_mavi = 2
                    # max_order_ = 2

                    # x = []
                    # x = [sp.Matrix([0])]
                    # sol_ref = []
                    # sol_ref = ['1']
                    # ORDER_USED = 2
                    x, (sol_ref, deg_used, order_used), eq, _, _ = [], ([], d_max_mavi, max_order_), '', '', ''

                    eqs = domavi(seq_id, csv, VERBOSITY, d_max_lib=d_max_lib,
                              d_max_mavi=d_max_mavi, max_order=max_order_, ground_truth=GROUND_TRUTH,
                              n_of_terms=n_of_terms_ed, library=library,
                              start_order=START_ORDER, init = None, sindy_hidden=preseqs,
                              print_epsilon=round_off, divisor=divisor)
                    eq = eqs[0] if len(eqs) > 0 else 'no equation found :-(';

                    printout = '\nPrinting all equations mavi has found:\n'
                    for n, e in enumerate(eqs):
                        printout += f'poly #{n}\n'
                        printout += f'{e}\n\n'

                else:
                    printout = ''
                    print('Attempting SINDy for', seq_id)
                    x, (sol_ref, deg_used, order_used), eq, _, _ = increasing_eed(one_results, seq_id, csv, VERBOSITY,
                                                          d_max, max_order_, ground_truth=GROUND_TRUTH,
                                                          n_of_terms=N_OF_TERMS_ED, library=library,
                                                          start_order=START_ORDER, init = None, sindy_hidden=preseqs)

                output_string += f'Preprocessing sees only first {len(seq)} terms.\n'

                output_string += f'Sindy threshold: {threshold}\n'
                # output_string += f'Default setting for how many terms should sindy see: {seq_len}\n'
                # max_order_ = min(heuristic(len(seq)), max_order_)
                output_string += f'Sindy will use max_order: {max_order_}\n'
                # x = sindy(list(seq), max_order_, seq_len=seq_len, threshold=threshold)
                # LIBRARY!!!
                # x, printout, x_avg = sindy_grid(seq, seq_id, csv, coeffs, max_order, seq_len, library=library)
                # xlib = library
                print('x', x)
                print('eq', eq)

                # print('x_avg', x_avg)
                # print(check_eq_man(x, seq_id, csv, n_of_terms=10 ** 5, library=library))
                # print(check_eq_man(x_avg, seq_id, csv, n_of_terms=10 ** 5, library=library))
                # 1/0
                output_string += printout
                # x = sp.Matrix([0, 0, 0, 0])

                # eq_avg = solution2str(x_avg, library)
                # # is_reconst_avg = solution_vs_truth(x, coeffs)
                # # is_check_avg = check_eq_man(x, seq_id, csv, n_of_terms=10 ** 5)[0]
                # is_reconst_avg = solution_vs_truth(x_avg, coeffs)
                # # is_check_avg = check_eq_man(x_avg, seq_id, csv, n_of_terms=10 ** 5)[0]
                # is_check_avg = check_eq_man(x_avg, seq_id, csv, n_of_terms=10 ** 5, library=library)[0]
                # output_string += f"\n\navg sindy: \n{eq_avg}\n"
                # output_string += f'{is_reconst_avg}  -  checked avg against website ground truth.     \n'
                # output_string += f'{is_check_avg}  -  \"manual\" check avg if equation is correct.    \n'
            # eq = solution2str(x, sol_ref)
            # xlib = f'{xlib} with and max_order:{order}'

            # grid = sindy_grid(seq, seq_id, csv, coeffs, max_order=5, seq_len=30)
            # for max_order_item in grid:
            #     print(max_order_item[0:])

        elif METHOD == 'MB':
            print('Attempting MB for', seq_id)
            print(f'with only 2*order + {n_more_terms} terms, ')
            print(f'args:', seq_id, max_order_, n_more_terms, EXECUTE_REAL, library, n_of_terms_ed,
                   '\n  MB arg: MAX_BITSIZE:', MAX_BITSIZE)
            # 1/0
            # first_generator, sol_ref, ideal_ = increasing_mb
            # VERBOSITY = 0

            # OEISformer = True  # 3.2.2025
            seq, coeffs, truth = unpack_seq(seq_id, csv) if GROUND_TRUTH else (unnan(csv[seq_id]), None, None)
            non_linears, eq, x, orders_used, eqs_explicit = increasing_mb(seq_id, csv, max_order_, n_more_terms, execute=EXECUTE_REAL,
                                                            library=library, n_of_terms=n_of_terms_ed,
                                                            ground_truth=GROUND_TRUTH, verbosity=0, max_bitsize=MAX_BITSIZE,
                                                            explicit=OEISformer)
            # OEISformer = False  # 3.2.2025
            deg_used, order_used = 'unknown_mb', 'unknown_mb'
            output_string += f'orders_used: {orders_used}\n'
            # print(orders_used)
            # print('non_linears', non_linears)
            # for expr in non_linears:
            #     print(expr)
            order_used = None if not orders_used else orders_used[0]
            # eq, x = first_generator, [], 'unknown_mb'
            # eq, x, sol_ref, truth = mbprintout, [], 'unknown_mb', 'unknown_mb'
            sol_ref = "unknown_mb"
            # eq = eq if eq != 'MB not reconst' else non_linears
            x = sp.Matrix([0]+x)

        else:
            # print('Going for exact ed')
            # print(' tle ', max_order_, linear, N_OF_TERMS_ED)
            # START_ORDER = 6
            # START_ORDER = 20

            if INCREASING_EED:
                x, (sol_ref, deg_used, order_used), eq, coeffs, truth = increasing_eed(exact_ed, seq_id, csv, VERBOSITY, d_max,
                                                                       max_order_,
                                                          ground_truth=GROUND_TRUTH,
                                                           # n_of_terms=N_OF_TERMS_ED,
                                                          library=library,
                                                          start_order=START_ORDER,
                                                                        )
                # x, eq, coeffs, truth = exact_ed(seq_id, csv, VERBOSITY, max_order_,
                #                                 n_of_terms=N_OF_TERMS_ED, linear=LINEAR)

        print('eq', eq, 'x', x, 'coeffs', coeffs, 'truth', truth)
        # print('deg_used', deg_used, 'order', order_used)
        is_reconst = solution_vs_truth(x, coeffs) if GROUND_TRUTH else "No ground truth :("
        if METHOD == 'MB':
            # non_linears
            # linears = [x]
            x = [] if x == sp.Matrix([0]) else x
            if not is_reconst and not not x:
                print('is_reconst', is_reconst)
                print('MB: seems like bug: ground truth says no while x is not empty!!!')
            is_check = not not non_linears
        else:
            is_check_verbose = check_eq_man(x, seq_id, csv, header=GROUND_TRUTH, n_of_terms=10**5, solution_ref=sol_ref)
            is_check = is_check_verbose[0]

        if OEISformer:
            acc_1, acc_10 = check_eq_dasco(x, seq_id, solution_ref=sol_ref, n_input=N_INPUT, eq=eq, mb=(METHOD == 'MB'))
            is_reconst = acc_10
            is_check = acc_1
            dasco_result = f'dasco\'s acc_1, acc_10: {acc_1}, {acc_10} is stored in is_reconst and is_check\n'
            output_string += dasco_result
            output_string += f'n_input: {N_INPUT}\n'
            print(dasco_result)
        # print(f"{is_reconst}!, reconstructed as in ground truth.")
        # print(f"{is_check}!, \"manually\" checked if the equation holds for all terms.")
        # print('second check: ', check_truth(seq_id, csv_filename)[0][0])
        # print(seq_id in false_truth, seq_id, len(blacklist))

        # 1/0

        # except Exception as error:
        #     print(type(error), ':', error)
        #     eq, truth, x = 'EXACT_ED ERROR', '\n'*3 + 'EXACT_ED ERROR!!, no output' + '\n'*3
        #     eq, truth, x = exact_ed(seq_id, csv, VERBOSITY)

        # results += [(seq_id, eq, truth, x, is_reconst, is_check_verbose)]

        print()
        if VERBOSITY>=2:
            now = timer(now=now, text=f"Exact ED for {task_id+1}-th sequence of {n_of_seqs} in "
                                      f"experiment set with id {seq_id} for first "
                                      f"{n_of_terms_ed} terms with max order {max_order} "
                                      f"while double checking against first {len(csv[seq_id])-1} terms.")
            timing_print = now[1]
        elif VERBOSITY >= 1:
            # refreshrate = 1100
            refreshrate = 1
            if task_id % refreshrate == 0:
                _, timing_print = timer(now=start, text=f"While total time consumed by now, scale:{task_id+1}/{n_of_seqs}, "
                                      f"seq_id:{seq_id}, order:{max_order}")
        # if task_id % SUMMARY_FREQUENCY == 0:
        #     print_results(results, verbosity=1)
        # elif task_id in INCREASING_FREQS:
        #     print_results(results, verbosity=1)
        # # except Exception as RuntimeError
        return eq, truth, x, deg_used, order_used, is_reconst, is_check, non_linears, eqs_explicit, timing_print, output_string

    # print('outer after', max_order)

    if MODE == 'black_check':
        output_string = ""
        is_check, truth = check_truth(seq_id, csv_filename)
        # print(is_check, truth)
        is_check = is_check[0]

        eq = 'This is blacklist discovery!!! i.e. only checking if ground truth holds.'
        is_reconst = '<empty>'
        _, timing_print = timer(now=start, text=f"While total time consumed by now, scale:{task_id + 1}/{n_of_seqs}, "
                                                f"seq_id:{seq_id}, order:{max_order}")
    else:
        eq, truth, x, deg_used, order_used, is_reconst, is_check, non_linears, eqs_explicit, timing_print, output_string = \
            doone(task_id=task_id, seq_id=seq_id, linear=True)
    # results += [doone(task_id=task_id, seq_id=seq_id)]
    # results += [(seq_id, eq, truth, x, is_reconst, is_check)]

    # output_string = ""
    output_string += timing_print
    # output_string += f'\nCORELIST: {CORELIST}, SINDy: {SINDy}, GROUND_TRUTH: {GROUND_TRUTH}, SINDy_default: {SINDy_default}, DEBUG: {DEBUG}'
    output_string += settings_memo
    output_string += f'\nLibrary: {library}, max_order {max_order}, threshold: {threshold}'
    if METHOD == 'MB':
        output_string += f'\n  MB:  n_more_terms: {n_more_terms}'
        output_string += f' MAX_BITSIZE: {MAX_BITSIZE}'
    output_string += f"\n\nby degree: {deg_used} and order: {order_used}.\neqs_explicit:\n{eqs_explicit}\nnon_linears:\n{non_linears}\n{seq_id}: \n{eq}" if not MODE == 'black_check' else ""
    output_string += f"\ntruth: \n{truth}\n\n"
    output_string += f'{is_reconst}  -  checked against website ground truth.     \n'
    output_string += f'{is_check}  -  \"manual\" check if equation is correct.    \n'

    print(output_string[-106:])

    # timer(now=start)

    if DEBUG:
        out_dir = f"results_debug"
        print(output_string)

    # print(DEBUG, experiment_id)
    if not DEBUG and not experiment_id == timestamp:
        f = open(out_fname, 'w')
        f.write(output_string)
        f.close()
        print(seq_id, f' done and written! (to {out_fname})')
    else:
        # print(output_string)
        print('seems no file was created by this [doone.py] file')
        pass

    print(seq_id, ' done!')




# print(xv, verbose_eq)
# print(verbose_eq[:, 1:][], xv)

def prt(matrix: sp.Matrix):
    print(matrix.__repr__())
    return
# print(verbose_eq)
# prt(verbose_eq)
# print('re', verbose_eq.__repr__())



# # ad-hoc loop-check
# csv = pd.read_csv(csv_filename, low_memory=False, usecols=[i for i in range(SCALE)])[:n_of_terms]
# id = "A000027"
# eq = exact_ed(id, csv)
# print('\n', id)
# print(eq)
# print(check_eq(eq[0], id, csv))
# print(check_eq(eq[0], id, csv, sp.floor(n_of_terms/2 -1)))

# li = [(i,j) for i in range(20) for j in range(20)]
# for i in range(20):
#     size = 5
#     print(li[size*i:size*(i+1)])
#     # for j in range(20):
#     #     print(i,j)
