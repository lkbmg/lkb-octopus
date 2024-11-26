from typing import Dict
from core.Common import DataType
from core.DataTypes.Null import BaseNullType

class NestedType(DataType):
    """Base class for nested types."""

class ListType(NestedType):
    """Represents list data types."""
    def __init__(self, inner_type: "DataType"):  # Use string annotation to defer import
        self.inner_type = inner_type

    def __repr__(self) -> str:
        return f"ListType({repr(self.inner_type)})"


class StructType(NestedType):
    """Represents struct data types with named fields."""
    def __init__(self, fields: Dict[str, "DataType"]):  # Use string annotation
        self.fields = fields

    def __repr__(self) -> str:
        field_str = ', '.join([f"{k}: {v}" for k, v in self.fields.items()])
        return f"StructType({field_str})"


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
