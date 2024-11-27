from core.DataTypes.Common import DataType

from core.Exceptions import UnsupportedTypeError, ConversionError, ValidationError
import re
from urllib.parse import urlparse


class Validation:
    """Provides validation utilities for various data types and formats."""

    @staticmethod
    def validate_mappings(mappings: dict):
        """
        Validates a mappings dictionary to ensure all entries resolve to valid DataType classes.

        Args:
            mappings (dict): A dictionary containing type mappings.

        Raises:
            UnsupportedTypeError: If a mapping contains invalid or unresolved entries.
        """
        for category, mapping in mappings.items():
            for key, value in mapping.items():
                if callable(value):
                    try:
                        resolved_value = value()  # Check if callable resolves correctly
                        if not isinstance(resolved_value, DataType):
                            raise UnsupportedTypeError(f"Resolved value {resolved_value} is not a DataType instance.")
                    except Exception as e:
                        raise UnsupportedTypeError(f"Invalid mapping for {key} in {category}: {e}")
                elif not isinstance(value, type) or not issubclass(value, DataType):
                    raise UnsupportedTypeError(f"Invalid DataType class {value} in {category} for key {key}")

    @staticmethod
    def validate_compatibility(dtype1: DataType, dtype2: DataType) -> bool:
        """
        Validates if two DataType instances are compatible.

        Args:
            dtype1 (DataType): First DataType instance.
            dtype2 (DataType): Second DataType instance.

        Returns:
            bool: True if the data types are compatible, False otherwise.

        Raises:
            ConversionError: If the data types are incompatible.
        """
        if not dtype1.is_compatible(dtype2):
            raise ConversionError(f"Data types {dtype1} and {dtype2} are not compatible.")
        return True

    URL_REGEX = re.compile(
        r'^(https?|ftp):\/\/'  # Protocol
        r'(([\w.-]+)|([a-zA-Z0-9.-]+))'  # Hostname or IP
        r'(:\d+)?'  # Port
        r'(\/[^\s]*)?$',  # Path
        re.IGNORECASE
    )

    @staticmethod
    def validate_url(url: str) -> str:
        """
        Validates and returns a properly formatted URL.

        Args:
            url (str): The URL to validate.

        Returns:
            str: The validated and normalized URL.

        Raises:
            ValidationError: If the URL is invalid.
        """
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValidationError(f"Invalid URL: {url}")
        if not Validation.URL_REGEX.match(url):
            raise ValidationError(f"Malformed URL: {url}")
        return url

    @staticmethod
    def validate_hostname(hostname: str) -> str:
        """
        Validates and formats a hostname.

        Args:
            hostname (str): The hostname to validate.

        Returns:
            str: The validated and formatted hostname.

        Raises:
            ValidationError: If the hostname is invalid.
        """
        if len(hostname) > 255 or hostname[-1] == ".":
            raise ValidationError(f"Invalid hostname: {hostname}")
        if not all(re.match(r'^[a-zA-Z0-9-]{1,63}$', part) for part in hostname.split(".")):
            raise ValidationError(f"Invalid hostname part in: {hostname}")
        return hostname.lower()

    @staticmethod
    def validate_non_empty_string(value: str, field_name: str = "Value") -> str:
        """
        Validates that a string is non-empty and stripped of extra spaces.

        Args:
            value (str): The string to validate.
            field_name (str): The name of the field (for error messages).

        Returns:
            str: The cleaned and validated string.

        Raises:
            ValidationError: If the string is empty or invalid.
        """
        if not value or not value.strip():
            raise ValidationError(f"{field_name} cannot be empty.")
        return value.strip()
