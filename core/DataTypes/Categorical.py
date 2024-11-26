#Categorical.py
from core.Common import DataType
from core.DataTypes.Null import BaseNullType

class CategoricalType(DataType):
    """Base class for categorical types."""
    def is_categorical(self) -> bool:
        return True


class BooleanType(CategoricalType):
    """Represents boolean data types."""


class StringType(CategoricalType):
    """Represents string data types."""


class BinaryType(CategoricalType):
    """Represents binary data types."""


class CategoricalNullType(BaseNullType):
    """Represents a null value for categorical types."""
    def __repr__(self):
        return "CategoricalNullType"

    def is_categorical(self) -> bool:
        return True
