from decimal import Decimal, InvalidOperation
from typing import Any, List, Dict
from datetime import datetime, date, time, timedelta
from core.DataTypes.Common import DataType
from core.Exceptions import DataTypeError, ConversionError
from core.DataTypes.Types import (
    NestedType, ListType, StructType, NestedNullType, 
    NumericType, IntegerType, FloatType, DecimalType, NumericNullType, 
    TemporalType, DateType, DatetimeType, TimeType, DurationType, TemporalNullType,
    CategoricalType, BooleanType, StringType, BinaryType, CategoricalNullType
)

class SchemaHelper:
    """Utility class for type checks and conversions."""
    
    @staticmethod
    def is_integer(value: Any) -> bool:
        """Check if a value is an integer."""
        try:
            return isinstance(value, int) and not isinstance(value, bool)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_float(value: Any) -> bool:
        """Check if a value is a float."""
        try:
            return isinstance(value, float) or isinstance(value, Decimal)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_decimal(value: Any) -> bool:
        """Check if a value is a Decimal."""
        try:
            Decimal(value)
            return True
        except InvalidOperation:
            return False

    @staticmethod
    def is_datetime(value: str) -> bool:
        """Check if a value is a datetime string."""
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
        for fmt in formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def parse_datetime(value: str) -> datetime:
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ConversionError(f"Invalid datetime format: {value}")

    @staticmethod
    def parse_date(value: str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ConversionError(f"Invalid date format: {value}")


class SchemaInference:
    """Class for inferring data types."""

    @staticmethod
    def infer_type(value: Any) -> DataType:
        """
        Infer the type of a single value.
        """
        if value is None:
            return NestedNullType()
        if isinstance(value, bool):
            return BooleanType()
        if SchemaHelper.is_integer(value):
            return IntegerType()
        if SchemaHelper.is_float(value):
            return FloatType()
        if SchemaHelper.is_decimal(value):
            return DecimalType()
        if isinstance(value, str):
            if SchemaHelper.is_datetime(value):
                return DatetimeType()
            return StringType()
        if isinstance(value, date):
            return DateType()
        if isinstance(value, list):
            element_types = [SchemaInference.infer_type(el) for el in value]
            unified_type = SchemaInference._unify_types(element_types)
            return ListType(unified_type)
        if isinstance(value, dict):
            fields = {k: SchemaInference.infer_type(v) for k, v in value.items()}
            return StructType(fields)
        raise ValueError(f"Cannot infer type for value: {value}")

    @staticmethod
    def _unify_types(types: List[DataType]) -> DataType:
        """
        Combine a list of types into a single type.
        """
        unique_types = list(set(types))

        if len(unique_types) == 1:
            return unique_types[0]

        # Handle numeric compatibility
        if all(isinstance(t, NumericType) for t in unique_types):
            return FloatType()

        # Handle string fallback for mixed types
        return StringType()

    @staticmethod
    def infer_schema(data: Any) -> DataType:
        """
        Infer the schema for complex or nested data structures.

        Args:
            data (Any): The data structure to infer the schema for.

        Returns:
            DataType: The inferred schema.
        """
        if isinstance(data, list):
            if not data:
                return ListType(NestedNullType())
            element_schemas = [SchemaInference.infer_schema(el) for el in data]
            unified_type = SchemaInference._unify_types(element_schemas)
            return ListType(unified_type)
        elif isinstance(data, dict):
            if not data:
                return StructType({})
            fields = {key: SchemaInference.infer_schema(value) for key, value in data.items()}
            return StructType(fields)
        else:
            return SchemaInference.infer_type(data)

    @staticmethod
    def describe_schema(schema: DataType) -> Dict[str, Any]:
        """
        Provide a descriptive representation of a schema.

        Args:
            schema (DataType): The schema to describe.

        Returns:
            Dict[str, Any]: A dictionary representation of the schema.
        """
        if isinstance(schema, StructType):
            return {"type": "struct", "fields": {k: SchemaInference.describe_schema(v) for k, v in schema.fields.items()}}
        elif isinstance(schema, ListType):
            return {"type": "list", "element": SchemaInference.describe_schema(schema.inner_type)}
        else:
            return {"type": schema.__class__.__name__}
