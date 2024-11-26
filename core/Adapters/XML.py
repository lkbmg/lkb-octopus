import xml.etree.ElementTree as ET
from core.Normalizer import ABCNormalizer
from core.DataTypes.Exceptions import ConversionError
from core.DataTypes.Schema import SchemaInference
from core.DataTypes.Map import ConversionMap
from core.DataTypes.Types import ListType, StructType, NestedNullType


class XMLAdapter(ABCNormalizer):
    """Adapter for handling XML data and converting it to/from structured formats."""

    @staticmethod
    def to_xml(data):
        """
        Convert normalized data to an XML string.

        Args:
            data (dict or list[dict]): Input data.

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
                    for sub_key, sub_value in value.items():
                        field_schema = schema.fields.get(sub_key, NestedNullType())
                        build_element(child, sub_key, sub_value, field_schema)
                elif isinstance(schema, ListType):
                    for item in value:
                        build_element(parent, key, item, schema.inner_type)
                else:
                    # Primitive or null types
                    child.text = ConversionMap.to_xml(value, schema)
            except Exception as e:
                raise ConversionError(f"Error building XML element for key '{key}': {e}")

        try:
            normalized_data = XMLAdapter.normalize_input(data)
            schema = SchemaInference.infer_schema(normalized_data)
            root = ET.Element("root")

            if isinstance(schema, ListType):
                for item in normalized_data:
                    item_schema = schema.inner_type if isinstance(schema.inner_type, StructType) else NestedNullType()
                    for key, value in item.items():
                        field_schema = item_schema.fields.get(key, NestedNullType()) if isinstance(item_schema, StructType) else NestedNullType()
                        build_element(root, key, value, field_schema)
            elif isinstance(schema, StructType):
                for key, value in normalized_data.items():
                    field_schema = schema.fields.get(key, NestedNullType())
                    build_element(root, key, value, field_schema)
            else:
                raise ConversionError("Unsupported root schema type for XML conversion.")

            return ET.tostring(root, encoding="unicode")
        except Exception as e:
            raise ConversionError(f"Error converting data to XML: {e}")

    @staticmethod
    def from_xml(xml_data):
        """
        Convert an XML string to a list of dictionaries.

        Args:
            xml_data (str): XML string.

        Returns:
            tuple: (data, inferred_schema)
                - data: Parsed XML data (list or dict).
                - inferred_schema: Inferred schema.

        Raises:
            ConversionError: If the XML data is malformed or conversion fails.
        """
        def parse_element(element):
            """
            Recursively parse an XML element into a dictionary or list.

            Args:
                element (ET.Element): The XML element to parse.

            Returns:
                Parsed Python object.
            """
            # Leaf node
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
            # Parse XML string into an ElementTree
            root = ET.fromstring(xml_data)

            # Recursively parse the XML structure
            parsed_data = parse_element(root)

            # Normalize data and infer schema
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
