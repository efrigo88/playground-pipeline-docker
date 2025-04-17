import os

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
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
            album_id INTEGER,
            user_id INTEGER,
            album_title TEXT,
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

    def save_dataframe_to_postgres(self, df: pd.DataFrame, table_name: str):
        """Save a pandas DataFrame to PostgreSQL.

        Args:
            df: pandas DataFrame to save
            table_name: Name of the target table
        """
        try:
            # Convert DataFrame to list of tuples
            records = [tuple(x) for x in df.to_numpy()]

            # Insert data into PostgreSQL
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    execute_values(
                        cur,
                        (
                            f"INSERT INTO {table_name} "
                            "(album_id, user_id, album_title, "
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
