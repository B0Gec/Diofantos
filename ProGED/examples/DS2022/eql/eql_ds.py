import pandas as pd
import numpy as np
import ProGED as pg
from ProGED.examples.DS2022.generate_data_ODE_systems import generate_ODE_data, lorenz, VDP
import time
print(22)

print(3)

data = generate_ODE_data(lorenz, [0, 1, 1.05])
df = pd.DataFrame(data)
#### pd.DataFrame(data).to_csv('file.csv')
check = pd.read_csv('file.csv')


# dsa
print(check)





