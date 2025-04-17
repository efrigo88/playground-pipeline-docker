from dotenv import load_dotenv
import pyspark.sql.functions as F
import pyspark.sql.types as T

from session import create_spark_session
from api import JSONPlaceholderClient
from db import PostgresManager
from logger import get_logger

logger = get_logger(__name__)


def transform_albums(spark, raw_path):
    """Transform raw albums data into a processed DataFrame.

    Args:
        spark: SparkSession instance
        raw_path: Path to the raw JSON data

    Returns:
        DataFrame: Processed DataFrame with transformed data
    """
    # Define schema for the albums data
    schema = T.ArrayType(
        T.StructType(
            [
                T.StructField("userId", T.IntegerType(), False),
                T.StructField("id", T.IntegerType(), False),
                T.StructField("title", T.StringType(), False),
            ]
        )
    )

    # Read JSON into DataFrame
    # Using multiLine=True since the JSON is a single array
    df = (
        spark.read.option("multiLine", True)
        .schema(schema)
        .json(raw_path)
        .select("element.*")
    )  # Flatten the array structure

    # Add ingestion timestamp and rename columns
    return df.withColumn(
        "ingestion_timestamp", F.current_timestamp()
    ).withColumnRenamed(
        "userId", "user_id"
    )  # Rename to match PostgreSQL naming convention


def main():
    """Main function to run the data processing pipeline."""
    try:
        # Load environment variables
        load_dotenv()

        # Initialize Spark session
        spark = create_spark_session()

        # Initialize database manager
        db_manager = PostgresManager()

        # Get data from JSONPlaceholder API
        api_client = JSONPlaceholderClient()
        albums_data = api_client.get_albums()
        logger.info("Successfully fetched %d albums", len(albums_data))

        # Save raw data
        raw_path = "data/raw/albums.json"
        api_client.save_albums(albums_data, raw_path)

        # Transform data
        bronze_df = transform_albums(spark, raw_path)

        # Save to Iceberg format
        logger.info("Saving to Iceberg format...")
        bronze_df.write.format("iceberg").mode("append").saveAsTable(
            "local.bronze.albums"
        )  # Updated to use the local catalog

        # Create PostgreSQL table if it doesn't exist
        db_manager.create_albums_table()

        # Save to PostgreSQL
        db_manager.save_dataframe_to_postgres(bronze_df, "albums")

        logger.info("Pipeline completed successfully!")

    except Exception as e:
        logger.error("Pipeline failed: %s", str(e))
        raise


if __name__ == "__main__":
    main()
