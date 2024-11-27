# Common.py
from abc import ABC, abstractmethod
from typing import Any


class ABCType(ABC):
    """Abstract base class for all data types."""

    @abstractmethod
    def is_numeric(self) -> bool:
        pass

    @abstractmethod
    def is_temporal(self) -> bool:
        pass

    @abstractmethod
    def is_categorical(self) -> bool:
        pass

    @abstractmethod
    def is_nested(self) -> bool:
        pass

    @abstractmethod
    def is_compatible(self, other: "ABCType") -> bool:
        pass


class DataType(ABCType):
    """Base class for all data types."""

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self))

    def __hash__(self) -> int:
        """Hash based on the class name."""
        return hash(self.__class__.__name__)

    def is_numeric(self) -> bool:
        """Default implementation for subclasses."""
        return False

    def is_temporal(self) -> bool:
        """Default implementation for subclasses."""
        return False

    def is_categorical(self) -> bool:
        """Default implementation for subclasses."""
        return False

    def is_nested(self) -> bool:
        """Default implementation for subclasses."""
        return False

    def is_compatible(self, other: "ABCType") -> bool:
        """Check if this type is compatible with another type."""
        return isinstance(other, type(self))
