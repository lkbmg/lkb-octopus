from core.DataTypes.Common import DataType
from core.DataTypes.Null import BaseNullType
from typing import Any
from decimal import Decimal, InvalidOperation


class NumericType(DataType):
    """Base class for numeric types."""
    def is_numeric(self) -> bool:
        return True

    def is_compatible(self, other: "DataType") -> bool:
        """Check compatibility with other numeric types."""
        return isinstance(other, NumericType)

    def cast(self, value: Any) -> Any:
        """Base cast method; should be overridden by subclasses."""
        raise NotImplementedError("Subclasses should implement casting logic.")


class IntegerType(NumericType):
    """Represents integer data types."""
    def __repr__(self):
        return "IntegerType"

    def cast(self, value: Any) -> int:
        """Cast value to integer."""
        try:
            return int(value)
        except (ValueError, TypeError):
            raise TypeError(f"Cannot cast {value} to IntegerType")


class FloatType(NumericType):
    """Represents floating-point data types."""
    def __repr__(self):
        return "FloatType"

    def cast(self, value: Any) -> float:
        """Cast value to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise TypeError(f"Cannot cast {value} to FloatType")


class DecimalType(NumericType):
    """Represents arbitrary precision decimal data types."""
    def __repr__(self):
        return "DecimalType"

    def cast(self, value: Any) -> Decimal:
        """Cast value to Decimal."""
        try:
            return Decimal(value)
        except InvalidOperation:
            raise TypeError(f"Cannot cast {value} to DecimalType")


class NumericNullType(BaseNullType):
    """Represents a null value for numeric types."""
    def __repr__(self):
        return "NumericNullType"

    def is_numeric(self) -> bool:
        return True

    def cast(self, value: Any) -> None:
        """Casting to a null type always returns None."""
        return None
