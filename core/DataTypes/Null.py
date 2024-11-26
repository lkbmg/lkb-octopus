from core.Common import DataType

class BaseNullType(DataType):
    """Base class for all null types."""
    def is_compatible(self, other: "DataType") -> bool:
        return True  # Null types are compatible with any type
