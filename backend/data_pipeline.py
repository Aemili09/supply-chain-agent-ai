from google.cloud import bigquery
import aisdb
from syda import SyntheticDataGenerator, ModelConfig
import polars as pl

def fetch_gdelt_risk():
    client = bigquery.Client()
    query = """
    SELECT V2Themes, V2Locations, SOURCEURL 
    FROM `gdelt-bq.gdeltv2.gkg` 
    WHERE DATE > 20260201000000 AND V2Themes LIKE '%SUPPLY_CHAIN%' 
    LIMIT 100
    """
    return client.query(query).to_dataframe()

def init_ais_db():
    aisdb.sqlite.create_db_table("vessels.db")
    return "AIS database initialized"

def generate_synthetic_erp():
    generator = SyntheticDataGenerator(
        model_config=ModelConfig(provider="openai", model_name="gpt-4o")
    )
    schema = {
        'suppliers': {
            'id': {'type': 'number', 'primary_key': True},
            'name': {'type': 'text'},
            'risk_score': {'type': 'number'}
        }
    }
    return generator.generate(schema)