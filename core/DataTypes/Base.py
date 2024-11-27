from typing import Any, List, Dict, Union
from core.DataTypes.Types import (
    DataType, NumericType, IntegerType, FloatType, DecimalType, TemporalType,
    DateType, DatetimeType, ListType, StructType, CategoricalType, StringType
)
from core.DataTypes.Cast import TypeCast
from core.Exceptions import DataTypeError, ConversionError


class BaseArray:
    """
    Array-like abstraction for managing data with custom DataTypes.

    Attributes:
        data (List[Any]): The raw data stored in the array.
        dtype (DataType): The DataType of the array elements.
    """

    def __init__(self, data: List[Any], dtype: DataType):
        self.dtype = dtype
        self.data = self._validate_data(data, dtype)

    def _validate_data(self, data: List[Any], dtype: DataType) -> List[Any]:
        """
        Validate that all elements in `data` conform to `dtype`.

        Args:
            data (List[Any]): The input data to validate.
            dtype (DataType): The expected data type.

        Returns:
            List[Any]: The validated data.
        """
        for item in data:
            if not self._is_valid_type(item, dtype):
                raise DataTypeError(f"Invalid data: {item} does not match type {dtype}.")
        return data

    def _is_valid_type(self, value: Any, dtype: DataType) -> bool:
        """
        Check if a value matches the expected DataType.

        Args:
            value (Any): The value to check.
            dtype (DataType): The expected DataType.

        Returns:
            bool: Whether the value matches the DataType.
        """
        if value is None:
            return True  # Allow None as a placeholder
        return isinstance(value, dtype.type_cls)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int | slice) -> Union[Any, "BaseArray"]:
        """
        Retrieve an item or slice of the array.

        Returns:
            BaseArray if slice, otherwise individual element.
        """
        if isinstance(index, slice):
            return BaseArray(self.data[index], self.dtype)
        return self.data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set the value at a specific index.
        """
        if not self._is_valid_type(value, self.dtype):
            raise DataTypeError(f"Invalid value: {value} does not match type {self.dtype}.")
        self.data[index] = value

    def __repr__(self) -> str:
        return f"BaseArray(data={self.data}, dtype={self.dtype})"

    def isna(self) -> List[bool]:
        """
        Check for missing (None) values.
        """
        return [x is None for x in self.data]

    def fillna(self, value: Any) -> None:
        """
        Fill missing values with a specified value.
        """
        if not self._is_valid_type(value, self.dtype):
            raise DataTypeError(f"Invalid fill value: {value} does not match type {self.dtype}.")
        self.data = [value if x is None else x for x in self.data]

    def apply(self, func: Any) -> "BaseArray":
        """
        Apply a function element-wise.

        Args:
            func (Callable): Function to apply to each element.

        Returns:
            BaseArray: A new BaseArray with the transformed data.
        """
        new_data = [func(x) if x is not None else None for x in self.data]
        return BaseArray(new_data, self.dtype)

    def astype(self, target_type: DataType) -> "BaseArray":
        """
        Cast the array to a specified DataType.

        Args:
            target_type (DataType): The target DataType.

        Returns:
            BaseArray: A new BaseArray with the casted data.
        """
        try:
            new_data = [TypeCast.cast_value(x, target_type) for x in self.data]
            return BaseArray(new_data, target_type)
        except ConversionError as e:
            raise DataTypeError(f"Cannot cast array to {target_type}: {e}")


class AdvancedBaseArray(BaseArray):
    """
    Extended BaseArray with support for advanced DataTypes like StructType and ListType.
    """

    def _is_valid_type(self, value: Any, dtype: DataType) -> bool:
        """
        Extended type validation for advanced types.

        Args:
            value (Any): The value to check.
            dtype (DataType): The expected DataType.

        Returns:
            bool: Whether the value matches the DataType.
        """
        if value is None:
            return True

        if isinstance(dtype, StructType):
            if not isinstance(value, dict):
                return False
            for key, sub_type in dtype.fields.items():
                if key in value:
                    if not self._is_valid_type(value[key], sub_type):
                        return False
            return True

        if isinstance(dtype, ListType):
            if not isinstance(value, list):
                return False
            return all(self._is_valid_type(item, dtype.inner_type) for item in value)

        return super()._is_valid_type(value, dtype)

