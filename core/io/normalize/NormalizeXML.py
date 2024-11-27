import xml.etree.ElementTree as ET
from core.io.normalize.NormalizeBase import NormalizeBase
from core.Exceptions import NormalizationError
from core.io.normalize.NormalizeUtils import NormalizationUtils


class NormalizeXML(NormalizeBase):
    """
    Normalization logic for XML data.
    """

    @staticmethod
    def normalize(data):
        """
        Normalize XML input into a standardized dictionary.

        Args:
            data (str): XML string.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            NormalizationError: If normalization fails.
        """
        try:
            root = ET.fromstring(data)
            normalized_data = NormalizeXML._xml_to_dict(root)
            # Wrap result in a root key
            return [{"root": normalized_data}]
        except ET.ParseError as e:
            raise NormalizationError(f"Invalid XML format: {e}")
        except Exception as e:
            raise NormalizationError(f"Error normalizing XML: {e}")

    @staticmethod
    def _xml_to_dict(element):
        """
        Convert an XML element into a dictionary.

        Args:
            element (xml.etree.ElementTree.Element): XML element.

        Returns:
            dict: Dictionary representation of the XML element.
        """
        # Convert element's children to a dictionary
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                child_repr = NormalizeXML._xml_to_dict(child)

                # Handle repeated tags as lists
                if child.tag in child_dict:
                    if not isinstance(child_dict[child.tag], list):
                        child_dict[child.tag] = [child_dict[child.tag]]
                    child_dict[child.tag].append(child_repr[child.tag])
                else:
                    child_dict.update(child_repr)

            # Include element's attributes and children
            element_data = {"attributes": element.attrib, **child_dict}
        else:
            # Leaf node
            element_data = {"attributes": element.attrib, "value": element.text.strip() if element.text else None}

        return {element.tag: element_data}
