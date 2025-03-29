# from saved_bfiled import core_bfiled_dict as bseqs 
from save_new_bfiles import bseqs  #newer: from ProGED.example.oeis.scraping.save_new_bfiles import bseqs
## -- obsolete more deletion -- ##
# more = ("A000109", "A000112", "A000609", "A002106", "A003094", "A005470", "A006966")
# print("more:", ", ".join(more))
# ids_nomore = list(set(bseqs).difference(set(more)))
# print("number of nomore seqs:", len(ids_nomore))
# nomore = {id: bseqs[id] for id in ids_nomore}
# bseqs = nomore
## -- -- ##
def basic_info(bseqs):
    print("number of all seqs:", len(bseqs))
    lens = [len(bseqs[id]) for id in bseqs]
    print("min, max number of terms in seqs:", min(lens), max(lens))
    # print(lens)
    return
basic_info(bseqs)

less = [(id, len(bseqs[id])) for id in bseqs if len(bseqs[id])<100]
def key_fun (i):
    return i[1]
less.sort(key=key_fun)
print("number of seqs with less than 100 terms:", len(less))
print("all seqs with less than 100 terms:", less)
print("all seqs with less than 100 terms, printed with their:\n"
    "        bfile url         | len | max ")
for id, j in less:
    maxi = max([abs(term) for term in bseqs[id]])
    max_str = "1e16" if maxi>1e16 else float(maxi)
    print("oeis.org/" + id + '/b' + id[1:] + '.txt', j, max_str)
    # if id in more:
    #     print(f"but {id} is in more, so ...")

##### ---- left out (not finished): ---- #####
# less = [(id, len(bseqs[id])) for id in bseqs if len(bseqs[id])<100]
maxs = [max([abs(term) for term in seq]) for _id, seq in bseqs.items()]
# print(maxs)  # too big to print.
avoid_overflow = [1016 if maxi>1e16 else float(maxi) for maxi in maxs]
# print(avoid_overflow)
# 1/0
##### ----    ---- #####

# to generate Mersene oeis:
# from sympy import isprime, prime
# for n in range(1, 10**2*2*2*2):
#     if isprime(2**prime(n)-1):
#         print((n, prime(n)), end=', ')
# AnsMy: Mersene out (they are hard (keyword))

# # Are there more with enough terms? No! (max 47 terms)
# print(10**5-3)
# maxs = [max([abs(term) for term in bseqs[id]]) for id in more]
# lens = [len(bseqs[id]) for id in more]
# print(maxs)
# print(lens)
# print("id", "max", "len")
# for id in more:
#     # print("oeis.org/" + id + '/b' + id[1:] + '.txt', seq)
#     maxi = max([abs(term) for term in bseqs[id]])
#     leni = len(bseqs[id])
#     max_str = "1e16" if maxi>1e16 else float(maxi)
#     print(id, max_str, leni)
# # AnsMy: all more go out.


### Answer by this bfiles: in dataset we keep: 
###     *keyword:core keyword:nice 
###     * and delete all sequences with absolute terms > 1e16.
###     * and delete sequence Mersene A000043, since only 47 terms (in hard keyword)
###             because we need at least 47 or should I say 100 terms (as it turns out).
###     ** it turns out all other remaining sequences in core have at least 100 terms. Very good.
