import os
import json
import logging
from typing import Dict, Any, List

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class JSONPlaceholderClient:
    """Class to handle JSONPlaceholder API interactions."""

    def __init__(self):
        """Initialize the JSONPlaceholder client."""
        self.base_url = "https://jsonplaceholder.typicode.com"

    def get_albums(self) -> List[Dict[str, Any]]:
        """Fetch albums data from JSONPlaceholder API.

        Returns:
            List[Dict[str, Any]]: List of album objects from the API

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/albums"
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            raise requests.exceptions.RequestException(
                f"API request failed with status code {response.status_code}: "
                f"{response.text}"
            )

        return response.json()

    def save_albums(
        self, albums_data: List[Dict[str, Any]], filepath: str
    ) -> None:
        """Save albums data to a JSON file.

        Args:
            albums_data (List[Dict[str, Any]]): Albums data to save
            filepath (str): Path where to save the JSON file

        Raises:
            IOError: If there's an error writing the file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(albums_data, f, indent=2)
        logger.info("Albums data saved successfully to %s", filepath)
