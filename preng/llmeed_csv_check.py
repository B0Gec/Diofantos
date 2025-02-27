import pandas as pd
df = pd.read_csv('linrec_and_dasco.csv', low_memory=False)
dfb = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
print(df)
print(dfb)

