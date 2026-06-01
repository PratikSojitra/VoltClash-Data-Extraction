import numpy as np
import pandas as pd



coc_data = pd.read_csv('data/defenses.csv')

group_by_cat = coc_data.groupby(['Category', 'Required Town Hall'])

for key, value in group_by_cat:
    print(key)
    print(value)
    print("\n")

