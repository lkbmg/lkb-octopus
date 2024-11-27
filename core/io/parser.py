import json
import xml.etree.ElementTree as ET
from typing import Any, List, Dict, Union
from core.DataTypes.Types import StructType, ListType, DataType
from core.DataTypes.Schema import SchemaInference
from core.Exceptions import ConversionError
from core.DataTypes.Cast import TypeCast


class GenericParser:
    """
    Generic parser to handle JSON and XML data and convert it to/from tabular formats.

    Attributes:
        schema (DataType): Schema for the data, inferred or provided.
    """

    def __init__(self, schema: DataType = None):
        self.schema = schema

    def infer_schema(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> DataType:
        """
        Infer schema from structured data.

        Args:
            data (dict or list[dict]): Input data.

        Returns:
            DataType: Inferred schema as a StructType.
        """
        try:
            schema = SchemaInference.infer_schema(data)
            if not isinstance(schema, StructType):
                raise ConversionError("Inferred schema is not a StructType.")
            self.schema = schema
            return schema
        except Exception as e:
            raise ConversionError(f"Error inferring schema: {e}")

    def to_rows(self, data: List[Dict[str, Any]]) -> List[List[Any]]:
        """
        Convert structured data to rows.

        Args:
            data (list[dict]): Structured data.

        Returns:
            list[list]: Data in row format.
        """
        try:
            rows = []
            for record in data:
                row = [record.get(field, None) for field in self.schema.fields.keys()]
                rows.append(row)
            return rows
        except Exception as e:
            raise ConversionError(f"Error converting to rows: {e}")

    def to_columns(self, data: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """
        Convert structured data to columns.

        Args:
            data (list[dict]): Structured data.

        Returns:
            dict: Data in column format.
        """
        try:
            columns = {field: [] for field in self.schema.fields.keys()}
            for record in data:
                for field in self.schema.fields.keys():
                    columns[field].append(record.get(field, None))
            return columns
        except Exception as e:
            raise ConversionError(f"Error converting to columns: {e}")

    def from_rows(self, rows: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        Convert rows back to structured data.

        Args:
            rows (list[list]): Data in row format.

        Returns:
            list[dict]: Structured data.
        """
        try:
            structured_data = []
            for row in rows:
                record = {
                    field: TypeCast.cast_value(value, self.schema.fields[field])
                    for field, value in zip(self.schema.fields.keys(), row)
                }
                structured_data.append(record)
            return structured_data
        except Exception as e:
            raise ConversionError(f"Error converting from rows: {e}")

    def from_columns(self, columns: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """
        Convert columns back to structured data.

        Args:
            columns (dict): Data in column format.

        Returns:
            list[dict]: Structured data.
        """
        try:
            row_count = len(next(iter(columns.values())))
            structured_data = [
                {key: columns[key][i] for key in columns.keys()} for i in range(row_count)
            ]
            return structured_data
        except Exception as e:
            raise ConversionError(f"Error converting from columns: {e}")

    def parse_json(self, json_data: str) -> Dict[str, Any]:
        """
        Parse JSON string to structured data.

        Args:
            json_data (str): JSON string.

        Returns:
            dict: Parsed structured data.
        """
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ConversionError(f"Error parsing JSON: {e}")

    def parse_xml(self, xml_data: str) -> List[Dict[str, Any]]:
        """
        Parse XML string to structured data.

        Args:
            xml_data (str): XML string.

        Returns:
            list[dict]: Parsed structured data.
        """
        try:
            root = ET.fromstring(xml_data)
            records = []
            for child in root:
                record = {subchild.tag: subchild.text for subchild in child}
                records.append(record)
            return records
        except ET.ParseError as e:
            raise ConversionError(f"Error parsing XML: {e}")



