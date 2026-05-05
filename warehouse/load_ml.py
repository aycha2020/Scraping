from sqlalchemy import create_engine

engine = create_engine("postgresql://admin:admin@localhost:5432/avito")

def load_ml(df):

    df_ml = df[[
        "prix",
        "surface",
        "prix_m2",
        "ville",
        "quartier",
        "chambres",
        "salles_bain",
        "age_bien"
    ]]

    df_ml.to_sql("dataset_ml", engine, schema="ml_schema", if_exists="append", index=False)

    print("ML dataset loaded")