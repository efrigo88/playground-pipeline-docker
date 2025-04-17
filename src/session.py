import os
import logging
from pyspark.sql import SparkSession
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = get_logger(__name__)


def create_spark_session():
    """Create and configure a Spark session.

    Returns:
        SparkSession: Configured Spark session
    """
    logger.info("Creating Spark session...")
    try:
        warehouse_path = os.path.abspath("data/warehouse")
        return (
            SparkSession.builder.appName("playground-pipeline")
            .config(
                "spark.sql.catalog.local",
                "org.apache.iceberg.spark.SparkCatalog",
            )
            .config("spark.sql.catalog.local.type", "hadoop")
            .config("spark.sql.catalog.local.warehouse", warehouse_path)
            .config(
                "spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            )
            .getOrCreate()
        )
    except Exception as e:
        logger.error("Failed to create Spark session: %s", str(e))
        raise
