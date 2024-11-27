from typing import cast, Type
from core.DataTypes.Types import (
    DataType, NumericType, IntegerType, FloatType, DecimalType, NumericNullType,
    TemporalType, DateType, DatetimeType, TimeType, DurationType, TemporalNullType,
    CategoricalType, BooleanType, StringType, BinaryType, CategoricalNullType,
    ListType, StructType, NestedType, BaseNullType, NestedNullType
)


def create_datatype_abc(name: str, attr: str, comp: set) -> Type:
    """
    Create an abstract base class (ABC) for data types.

    Args:
        name (str): The name of the ABC.
        attr (str): The attribute to check on the instance.
        comp (set): The set of values that the attribute can take to qualify as this type.

    Returns:
        Type: The generated ABC class.
    """
    def _check(inst) -> bool:
        return getattr(inst, attr, "_typ") in comp

    @classmethod
    def _instancecheck(cls, inst) -> bool:
        return _check(inst) and not isinstance(inst, type)

    @classmethod
    def _subclasscheck(cls, inst) -> bool:
        if not isinstance(inst, type):
            raise TypeError("issubclass() arg 1 must be a class")
        return _check(inst)

    dct = {"__instancecheck__": _instancecheck, "__subclasscheck__": _subclasscheck}
    meta = type("ABCBase", (type,), dct)
    return meta(name, (), dct)


# Define ABCs for the various DataTypes
ABCNumericType = cast(
    "Type[NumericType]",
    create_datatype_abc("ABCNumericType", "_typ", {"numeric", "integer", "float", "decimal"}),
)
ABCIntegerType = cast(
    "Type[IntegerType]",
    create_datatype_abc("ABCIntegerType", "_typ", {"integer"}),
)
ABCFloatType = cast(
    "Type[FloatType]",
    create_datatype_abc("ABCFloatType", "_typ", {"float"}),
)
ABCDecimalType = cast(
    "Type[DecimalType]",
    create_datatype_abc("ABCDecimalType", "_typ", {"decimal"}),
)
ABCNumericNullType = cast(
    "Type[NumericNullType]",
    create_datatype_abc("ABCNumericNullType", "_typ", {"numeric_null"}),
)

ABCTemporalType = cast(
    "Type[TemporalType]",
    create_datatype_abc("ABCTemporalType", "_typ", {"temporal", "date", "datetime", "time", "duration"}),
)
ABCDateType = cast(
    "Type[DateType]",
    create_datatype_abc("ABCDateType", "_typ", {"date"}),
)
ABCDatetimeType = cast(
    "Type[DatetimeType]",
    create_datatype_abc("ABCDatetimeType", "_typ", {"datetime"}),
)
ABCDurationType = cast(
    "Type[DurationType]",
    create_datatype_abc("ABCDurationType", "_typ", {"duration"}),
)

ABCCategoricalType = cast(
    "Type[CategoricalType]",
    create_datatype_abc("ABCCategoricalType", "_typ", {"categorical", "string", "boolean", "binary"}),
)
ABCStringType = cast(
    "Type[StringType]",
    create_datatype_abc("ABCStringType", "_typ", {"string"}),
)
ABCBooleanType = cast(
    "Type[BooleanType]",
    create_datatype_abc("ABCBooleanType", "_typ", {"boolean"}),
)
ABCBinaryType = cast(
    "Type[BinaryType]",
    create_datatype_abc("ABCBinaryType", "_typ", {"binary"}),
)

ABCNestedType = cast(
    "Type[NestedType]",
    create_datatype_abc("ABCNestedType", "_typ", {"nested", "list", "struct"}),
)
ABCListType = cast(
    "Type[ListType]",
    create_datatype_abc("ABCListType", "_typ", {"list"}),
)
ABCStructType = cast(
    "Type[StructType]",
    create_datatype_abc("ABCStructType", "_typ", {"struct"}),
)
ABCNullType = cast(
    "Type[BaseNullType]",
    create_datatype_abc("ABCNullType", "_typ", {"null"}),
)

# Optional: A catch-all DataType ABC
ABCDataType = cast(
    "Type[DataType]",
    create_datatype_abc("ABCDataType", "_typ", {
        "numeric", "integer", "float", "decimal", "numeric_null",
        "temporal", "date", "datetime", "time", "duration", "temporal_null",
        "categorical", "string", "boolean", "binary", "categorical_null",
        "nested", "list", "struct", "null"
    }),
)
