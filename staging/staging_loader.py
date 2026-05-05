import os
import pandas as pd

def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "scraped_data.csv")

    df = pd.read_csv(file_path, encoding="utf-8-sig")
    return df