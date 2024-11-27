from abc import ABC, abstractmethod

class NormalizeBase(ABC):
    """
    Abstract base class for format-specific normalization.
    """

    @staticmethod
    @abstractmethod
    def normalize(data):
        """
        Normalize input data to a standardized format.

        Args:
            data: Input data specific to the format.

        Returns:
            Normalized data.
        """
        pass
