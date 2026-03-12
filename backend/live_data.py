from google.cloud import bigquery
import polars as pl

def fetch_gdelt_risk_data() -> pl.DataFrame:
    """Fetches live supply chain disruption data from GDELT 2.0 via BigQuery."""
    client = bigquery.Client()
    
    
    query = """
    SELECT
        PARSE_DATE('%Y%m%d', CAST(DATE AS STRING)) AS event_date,
        DocumentIdentifier,
        V2Locations,
        V2Themes,
        AvgTone as sentiment_score
    FROM `gdelt-bq.gdeltv2.gkg`
    WHERE DATE > 20260101000000 
    AND V2Themes LIKE '%ECON_SUPPLYCHAIN%'
    LIMIT 5000
    """
    
    query_job = client.query(query)
    
    
    df = pl.from_arrow(query_job.to_arrow())
    return df