import xml.etree.ElementTree as ET
from core.io.normalize.NormalizeXML import NormalizeXML
from core.Exceptions import ConversionError


class XmlIO:
    """Adapter for handling XML data."""

    @staticmethod
    def normalize_input(data):
        """
        Normalize input XML data.

        Args:
            data (str): XML string.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            ConversionError: If normalization fails.
        """
        try:
            return NormalizeXML.normalize(data)
        except Exception as e:
            raise ConversionError(f"Error normalizing input XML: {e}")

    @staticmethod
    def to_xml(data):
        """
        Convert Python dictionary to XML string.

        Args:
            data (dict): Input data to convert.

        Returns:
            str: XML string.

        Raises:
            ConversionError: If conversion fails.
        """
        def build_element(parent, key, value):
            """
            Recursively build XML elements from key-value pairs.

            Args:
                parent (ET.Element): Parent XML element.
                key (str): Element name.
                value (Any): Element value.
            """
            try:
                child = ET.SubElement(parent, key)
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        build_element(child, sub_key, sub_value)
                elif isinstance(value, list):
                    for item in value:
                        build_element(child, "item", item)
                elif value is None:
                    child.text = ""  # Represent null as an empty tag
                else:
                    child.text = str(value)
            except Exception as e:
                raise ConversionError(f"Error building XML element for key '{key}': {e}")

        try:
            # Ensure data is normalized before building XML
            normalized_data = XmlIO.normalize_input(data)
            root_key = next(iter(normalized_data[0].keys()))
            root_value = normalized_data[0][root_key]

            root = ET.Element(root_key)
            if isinstance(root_value, list):
                for item in root_value:
                    build_element(root, "item", item)
            elif isinstance(root_value, dict):
                for key, value in root_value.items():
                    build_element(root, key, value)
            else:
                raise ConversionError("Unsupported root structure for XML conversion.")

            return ET.tostring(root, encoding="unicode")
        except Exception as e:
            raise ConversionError(f"Error converting data to XML: {e}")

    @staticmethod
    def from_xml(xml_data):
        """
        Convert an XML string to a Python dictionary.

        Args:
            xml_data (str): XML string.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            ConversionError: If decoding fails.
        """
        def parse_element(element):
            """
            Recursively parse an XML element into a dictionary or list.

            Args:
                element (ET.Element): The XML element to parse.

            Returns:
                dict or list: Parsed Python object.
            """
            if len(element) == 0:  # Leaf node
                return element.text.strip() if element.text else None

            result = {}
            for child in element:
                parsed_child = parse_element(child)
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(parsed_child)
                else:
                    result[child.tag] = parsed_child
            return result

        try:
            root = ET.fromstring(xml_data)
            parsed_data = {root.tag: parse_element(root)}
            return XmlIO.normalize_input(parsed_data)
        except ET.ParseError as e:
            raise ConversionError(f"Error parsing XML: {e}")
        except Exception as e:
            raise ConversionError(f"Error normalizing XML: {e}")

    @staticmethod
    def to_file(data, file_path):
        """
        Save data to a file in XML format.

        Args:
            data (dict): Data to save.
            file_path (str): Path to the file.

        Raises:
            ConversionError: If saving to file fails.
        """
        try:
            xml_string = XmlIO.to_xml(data)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(xml_string)
        except Exception as e:
            raise ConversionError(f"Error saving XML to file: {e}")

    @staticmethod
    def from_file(file_path):
        """
        Load data from an XML file.

        Args:
            file_path (str): Path to the file.

        Returns:
            list[dict]: Parsed and normalized data.

        Raises:
            ConversionError: If loading from file fails.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_data = file.read()
            return XmlIO.from_xml(xml_data)
        except FileNotFoundError:
            raise ConversionError(f"File not found: {file_path}")
        except Exception as e:
            raise ConversionError(f"Error loading XML from file: {e}")
