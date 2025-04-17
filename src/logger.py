import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name):
    """Get a logger instance with the configured settings.

    Args:
        name: Name of the logger

    Returns:
        Logger: Configured logger instance
    """
    return logging.getLogger(name)
