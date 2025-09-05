""" This guy gathers the zshot evaluations and summarizes them."""


import os
import re

# from evaluate_testset import parse_response

PY_ERRORS = ['KeyError', 'PermissionError', 'RecursionError', 'NameError', 'IndexError', 'ValueError', 'TypeError',]
AUX_ERRORS = ['empty file']

def extract_eval(file_content: str):
    """Extract the eval results from the file content. """

    is_dasco = None
    seq_id = 'unknown (proabaly error)'
    errors = dict()
    regex = re.findall(r'is_Dasco (\w{4,5})', file_content)
    if regex:
        is_dasco = 1 if regex[0] == 'True' else 0
        seq_id = re.findall(r'Ground truth: (A\d{6})', file_content)[0]
    else:
        for error in PY_ERRORS:
            error_found = re.findall(rf'{error}: .+', file_content)
            if error_found:
                errors[error] = error_found[0]
        if len(file_content) < 100:
            print(file_content)
            errors['empty file'] = f'{file_content = }'

    return is_dasco, seq_id, errors


def extract_dfmb(file_content: str):
    """Extract the eval results from the Diofantos and MuadeeB results files."""
    is_dasco = 0
    regex = re.findall(r'(\w{4,5})  -  checked against', file_content)
    if regex:
        is_dasco = 1 if regex[0] == 'True' else 0
    return is_dasco


