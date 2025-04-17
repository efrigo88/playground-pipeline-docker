import os

import psycopg2
from psycopg2.extras import execute_values
from pyspark.sql import DataFrame
from dotenv import load_dotenv

from logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class PostgresManager:
    """Manager for PostgreSQL database operations."""

    def __init__(self):
        """Initialize the PostgresManager with connection parameters."""
        self.conn_params = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME"),
        }

    def create_albums_table(self):
        """Create the albums table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS albums (
            user_id INTEGER,
            id INTEGER,
            title TEXT,
            ingestion_timestamp TIMESTAMP
        )
        """
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(create_table_query)
                    conn.commit()
            logger.info("Albums table created or already exists")
        except Exception as e:
            logger.error("Failed to create albums table: %s", str(e))
            raise

    def save_dataframe_to_postgres(self, df: DataFrame, table_name: str):
        """Save a Spark DataFrame to PostgreSQL.

        Args:
            df: Spark DataFrame to save
            table_name: Name of the target table
        """
        try:
            # Convert Spark DataFrame to list of tuples
            data = df.collect()
            records = [
                (row.user_id, row.id, row.title, row.ingestion_timestamp)
                for row in data
            ]

            # Insert data into PostgreSQL
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    execute_values(
                        cur,
                        (
                            f"INSERT INTO {table_name} "
                            "(user_id, id, title, "
                            "ingestion_timestamp) VALUES %s"
                        ),
                        records,
                    )
                    conn.commit()
            logger.info(
                "Successfully saved %d records to %s", len(records), table_name
            )
        except Exception as e:
            logger.error("Failed to save data to PostgreSQL: %s", str(e))
            raise
