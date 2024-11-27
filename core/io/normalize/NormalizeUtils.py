from typing import Union, Dict, Any, List, Optional
from urllib.parse import urlparse, urlunparse
from core.Exceptions import NormalizationError
from core.DataTypes.Missing import MissingHandler


class NormalizationUtils:
    """
    Shared utilities for data normalization.
    """

    @staticmethod
    def handle_nulls(data):
        """
        Ensure all null-like values are standardized.

        Args:
            data (Any): Input data.

        Returns:
            Any: Data with nulls handled.
        """
        return MissingHandler.fill_nulls(data, None)

    @staticmethod
    def normalize_whitespace(value: str) -> str:
        """Collapse consecutive spaces in a string."""
        if not isinstance(value, str):
            raise NormalizationError(f"Expected a string, got {type(value)}")
        return " ".join(value.split())

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
    def normalize_url(url: str) -> str:
        """Normalize and validate a URL."""
        if not isinstance(url, str):
            raise NormalizationError(f"Expected a string for URL, got {type(url)}")
        url = url.strip()
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise NormalizationError(f"Invalid URL: {url}")
        return urlunparse(parsed)


def flatten_structure(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    parent_key: str = '',
    sep: str = '.',
    max_level: Optional[int] = None,
    lowercase_keys: bool = True
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Normalize (flatten) a nested structure iteratively.

    Args:
        data: Input data to be flattened. Can be a dictionary or a list of dictionaries.
        parent_key: Prefix to append to keys in the flattened structure.
        sep: Separator to use for concatenating keys.
        max_level: Maximum depth of recursion to flatten nested structures.
        lowercase_keys: Whether to convert keys to lowercase.

    Returns:
        A flattened dictionary or list of flattened dictionaries.
    """

    def flatten_dict(d: Dict[str, Any], parent_key: str = '', level: int = 0) -> Dict[str, Any]:
        """Flatten a dictionary structure iteratively."""
        items = []
        stack = [(parent_key, d, 0)]  # Stack holds (current_key, current_value, level)

        while stack:
            current_key, current_value, level = stack.pop()

            for k, v in current_value.items():
                new_key = f"{current_key}{sep}{k}" if current_key else k
                if lowercase_keys:
                    new_key = new_key.lower()

                if isinstance(v, dict) and (max_level is None or level < max_level):
                    stack.append((new_key, v, level + 1))
                elif isinstance(v, list):
                    items.extend(flatten_list(v, new_key, level + 1).items())
                else:
                    items.append((new_key, v))

        return dict(items)

    def flatten_list(l: List[Any], parent_key: str, level: int = 0) -> Dict[str, Any]:
        """Flatten a list by iterating through it."""
        items = {}
        for idx, item in enumerate(l):
            new_key = f"{parent_key}{sep}{idx}"

            if isinstance(item, dict):
                items.update(flatten_dict(item, new_key, level + 1))
            elif isinstance(item, list):
                items.update(flatten_list(item, new_key, level + 1))
            else:
                items[new_key] = item

        return items

    if isinstance(data, list):
        return [flatten_dict(d, parent_key) for d in data]
    elif isinstance(data, dict):
        return flatten_dict(data, parent_key)
    else:
        raise ValueError("Input data must be a dictionary or a list of dictionaries.")
