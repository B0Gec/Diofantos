txt = """# Greetings from The On-Line Encyclopedia of Integer Sequences! http://oeis.org/
Search: keyword:core
Showing 1-10 of 178
%I A000040 M0652 N0241
%S A000040 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,
%T A000040 97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,
%U A000040 181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271
%N A000040 The prime numbers.
%C A000040 See A065091 for comments, formulas etc. concerning only odd primes. For all information concerning prime powers, see A000961. For contributions concerning "almost primes" see A002808.
"""
from urllib import request
import re
import time


def bfile2list(id_: str, max_seq_length: int) -> list:
    """Fetch b-file and return list."""

    # max_read_url = (2+3+16+2) * max_seq_length
    max_read_url = 10 * (2+3+28+2) * max_seq_length
    # print(f'max_read_url: {max_read_url}')
    baddress = id_ + '/b' + id_[1:] +'.txt'
    print(baddress)
    # Make sure to read only *max_read_url* characters from URL.
    bfile = request.urlopen('https://oeis.org/'+baddress).read(max_read_url).decode()
    # new_seq_str = re.findall(r"\d+[ \t]+(-?\d+)\n", bfile)
    new_seq_str = re.findall(r"\d+[ \t]+(-?\d+)[ \t]?\n", bfile)
    # new_seq_str = re.findall(r"\d+([^b]{1,10}-?\d+)\n", bfile)
    # Make sure to take only first *max_seq_length* terms of sequence.
    new_seq = [int(term) for term in new_seq_str[:max_seq_length]]
    return new_seq
    # return new_seq_str

def variable2file(variable, variable_name, filename) -> None:
    """Write variable to file using repr function."""

    file = open(filename, "w")
    file.write(variable_name + " = " + repr(variable) + "\n")
    file.close()
    print(f"Variable named {variable_name} was written into "
          f"the file {filename}.")
    return

