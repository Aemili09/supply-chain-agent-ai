import polars as pl
import pandera.polars as pa


schema = pa.DataFrameSchema({
    "event_date": pa.Column(pl.Date, required=True),
    "DocumentIdentifier": pa.Column(pl.Utf8, required=True),
    "V2Locations": pa.Column(pl.Utf8, nullable=True),
    "sentiment_score": pa.Column(pl.Float64, pa.Check.in_range(-100.0, 100.0))
})

def validate_and_save(df: pl.DataFrame) -> str:
    """Validates data against the contract and writes to Delta Lake."""
    try:
        
        validated_df = schema.validate(df)
        
        
        validated_df.write_delta(
            "data/silver_layer", 
            mode="overwrite"
        )
        return "Success: Data passed contract and saved to Delta Lake."
    except pa.errors.SchemaError as e:
        return f"Pipeline Failed: Data Contract Violation - {e}"