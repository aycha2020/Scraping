import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


df= pd.read_csv(r"C:\Users\user\Desktop\scraping\scraped_data.csv", encoding="utf-8-sig") 

df["prix"].skew()

import numpy as np

df["prix_log"] = np.log1p(df["prix"])

sns.histplot(df["prix_log"],kde= True , bins=50)
plt.show()

Q1 = df["prix"].quantile(0.25)
Q3 = df["prix"].quantile(0.75)
IQR = Q3 - Q1

borne_sup = Q3 + 1.5 * IQR

df["prix"] = df["prix"].clip(upper=borne_sup)

df.sort_values(by="prix", ascending=False).head(10)