import os
import json
from typing import Dict, Any, List

import requests
from logger import get_logger

logger = get_logger(__name__)


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
        self,
        albums_data: List[Dict[str, Any]],
        filepath: str,
        overwrite: bool = True,
    ) -> None:
        """Save albums data to a JSON file.

        Args:
            albums_data (List[Dict[str, Any]]): Albums data to save
            filepath (str): Path where to save the JSON file
            overwrite (bool, optional): Whether to overwrite existing file.
                Defaults to True.

        Raises:
            IOError: If there's an error writing the file
            FileExistsError: If file exists and overwrite is False
        """
        if not overwrite and os.path.exists(filepath):
            raise FileExistsError(
                f"File {filepath} already exists and overwrite is False"
            )

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(albums_data, f, indent=2)
        logger.info("Albums data saved successfully to %s", filepath)
