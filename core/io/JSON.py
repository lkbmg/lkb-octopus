import json, sys, os, logging
from core.NormalizeBase import ABCNormalizer
from core.utility.Normalize import Normalization
from core.DataTypes.Schema import SchemaInference
from core.Exceptions import ConversionError, NormalizationError

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+'/../'))

class JSONAdapter(ABCNormalizer):
    """Adapter for handling JSON data."""

    @staticmethod
    def normalize_input(data):
        """
        Normalize input JSON data.

        Args:
            data (dict or list[dict]): The data to normalize.

        Returns:
            list[dict]: Normalized list of dictionaries.
        """
        try:
            # Normalize whitespace and ensure it's a list of dictionaries
            data = Normalization.normalize_json(data)
            list_data = Normalization.normalize_list(data)

            return Normalization.normalize_input(list_data) 
        except NormalizationError as e:
            raise ConversionError(f"Error normalizing input JSON: {e}")

    def from_normalized(self, data):
        """
        Convert normalized data back to JSON string.

        Args:
            data (list[dict]): Normalized list of dictionaries.

        Returns:
            str: JSON string.
        """
        try:
            return json.dumps(data, indent=4)
        except Exception as e:
            raise ConversionError(f"Error converting normalized data to JSON: {e}")

    @staticmethod
    def to_json(data):
        """
        Convert data to JSON string, with schema inference.

        Args:
            data (dict or list[dict]): Input data to convert.

        Returns:
            tuple: (JSON string representation of the data, inferred schema)

        Raises:
            ConversionError: If conversion fails.
        """
        try:
            normalized_data = JSONAdapter.normalize_input(data)
            schema = SchemaInference.infer_schema(normalized_data)
            json_string = json.dumps(normalized_data, ensure_ascii=False, indent=4)
            return json_string, schema
        except Exception as e:
            raise ConversionError(f"Error converting to JSON: {e}")

    @staticmethod
    def from_json(json_data):
        """
        Convert JSON string to Python objects, with schema inference.

        Args:
            json_data (str): JSON string.

        Returns:
            tuple: (data, inferred schema)
                - data: Parsed JSON data (dict or list[dict]).
                - inferred schema: Inferred schema as a DataType instance.

        Raises:
            ConversionError: If decoding or schema inference fails.
        """
        try:
            parsed_data = json.loads(json_data)
            normalized_data = JSONAdapter.normalize_input(parsed_data)
            schema = SchemaInference.infer_schema(normalized_data)
            return normalized_data, schema
        except json.JSONDecodeError as e:
            raise ConversionError(f"Error decoding JSON: {e}")
        except Exception as e:
            raise ConversionError(f"Error inferring schema from JSON: {e}")

    @staticmethod
    def to_file(data, file_path):
        """
        Save data to a file in JSON format, with schema inference.

        Args:
            data (dict or list[dict]): Data to save.
            file_path (str): Path to the file where data will be saved.

        Returns:
            DataType: Inferred schema.

        Raises:
            ConversionError: If saving to file fails.
        """
        try:
            json_string, schema = JSONAdapter.to_json(data)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json_string)
            return schema
        except Exception as e:
            raise ConversionError(f"Error saving JSON to file: {e}")

    @staticmethod
    def from_file(file_path):
        """
        Load data from a JSON file, with schema inference.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            tuple: (data, inferred schema)
                - data: Parsed JSON data (dict or list[dict]).
                - inferred schema: Inferred schema as a DataType instance.

        Raises:
            ConversionError: If loading from file fails.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_string = file.read()
            return JSONAdapter.from_json(json_string)
        except FileNotFoundError:
            raise ConversionError(f"File not found: {file_path}")
        except Exception as e:
            raise ConversionError(f"Error loading JSON from file: {e}")

    @staticmethod
    def infer_schema(data):
        """
        Infer schema from data.

        Args:
            data (dict, list[dict], or str): JSON data (string or parsed).

        Returns:
            DataType: Inferred schema.

        Raises:
            ConversionError: If schema inference fails.
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)
            normalized_data = JSONAdapter.normalize_input(data)
            return SchemaInference.infer_schema(normalized_data)
        except Exception as e:
            raise ConversionError(f"Error inferring schema: {e}")

    @staticmethod
    def describe_schema(data):
        """
        Describe the schema of the data.

        Args:
            data (dict, list[dict], or str): JSON data (string or parsed).

        Returns:
            dict: Descriptive schema representation.

        Raises:
            ConversionError: If schema description fails.
        """
        try:
            schema = JSONAdapter.infer_schema(data)
            return SchemaInference.describe_schema(schema)
        except Exception as e:
            raise ConversionError(f"Error describing schema: {e}")

    def from_normalized(self, data):
        """
        Convert normalized data to JSON string.

        Args:
            data (list[dict]): Normalized list of dictionaries.

        Returns:
            str: JSON string representation.
        """
        try:
            return json.dumps(data, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConversionError(f"Error converting normalized data to JSON: {e}")
