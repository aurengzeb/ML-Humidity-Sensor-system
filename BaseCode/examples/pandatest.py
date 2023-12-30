import pandas as pd
import numpy as np
df = pd.read_excel('MetaData.xlsx')
print(df.columns)
A0 = df['A0']
A1 = df['A1']
A2 = df['A2']
A3 = df['A3']

A0P = A0.tolist()
A1P = A1.tolist()
A2P = A2.tolist()
A3P = A3.tolist()

datatotrain = []
for i in range(len(A0P)):
	datatotrain.append([A0P[i],A1P[i],A2P[i],A3P[i]])
print(datatotrain)

