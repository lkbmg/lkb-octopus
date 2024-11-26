from decimal import Decimal, InvalidOperation
from typing import Any, List, Dict
from datetime import datetime, date, time, timedelta
from core.Common import DataType
from core.Exceptions import DataTypeError, ConversionError
from core.DataTypes.Types import (
    NestedType, ListType, StructType, NestedNullType, 
    NumericType, IntegerType, FloatType, DecimalType, NumericNullType, 
    TemporalType, DateType, DatetimeType, TimeType, DurationType, TemporalNullType,
    CategoricalType, BooleanType, StringType, BinaryType, CategoricalNullType
)

class SchemaHelper:
    """Utility class for shared parsing logic."""
    
    @staticmethod
    def is_integer(value: str) -> bool:
        return value.isdigit()
    
    @staticmethod
    def is_decimal(value: str) -> bool:
        try:
            Decimal(value)
            return True
        except InvalidOperation:
            return False
    
    @staticmethod
    def is_datetime(value: str) -> bool:
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
    """Class for inferring data types and schemas from raw data."""

    @staticmethod
    def infer_type(data: Any) -> DataType:
        """
        Infer the DataType for a single element.

        Args:
            data (Any): The element for which to infer the type.

        Returns:
            DataType: The inferred DataType.
        """
        if data is None:
            return NestedNullType()
        elif isinstance(data, bool):
            return BooleanType()
        elif isinstance(data, int):
            return IntegerType()
        elif isinstance(data, float):
            return NumericNullType() if data != data else FloatType()  # NaN handling
        elif isinstance(data, Decimal):
            return DecimalType()
        elif isinstance(data, str):
            if SchemaHelper.is_integer(data):
                return IntegerType()
            if SchemaHelper.is_decimal(data):
                return DecimalType()
            if SchemaHelper.is_datetime(data):
                return DatetimeType()
            return StringType()
        elif isinstance(data, date) and not isinstance(data, datetime):
            return DateType()
        elif isinstance(data, datetime):
            return DatetimeType()
        elif isinstance(data, list):
            element_type = SchemaInference._unify_types([SchemaInference.infer_type(el) for el in data])
            return ListType(element_type)
        elif isinstance(data, dict):
            fields = {k: SchemaInference.infer_type(v) for k, v in data.items()}
            return StructType(fields)
        else:
            raise DataTypeError(f"Unsupported data type: {type(data)}")

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
    def _unify_types(types: List[DataType]) -> DataType:
        unique_types = list(set(types))

        if len(unique_types) == 1:
            return unique_types[0]

        # Handle null types
        null_types = [NestedNullType(), NumericNullType(), TemporalNullType(), CategoricalNullType()]
        non_null_types = [t for t in unique_types if t not in null_types]
        if len(non_null_types) == 1:
            return non_null_types[0]

        # Handle mixed list types
        if all(isinstance(t, ListType) for t in unique_types):
            inner_types = [t.inner_type for t in unique_types if not isinstance(t.inner_type, NestedNullType)]
            unified_inner = SchemaInference._unify_types(inner_types) if inner_types else NestedNullType()
            return ListType(unified_inner)

        # Handle nested structs
        if all(isinstance(t, StructType) for t in unique_types):
            unified_fields = {}
            all_fields = [t.fields for t in unique_types]
            field_keys = set(k for fields in all_fields for k in fields.keys())
            for key in field_keys:
                field_types = [fields[key] for fields in all_fields if key in fields]
                unified_fields[key] = SchemaInference._unify_types(field_types)
            return StructType(unified_fields)

        # Fallback to StringType for mixed types
        return StringType()

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