def new_fetch (start=0, end=1e10, do_write=False, max_seq_length=100, output_file="save_new_bfiles.py"):
    """Fetch all sequences from b-files."""

    # 0.) Check, if possible to write to file
    if do_write:
        variable2file({}, "empty_set", output_file)

    # 1.) First fetch total number of sequences do download.
    search=request.urlopen(
        'https://oeis.org/search?q=keyword%3acore'
        + '%20keyword%3anice%20-keyword%3amore&start=10&fmt=data')
    header_length = 5000  # number of characters in header.
    # import header as header_module
    header = search.read(header_length).decode()
    # print(header)
    total = int(re.findall(
        "Displaying \d+-\d+ of (\d+) results found.", header)[0])
    print(total)

    # 2.) Next, fly through pages to download 10 b-files at once.
    cropped = min(total, end)
    beginning = max(0, cropped-start)
    number_of_sequences = beginning
    print(f"total number of sequences found: {total}\n"
        f"start: {start}, end: {end}, "
        f"sequences of intersection:{number_of_sequences}")
    seqs = {}
    for i_ten in range((number_of_sequences-1)//10+1):  # 178->10-20...160-170
        print(i_ten)
        search = request.urlopen(
            f'https://oeis.org/search?q=keyword:core%20keyword:nice'
            f'%20-keyword:more&fmt=data&start={start+i_ten*10}')
        print(i_ten, "after wget")
        page = search.read().decode()
        # fmt=data returns: <a href="/A226898">A226898</a>
        # ten_ids = re.findall(r">(A\d{6})<", page)
        ten_ids = re.findall(r"<a href=\"/(A\d{6})\">A\d{6}</a>", page)
        # ten_ids = re.findall(r"<a href=\"/(\d{6})\">\d{6}</a>", page)
        ten_seqs = {id_: bfile2list(id_, max_seq_length) for id_ in ten_ids}
        # ten_seqs = {id_: header_module.header(id_)
        #                 + bfile2list(id_, max_seq_length) for id_ in ten_ids}
        seqs.update(ten_seqs)
    
    # 3.) Write sequences into file if need be:
    if do_write:
        variable2file(seqs, "bseqs", output_file)

    return seqs


new_fetch()
# new_fetch(do_write=True)
# new_fetch(start=10, end=24, do_write=False, max_seq_length=55, output_file=None)
# new_fetch(start=0, end=1e10, do_write=True, max_seq_length=1000, output_file="saved_new_bfile2.py")
# new_fetch(start=0, end=1e10, do_write=True, max_seq_length=10000, output_file="saved_new_bfile10000.py")

def fetch_old(start=0, end=1e10, do_write=False):
    search=request.urlopen('https://oeis.org/search?q=keyword:core%20keyword:nice&fmt=text')
    header_length = 1500  # number of characters in header
    header = search.read(header_length).decode()
    print(header)
    print('time of fetch():', time.perf_counter()-starting_time)
    total = int(re.findall("Search: .+\nShowing \d+-\d+ of (\d+)\n", header)[0])
    print(total)
    seqs = []
    # number_of_sequences = 30  # ... test
    cropped = min(total, end)
    beginning = max(0, cropped-start)
    number_of_sequences = beginning
    print(f"total number of sequences found: {total}\n"
        f"start: {start}, end: {end}, "
        f"sequences of intersection:{number_of_sequences}")

    for i in range((number_of_sequences-1)//10+1):  # 178 -> 10-20, 20-30, ..., 170-180
        # print(i)
        search=request.urlopen(
            f'https://oeis.org/search?q=keyword:core%20keyword:nice&fmt=text&start={start+i*10}')
        print(i, "after wget")
        page = search.read().decode()
        # print(i, "after decode")
        stu_lines = re.findall(
            r"%S (A\d{6}) (.+)\n(%T A\d{6} (.*)\n)*(%U A\d{6} (.*)\n)*", page)
        # ten_seqs = [(seq[0], seq[1]+seq[3]+seq[5]) for seq in stu_lines]
        ten_seqs = [(seq[0], [int(a_n) for a_n in (seq[1]+seq[3]+seq[5]).split(",")])
            for seq in stu_lines]
        # print(ten_seqs)
        if len(ten_seqs)<10: print("\n\n\n less than 10 !!!!\n\n\n")
        print(len(ten_seqs))
        seqs += [ten_seqs]
        # print(i, "after regex ")
        
    seqs_flatten = []
    for ten_seq in seqs:
        seqs_flatten += ten_seq
    print("all seqs:", len(seqs_flatten))
    if do_write:
        file = open("../selection-process/saved_core.py", "w")
        file.write("core_list = " + repr(seqs_flatten) + "\n"
                + "core_unflatten = " + repr(seqs) + "\n")
        file.close()
    print("fetch ended")
    return
# fetch_old(130, 190)
# fetch_old()
# print("end of fetch")


## -- download b-files via saved sequences -- ##
# import saved_core
# seqs = saved_core.core_list
# seqs_unflatten = saved_core.core_unflatten
# dict_seqs = dict(seqs)
# print(seqs[0])

def fetch_bfiles_old(start=0, end=180, do_write=True, max_seq_length=100):
    """Download extended sequences from bfiles of all sequences."""

    counter = start
    new_seqs ={}
    for id in list(dict_seqs)[start:end]:
        baddress = id + '/b' + id[1:] +'.txt'
        print(baddress)
        bfile = request.urlopen('https://oeis.org/'+baddress).read().decode()
        # new_seq = re.findall("(\d+) (\d+)\n", bfile)
        new_seq_check = re.findall(r"(\d+)([ \t]+)(-?\d+)\n", bfile)  # with a ^ 
        first_findall = new_seq_check[0]
        # print("first findall:", first_findall)
        first_space = first_findall[1]
        if len(first_space) > 1:
            print("\"" + first_space + '\"', len(first_space))
        first_index = first_findall[0]
        legal = ('-1', '0', '1')
        if first_index in legal:
            # print("all is well, really")
            pass
        else:
            print(f"first index is not in {legal}:", first_index)
        new_seq = [triple[2] for triple in new_seq_check[:max_seq_length]]
        # print(new_seq)
        new_seqs[id] = [int(term) for term in new_seq]
        # print(new_seqs[id])
        # print("len of new seq", len(new_seqs[id]))
        counter += 1
        if (counter%10) == 0: print(counter)

    print("all bfiled seqs:", len(new_seqs), "all original seqs:", len(dict_seqs))
    if do_write:
        file = open("../selection-process/saved_bfiled.py", "w")
        file.write("core_bfiled_dict = " + repr(new_seqs) + "\n")
        file.close()
        print("Sequences \"as are\" are written into the output file.")
    print("fetch of b-files ended")
    return
# fetch_bfiles_old(130, 140, do_write=False)
# fetch_bfiles(do_write=False)
# fetch_bfiles(80, 180, do_write=False)
# fetch_bfiles(do_write=False)
# fetch_bfiles(80, 90)
# fetch_bfiles()
