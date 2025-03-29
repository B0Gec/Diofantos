import pandas as pd
# from selection import basic_info
# from selection import final_selection

# # From zero:
# # 1.) first download all (core,nice,-more) into dictionary
# from download import new_fetch
# bseqs = new_fetch(do_write=False, max_seq_length=50)  # = default length
# # bseqs = new_fetch(0, 3, do_write=False, max_seq_length=50)  # = default length
# # or equivalently load already downloaded:
from saved_new_bfile10000 import bseqs
# # 2.) remove Mersene seq:
# bseqs.pop('A000043')
# # bseqs.pop('A000043', None)
# # 3.) select small:
from selection import select
seqs = select(bseqs, head_length=1000, has_titles=1, float_limit=1e16)

# # Then header, body. 
df = pd.DataFrame(seqs)
df_sorted = df.sort_index(axis=1)
print(df_sorted.head())
# csv_filename = "oeis_selection.csv"  # Masters
csv_filename = "oeis_dmkd.csv"
# df_sorted.to_csv(csv_filename, index=False)

# # after download:
check = pd.read_csv(csv_filename)
print("Read file from csv:")
print(check)
# 1/0

selection = (
        # "A000009", 
        "A000040", 
        # "A000045", 
        "A000124", 
        # "A000108", 
        # "A000219", 
        "A000292", 
        "A000720", 
        # "A001045", 
        "A001097", 
        "A001481", 
        "A001615", 
        # "A002572", 
        # "A005230", 
        # "A027642", 
        )

for i in selection:
    biggys = list(check[i][1:])[-4:]
    # print(biggys[-1]*10**16))
    # print( f"{1234567890123456789012345:e}")
    print(i)
    print( f"{int(biggys[-1]):e}")
    # print(float(biggys[-1]*10**16)/10**16)
# print(check[list(selection)][20])
# seq = check[selection[0]]
# print(list(seq[1:])[-9:])
