from datetime import datetime, date, time, timedelta
from decimal import Decimal, InvalidOperation

from core.Common import DataType
from core.DataTypes.Schema import SchemaHelper
from core.Exceptions import DataTypeError, ConversionError
from core.DataTypes.Types import (
    NestedType, ListType, StructType, NestedNullType, 
    NumericType, IntegerType, FloatType, DecimalType, NumericNullType, 
    TemporalType, DateType, DatetimeType, TimeType, DurationType, TemporalNullType,
    CategoricalType, BooleanType, StringType, BinaryType, CategoricalNullType
)

class ConversionMap:
    """Class for handling type conversions based on inferred schemas."""

    @staticmethod
    def to_python(value, schema):
        if isinstance(schema, IntegerType):
            return int(value)
        if isinstance(schema, FloatType):
            return float(value)
        if isinstance(schema, DecimalType):
            return Decimal(value)
        if isinstance(schema, DatetimeType):
            return SchemaHelper.parse_datetime(value)
        if isinstance(schema, DateType):
            return SchemaHelper.parse_date(value)
        if isinstance(schema, BooleanType):
            return value.lower() == "true"
        if isinstance(schema, StringType):
            return value
        return value  # Fallback for unhandled types

    @staticmethod
    def to_xml(value, schema):
        if isinstance(schema, DatetimeType):
            return value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else str(value)
        if isinstance(schema, IntegerType) or isinstance(schema, FloatType):
            return str(value)
        if isinstance(schema, BooleanType):
            return "true" if value else "false"
        return str(value)  # Fallback for unhandled types