if __name__ == '__main__':
    EXPERIMENT_ID = 'zshot_eval-merge1112'

    df_dir = '../results/good/re2-transfoeis_acc2'
    mb_dir = '../results/goodmb/re2-mbtmN25'

    results_dir = f'results/{EXPERIMENT_ID}/'
    print(f'{results_dir=}')


    SCALE = 30000
    # SCALE = 100
    files = sorted(os.listdir(results_dir))[:SCALE]
    df_files = sorted(os.listdir(df_dir))[:SCALE]
    mb_files = sorted(os.listdir(mb_dir))[:SCALE]

    total = len(files)
    print(f'{len(files) = }')

    # 1/0
    # buggy = []
    store, df_store, mb_store = dict(), dict(), dict()
    errors_store = dict()
    no_error_fails = []
    errors_count = {error: 0 for error in PY_ERRORS + AUX_ERRORS}
    dasco_re_count = 0
    count = 0
    for filename in files:
        with open(os.path.join(results_dir, filename), 'r') as f:
            # print(f'{filename=}')
            # is_manual_check, seq_id, eq = extract_eval(f.read())
            is_dasco, seq_id, errors = extract_eval(f.read())
            dasco_re = is_dasco is not None
            is_dasco_num = 0 if is_dasco is None else is_dasco
            if dasco_re and not is_dasco_num:
                no_error_fails.append(filename[:5])
            store[filename[:5]] = is_dasco_num
            errors_store[filename[:5]] = errors
            for error in errors:
                if errors[error]:  # not needed anymore
                    errors_count[error] += 1

            dasco_re_count += dasco_re
            # sanity check:
            print(f'{is_dasco}, {errors}, {seq_id}, {filename}')
            print(f'{dasco_re + sum([1 for error in errors if errors[error]]) = }')
            assert dasco_re + sum([1 for error in errors if errors[error]]) == 1
            # seq = csv[seq_id]
            # equiv = check_equiv(eq, seq)
            count += is_dasco_num
            # print(count)


    for filename in df_files:  # df
        with open(os.path.join(df_dir, filename), 'r') as f:
            df_store[filename[:5]] = extract_dfmb(f.read())
    for filename in mb_files:  # fb
        with open(os.path.join(mb_dir, filename), 'r') as f:
            mb_store[filename[:5]] = extract_dfmb(f.read())

    acc = count / total
    print(f'\nAccuracy so far from {total} files: \n{acc*100:.2f}%')
    print(f'In worst case, the accuracy for 10k sequences will be: \n{count/10000*100:.2f}%')

    print(store)
    print(len(store.keys()))

    # 1/0

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
        319/1000   7k  # 81/1000   8k    (missing 550 in total)
        105/1000   9k  (final)
        """



    # Missing bins:
    # miss_sums = {'miss 0k': 655, 'miss 1k': 386, 'miss 2k': 0, 'miss 3k': 0, 'miss 4k': 0, 'miss 5k': 126, 'miss 6k': 0, 'miss 7k': 225, 'miss 8k': 326, 'miss 9k': 0}
    # Mising groups: start - end
    # {'miss 0k': ['00252', '00276', '00370'], 'miss 1k': ['01385'], 'miss 2k': [], 'miss 3k': [], 'miss 4k': [], 'miss 5k': ['05384', '05509'], 'miss 6k': [], 'miss 7k': ['07663'], 'miss 8k': ['08325'], 'miss 9k': []}
    # i.e.
    # '00252 - '00276', 00370 - '01385', '05384' - '05509', '07663' - '08325'

    # proposed bins: 0-200, 1400-2000, 5000-5300, 5600-6000, 7000-7800, 8400-9000.
    # more refined bins: 0-250, 1400-2000, 5000-5350, 5550-6000, 7000-7800, 8350-9000.

    bins_def = [(0, 200), (1400, 2000),
                (5000, 5300), (5600, 6000),
                # (7000, 7800), (8400, 9000)]
                (7000, 7900), (8400, 9000)]
    bins_def = [(0, 250), (1400, 2000),
                (5000, 5350), (5550, 6000),
                (7000, 7900), (8350, 9000)]

    bins_def = [(0, 252),
                (252, 270),
                (277, 370),
                # (370, 885),
                (370, 885),
                (885, 948),
                # (576, 699),
                # (277, 699),
                # (277, 885),
                # (277, 885),
                (1386, 2000),
                (5000, 5384),
                (5384, 5510),
                (5510, 6000),
                # (5000, 6000),
                ]

    filler = [
                (2000,  3000),
                (3000,  4000),
                (4000,  5000),
                (6000,  7000),
                (7000,  8000),
                (8000,  9000),
                (9000, 10000),
        ]
    bins_def = sorted(bins_def+filler)
    print(bins_def)
    print(len(bins_def))

    # (2000,  3000)
    # (5000,  6000)
    # (6000,  7000)
    # (7000,  8000)
    # (8000,  9000)
    # (9000, 10000)
    #
    bins_sizes = [b-a for a,b in bins_def]

    acks = [(a, b, [ v for k, v in store.items() if f'{a:0>5}' <= k < f'{b:0>5}']) for a,b in bins_def]
    # print(acks)
    print()
    print(f'\ntotal true files: {sum([sum(bin) for a, b, bin in acks])}')
    print(f'total binned acc: {sum([sum(bin) for a, b, bin in acks])/sum([len(bin) for a, b, bin in acks])*100:0.2f}%')
    for a, b, bin in acks:
        print(f'{sum(bin): >4}/{len(bin): <4}      = {sum(bin)/len(bin)*100:0.2f}%     {str(a)[0]}k  ({a: >4}-{b})')

    # print(df_store)
    # print(mb_store)

    # print(f'{sum(df_store.values()) = }')
    # print(f'{sum(mb_store.values()) = }')

    df_acks = [(a, b, [ v for k, v in df_store.items() if f'{a:0>5}' <= k < f'{b:0>5}']) for a,b in bins_def]
    # print(acks)
    print()
    print('df:')
    for n, abin in enumerate(df_acks):
        a, b, bin = abin
        print(f'{sum(bin): >4}/{bins_sizes[n]: <4}     = {sum(bin)/bins_sizes[n]*100:0.2f}%     {str(a)[0]}k  ({a: >4}-{b})')

    mb_acks = [(a, b, [ v for k, v in mb_store.items() if f'{a:0>5}' <= k < f'{b:0>5}']) for a,b in bins_def]
    # print(acks)
    print('mb:')
    for a, b, bin in mb_acks:
        print(f'{sum(bin): >4}/{len(bin): <4}     = {sum(bin)/len(bin)*100:0.2f}%     {str(a)[0]}k  ({a: >4}-{b})')

    print(f'total binned df acc: {sum([sum(bin) for a, b, bin in df_acks])/sum([bins_sizes[n] for n in range(len(df_acks))])*100:0.2f}%')
    print(f'total binned mb acc: {sum([sum(bin) for a, b, bin in mb_acks])/sum([len(bin) for a, b, bin in mb_acks])*100:0.2f}%')
    print(f'\n{len(files) = }')
    print(f'total tasks in bins: {sum(bins_sizes)}')

    # 1/0


    # 3. Fails analisys:
    doFail_analisys = False
    # doFail_analisys = True
    if doFail_analisys:
        print(f'\n{len(files) = }')
        print(f'is_Dasco occurs: {dasco_re_count}, Errors: {sum([amount for error, amount in errors_count.items()]) }')
        print(f'total: {dasco_re_count + sum([amount for error, amount in errors_count.items()]) }')
        # 1/0


        print(f'{errors_count = }')

        has_errors_store = {task: es for task, es in errors_store.items() if es}
        print(f'{len(has_errors_store) = }')
        print(f'{has_errors_store = }')

        errors_store_byerror = {ern: [(task, err[ern]) for task, err in has_errors_store.items() if ern in err] for ern in PY_ERRORS + AUX_ERRORS }
        print(errors_store_byerror)
        print(errors_store_byerror['TypeError'])
        print(errors_store_byerror['IndexError'])
        # 1/0

        # 3.1 Empty files
        # # empty file content (evals not finished in 1h (look TODO))
        emptys = [{t: es['empty file']} for t, es in has_errors_store.items() if 'empty file' in es]
        print(emptys)
        # print(nonempty_empties)  # (05007, ''), (06710, '')


    # 3.2 some errors
    # erns = ['KeyError', 'PermissionError', 'RecursionError']
    # for ern in erns:
    # # for ern in errors_count:
    #     print()
    #     for task, err in [(task_, errd) for task_, errd in has_errors_store.items() if ern in errd]:
    #         print(f'{task}: {err}')
    #
    # some_errors = [ [f'{task}: {err}' for task, err in [(task_, errd) for task_, errd in has_errors_store.items() if ern in errd]] for ern in erns ]
    # print(some_errors)
    # # for some in some_errors:
    # #     print(some)
    # compressed_some_errors = { ern: [task for task, errd in has_errors_store.items() if ern in errd] for ern in erns}
    # print(compressed_some_errors)
    # 1/0

    # '00214', '00313', '03274', '04407', '04435', '04915', '06939', '08820', '09679']

    # 3.3 TypeError:
    # print()
    # for task, err in errors_store_byerror['TypeError']:
    #     print(f'{task}: {err}')

    # # Type errors:
    # TYPEERRORS = ['TypeError: list indices must be integers or slices, not float',
    #               "TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'",
    #               "TypeError: unsupported operand type(s) for -: 'int' and 'ellipsis'",
    #               "TypeError: unsupported operand type(s) for +: 'int' and 'tuple'",
    #               "TypeError: int() argument must be a string, a bytes-like object or a real number, not 'tuple'",
    #               "TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'",
    #               "TypeError: unsupported operand type(s) for *: 'functools._lru_cache_wrapper' and 'int'",
    #               "TypeError: unsupported operand type(s) for -: 'int' and 'functools._lru_cache_wrapper'",
    #               "TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'functools._lru_cache_wrapper'",
    #               "TypeError: find_next_prime() missing 1 required positional argument: 'prev'",
    #               "TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex'", ]
    # specific = 10000
    # for type_suberror in TYPEERRORS[:specific]:
    #     for task, err in errors_store_byerror['TypeError']:
    #         if err == type_suberror:
    #             print(f'{task}: {err}')
    #     if err not in TYPEERRORS:
    #         print(f'{task}: {err}')


    # # 3.4 Index Error:
    # for task, err in errors_store_byerror['IndexError']:
    #     print(f'{task}: {err}')
    # INDEX_ERRORS = ['IndexError: list assignment index out of range',
    #               'IndexError: list index out of range',
    #                 ]
    #
    # specific = 1000000
    # subcount = dict()
    #
    # print(len(errors_store_byerror['IndexError']))
    # # 1/0
    #
    #
    # for type_suberror in INDEX_ERRORS[:specific]:
    #     for task, err in errors_store_byerror['IndexError']:
    #         # print(subcount)
    #         if err == type_suberror:
    #             subcount[err] = subcount.get(err, 0) + 1
    #             print(f'{task}: {err}')
    #         if err not in INDEX_ERRORS:
    #             subcount[err] = subcount.get(err, 0) + 1
    #             print(f'{task}: {err}')
    # print(subcount)
    # # 2 special errors: false


    # 3.5 ValueError:
    doValueError = True
    doValueError = False
    if doValueError:
        subcount = dict()
        print(len(errors_store_byerror['ValueError']))
        # for type_suberror in INDEX_ERRORS[:specific]:
        for task, err in errors_store_byerror['ValueError']:
            subcount[err] = subcount.get(err, 0) + 1
        print(subcount)
        # 1/0


    # 3.6 NameError:
    doNameError = True
    doNameError = False
    if doNameError:
        subcount = dict()
        print(len(errors_store_byerror['NameError']))
        # for type_suberror in INDEX_ERRORS[:specific]:
        for task, err in errors_store_byerror['NameError']:
            subcount[err] = subcount.get(err, 0) + 1
        print(subcount)
        for err in sorted(subcount.keys(), key=lambda x: -subcount[x]):
            for task in [task_ for task_, err_ in errors_store_byerror['NameError'] if err_ == err]:
                print(f'{task}: {err}')

        print(sorted(subcount.values()))
    # 1/0


    print(f'{errors_count = }')



    # errors_count = {'KeyError': 1, 'PermissionError': 7, 'RecursionError': 14, 'NameError': 543, 'IndexError': 655, 'ValueError': 4092, 'TypeError': 283, 'empty file': 2}
    #                   false           2 true of 7                                                                                                             2x false
    # errors_count (8833 files) = {'KeyError': 1, 'PermissionError': 9, 'RecursionError': 17, 'NameError': 600, 'IndexError': 152, 'ValueError': 4495, 'TypeError': 295, 'empty file': 3}
    #                              false           4 true of 9                                                   missing files       eq not found          c1*a(n-2)          2/3? x false
    # {'KeyError': ['05553'], 'PermissionError': ['00214', '00313', '03274', '04407', '04435', '04915', '06939', '08820', '09679'], 'RecursionError': ['00107', '02070', '02373', '03342', '03729', '04931', '05184', '05923', '06104', '06130', '06185', '06494', '07859', '07928', '08003', '08415', '09505']}


    # KeyError 05553: bad function - true negative.
    # permission: 03274: main)

    # look main_failed_codes for solutions and manual check

    # RecursionError:
    # 02070, 02373, 03729, 04931, 05184, 08415, 09505 : self-reccerence or a(n+1)
    # 03342, 05923, 06104, 06130, 06185, 06494, 07859,   analized, all false

    # TypeError:
    # 33: false,
    # 1717 02592: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'complex'
    #       -  (-1)**(1/2) or similar will produce complex number. ( sqrt(-1) = i )
    # 5006: using some other function after calculate_sequence.
    # 7528, 6137, 3203, 6175:  # 2**latex_seq  # TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'functools._lru_cache_wrapper'
    #    - no new insight, bad prediction.
    # 333, 2402, 5252  a(n) = a(n-2), -> this is tuple.  # TypeError: int() argument must be a string, a bytes-like object or a real number, not 'tuple'
    # 4622, 5382, 9675, 9680,  : unrelated

    # IndexError:
    # mainly missing files, other halucinations. (this error is very clean-cut)


    # 3.7? Local errors
    a,b = 5384, 5493
    tasks = list(range(a, b))
    print(f'{a}, {b}, {b-a}')
    # print(errors_store.items())
    # print({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}.items())
    # {'True': }
    store.items()
    print(f'Success: {sum(succ for task, succ in store.items() if task in tasks)}')
    # print(store)
    1/0

    local_err_count = {err: len([task for task, err_dict in errors_store.items() if task in tasks and err in err_dict.keys()]) for err in errors_count.keys()}
    print(local_err_count)
    print(sum(local_err_count.values()))

    1/0
    # {}


    # 4.0  mb vs zshot 1 vs 0.
    # ========================

    # print(f'{store = }')
    # print(f'{mb_store = }')

    # print(f'{mb_acks = }')
    # scope =

    binsizes = [ len(bin[2]) for n, bin in enumerate(mb_acks) ]
    print(binsizes)
    zs_real_acks = [f'{sum(bin[2]) / len(bin[2]):.4}' for n, bin in enumerate(acks)]
    print(zs_real_acks)
    mb_real_acks = [ f'{sum(bin[2])/len(bin[2]):.4}' for n, bin in enumerate(mb_acks) ]
    print(mb_real_acks)
    acc_diffs = [ f'{sum(acks[n][2])/len(acks[n][2]) - sum(bin[2])/len(bin[2]):.4}' for n, bin in enumerate(mb_acks) ]
    print(acc_diffs)

    nbin = 6
    a, b = mb_acks[nbin][0], mb_acks[nbin][1]
    print(f'a: {a}, b: {b}')

    # print(mb_acks[nbin])
    print(f'{len(mb_acks[nbin][2]) = }')
    print(f'{sum(acks[nbin][2]) = }')
    print(f'{sum(mb_acks[nbin][2]) = }')
    # print(store)
    zs_bin = {k: v for k, v in store.items() if f'{a:0>5}' <= k < f'{b:0>5}'}
    mb_bin = {k: v for k, v in mb_store.items() if f'{a:0>5}' <= k < f'{b:0>5}'}
    print(f'bin len: {b-a}')
    print(f'zs bin sum: {sum(zs_bin.values())}')
    print(f'mb bin sum: {sum(mb_bin.values())}')
    succs_zs = [task for task, succ in zs_bin.items() if succ]
    succs_mb = [task for task, succ in mb_bin.items() if succ]
    doable_fails = [task for task in succs_mb if task not in succs_zs ]
    print(doable_fails)
    # print(succs_zs[:10])
    # print(succs_mb[:10])

    # print(f'not zs but in mb: {len([task for task, succ in zs_bin.items() if not succ and ])}')
    # ['05010', '05024', '05073', '05091', '05092', '05097', '05122', '05148', '05149', '05150', '05173', '05174',
    #  '05175', '05177', '05184', '05185', '05213', '05214', '05215', '05216', '05219', '05221', '05226', '05227',
    #  '05228', '05229', '05230', '05231', '05256', '05257', '05258', '05259', '05260', '05261', '05263', '05264',
    #  '05265', '05266', '05268', '05269', '05270', '05271', '05272', '05273', '05274', '05275', '05276', '05280',
    #  '05281', '05283', '05284', '05285', '05286', '05315', '05316', '05317', '05318', '05320', '05321', '05322',
    #  '05323', '05324', '05325', '05327', '05328', '05329', '05330', '05331', '05332', '05333', '05334', '05335',
    #  '05337', '05338', '05339', '05340', '05341', '05357', '05358', '05359']

    1/0
    print(zs_bin)
    # mb_acks = [(a, b, [ v for k, v in store.items() if f'{a:0>5}' <= k < f'{b:0>5}']) for a,b in bins_def]
    # print(acks)

    1/0
    print(f' zs successes: {[i for i, succ in enumerate(acks[nbin][2]) if succ]}' )
    print(f' mb successes: {[i for i, succ in enumerate(mb_acks[nbin][2]) if succ]}' )
    print(f' zs successes: {[i for i, succ in enumerate(acks[nbin][2]) if succ]}' )
    # print([i for i, succ in enumerate(mb_acks[nbin][2]) if succ] )

