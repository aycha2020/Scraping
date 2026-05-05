import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:admin@localhost:5432/avito")

def load_bi(df):

    # 🔹 Dim Temps
    dim_temps = df[["date"]].copy()
    dim_temps["annee"] = pd.to_datetime(dim_temps["date"]).dt.year
    dim_temps["mois"] = pd.to_datetime(dim_temps["date"]).dt.month
    dim_temps = dim_temps.drop_duplicates()

    dim_temps.to_sql("dim_temps", engine, schema="bi_schema", if_exists="append", index=False)

    # 🔹 Dim Localisation
    dim_loc = df[["ville", "quartier"]].drop_duplicates()
    dim_loc.to_sql("dim_localisation", engine, schema="bi_schema", if_exists="append", index=False)

    # 🔹 Dim Caractéristiques
    dim_car = df[["surface", "chambres", "salles_bain"]].drop_duplicates()
    dim_car.to_sql("dim_caracteristiques", engine, schema="bi_schema", if_exists="append", index=False)

    print("BI loaded ")