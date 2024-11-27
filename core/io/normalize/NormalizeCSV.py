import csv
from io import StringIO
from core.io.normalize.NormalizeBase import NormalizeBase
from core.Exceptions import NormalizationError

class NormalizeCSV(NormalizeBase):
    """
    Normalization logic for CSV data.
    """

    @staticmethod
    def normalize(data):
        """
        Normalize CSV input into a standardized list of dictionaries.

        Args:
            data (str): CSV string.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            NormalizationError: If normalization fails.
        """
        try:
            if not isinstance(data, str):
                raise NormalizationError("Expected CSV input as a string.")
            reader = csv.DictReader(StringIO(data))
            return [row for row in reader]
        except Exception as e:
            raise NormalizationError(f"Error normalizing CSV: {e}")
