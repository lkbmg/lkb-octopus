from typing import Any
from core.DataTypes.Types import DataType, NestedNullType, StringType, NumericType
from core.Exceptions import NormalizationError


class MissingHandler:
    """
    Utility class for handling missing values.
    """

    NULL_VALUES = {None, "", "NULL", "null", "N/A", "n/a", "-", "--"}

    @staticmethod
    def is_null(value: Any) -> bool:
        """
        Determine if a value should be considered as 'missing' or null.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is null, False otherwise.
        """
        if isinstance(value, str):
            return value.strip() in MissingHandler.NULL_VALUES
        return value is None

    @staticmethod
    def fill_nulls(data: Any, fill_value: Any) -> Any:
        """
        Replace null values in data with a specified fill value.

        Args:
            data (Any): The data to process.
            fill_value (Any): The value to use as a replacement for nulls.

        Returns:
            Any: Data with nulls replaced.
        """
        if isinstance(data, dict):
            return {k: MissingHandler.fill_nulls(v, fill_value) for k, v in data.items()}
        if isinstance(data, list):
            return [MissingHandler.fill_nulls(v, fill_value) for v in data]
        return fill_value if MissingHandler.is_null(data) else data

    @staticmethod
    def detect_null_type(value: Any) -> DataType:
        """
        Detect the null-compatible type of a value.

        Args:
            value (Any): The value to check.

        Returns:
            DataType: The detected null-compatible DataType.
        """
        if MissingHandler.is_null(value):
            return NestedNullType()
        if isinstance(value, str):
            return StringType()
        if isinstance(value, (int, float)):
            return NumericType()
        raise NormalizationError(f"Unknown type for value: {value}")
