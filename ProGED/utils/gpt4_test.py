import pandas as pd

coarsness = 'coarse'
dirn = f'dynobench/data/{coarsness}/vdp/'
# csvin = pd.read_csv(dirn + "data_vdp_len20_rate001_snrNone_init0.csv")
csvin = pd.read_csv(dirn + "data_vdp_len10_rate01_snrNone_init0.csv")
for i in range(3, 6):
    csv = csvin.round(i)
    csv.to_csv(dirn + f"rounded{i}.csv", index=False)
    print(csv)



