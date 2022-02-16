import numpy as np
import pandas

dict = {
    "Model": ["Opel","Fiat","Ferrari"],
    "Rok": [2000,3000,4000]
}

df = pandas.DataFrame(dict)

# proba 1 failed
# for index,row in df.iterrows():
#     row["Kolor"] = index

arr = np.array([
    [0,1,2]
])

class D:
    def __init__(self,v):
        self.v = v

for i in range(len(df)):
    df.loc[i,"Kolor"] = D(arr)

print(df)
print("---")
print(df.loc[1,"Kolor"].v)
