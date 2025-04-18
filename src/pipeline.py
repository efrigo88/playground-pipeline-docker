import pandas as pd
from client import JSONPlaceholderClient
from db import PostgresManager
from logger import get_logger

logger = get_logger(__name__)


def transform_albums(raw_path: str) -> pd.DataFrame:
    """Transform raw albums data into a processed DataFrame.

    Args:
        raw_path: Path to the raw JSON data

    Returns:
        DataFrame: Processed DataFrame with transformed data
    """
    # Read JSON into DataFrame
    df = pd.read_json(raw_path)

    # Define column mappings and data types
    column_mappings = {
        "userId": "user_id",
        "id": "album_id",
        "title": "album_title",
    }

    # Convert data types
    df = df.astype({"userId": "int32", "id": "int32", "title": "string"})

    # Rename columns
    df = df.rename(columns=column_mappings)

    # Add ingestion timestamp
    df["ingestion_timestamp"] = pd.Timestamp.now()

    # Reorder columns
    df = df[["album_id", "user_id", "album_title", "ingestion_timestamp"]]

    return df


def run_pipeline():
    """Run the data processing pipeline."""
    try:
        # Initialize database manager
        db_manager = PostgresManager()

        # Get data from JSONPlaceholder API
        api_client = JSONPlaceholderClient()
        albums_data = api_client.get_albums()
        logger.info("Successfully fetched %d albums", len(albums_data))

        # Save raw data
        raw_path = "data/warehouse/raw/albums.json"
        api_client.save_albums(albums_data, raw_path)

        # Transform data
        bronze_df = transform_albums(raw_path)

        # Save the curated file in bronze layer
        bronze_path = "data/warehouse/bronze/albums.json"
        bronze_df.to_json(
            bronze_path, orient="records", force_ascii=False, indent=2
        )

        # Create PostgreSQL table if it doesn't exist
        db_manager.create_albums_table()

        # Save to PostgreSQL
        db_manager.save_dataframe_to_postgres(bronze_df, "albums")

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.error("Pipeline failed: %s", str(e))
        raise
