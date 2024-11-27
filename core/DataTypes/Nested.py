from typing import Dict, List, Any
from core.DataTypes.Common import DataType
from core.DataTypes.Null import BaseNullType


class NestedType(DataType):
    """Base class for nested types."""

    def is_nested(self) -> bool:
        return True

    def is_compatible(self, other: "DataType") -> bool:
        """Check compatibility with other nested types."""
        return isinstance(other, NestedType)


class ListType(NestedType):
    """Represents list data types."""
    def __init__(self, inner_type: "DataType"):  # Use string annotation to defer import
        self.inner_type = inner_type

    def __repr__(self) -> str:
        return f"ListType({repr(self.inner_type)})"

    def validate(self, value: Any) -> bool:
        """Validate that the value matches the list schema."""
        if not isinstance(value, list):
            return False
        return all(isinstance(item, self.inner_type.__class__) for item in value)

    def cast(self, value: Any) -> List:
        """Cast the value to a list with elements of the inner type."""
        if not isinstance(value, list):
            raise TypeError(f"Cannot cast {value} to ListType({self.inner_type})")
        return [self.inner_type.cast(item) for item in value]


class StructType(NestedType):
    """Represents struct data types with named fields."""
    def __init__(self, fields: Dict[str, "DataType"]):  # Use string annotation
        self.fields = fields

    def __repr__(self) -> str:
        field_str = ', '.join([f"{k}: {v}" for k, v in self.fields.items()])
        return f"StructType({field_str})"

    def validate(self, value: Any) -> bool:
        """Validate that the value matches the struct schema."""
        if not isinstance(value, dict):
            return False
        for key, field_type in self.fields.items():
            if key in value and not isinstance(value[key], field_type.__class__):
                return False
        return True

    def cast(self, value: Any) -> Dict[str, Any]:
        """Cast the value to a struct with the defined schema."""
        if not isinstance(value, dict):
            raise TypeError(f"Cannot cast {value} to StructType")
        casted_value = {}
        for key, field_type in self.fields.items():
            if key in value:
                casted_value[key] = field_type.cast(value[key])
            else:
                casted_value[key] = None  # Default missing fields to None
        return casted_value


class NestedNullType(BaseNullType):
    """Represents a null or NaN value for nested types."""
    def __repr__(self):
        return "NestedNullType"

    def is_numeric(self) -> bool:
        return False

    def is_temporal(self) -> bool:
        return False

    def is_categorical(self) -> bool:
        return False

    def is_nested(self) -> bool:
        return True

    def cast(self, value: Any) -> None:
        """Casting to a null type always returns None."""
        return None
