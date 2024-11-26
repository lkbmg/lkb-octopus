from abc import ABC, abstractmethod


class ABCNormalizer(ABC):
    """
    Abstract base class to enforce input normalization for adapters.
    """

    @staticmethod
    def normalize_input(data):
        """
        Normalize input to a standard list of dictionaries.

        Args:
            data (dict or list[dict]): The data to normalize.

        Returns:
            list[dict]: Normalized list of dictionaries.

        Raises:
            ValueError: If the input is not a dict or list[dict].
        """
        if isinstance(data, dict):
            return [data]  # Wrap single dict in a list
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            return data
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries.")

    @abstractmethod
    def from_normalized(self, data):
        """
        Abstract method for converting normalized input to the adapter's output.
        Must be implemented by subclasses.
        """
        pass
