# from save_new_bfiles import bseqs
# Selection begins with select() (or 2 lines before).
from saved_new_bfile10000 import bseqs

def abs_max(seq):
    return max([abs(term) for term in seq])
def power_order(number):
    bigger = [order for order in range(-100, 100) if number > 10**order]
    return bigger[-1]

def basic_info(seqs, has_titles: int = 1, display_len: int = 100, float_limit=1e16):
    """Print basic info of the dataset."""
    print("number of all seqs:", len(seqs))
    lens = [len(seqs[id_][has_titles:]) for id_ in seqs]
    # len_tuples = [(id_, len(seqs[id_][has_titles:])) for id_ in seqs]
    maxs = [abs_max(seq[has_titles:]) for id_, seq in seqs.items()]
    # max_tuples = [(id_, abs_max(seq[has_titles:])) for id_, seq in seqs.items()]
    # min_len_index = lens.index(min(lens))
    # min_len_seq = seqs[min_len_index]
    # print(min_len_seq)

    print("min, max number of terms in seqs:", min(lens), max(lens))
    print(f"max({float_limit} limit) absolute value in seqs:",
          f"10e{power_order(max(maxs))}")
         # f"{max(maxs):e}")
    # print(lens)  # print(maxs) too big to print
    print("first two sequences:", [(i, seqs[i][:display_len]) for i in list(seqs)[:2]])
    return
# basic_info(bseqs)
# basic_info(bseqs, has_titles=1, display_len=100)

def display_them(seqs, has_titles: int = 1, display_len: int = 100):
    sorted_seqs = sorted([(i, seq) for i, seq in small.items()], key=(lambda x: x[0]))
    for pair in sorted_seqs:
        print('')
        print(pair[0])
        print(pair[1][0])
        print(max(pair[1][1:50]), pair[1][1:50])

    return

def less_len(seqs, max_len=100, has_titles=1):
    """Make sure, which sequences have less than 100 terms. 
    Also see their max value.
    """
    less = [(id_, len(seqs[id_][has_titles:])) for id_ in seqs if len(seqs[id_])<max_len]
    def key_fun (i):
        return i[1]
    less.sort(key=key_fun)
    print(f"number of seqs with less than {max_len} terms:", len(less))
    # print("all seqs with less than 100 terms:", less)
    print(f"all seqs with less than {max_len} terms, printed with their:\n"
        "        bfile url         | len | max ")
    for id_, j in less:
        maxi = max([abs(term) for term in bseqs[id_][has_titles:]])
        max_str = 1e16 if maxi>1e16 else float(maxi)
        print("oeis.org/" + id_ + '/b' + id_[1:] + '.txt', j, max_str)
        # if id in more:
        #     print(f"but {id} is in more, so ...")
    return
# less_len(bseqs)

def print_big(seqs):
    """Mostly useless."""
    maxs = [abs_max(seq) for _id, seq in seqs.items()]
    avoid_overflow = [1e16 if maxi>1e16 else float(maxi) for maxi in maxs]
    print(avoid_overflow)
    return
# print_big(bseqs)


### start selection ###
# def abs_max(seq):
#     return max([abs(term) for term in seq])

# remove Mersene seq:
# bseqs.pop('A000043')

def select(seqs: dict,
            head_length=1000,
            float_limit=1e16,
            has_titles=0):
    small = {id_: seq[:head_length+has_titles] for id_, seq in seqs.items()
            if abs_max(seq[has_titles:head_length+has_titles]) < float_limit
                and len(seq[has_titles:head_length+has_titles]) >= head_length}
    return small
# small = select(bseqs)

if __name__ == "__main__":
    # execute only if run as a script

    # dmkd:
    small = select(bseqs, head_length=1000, has_titles=1, float_limit=1e16)
    print('A000045' in small)
    print("selected:")
    print("\nbasic_info(1000):")
    basic_info(small, display_len=20)
    print(len(small))
    # EOf dmkd:

    # # Masters
    # # filter accordingly only first 100 terms:
    # small = select(bseqs, head_length=100)
    # print("selected:")
    # basic_info(small)
    # print(len(small), small.popitem())
    # # end of Masters
    
# For use outside of this file.
# final_selection = select(bseqs)







### Answer by bfiles_old: in dataset we keep: 
###     *keyword:core keyword:nice 
###     * and delete all sequences with absolute terms > 1e16.
###     * and delete sequence Mersene A000043, since only 47 terms (in hard keyword)
###             because we need at least 47 or should I say 100 terms (as it turns out).
###     ** it turns out all other remaining sequences in core have at least 100 terms. Very good.
