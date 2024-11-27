from typing import Any
from datetime import timedelta
from core.DataTypes.Types import (
    DataType, NumericType, IntegerType, FloatType, DecimalType, NumericNullType,
    TemporalType, DateType, DatetimeType, TimeType, DurationType, TemporalNullType,
    CategoricalType, BooleanType, StringType, BinaryType, CategoricalNullType,
    ListType, StructType, NestedNullType
)
from core.Exceptions import DataTypeError, ConversionError


class TypeCast:
    """Utility class for type casting and promotion."""
    
    @staticmethod
    def promote_types(type1: DataType, type2: DataType) -> DataType:
        """
        Promote two data types to a common type, supporting nested structures.
        """
        # Handle null types
        if isinstance(type1, (NumericNullType, TemporalNullType, CategoricalNullType, NestedNullType)):
            return type2
        if isinstance(type2, (NumericNullType, TemporalNullType, CategoricalNullType, NestedNullType)):
            return type1

        # Numeric promotion
        if isinstance(type1, NumericType) and isinstance(type2, NumericType):
            if isinstance(type1, DecimalType) or isinstance(type2, DecimalType):
                return DecimalType()
            if isinstance(type1, FloatType) or isinstance(type2, FloatType):
                return FloatType()
            return IntegerType()

        # Temporal promotion
        if isinstance(type1, TemporalType) and isinstance(type2, TemporalType):
            if isinstance(type1, DurationType) or isinstance(type2, DurationType):
                return DurationType()
            if isinstance(type1, DatetimeType) or isinstance(type2, DatetimeType):
                return DatetimeType()
            if isinstance(type1, DateType) or isinstance(type2, DateType):
                return DateType()
            return TimeType()

        # Categorical promotion
        if isinstance(type1, CategoricalType) and isinstance(type2, CategoricalType):
            if isinstance(type1, StringType) or isinstance(type2, StringType):
                return StringType()
            if isinstance(type1, BooleanType) and isinstance(type2, BooleanType):
                return BooleanType()
            return CategoricalType()

        # Promote ListType
        if isinstance(type1, ListType) and isinstance(type2, ListType):
            promoted_inner = TypeCast.promote_types(type1.inner_type, type2.inner_type)
            return ListType(promoted_inner)

        # Promote StructType
        if isinstance(type1, StructType) and isinstance(type2, StructType):
            unified_fields = {
                key: TypeCast.promote_types(type1.fields.get(key, NestedNullType()),
                                            type2.fields.get(key, NestedNullType()))
                for key in set(type1.fields) | set(type2.fields)
            }
            return StructType(unified_fields)

        # Binary type promotion
        if isinstance(type1, BinaryType) and isinstance(type2, BinaryType):
            return BinaryType()

        # Unsupported types
        raise DataTypeError(f"Cannot promote types: {type1} and {type2}")

    @staticmethod
    def cast_value(value: Any, target_type: DataType) -> Any:
        """
        Cast a value to a specified data type, supporting nested structures.
        """
        if value is None:
            if isinstance(target_type, (NumericType, TemporalType, CategoricalType, ListType, StructType)):
                return None
            raise ConversionError(f"Cannot cast None to {target_type}")

        if isinstance(target_type, IntegerType):
            return int(value)
        if isinstance(target_type, FloatType):
            return float(value)
        if isinstance(target_type, DecimalType):
            from decimal import Decimal
            return Decimal(value)
        if isinstance(target_type, BooleanType):
            if isinstance(value, str):
                if value.lower() in {"true", "1"}:
                    return True
                if value.lower() in {"false", "0"}:
                    return False
            return bool(value)
        if isinstance(target_type, StringType):
            return str(value)
        if isinstance(target_type, DateType):
            from datetime import datetime
            return datetime.strptime(value, "%Y-%m-%d").date()
        if isinstance(target_type, DatetimeType):
            from datetime import datetime
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if isinstance(target_type, ListType):
            if not isinstance(value, list):
                raise ConversionError(f"Cannot cast {value} to ListType")
            return [TypeCast.cast_value(item, target_type.inner_type) for item in value]
        if isinstance(target_type, StructType):
            if not isinstance(value, dict):
                raise ConversionError(f"Cannot cast {value} to StructType")
            return {
                key: TypeCast.cast_value(value.get(key, None), field_type)
                for key, field_type in target_type.fields.items()
            }

        raise ConversionError(f"Unsupported target type: {target_type}")

    @staticmethod
    def can_cast(source_type: DataType, target_type: DataType) -> bool:
        """
        Check if a value of the source type can be cast to the target type.

        Args:
            source_type (DataType): The source data type.
            target_type (DataType): The target data type.

        Returns:
            bool: True if casting is possible, False otherwise.
        """
        try:
            TypeCast.promote_types(source_type, target_type)
            return True
        except DataTypeError:
            return False
