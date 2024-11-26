# Exceptions.py

class BaseError(Exception):
    """Base exception for the application."""

class DataTypeError(BaseError):
    """Base exception for data type operations."""

class UnsupportedTypeError(DataTypeError):
    """Raised when an unsupported type is encountered."""

class ConversionError(DataTypeError):
    """Raised when a conversion fails."""

class HttpRequestError(BaseError):
    """Raised when an HTTP request fails."""
    def __init__(self, url, status_code, message):
        super().__init__(f"Request to '{url}' failed with status code {status_code}: {message}")
        self.url = url
        self.status_code = status_code
        self.message = message

class CommandExecutionError(BaseError):
    """Custom exception for command execution errors."""
    def __init__(self, command, returncode, stderr):
        stderr = stderr.decode('utf-8', errors='replace') if isinstance(stderr, bytes) else stderr
        super().__init__(f"Command '{' '.join(command)}' failed with exit code {returncode}. Error: {stderr}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr

class ValidationError(BaseError):
    """Raised when a validation check fails."""

class NormalizationError(BaseError):
    """Raised when data normalization fails."""
