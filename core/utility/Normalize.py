from urllib.parse import urlparse, urlunparse
import json
from core.Exceptions import NormalizationError


class Normalization:
    """Provides data normalization utilities."""

    @staticmethod
    def normalize_json(data):
        """
        Ensure JSON-like data is normalized to a dictionary or a list of dictionaries.

        Args:
            data (dict, list, or str): The data to normalize.

        Returns:
            dict or list: Normalized dictionary or list of dictionaries.

        Raises:
            NormalizationError: If the input is not valid JSON.
        """
        if isinstance(data, (dict, list)):
            return data  # Return as is if it's already a dict or list
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as e:
                raise NormalizationError(f"Invalid JSON string: {e}")
        raise NormalizationError(f"Expected a dict, list, or JSON string, got {type(data)}")

    @staticmethod
    def normalize_list(data):
        """
        Ensure input is a list of dictionaries.

        Args:
            data: The input data to normalize.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            NormalizationError: If the data cannot be normalized.
        """
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data
        raise NormalizationError("Expected a dict or list of dictionaries.")
    
    @staticmethod
    def normalize_whitespace(value: str) -> str:
        """Collapse consecutive spaces in a string."""
        if not isinstance(value, str):
            raise NormalizationError(f"Expected a string, got {type(value)}")
        return " ".join(value.split())

    @staticmethod
    def normalize_dict(data):
        """Ensure input is a valid dictionary."""
        if isinstance(data, dict):
            return data
        raise NormalizationError(f"Expected a dictionary, got {type(data)}")

    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize and validate a URL."""
        if not isinstance(url, str):
            raise NormalizationError(f"Expected a string for URL, got {type(url)}")
        url = url.strip()
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise NormalizationError(f"Invalid URL: {url}")
        return urlunparse(parsed)

    @staticmethod
    def normalize_hostname(hostname: str) -> str:
        """Normalize and validate a hostname."""
        if not isinstance(hostname, str):
            raise NormalizationError(f"Expected a string for hostname, got {type(hostname)}")
        hostname = hostname.strip().lower()
        if not hostname or len(hostname) > 255 or any(len(label) > 63 for label in hostname.split(".")):
            raise NormalizationError(f"Invalid hostname: {hostname}")
        return hostname

    @staticmethod
    def normalize_keys(data: dict, case="lower") -> dict:
        """
        Normalize keys in a dictionary to a specific case.

        Args:
            data (dict): Input dictionary.
            case (str): Case to normalize to ('lower', 'upper').

        Returns:
            dict: Dictionary with normalized keys.
        """
        if not isinstance(data, dict):
            raise NormalizationError(f"Expected a dictionary, got {type(data)}")
        if case not in ("lower", "upper"):
            raise ValueError("Case must be 'lower' or 'upper'")
        return {k.lower() if case == "lower" else k.upper(): v for k, v in data.items()}

    @staticmethod
    def normalize_input(data):
        """
        Normalize input JSON data.

        Args:
            data (dict or list[dict]): The data to normalize.

        Returns:
            dict: Normalized dictionary with a clear root.

        Raises:
            NormalizationError: If the input cannot be normalized.
        """
        try:
            # If the input is a dictionary, return it directly
            if isinstance(data, dict):
                return data

            # If the input is a list, check for proper structure and wrap it
            if isinstance(data, list):
                if not data or not isinstance(data[0], dict):
                    raise NormalizationError("Cannot normalize a list without dictionary elements.")
                # If the list already has a proper key (e.g., 'computer_reports'), don't re-wrap
                if len(data) == 1 and isinstance(data[0], dict) and len(data[0]) == 1:
                    return data[0]
                # Otherwise, wrap it using the first dictionary's first key
                root_key = "root"  # Use 'root' as a fallback if no key is found
                return {root_key: data}

            raise NormalizationError("Input must be a dictionary or a list of dictionaries.")
        except Exception as e:
            raise NormalizationError(f"Error normalizing input: {e}")
