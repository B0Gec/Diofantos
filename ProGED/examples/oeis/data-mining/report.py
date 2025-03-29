# print(2)
import re
import pandas as pd
import sys
data_filename = '../outputs_golden/cluster-sam100-ord0-dirTrue.log'
data_filename = '../outputs_newgrammar/log_oeis_2021-06-12_10-29-38_success-14-newgrammar.txt'
data_filename = '../outputs_newgrammar/cluster-sam100-new.log'
data_filename = '../firstCatalan.txt'
data_filename = '../fibonaciresults.txt'
data_filename = '../catalan_phd_output.txt'
flags_dict = { i.split("=")[0]:  i.split("=")[1] for i in sys.argv[1:] if len(i.split("="))>1}
data_filename = flags_dict.get("--data_filename", data_filename)
f = open(data_filename, mode='r', encoding='utf-8')
log = f.read()
log_length = len(log)
# print(type(log), f"{log_length:e}")
# print(log[1:3000])
# print(log[1:30])
# print(23)


# =======================SPECS:=======================================

specs_orig = """
Running equation discovery for all oeis sequences, with these settings:
=>> sample_size = 50
=>> grammar's q and p = 0.5 and 0.3
=>> grammar_template_name = simplerational2
=>> generator_settings = {'functions': ["'sqrt'", "'exp'", "'log'"], 'p_F': [0.333, 0.333, 0.333]}
=>> optimizer = differential_evolution
=>> task_type = algebraic
=>> timeout = inf
=>> random_seed = 5
=>> lower_upper_bounds = (-4, 4)
=>> number of terms in every sequence = 50
=>> number of all considered sequences = 14
=>> list of considered sequences = ('A000009', 'A000040', 'A000045', 'A000124', 'A000219', 'A000292', 'A000720', 'A001045', 'A001097', 'A001481', 'A001615', 'A002572', 'A005230', 'A027642')
=>> Grammar used: 
Grammar with 61 productions (start state = S)
    S -> P '/' R [0.2]
    S -> P [0.8]
    P -> P '+' 'C' '*' R [0.4]
    P -> 'C' '*' R [0.3]
    P -> 'C' [0.3]
    R -> 'sqrt' '(' 'C' '*' M ')' [0.133253]
    R -> 'exp' '(' 'C' '*' M ')' [0.133253]
    R -> 'log' '(' 'C' '*' M ')' [0.133253]
    R -> M [0.60024]
    M -> M '*' V [0.4]
    M -> V [0.6]
    V -> 'n' [0.5]
    V -> 'an_1' [0.319672]
    V -> 'an_2' [0.0965392]
    V -> 'an_3' [0.0295993]
    V -> 'an_4' [0.0095173]
    V -> 'an_5' [0.00349271]
    V -> 'an_6' [0.00168534]
    V -> 'an_7' [0.00114312]
    V -> 'an_8' [0.00098046]
    V -> 'an_9' [0.000931661]
    V -> 'an_10' [0.000917021]
    V -> 'an_11' [0.000912629]
    V -> 'an_12' [0.000911311]
    V -> 'an_13' [0.000910916]
    V -> 'an_14' [0.000910798]
    V -> 'an_15' [0.000910762]
    V -> 'an_16' [0.000910751]
    V -> 'an_17' [0.000910748]
    V -> 'an_18' [0.000910747]
    V -> 'an_19' [0.000910747]
    V -> 'an_20' [0.000910747]
    V -> 'an_21' [0.000910747]
    V -> 'an_22' [0.000910747]
    V -> 'an_23' [0.000910747]
    V -> 'an_24' [0.000910747]
    V -> 'an_25' [0.000910747]
    V -> 'an_26' [0.000910747]
    V -> 'an_27' [0.000910747]
    V -> 'an_28' [0.000910747]
    V -> 'an_29' [0.000910747]
    V -> 'an_30' [0.000910747]
    V -> 'an_31' [0.000910747]
    V -> 'an_32' [0.000910747]
    V -> 'an_33' [0.000910747]
    V -> 'an_34' [0.000910747]
    V -> 'an_35' [0.000910747]
    V -> 'an_36' [0.000910747]
    V -> 'an_37' [0.000910747]
    V -> 'an_38' [0.000910747]
    V -> 'an_39' [0.000910747]
    V -> 'an_40' [0.000910747]
    V -> 'an_41' [0.000910747]
    V -> 'an_42' [0.000910747]
    V -> 'an_43' [0.000910747]
    V -> 'an_44' [0.000910747]
    V -> 'an_45' [0.000910747]
    V -> 'an_46' [0.000910747]
    V -> 'an_47' [0.000910747]
    V -> 'an_48' [0.000910747]
    V -> 'an_49' [0.000910747]

ModelBox: 44 models
"""

specs_orig_old = """=>> is_direct = True
=>> sample_size = 100
=>> grammar_template_name = polynomial
=>> generator_settings = {p_T: [0.4, 0.6], p_R: [0.6, 0.4]}
=>> optimizer = <function DE_fit at 0x1541cac7f700>
=>> timeout = inf"""
# print( "\n"*10)

