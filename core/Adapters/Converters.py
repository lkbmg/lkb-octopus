from core.AdapterRegistry import Registry
from core.DataTypes.Exceptions import ConversionError

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
            return Registry.get("JSON", category="adapters").to_json(data)
        except Exception as e:
            raise ConversionError(f"Error converting XML to JSON: {e}")

    @staticmethod
    def json_to_xml(json_data):
        """
        Convert JSON to XML.

        Args:
            json_data (str): JSON string.

        Returns:
            str: XML string.
        """
        try:
            data, _ = Registry.get("JSON", category="adapters").from_json(json_data)
            return Registry.get("XML", category="adapters").to_xml(data)
        except Exception as e:
            raise ConversionError(f"Error converting JSON to XML: {e}")

