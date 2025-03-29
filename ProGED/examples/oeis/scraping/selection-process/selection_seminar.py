# from save_new_bfiles import bseqs
# from saved_new_bfile2 import bseqs
from saved_new_bfile10000 import bseqs
from selection import basic_info, select, less_len, display_them


# if __name__ == "__main__":
#     # execute only if run as a script

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

# print('\n'*10)
# float_limit = 1e10
float_limit = 1e16
# small3600 = select(bseqs, head_length=3580, has_titles=1, float_limit=float_limit)
small = select(bseqs, head_length=1000, has_titles=1, float_limit=float_limit)
# small79 = select(bseqs, head_length=79, has_titles=1, float_limit=float_limit)
print('A000045' in small)
print("selected:")
print("\nbasic_info(1000):")
basic_info(small, display_len=20)
display_len = 30
inter = set(mag_selection).intersection(small)
print('intersection 1000',  len(inter), 'of', len(mag_selection), inter)

# 1/0
# print('\n'*20)

# sorted_seqs = sorted([(i, seq) for i, seq in small.items()], key=(lambda x: x[0]))
# # print(sorted_seqs)
# for pair in sorted_seqs:
#     print('')
# #     print(i)
# #     print(max(seq[1:]), seq[0], seq[1:50])
#     print(pair[0])
#     print(pair[1][0])
#     print(max(pair[1][1:50]), pair[1][1:50])

print(len(small))
