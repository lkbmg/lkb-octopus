# Factory.py
from core.DataTypes.Types import IntegerType, FloatType, DecimalType, NumericNullType, \
    BooleanType, StringType, BinaryType, CategoricalNullType, ListType, StructType, NestedNullType, \
    DateType, DatetimeType, TimeType, DurationType, TemporalNullType 

import numpy as np
from datetime import datetime, date, time, timedelta
from decimal import Decimal as PyDecimal

class TypeFactory:
    """Factory to map native types to DataType instances."""
    MAPPINGS = {
        "python": {
            int: IntegerType,
            float: FloatType,
            bool: BooleanType,
            str: StringType,
            list: lambda: ListType(NestedNullType()),
            dict: lambda: StructType({}),
            type(None): CategoricalNullType,
            datetime: DatetimeType,
            date: DateType,
            time: TimeType,
            timedelta: DurationType,
            PyDecimal: DecimalType,
        },
        "numpy": {
            np.int32: IntegerType,
            np.int64: IntegerType,
            np.float32: FloatType,
            np.float64: FloatType,
            np.bool_: BooleanType,
            np.object_: StringType,
            np.str_: StringType,
            np.bytes_: BinaryType,
            np.datetime64: DatetimeType,
        },
        "sql": {
            "bigint": FloatType,
            "binary": BinaryType,
            "bit": BooleanType,
            "char": StringType,
            "date": DateType,
            "datetime": DatetimeType,
            "float": FloatType,
            "nchar": StringType,
            "nvarchar": StringType,
            "nvarchar(max)": StringType,
            "real": FloatType,
            "smalldatetime": DatetimeType,
            "smallint": IntegerType,
            "tinyint": IntegerType,
            "uniqueidentifier": StringType,
            "varbinary": BinaryType,
            "varbinary(max)": BinaryType,
            "varchar(n)": StringType,
            "varchar(max)": StringType,
        },
    }

    @classmethod
    def register_mapping(cls, category, native_type, data_type):
        """
        Dynamically register a new type mapping.

        Args:
            category (str): Category of the type system (e.g., 'python', 'numpy').
            native_type (Any): The native type (e.g., `int`, `np.float32`).
            data_type (DataType): The corresponding `DataType` instance.
        """
        if category not in cls.MAPPINGS:
            cls.MAPPINGS[category] = {}
        cls.MAPPINGS[category][native_type] = data_type

    @classmethod
    def from_python(cls, input_type):
        """Map Python and NumPy native types to DataType."""
        for category in ["python", "numpy"]:
            if input_type in cls.MAPPINGS[category]:
                dtype = cls.MAPPINGS[category][input_type]
                return dtype() if callable(dtype) else dtype

        raise ValueError(f"Unsupported type: {input_type}. Known categories: {list(cls.MAPPINGS.keys())}")