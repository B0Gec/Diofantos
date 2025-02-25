import pandas as pd

from exact_ed import unnan

csv_filename = 'cores_test.csv'
# pd.read_csv(csv_filename, index_col=0).to_excel('data/oeis.xlsx')
df = pd.read_csv(csv_filename, index_col=0)
print(df)
ids = df.columns
print(ids)
urls = [f'https://oeis.org/{i}' for i in ids]
n_of_terms = [len(unnan(list(df[i]))) for i in ids]
length_col_name = 'length (# available seq members leq 200)'

newcols = ['sequence ID', 'URL', length_col_name, 'cathegory (trivial/exists/none)', 'ground truth', 'Diofantos', 'SINDy']
outdf = pd.DataFrame(columns=newcols, index=None , data={'sequence ID': ids, 'URL': urls, length_col_name: n_of_terms})
# outdf.to_csv('ground_truth2.csv', index=None)
# print(outdf)

print(urls[0])