pattern = """
Running equation discovery for all oeis sequences, with these settings:
=>> sample_size = \d+
=>> grammar's q and p = [\d.]+ and [\d.]+
=>> grammar_template_name = \w+
=>> generator_settings = [\w\W]+?
=>> optimizer = \w+
=>> task_type = \w+
=>> timeout = [\w.]+
=>> random_seed = \w+
=>> lower_upper_bounds = [\d()\[\]\ .,-]+
=>> number of terms in every sequence = \d+
=>> number of all considered sequences = \d+
=>> list of considered sequences = [()\[\],\w\ '"]+
=>> Grammar used: 
"""
grammy = "[\w\W]+?"
mb = "ModelBox: \d+ models"

specs = re.findall(pattern + grammy + mb, log)
# print('specs:', specs)
print('specs:')
# print('len(specs)', len(specs))
print(specs[0] if len(specs)>0 else None)
# # =======================End Of SPECS:================================

seq_orig = "Parameter fitting for sequence A000001 took 209.85773301217705 secconds."
start = re.findall("ModelBox: (\d+) models", log)
seqs = re.findall(
        "ModelBox: \d+ models\n"
        "[\w\W]+?Parameter fitting for sequence \w+ took \d+.\d+ secconds.", log)
seq_ids = re.findall("Parameter fitting for sequence (\w+) took \d+.\d+ secconds.", log)
# print('seqs: \n', seqs[:150][0][-1000:], f"{len(seqs):e} {len(seqs[0]):e}")
# print('seqs: \n', seqs[0])  # lengthy output
print('sequences extracted:', f"{len(seqs)}")
# print('length of text of one seq\'s result:', f"{len(seqs[0])}")
# print(f'log_length: {log_length:e}')
# print('seqs:', seqs)
seq = seqs[0]
def final_scores(log: str = log):
    seqs = re.findall(
            "Parameter fitting for sequence \w+ took \d+.\d+ secconds.\n"
            "[\w\W]+?Total time consumed by now:\d+.\d+", log)
    # print(seqs)
    print('sequences extracted:', f"{len(seqs)}")
    return seqs
seqs_final_scores = final_scores(log)

formulas_file = "oeis_formulas.csv" if data_filename[:2] == ".." else "data-mining/oeis_formulas.csv"
formulas_df = pd.read_csv(formulas_file)
def get_formulas(id_):
    def empty_list(listi: list, empty_type=type(0.0), empty=''):
        return [i for i in listi if (i!='' and not isinstance(i, empty_type))]
    return empty_list(formulas_df[id_])
# print(get_formulas('A000009'))

def look_seq(seq_log, final_score: bool = False):
    seq = seq_log
    seq_id = re.findall("Parameter fitting for sequence (\w+) took \d+.\d+ secconds.", seq)[0]
    print("seq ID:", seq_id)
    # print('seq:', seq[:800])

    # formulas = get_formulas(seq_id)
    # print('')
    # for i in formulas:
    #     print(i)
    # print('')

    # models_card = int(re.findall("ModelBox: (\d+) models", seq)[0])
    # print(models_card)
    if not final_score: # default (old)
        fitting = re.findall("(model: [\w.+/*\-()\ ]+); p: [\de.+\-\ ]+ ; (error: [\de.+\-\ ]+)\n", seq)
    else:
        fitting = re.findall("(model: [\w.+/*\-()\ ]+); (error: [\de.+\-\ ]+)\n", seq)
    # fitting = re.findall("(model: )(([a-zA-Z_+/*\-()\ ]*?)([\d.]+))+([a-zA-Z_+/*\-()\ ]*); p: [\de.+\-\ ]+ ; (error: [\de.+\-\ ]+)\n", seq) 
    # print('substit', substit)
    # 1/0

    # if not final_score:
    # print('check fitting', len(fitting), models_card)
    print('check fitting: len(fitting) vs. models_card', len(fitting))
    if not final_score and not len(fitting) == models_card:
        print("!!!! REGULAR EXPRESSIONS NOT SUFFICIENTLLY COVERED !!!!")
        print('len(fitting) vs models_card:', len(fitting), models_card)
        print('fitting:', fitting)
        # print('log:\n', seq)
    else:
        # for model, error in fitting:
        # # for n, i in enumerate(fitting):
        #     print(model, error)
        #     # print(error, substit)
        #     # print(i)
        #     # print("".join(fitting_simple[n]))
        #     # print("".join(i))
        #     # print("".join(i) == "".join(fitting_simple[n]))
        #     # if not "".join(i) == "".join(fitting_simple[n]):
        #     #     print("!!!! REGULAR EXPRESSIONS WRONG !!!!")
        def extract(error):
            value = float(re.findall("error: ([\de.+\-\ ]+)", error)[0])
            return value

        substit = [(re.sub("([\d.]{1,5})[\d.]*", r"\1", model), error) for model, error in fitting]
        sort = sorted(substit, key=lambda x: extract(x[1]))
        # sort = fitting
        # sort = substit
        # print('\n\n\nsorted:\n\n\n')
        for model, error in sort:
        #     # print(i[1])
            print(f"{error:<30} {model}")
        print("\n")
    return


IS_FINAL_SCORE = False  # default
IS_FINAL_SCORE = True
if IS_FINAL_SCORE:
    seqs = seqs_final_scores
for n, i in enumerate(seqs):
    print('sequence', n)
    look_seq(i, IS_FINAL_SCORE)





f.close()
