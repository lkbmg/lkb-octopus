from core.Common import DataType
from core.DataTypes.Null import BaseNullType


class TemporalType(DataType):
    """Base class for temporal types."""
    def is_temporal(self) -> bool:
        return True


class DateType(TemporalType):
    """Represents date data types."""


class DatetimeType(TemporalType):
    """Represents datetime data types."""


class TimeType(TemporalType):
    """Represents time data types."""


class DurationType(TemporalType):
    """Represents duration data types."""


class TemporalNullType(BaseNullType):
    """Represents a null value for temporal types."""
    def __repr__(self):
        return "TemporalNullType"

    def is_temporal(self) -> bool:
        return True
