import pandas as pd
from download import new_fetch
# from saved_catalan import a
# from saved_catalan import bseqs
# print(a)
# print(bseqs)
# print(type(bseqs))
# bseqs = new_fetch(0, 1, do_write=False, max_seq_length=50)  # = default length

# for i in bseqs:
#     # print(i, bseqs[i], type(bseqs[i]))
#     print(i, len(bseqs[i]))

# a = [1,2,3,4]
# f = open("saved_catalan.py", 'w')
# # f.write("a = "+ repr(bseqs))
# f.write("\nbseqs = "+ repr(bseqs))
# f.close()
# print(a)
# import
# f = open("saved_catalan.py", 'r')
# b = f.read()
# f.close()
# print(b)



# df = pd.DataFrame(bseqs)
# df_sorted = df.sort_index(axis=1)
# # print(df_sorted.head())
csv_filename_cata = "catalan_selection.csv"
csv_filename = "oeis_selection.csv"
# df_sorted.to_csv(csv_filename, index=False)

# # after download:
# cata = pd.read_csv(csv_filename_cata)
check = pd.read_csv(csv_filename)
# check['A000108'] = cata['A000108']
# df_sorted = check.sort_index(axis=1)
# df_sorted.to_csv(csv_filename, index=False)
print("Read file from csv:")
# print(check)
for i in list(check['A000108'][1:23]):
    print(i)
from check_download import check_out
check_out(csv_filename=csv_filename)

## Add new seq into old csv:
print(check)
print(check['A000108'])
