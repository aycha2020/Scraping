import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clean.clean_data import clean_data 


from clean import clean_data
from features.feature_engineering import feature_engineering
from warehouse.load_bi import load_bi
from warehouse.load_ml import load_ml




from staging.staging_loader import load_data
from clean.clean_data import clean_data

def run_pipeline():
    df = load_data()
    df = clean_data(df)
    return df

if __name__ == "__main__":
    run_pipeline()

def run_pipeline():
    df = load_data()      
    df = clean_data(df)   
    return df

def run_pipeline():
    df = clean_data()  
    df = feature_engineering(df) 
    return df


if __name__ == "__main__":
    run_pipeline()



logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():
    try:
        logging.info("Pipeline started")
        

      

        # 2. TRANSFORM / FEATURES
        logging.info(" Feature engineering...")
        df = feature_engineering(df)

        # 3. LOAD BI
        logging.info("Loading BI schema...")
        load_bi(df)

        # 4. LOAD ML
        logging.info("Loading ML table...")
        load_ml(df)

        logging.info("Pipeline finished successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_pipeline()

    import os
print(os.getcwd())
print(os.listdir())

