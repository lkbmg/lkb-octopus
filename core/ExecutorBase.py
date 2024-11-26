#!/usr/bin/env python3
'''
BaseExecutor.py
Written by pollardm
Written: 11/12/24
Description: Base Class for command execution.
'''
from abc import ABC, abstractmethod

class BaseExecutor(ABC):
    def __init__(self, binary_path):
        self.binary_path = binary_path

    @abstractmethod
    def execute(self, *args, debug=False, input_data=None, **kwargs):
        pass
