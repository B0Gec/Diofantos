
from save_new_bfiles import bseqs
# Selection begins with select small (or 2 lines before).
# New download:
from saved_new_bfile2 import bseqs
from saved_new_bfile10000 import bseqs
from selection import basic_info, select, less_len, display_them

# def abs_max(seq):
#     return max([abs(term) for term in seq])
# def power_order(number):
#     bigger = [order for order in range(-100, 100) if number > 10**order]
#     return bigger[-1]

# def basic_info(seqs, has_titles: int = 1, display_len: int = 100, float_limit=1e16):
#     """Print basic info of the dataset."""
#     print("number of all seqs:", len(seqs))
#     lens = [len(seqs[id_][has_titles:]) for id_ in seqs]
#     # len_tuples = [(id_, len(seqs[id_][has_titles:])) for id_ in seqs]
#     maxs = [abs_max(seq[has_titles:]) for id_, seq in seqs.items()]

#     # max_tuples = [(id_, abs_max(seq[has_titles:])) for id_, seq in seqs.items()]
#     # min_len_index = lens.index(min(lens))
#     # min_len_seq = seqs[min_len_index]
#     # print(min_len_seq)

#     print("min, max number of terms in seqs:", min(lens), max(lens))
#     print(f"max({float_limit} limit) absolute value in seqs:",
#           f"10e{power_order(max(maxs))}")
#          # f"{max(maxs):e}")
#     # print(lens)  # print(maxs) too big to print
#     print("first two sequences:", [(i, seqs[i][:display_len]) for i in list(seqs)[:2]])
#     return
# # basic_info(bseqs)
# # basic_info(bseqs, has_titles=1, display_len=100)
# # 1/0

# def display_them(seqs, has_titles: int = 1, display_len: int = 100):
#     sorted_seqs = sorted([(i, seq) for i, seq in small.items()], key=(lambda x: x[0]))
#     for pair in sorted_seqs:
#         print('')
#         print(pair[0])
#         print(pair[1][0])
#         print(max(pair[1][1:50]), pair[1][1:50])

#     return

# def less_len(seqs, max_len=100, has_titles=1):
#     """Make sure, which sequences have less than 100 terms. 
#     Also see their max value.
#     """
#     less = [(id_, len(seqs[id_][has_titles:])) for id_ in seqs if len(seqs[id_])<max_len]
#     def key_fun (i):
#         return i[1]
#     less.sort(key=key_fun)
#     print(f"number of seqs with less than {max_len} terms:", len(less))
#     # print("all seqs with less than 100 terms:", less)
#     print(f"all seqs with less than {max_len} terms, printed with their:\n"
#         "        bfile url         | len | max ")
#     for id_, j in less:
#         maxi = max([abs(term) for term in bseqs[id_][has_titles:]])
#         max_str = 1e16 if maxi>1e16 else float(maxi)
#         print("oeis.org/" + id_ + '/b' + id_[1:] + '.txt', j, max_str)
#         # if id in more:
#         #     print(f"but {id} is in more, so ...")
#     return
# # less_len(bseqs)

# def print_big(seqs):
#     """Mostly useless."""
#     maxs = [abs_max(seq) for _id, seq in seqs.items()]
#     avoid_overflow = [1e16 if maxi>1e16 else float(maxi) for maxi in maxs]
#     print(avoid_overflow)
#     return
# # print_big(bseqs)


# ### start selection ###
# # def abs_max(seq):
# #     return max([abs(term) for term in seq])

# # remove Mersene seq:
# # bseqs.pop('A000043')

# def select(seqs: dict, 
#             head_length=1000, 
#             float_limit=1e16, 
#             has_titles=0):
#     small = {id_: seq[:head_length+has_titles] for id_, seq in seqs.items() 
#             if abs_max(seq[has_titles:head_length+has_titles]) < float_limit 
#                 and len(seq[has_titles:head_length+has_titles]) >= head_length}
#     return small
# # small = select(bseqs)

if __name__ == "__main__":
    # execute only if run as a script

    mag_selection = (
            "A000009", 
            "A000040", 
            "A000045", 
            "A000124", 
            # "A000108", 
            "A000219", 
            "A000292", 
            "A000720", 
            "A001045", 
            "A001097", 
            "A001481", 
            "A001615", 
            "A002572", 
            "A005230", 
            "A027642", 
            )
    # filter accordingly only first 100 terms:
    # small = select(bseqs, head_length=100)
    # small = select(bseqs, head_length=50)

    # basic_info(bseqs)
    # less_len(bseqs, max_len=500)
    # 1/0

    # 1/0
    # small = select(bseqs, head_length=10, has_titles=1)
    # small = select(bseqs, head_length=1000, has_titles=1)
    # print('\n'*10)
    float_limit = 1e10
    float_limit = 1e16
    small3600 = select(bseqs, head_length=3580, has_titles=1, float_limit=float_limit)
    small = select(bseqs, head_length=1000, has_titles=1, float_limit=float_limit)
    small79 = select(bseqs, head_length=79, has_titles=1, float_limit=float_limit)
    print('A000045' in small)
    # print('small', small)
    print("selected:")
    print("\nbasic_info(1000):")
    basic_info(small, display_len=20)
    print("\nbasic_info(79):")
    basic_info(small79, display_len=20)
    print("\nbasic_info(3600):")
    basic_info(small3600, display_len=20)
    # less_len(small, max_len=1000)
    display_len = 30
    # display_them(small)
    inter = set(mag_selection).intersection(small)
    inter79 = set(mag_selection).intersection(small79)
    inter3600 = set(mag_selection).intersection(small3600)
    print('intersection 1000',  len(inter), 'of', len(mag_selection), inter)
    print('intersection 79',  len(inter79), 'of', len(mag_selection), inter79)
    print('intersection 3600',  len(inter3600), 'of', len(mag_selection), inter3600)
    print('diff 1000 vs 79', inter.symmetric_difference(inter79))
    print('diff 3600 vs 79', inter3600.symmetric_difference(inter79))
    print('Result: not meaning loss in interesting sequences from 1000 to 3600')
    print('rule of thumb: 10x more examples (samples) in dataset than features, ergo take 1000')

    



    1/0
    # print('\n'*20)


    sorted_seqs = sorted([(i, seq) for i, seq in small.items()], key=(lambda x: x[0]))
    # print(sorted_seqs)
    for pair in sorted_seqs:
        print('')
    #     print(i)
    #     print(max(seq[1:]), seq[0], seq[1:50])
        print(pair[0])
        print(pair[1][0])
        print(max(pair[1][1:50]), pair[1][1:50])

    # 1/0

    # for i, seq in small.items():
    #     print('')
    #     print(i)
    #     print(max(seq[1:]), seq[0], seq[1:50])
    1/0
    bseqs.pop('A000043')
    small = select(bseqs, head_length=1000, has_titles=1)
    print('\n'*10, 'just popped')
    basic_info(small, display_len=20)
    print(len(small))
    # print(small.popitem())
    
# For use outside of this file.
# final_selection = select(bseqs)







### Answer by bfiles_old: in dataset we keep: 
###     *keyword:core keyword:nice 
###     * and delete all sequences with absolute terms > 1e16.
###     * and delete sequence Mersene A000043, since only 47 terms (in hard keyword)
###             because we need at least 47 or should I say 100 terms (as it turns out).
###     ** it turns out all other remaining sequences in core have at least 100 terms. Very good.
