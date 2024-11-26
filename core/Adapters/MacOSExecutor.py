#!/usr/bin/env python3
'''
MacOSExecutor.py
Written by pollardm
Written: 11/12/24
Description: MacOS command executor
'''
import subprocess
from .ExecutorBase import BaseExecutor, CommandExecutionError  # Relative import

class Executor(BaseExecutor):
    def __init__(self, binary_path):
        super().__init__(binary_path)

    def execute(self, *args, debug=False, input_data=None, **kwargs):
        full_command = [self.binary_path] + list(args)

        for key, value in kwargs.items():
            full_command.append(key)
            if value is not None:
                full_command.append(str(value))
        
        if debug:
            print(f"Executing command: {' '.join(full_command)}")

        with subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            stdout, stderr = process.communicate(input=input_data)

            if debug:
                print(f"Output: {stdout.decode('utf-8', errors='replace')}")
                print(f"Error: {stderr.decode('utf-8', errors='replace')}")

            if process.returncode != 0:
                raise CommandExecutionError(full_command, process.returncode, stderr)
            
            return stdout  # Return as bytes
