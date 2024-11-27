from core.DataTypes.Common import DataType
from core.DataTypes.Null import BaseNullType
from datetime import datetime, date, time, timedelta
from typing import Any


class TemporalType(DataType):
    """Base class for temporal types."""
    def is_temporal(self) -> bool:
        return True

    def is_compatible(self, other: "DataType") -> bool:
        """Check compatibility with other temporal types."""
        return isinstance(other, TemporalType)

    def cast(self, value: Any) -> Any:
        """Base cast method; should be overridden by subclasses."""
        raise NotImplementedError("Subclasses should implement casting logic.")


class DateType(TemporalType):
    """Represents date data types."""
    def __repr__(self):
        return "DateType"

    def cast(self, value: Any) -> date:
        """Cast value to a date."""
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise TypeError(f"Cannot cast {value} to DateType")
        raise TypeError(f"Cannot cast {value} to DateType")


class DatetimeType(TemporalType):
    """Represents datetime data types."""
    def __repr__(self):
        return "DatetimeType"

    def cast(self, value: Any) -> datetime:
        """Cast value to a datetime."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    raise TypeError(f"Cannot cast {value} to DatetimeType")
        raise TypeError(f"Cannot cast {value} to DatetimeType")


class TimeType(TemporalType):
    """Represents time data types."""
    def __repr__(self):
        return "TimeType"

    def cast(self, value: Any) -> time:
        """Cast value to a time."""
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%H:%M:%S").time()
            except ValueError:
                raise TypeError(f"Cannot cast {value} to TimeType")
        raise TypeError(f"Cannot cast {value} to TimeType")


class DurationType(TemporalType):
    """Represents duration data types."""
    def __repr__(self):
        return "DurationType"

    def cast(self, value: Any) -> timedelta:
        """Cast value to a timedelta."""
        if isinstance(value, timedelta):
            return value
        if isinstance(value, str):
            try:
                hours, minutes, seconds = map(int, value.split(":"))
                return timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                raise TypeError(f"Cannot cast {value} to DurationType")
        raise TypeError(f"Cannot cast {value} to DurationType")


class TemporalNullType(BaseNullType):
    """Represents a null value for temporal types."""
    def __repr__(self):
        return "TemporalNullType"

    def is_temporal(self) -> bool:
        return True

    def cast(self, value: Any) -> None:
        """Casting to a null type always returns None."""
        return None
