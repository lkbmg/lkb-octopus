from core.utility.AdapterRegistry import Registry
from core.Exceptions import ConversionError
from core.utility.Normalize import Normalization


class Converter:
    """Handles conversions between JSON and XML formats."""

    @staticmethod
    def xml_to_json(xml_data):
        """
        Convert XML to JSON.

        Args:
            xml_data (str): XML string.

        Returns:
            str: JSON string.
        """
        try:
            data, _ = Registry.get("XML", category="adapters").from_xml(xml_data)
            json, schema = Registry.get("JSON", category="adapters").to_json(data)
            return Normalization.normalize_json(json)
        except Exception as e:
            raise ConversionError(f"Error converting XML to JSON: {e}")

    @staticmethod
    def json_to_xml(json_data):
        """
        Convert JSON to XML.

        Args:
            json_data (str or list[dict]): JSON string or Python object.

        Returns:
            str: XML string.
        """
        try:
            # If json_data is already a Python object, skip parsing
            if isinstance(json_data, (list, dict)):
                normalized_data = Registry.get("JSON", category="adapters").normalize_input(json_data)
            else:
                # Parse JSON string
                normalized_data, schema = Registry.get("JSON", category="adapters").from_json(json_data)

            # Convert to XML
            return Registry.get("XML", category="adapters").to_xml(normalized_data)
        except Exception as e:
            raise ConversionError(f"Error converting JSON to XML: {e}")
