import json
from typing import Optional
from core.io.normalize.NormalizeBase import NormalizeBase
from core.Exceptions import NormalizationError
from core.io.normalize.NormalizeBase import NormalizeBase
from core.io.normalize.NormalizeUtils import flatten_structure
from core.Exceptions import NormalizationError

# core/io/normalize/NormalizeJSON.py



class NormalizeJSON(NormalizeBase):
    """
    Normalization logic for JSON data.
    """

    @staticmethod
    def normalize(data, flatten: bool = False, sep: str = "_", max_level: Optional[int] = None):
        """
        Normalize JSON input into a standardized structure.

        Args:
            data (str, dict, or list[dict]): JSON data.
            flatten (bool): Whether to flatten the structure.
            sep (str): Separator for flattened keys.
            max_level (Optional[int]): Maximum depth for flattening.

        Returns:
            dict or list[dict]: Normalized data.

        Raises:
            NormalizationError: If normalization fails.
        """
        try:
            if flatten:
                return flatten_structure(data, sep=sep, max_level=max_level)
            else:
                # Original normalization logic
                if isinstance(data, str):
                    data = json.loads(data)
                if isinstance(data, dict):
                    return [data]
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    return data
                raise NormalizationError("Expected a dict, list of dicts, or JSON string.")
        except Exception as e:
            raise NormalizationError(f"Error normalizing JSON: {e}")

