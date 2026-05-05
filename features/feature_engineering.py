import pandas as pd
import numpy as np
from datetime import datetime


def feature_engineering(df):

    df = df.copy()

  
    # 1. BASIC CLEAN
   
    df = df.dropna(subset=["prix", "surface", "ville"])
    df = df[df["surface"] > 0]
    df = df[df["prix"] > 0]

   
    # 2. FEATURE CORE
   
    df["prix_par_m2"] = df["prix"] / df["surface"]


    # 3. GEO CLEAN
   
    df["ville"] = df["ville"].astype(str).str.strip().str.lower()

    if "quartier" in df.columns:
        df["quartier"] = df["quartier"].astype(str).str.strip().str.lower()

   
    # 4. MARKET FEATURES
    
    df["nb_annonces_ville"] = df.groupby("ville")["prix"].transform("count")

    if "quartier" in df.columns:
        df["nb_annonces_quartier"] = df.groupby("quartier")["prix"].transform("count")

   
    # 5. SEGMENTATION PRIX
    
    df["segment_prix"] = pd.qcut(
        df["prix"],
        q=3,
        labels=["low", "medium", "high"]
    )

   
    # 6. SEGMENTATION SURFACE
   
    df["segment_surface"] = pd.cut(
        df["surface"],
        bins=[0, 50, 100, 200, 1000],
        labels=["small", "medium", "large", "luxury"]
    )

   
    # 7. AGE BIEN (optional)
  
    if "annee_construction" in df.columns:
        current_year = datetime.now().year
        df["age_bien"] = current_year - df["annee_construction"]
        df["age_bien"] = df["age_bien"].clip(lower=0)

    
    # 8. OUTLIER FILTER (SAFE)

    df = df[df["prix"] < df["prix"].quantile(0.99)]
    df = df[df["surface"] < df["surface"].quantile(0.99)]

    
    # 9. FINAL CLEAN (SAFE)
  
    df = df.reset_index(drop=True)

    return df






