#!/usr/bin/env python3
"""
MacOSExecutor.py
Written by pollardm
Written: 11/12/24
Description: MacOS command executor
"""
import os
import subprocess
import logging
from core.ExecutorBase import BaseExecutor
from core.Exceptions import CommandExecutionError


class Executor(BaseExecutor):
    def __init__(self, binary_path):
        if not os.path.isfile(binary_path):
            raise ValueError(f"The specified binary path does not exist: {binary_path}")
        if not os.access(binary_path, os.X_OK):
            raise ValueError(f"The specified binary path is not executable: {binary_path}")
        super().__init__(binary_path)

    def execute(self, *args, debug=False, input_data=None, timeout=None, env=None, encoding="utf-8", **kwargs):
        """
        Execute a system command using the specified binary.

        Args:
            *args: Positional arguments to pass to the binary.
            debug (bool): If True, logs the command and outputs for debugging.
            input_data (bytes/str): Data to pass to the command's stdin.
            timeout (int): Maximum time in seconds to wait for the command to complete.
            env (dict): Environment variables to use for the command.
            encoding (str): Encoding to use for decoding the output.
            **kwargs: Key-value arguments to append as options to the command.

        Returns:
            str: The command's stdout as a decoded string.

        Raises:
            CommandExecutionError: If the command exits with a non-zero status or fails.
        """
        full_command = [self.binary_path] + list(args)
        for key, value in kwargs.items():
            full_command.append(key)
            if value is not None:
                full_command.append(str(value))

        if debug:
            logging.info(f"Executing command: {' '.join(full_command)}")

        try:
            with subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE if input_data else None,
                env=env,
                text=True,
                encoding=encoding,  # Explicitly set encoding
            ) as process:
                stdout, stderr = process.communicate(input=input_data, timeout=timeout)

                if debug:
                    logging.info(f"Output: {stdout}")
                    logging.info(f"Error: {stderr}")

                if process.returncode != 0:
                    raise CommandExecutionError(full_command, process.returncode, stderr)

                return stdout.strip()
        except subprocess.TimeoutExpired as e:
            process.kill()
            raise CommandExecutionError(full_command, None, f"Command timed out after {timeout}s") from e
        except Exception as e:
            logging.error(f"Unexpected error while executing command: {e}")
            raise CommandExecutionError(full_command, None, str(e)) from e

    def close(self):
        """No resources to clean up in this implementation."""
        pass
