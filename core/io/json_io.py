import json
from core.io.normalize.NormalizeJSON import NormalizeJSON
from core.Exceptions import ConversionError


class JsonIO:
    """Adapter for handling JSON data."""

    @staticmethod
    def normalize_input(data):
        """
        Normalize input JSON data.

        Args:
            data (dict or list[dict]): The data to normalize.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            ConversionError: If normalization fails.
        """
        try:
            return NormalizeJSON.normalize(data)
        except Exception as e:
            raise ConversionError(f"Error normalizing input JSON: {e}")

    @staticmethod
    def from_normalized(data):
        """
        Convert normalized data back to JSON string.

        Args:
            data (list[dict]): Normalized list of dictionaries.

        Returns:
            str: JSON string.

        Raises:
            ConversionError: If conversion fails.
        """
        try:
            if not data:
                return "[]"  # Represent empty data as an empty JSON array
            return json.dumps(data, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConversionError(f"Error converting normalized data to JSON: {e}")

    @staticmethod
    def to_json(data):
        """
        Convert data to JSON string.

        Args:
            data (dict or list[dict]): Input data to convert.

        Returns:
            str: JSON string.

        Raises:
            ConversionError: If conversion fails.
        """
        try:
            normalized_data = JsonIO.normalize_input(data)
            return JsonIO.from_normalized(normalized_data)
        except Exception as e:
            raise ConversionError(f"Error converting to JSON: {e}")

    @staticmethod
    def from_json(json_data):
        """
        Convert JSON string to Python objects.

        Args:
            json_data (str): JSON string.

        Returns:
            list[dict]: Parsed and normalized data.

        Raises:
            ConversionError: If decoding fails.
        """
        try:
            if not json_data.strip():
                raise ConversionError("Input JSON string is empty or whitespace.")
            parsed_data = json.loads(json_data)
            return JsonIO.normalize_input(parsed_data)
        except json.JSONDecodeError as e:
            raise ConversionError(f"Error decoding JSON: {e}")
        except Exception as e:
            raise ConversionError(f"Error normalizing JSON: {e}")

    @staticmethod
    def to_file(data, file_path):
        """
        Save data to a file in JSON format.

        Args:
            data (dict or list[dict]): Data to save.
            file_path (str): Path to the file where data will be saved.

        Raises:
            ConversionError: If saving to file fails.
        """
        try:
            if not file_path:
                raise ConversionError("File path cannot be empty.")
            json_string = JsonIO.to_json(data)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json_string)
        except Exception as e:
            raise ConversionError(f"Error saving JSON to file: {e}")

    @staticmethod
    def from_file(file_path):
        """
        Load data from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            list[dict]: Parsed and normalized data.

        Raises:
            ConversionError: If loading from file fails.
        """
        try:
            if not file_path:
                raise ConversionError("File path cannot be empty.")
            with open(file_path, 'r', encoding='utf-8') as file:
                json_string = file.read()
            return JsonIO.from_json(json_string)
        except FileNotFoundError:
            raise ConversionError(f"File not found: {file_path}")
        except Exception as e:
            raise ConversionError(f"Error loading JSON from file: {e}")
