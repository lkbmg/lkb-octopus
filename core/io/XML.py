import xml.etree.ElementTree as ET
import sys
import os
import logging
from core.NormalizeBase import ABCNormalizer
from core.utility.Normalize import Normalization
from core.Exceptions import ConversionError, NormalizationError
from core.DataTypes.Schema import SchemaInference
from core.DataTypes.Types import ListType, StructType, NestedNullType

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))


class XMLAdapter(ABCNormalizer):
    """Adapter for handling XML data and converting it to/from structured formats."""
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
            # Ensure input is JSON-like
            data = Normalization.normalize_json(data)

            # Handle list or dict inputs
            if isinstance(data, dict):
                return data  # Already normalized as a dict
            elif isinstance(data, list):
                # Single dict in a list should not be re-wrapped
                if len(data) == 1 and isinstance(data[0], dict):
                    return data[0]
                # Wrap list under a 'root' key
                return {"root": data}

            raise NormalizationError("Expected a dictionary or list for normalization.")
        except NormalizationError as e:
            raise ConversionError(f"Error normalizing input JSON: {e}")

    @staticmethod
    def to_xml(data):
        """
        Convert normalized data to an XML string.

        Args:
            data (dict): Normalized dictionary.

        Returns:
            str: XML string representation.

        Raises:
            ConversionError: If the input data is invalid or conversion fails.
        """
        def build_element(parent, key, value, schema):
            """
            Recursively build XML elements from key-value pairs.

            Args:
                parent (ET.Element): Parent XML element.
                key (str): Element name.
                value (Any): Element value.
                schema (DataType): Schema describing the structure.
            """
            try:
                child = ET.SubElement(parent, key)
                if isinstance(schema, StructType):
                    for sub_key, sub_value in (value or {}).items():
                        field_schema = schema.fields.get(sub_key, NestedNullType())
                        build_element(child, sub_key, sub_value, field_schema)
                elif isinstance(schema, ListType):
                    for item in value or []:
                        item_wrapper = ET.SubElement(child, "item")
                        item_schema = schema.inner_type if isinstance(schema.inner_type, StructType) else NestedNullType()
                        build_element(item_wrapper, "item", item, item_schema)
                elif isinstance(schema, NestedNullType):
                    child.text = ""  # Represent null as an empty tag
                else:
                    child.text = str(value)  # Handle primitives
            except Exception as e:
                raise ConversionError(f"Error building XML element for key '{key}': {e}")

        try:
            # Normalize data and infer schema
            normalized_data = XMLAdapter.normalize_input(data)
            schema = SchemaInference.infer_schema(normalized_data)

            # Dynamically determine root key
            root_key = next(iter(normalized_data.keys())) if isinstance(normalized_data, dict) else "root"
            root_value = normalized_data[root_key] if isinstance(normalized_data, dict) else normalized_data
            root_schema = schema.fields.get(root_key, NestedNullType()) if isinstance(schema, StructType) else schema

            if isinstance(root_schema, NestedNullType):
                raise ConversionError(f"Root schema cannot be inferred correctly: {type(root_schema)}")

            # Create the XML root element
            root = ET.Element(root_key)

            # Build XML structure
            if isinstance(root_schema, ListType):
                for item in root_value or []:
                    item_wrapper = ET.SubElement(root, "item")
                    item_schema = root_schema.inner_type if isinstance(root_schema.inner_type, StructType) else NestedNullType()
                    for key, value in (item or {}).items():
                        field_schema = item_schema.fields.get(key, NestedNullType()) if isinstance(item_schema, StructType) else NestedNullType()
                        build_element(item_wrapper, key, value, field_schema)
            elif isinstance(root_schema, StructType):
                for key, value in root_value.items():
                    field_schema = root_schema.fields.get(key, NestedNullType())
                    build_element(root, key, value, field_schema)
            else:
                raise ConversionError(f"Unsupported root schema type for XML conversion: {type(root_schema)}")

            return ET.tostring(root, encoding="unicode")
        except Exception as e:
            raise ConversionError(f"Error converting data to XML: {e}")



    def from_xml(xml_data):
        """
        Convert an XML string to a dictionary with the root structure preserved.

        Args:
            xml_data (str): XML string.

        Returns:
            tuple: (data, inferred_schema)
                - data: Parsed XML data with the correct root structure.
                - inferred_schema: Inferred schema of the parsed data.

        Raises:
            ConversionError: If the XML data is malformed or conversion fails.
        """

        def parse_element(element):
            """
            Recursively parse an XML element into a dictionary or list.

            Args:
                element (ET.Element): The XML element to parse.

            Returns:
                Parsed Python object with root key preserved.
            """
            # Handle leaf node
            if len(element) == 0:
                return element.text.strip() if element.text else None

            # Parse children into a dictionary
            result = {}
            for child in element:
                parsed_child = parse_element(child)

                # Handle repeated tags as lists
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(parsed_child)
                else:
                    result[child.tag] = parsed_child

            return result

        try:
            root = ET.fromstring(xml_data)            
            # Parse the root as a list structure if needed
            parsed_data = {
                root.tag: [parse_element(child) for child in root]
            }
            
            # Normalize and infer schema
            normalized_data = XMLAdapter.normalize_input(parsed_data)
            schema = SchemaInference.infer_schema(normalized_data)
            
            return normalized_data, schema
        except ET.ParseError as e:
            raise ConversionError(f"Error parsing XML: {e}")
        except Exception as e:
            raise ConversionError(f"Error converting XML to data: {e}")

    @staticmethod
    def infer_schema(xml_data):
        """
        Infer the schema of an XML string.

        Args:
            xml_data (str): XML string.

        Returns:
            DataType: Inferred schema.

        Raises:
            ConversionError: If the XML data is malformed or schema inference fails.
        """
        try:
            data, _ = XMLAdapter.from_xml(xml_data)
            return SchemaInference.infer_schema(data)
        except Exception as e:
            raise ConversionError(f"Error inferring schema from XML: {e}")

    @staticmethod
    def describe_schema(xml_data):
        """
        Provide a descriptive schema representation for an XML string.

        Args:
            xml_data (str): XML string.

        Returns:
            dict: Descriptive schema representation.

        Raises:
            ConversionError: If schema description fails.
        """
        try:
            schema = XMLAdapter.infer_schema(xml_data)
            return SchemaInference.describe_schema(schema)
        except Exception as e:
            raise ConversionError(f"Error describing schema from XML: {e}")

    def from_normalized(self, data):
        """
        Convert normalized data to XML string.

        Args:
            data (list[dict]): Normalized list of dictionaries.

        Returns:
            str: XML string representation.
        """
        return self.to_xml(data)
