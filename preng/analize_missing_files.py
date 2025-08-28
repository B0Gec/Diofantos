"""For zero-shot 10k experiments, look how and which files are missing, calculate accuracy to compare with other methods."""

import os


if __name__ == '__main__':
    EXPERIMENT_ID = 'obat-dasco25-10k-merged'  # pgeq LLM linrec n_input=15

    # results_dir = f'../results/lhevaluate/{EXPERIMENT_ID}/'
    results_dir = f'results/{EXPERIMENT_ID}/'
    print(f'{results_dir=}')


    # SCALE =  1000
    SCALE = 30000
    files = sorted(os.listdir(results_dir))[:SCALE]
    ids = [file[:5] for file in files]
    print(f'{len(files) = }')
    print(f'{files[:10] = }')

    # 1k bins:
    bins = {f'{k}k': [file for file in files if file[1] == str(k)] for k in range(10)}
    print(bins.keys())
    print({k: lst[:3] for k, lst in bins.items()})
    bins_sums = {k: len(lst) for k, lst in bins.items()}
    print(bins_sums)

    # 2. missing
    print('\nMissing bins:')
    miss_bins = {f'miss {k}k': [y for i in range(k*1000, (k+1)*1000) if (y:=f'{i:0>5}') not in ids] for k in range(10)}
    size = 50
    print(f'first {size}:', {k: lst[:size] for k, lst in miss_bins.items()})
    miss_sums = {k: len(lst) for k, lst in miss_bins.items()}
    print(f'{miss_sums = }')

    # 2.1: missing groups (e.g. 212-334, 703-708)
    print('\nMising groups: start - end')
    miss_bins_se = {f'miss {k}k': [y for i in range(k*1000, (k+1)*1000) if (y:=f'{i:0>5}') not in ids and not (f'{i-1:0>5}' not in ids and f'{i+1:0>5}' not in ids)] for k in range(10)}
    print(miss_bins_se)
    # 1/0

    # 1/0
    # print(miss_bins)
    miss_100bins = {f'miss {k}k': {f'{h} hekto': [y for i in range(k*1000 + h*100, k*1000 + (h+1)*100) if (y:=f'{i:0>5}') not in ids] for h in range(10)} for k in range(10)}
    print('\nMissing 100 bins (first 3:')
    print({k: {h: l[:3] for h, l in d.items()} for k, d in miss_100bins.items()})
    for k, d in miss_100bins.items():
        print(k, {h: len(l) for h, l in d.items()})
    # print(miss_100bins)


# Output:
# Missing bins:
# miss_sums = {'miss 0k': 655, 'miss 1k': 386, 'miss 2k': 0, 'miss 3k': 0, 'miss 4k': 0, 'miss 5k': 126, 'miss 6k': 0, 'miss 7k': 225, 'miss 8k': 326, 'miss 9k': 0}
# Mising groups: start - end
# {'miss 0k': ['00252', '00276', '00370'], 'miss 1k': ['01385'], 'miss 2k': [], 'miss 3k': [], 'miss 4k': [], 'miss 5k': ['05384', '05509'], 'miss 6k': [], 'miss 7k': ['07663'], 'miss 8k': ['08325'], 'miss 9k': []}
# i.e.
# '00252 - '00276', 00370 - '01385', '05384' - '05509', '07663' - '08325'

# data files:
# 00252 - 00276       file created [25 missing]
# 00370 - 01385       s370-1385 [~1015 missing]
# 05384 - 05509       file created [126 missing]
# 07663 - 08325:      s6257-8325 [~663 missing]

# i.e. problematic: 0,1, 5, 7,8


