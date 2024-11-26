from core.Common import DataType
from core.DataTypes.Null import BaseNullType

class NumericType(DataType):
    """Base class for numeric types."""
    def is_numeric(self) -> bool:
        return True


class IntegerType(NumericType):
    """Represents integer data types."""


class FloatType(NumericType):
    """Represents floating-point data types."""


class DecimalType(NumericType):
    """Represents arbitrary precision decimal data types."""


class NumericNullType(BaseNullType):
    """Represents a null value for numeric types."""
    def __repr__(self):
        return "NumericNullType"

    def is_numeric(self) -> bool:
        return True
