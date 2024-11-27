from typing import List, Any
from core.DataTypes.Common import DataType
from core.DataTypes.Null import BaseNullType


class CategoricalType(DataType):
    """Base class for categorical types."""
    def is_categorical(self) -> bool:
        return True


class BooleanType(CategoricalType):
    """Represents boolean data types."""
    def __repr__(self):
        return "BooleanType"

    def validate(self, value: Any) -> bool:
        """Validate that the value is a boolean."""
        return isinstance(value, bool)

    def cast(self, value: Any) -> bool:
        """Cast the value to a boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() in {"true", "1"}:
                return True
            if value.lower() in {"false", "0"}:
                return False
        raise TypeError(f"Cannot cast {value} to BooleanType")


class StringType(CategoricalType):
    """Represents string data types."""
    def __repr__(self):
        return "StringType"

    def validate(self, value: Any) -> bool:
        """Validate that the value is a string."""
        return isinstance(value, str)

    def cast(self, value: Any) -> str:
        """Cast the value to a string."""
        if isinstance(value, str):
            return value
        return str(value)


class BinaryType(CategoricalType):
    """Represents binary data types."""
    def __repr__(self):
        return "BinaryType"

    def validate(self, value: Any) -> bool:
        """Validate that the value is binary (bytes)."""
        return isinstance(value, (bytes, bytearray))

    def cast(self, value: Any) -> bytes:
        """Cast the value to binary (bytes)."""
        if isinstance(value, (bytes, bytearray)):
            return bytes(value)
        if isinstance(value, str):
            return value.encode("utf-8")
        raise TypeError(f"Cannot cast {value} to BinaryType")


class EnumType(CategoricalType):
    """Represents enumerated types."""
    def __init__(self, allowed_values: List[Any]):
        """
        Initialize an EnumType.

        Args:
            allowed_values (List[Any]): List of allowed values for the enumeration.
        """
        self.allowed_values = allowed_values

    def __repr__(self):
        return f"EnumType({self.allowed_values})"

    def validate(self, value: Any) -> bool:
        """Validate that the value is within the allowed enumeration."""
        return value in self.allowed_values

    def cast(self, value: Any) -> Any:
        """Cast the value to one of the allowed enumeration values."""
        if value in self.allowed_values:
            return value
        raise TypeError(f"Cannot cast {value} to EnumType. Allowed values are: {self.allowed_values}")


class CategoricalNullType(BaseNullType):
    """Represents a null value for categorical types."""
    def __repr__(self):
        return "CategoricalNullType"

    def is_categorical(self) -> bool:
        return True

    def cast(self, value: Any) -> None:
        """Casting to a null type always returns None."""
        return None
