import pandas as pd
import numpy as np

# 1. LOAD DATA
df = pd.read_csv(r"C:\Users\user\Desktop\scraping\data\scraped_data.csv", encoding="utf-8-sig")

def clean_data(df):

    df["prix"] = (
        df["prix"]
        .astype(str)
        .str.replace("DH", "", regex=False)
        .str.replace("\u202f", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    df["prix"] = pd.to_numeric(df["prix"], errors="coerce")

    df = df.dropna(subset=["prix"])

    return df

# 3. CLEAN SURFACE

df["surface"] = (
    df["surface"]
    .astype(str)
    .str.extract(r"(\d+\.?\d*)")[0]
    .astype(float)
)


# 4. CLEAN CHAMBRES & SALLE DE BAIN

df["chambres"] = df["chambres"].astype(str).str.extract(r"(\d+)")[0].astype(float)
df["salle_de_bain"] = df["salle_de_bain"].astype(str).str.extract(r"(\d+)")[0].astype(float)


# 5. CLEAN VILLE

df["ville"] = df["ville"].astype(str).str.split(",").str[0]
df["ville"] = df["ville"].astype("category")


# 6. REMOVE OUTLIERS (PRIX)

q_low = df["prix"].quantile(0.01)
q_high = df["prix"].quantile(0.99)

df = df[(df["prix"] >= q_low) & (df["prix"] <= q_high)]


# 7. FEATURE ENGINEERING

df["prix_log"] = np.log1p(df["prix"])

df["prix_par_m2"] = df["prix"] / df["surface"]


# 8. DROP MISSING IMPORTANT DATA

df = df.dropna(subset=["prix", "surface"])


# 9. RESET INDEX

df = df.reset_index(drop=True)


# 10. SAVE CLEAN DATA

df.to_csv(r"C:\Users\user\Desktop\scraping\cleaned_data.csv", index=False, encoding="utf-8-sig")
print(df["prix"].dtype)