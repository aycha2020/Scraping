# ============================================================
#  Avito.ma — Staging Loader
#  Layer : Staging
#  Charge le JSON brut dans la table staging de la DB
#  Usage : python staging_loader.py --file data/raw/avito_raw_*.json
# ============================================================

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"staging_{datetime.now():%Y%m%d_%H%M%S}.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  CONNEXION
# ─────────────────────────────────────────────
DB_USER     = os.getenv("DB_USER",     "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_PORT     = os.getenv("DB_PORT",     "5432")
DB_NAME     = os.getenv("DB_NAME",     "avito_dw")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True
)

# ─────────────────────────────────────────────
#  DDL — création de la table staging
# ─────────────────────────────────────────────
DDL_STAGING = """
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.annonces_raw (
    id               SERIAL PRIMARY KEY,
    titre            TEXT,
    prix             TEXT,
    ville            TEXT,
    quartier         TEXT,
    surface_m2       TEXT,
    nb_chambres      TEXT,
    nb_salles_bain   TEXT,
    etage            TEXT,
    annee_construction TEXT,
    type_bien        TEXT,
    lien             TEXT,
    date_scraping    TEXT,
    batch_id         TEXT,
    loaded_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_staging_lien     ON staging.annonces_raw(lien);
CREATE INDEX IF NOT EXISTS idx_staging_batch    ON staging.annonces_raw(batch_id);
CREATE INDEX IF NOT EXISTS idx_staging_loaded   ON staging.annonces_raw(loaded_at);
"""

def create_staging_table():
    with engine.begin() as conn:
        conn.execute(text(DDL_STAGING))
    log.info("Table staging.annonces_raw prête")


# ─────────────────────────────────────────────
#  CHARGEMENT
# ─────────────────────────────────────────────
def load_json_to_staging(json_path: Path) -> int:
    batch_id = f"batch_{datetime.now():%Y%m%d_%H%M%S}"

    with open(json_path, encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        log.warning(f"Fichier vide : {json_path}")
        return 0

    log.info(f"Chargement de {len(records)} enregistrements | batch: {batch_id}")

    insert_sql = text("""
        INSERT INTO staging.annonces_raw (
            titre, prix, ville, quartier, surface_m2,
            nb_chambres, nb_salles_bain, etage,
            annee_construction, type_bien, lien,
            date_scraping, batch_id
        ) VALUES (
            :titre, :prix, :ville, :quartier, :surface_m2,
            :nb_chambres, :nb_salles_bain, :etage,
            :annee_construction, :type_bien, :lien,
            :date_scraping, :batch_id
        )
        ON CONFLICT DO NOTHING
    """)

    loaded = 0
    with engine.begin() as conn:
        for rec in records:
            try:
                conn.execute(insert_sql, {**rec, "batch_id": batch_id})
                loaded += 1
            except Exception as e:
                log.warning(f"Erreur insertion : {e} | lien: {rec.get('lien')}")

    log.info(f"Chargés : {loaded}/{len(records)}")
    return loaded


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Staging loader Avito.ma")
    parser.add_argument("--file", required=True, help="Chemin vers le fichier JSON brut")
    args = parser.parse_args()

    create_staging_table()
    n = load_json_to_staging(Path(args.file))
    print(f"\n✅ {n} enregistrements chargés en staging")
