""" This guy gathers the zshot evaluations and summarizes them."""


import os
import re

# from evaluate_testset import parse_response

def extract_eval(file_content: str):
    """Extract the eval results from the file content. """

    is_dasco = 0
    seq_id = 'unknown (proabaly error)'
    # print(f'file_content = {file_content}' + '\n'*4)
    regex = re.findall(r'is_Dasco (\w{4,5})', file_content)
    if regex:
        is_dasco = 1 if regex[0] == 'True' else 0
        seq_id = re.findall(r'Ground truth: (A\d{6})', file_content)[0]
    # else:
    #     error = re.findall(r'is_Dasco: (\w{4,5})', file_content)

    # print(is_dasco, 0 + is_dasco)
    # print(type(is_dasco))
    return is_dasco, seq_id
    # eq_regex = re.findall( r'lambda a_n: [ absignqrt()/*_\[\]\d+-]+', file_content)
    # eq = eq_regex[0] if eq_regex else None
    #
    # # print(regex)
    # # print(f'seq_id = {seq_id}')
    # # print(f'{eq_regex = }')
    # # print(f'{eq = }')
    # is_manual_check = {'True': True, 'False': False, 'no match found': 'Fail'}.get(regex[0])
    # # print(f'{is_manual_check = }')
    #
    # # _seq, eq = parse_response(file_content)


    # return is_dasco, seq_id, eq

#
# # list all files in experiment_id directory
# # for file in os.listdir(out_dir):
# # count_manual += is_manual(file)
#

if __name__ == '__main__':
    EXPERIMENT_ID = 'zshot_eval-merge1112'

    results_dir = f'results/{EXPERIMENT_ID}/'
    print(f'{results_dir=}')


    SCALE = 30000
    files =  sorted(os.listdir(results_dir))[:SCALE]

    total = len(files)
    print(f'{len(files) = }')

    # 1/0
    # buggy = []
    store = dict()
    count = 0
    for filename in files:
        with open(os.path.join(results_dir, filename), 'r') as f:
            # print(f'{filename=}')
            # is_manual_check, seq_id, eq = extract_eval(f.read())
            is_dasco, seq_id = extract_eval(f.read())
            store[filename[:5]] = is_dasco
            # seq = csv[seq_id]
            # equiv = check_equiv(eq, seq)
            count += is_dasco
            # print(count)

    acc = count / total
    print(f'\nAccuracy so far from {total} files: \n{acc*100:.2f}%')
    print(f'In worst case, the accuracy for 10k sequences will be: \n{count/10000*100:.2f}%')

    print(store)
    print(len(store.keys()))

    # 2. Bins of accuracy
    ac100 = [k for k,v in store.items() if k < '00100']
    print(ac100)
    ac100 = [v for k,v in store.items() if k < '00100']
    print(ac100)
    ac200 = [(k, v) for k,v in store.items() if k < '00200']
    print(ac200)
    ac200 = [v for k,v in ac200]
    # print(len(ac100))
    # print(len(ac200))
    print(f'  {sum(ac100)}/100    {sum(ac200)}/200')

    ac500 = [(k, v) for k,v in store.items() if '01500' <= k < '02000']
    # print(ac500)
    ac500 = [v for k,v in ac500]
    ac2k = [(k, v) for k,v in store.items() if '02000' <= k < '03000']
    # print(ac2k)
    # print(len(ac500))
    # print(len(ac2k))
    ac2k = [v for k,v in ac2k]
    print(f' {sum(ac500)}/500   1k  # {sum(ac2k)}/1000  2k')

    ac3k = [(k, v) for k,v in store.items() if '03000' <= k < '04000']
    # print(ac3k)
    ac3k = [v for k,v in ac3k]
    ac4k = [(k, v) for k,v in store.items() if '04000' <= k < '05000']
    # print(ac4k)
    # print(len(ac3k))
    # print(len(ac4k))
    ac4k = [v for k,v in ac4k]
    print(f'{sum(ac3k)}/1000   3k  # {sum(ac4k)}/1000  4k')
    # 106/1000  3k  # 123/1000  4k  (slight difference)

    ac300 = [(k, v) for k,v in store.items() if '05000' <= k < '05300']
    # print(ac300)
    ac300 = [v for k,v in ac300]
    # print(len(ac300))
    print(f'For archive:\n{sum(ac300)}/300   5k')
    # 106/1000  3k  # 123/1000  4k  (slight difference)

    ac5k = [(k, v) for k,v in store.items() if '05000' <= k < '06000']
    # print(ac5k)
    ac5k = [v for k,v in ac5k]
    ac6k = [(k, v) for k,v in store.items() if '06000' <= k < '07000']
    # print(ac6k)
    ac6k = [v for k,v in ac6k]
    # print(len(ac5k))
    # print(len(ac6k))
    print(f'New:\n{sum(ac5k)}/1000   5k  # {sum(ac6k)}/1000  6k')

    ac7k = [(k, v) for k,v in store.items() if '07000' <= k < '08000']
    # print(ac7k)
    ac7k = [v for k,v in ac7k]
    ac8k = [(k, v) for k,v in store.items() if '08000' <= k < '09000']
    # print(ac8k)
    ac8k = [v for k,v in ac8k]
    # print(len(ac7k))
    # print(len(ac8k))
    print(f'{sum(ac7k)}/1000   7k  # {sum(ac8k)}/1000  8k')


    ac9k = [(k, v) for k,v in store.items() if '09000' <= k < '10000']
    # print(ac9k)
    ac9k = [v for k,v in ac9k]
    # print(len(ac9k))
    print(f'{sum(ac9k)}/1000   9k ')


    # older eval11 results:
    # 36/100 58/200
    # 213/500   1k  # 321/1000  2k
    # 104/1000  3k  # 121/1000  4k
    # 22/300    5k
    
    # New eval12 (same code as 11):
"""  36/100    58/200               (missing 655)
     213/500   1k  # 321/1000  2k (missing 386, final)
    106/1000   3k  # 123/1000  4k (both final)
    168/1000   5k  # 365/1000  6k (missing 126, final)
    319/1000   7k  # 81/1000  8k    (missing 550 in total)
    105/1000   9k  (final)
    """



# Missing bins:
# miss_sums = {'miss 0k': 655, 'miss 1k': 386, 'miss 2k': 0, 'miss 3k': 0, 'miss 4k': 0, 'miss 5k': 126, 'miss 6k': 0, 'miss 7k': 225, 'miss 8k': 326, 'miss 9k': 0}
# Mising groups: start - end
# {'miss 0k': ['00252', '00276', '00370'], 'miss 1k': ['01385'], 'miss 2k': [], 'miss 3k': [], 'miss 4k': [], 'miss 5k': ['05384', '05509'], 'miss 6k': [], 'miss 7k': ['07663'], 'miss 8k': ['08325'], 'miss 9k': []}
# i.e.
# '00252 - '00276', 00370 - '01385', '05384' - '05509', '07663' - '08325'
