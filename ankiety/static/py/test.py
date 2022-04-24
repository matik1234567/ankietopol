import pandas as pd

d = [2.0, 5.3, [2.8, 3.0]]
df = pd.Series(data=d)
print (df)

df = df.explode()
print (df)
