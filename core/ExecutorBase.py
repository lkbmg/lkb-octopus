#!/usr/bin/env python3
'''
BaseExecutor.py
Written by pollardm
Written: 11/12/24
Description: Base Class for command execution.
'''
from abc import ABC, abstractmethod

class CommandExecutionError(Exception):
    """Custom exception for command execution errors."""
    def __init__(self, command, returncode, stderr):
        stderr = stderr.decode('utf-8', errors='replace') if isinstance(stderr, bytes) else stderr
        super().__init__(f"Command '{' '.join(command)}' failed with exit code {returncode}. Error: {stderr}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr

class BaseExecutor(ABC):
    def __init__(self, binary_path):
        self.binary_path = binary_path

    @abstractmethod
    def execute(self, *args, debug=False, input_data=None, **kwargs):
        pass
