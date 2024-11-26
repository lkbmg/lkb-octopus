#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.Adapters.MacOSExecutor import Executor


class Plutil:
    def __init__(self):
        """
        Initialize Executor with the default binary path for plutil.
        """
        self.plutil = Executor('/usr/bin/plutil')

    def execute(self, *args, debug=False):
        """
        Execute a `plutil` command with the specified arguments.

        Args:
            *args: Command arguments for `plutil`.
            debug (bool): If True, enables debug output.

        Returns:
            str: The command output as a stripped string.
        """
        return self.plutil.execute(*args, debug=debug).strip()

    def help(self, debug=False):
        """Show the usage information for plutil."""
        return self.execute("-help", debug=debug)

    def print_plist(self, file_path, debug=False):
        """Print the property list in a human-readable format."""
        return self.execute("-p", file_path, debug=debug)

    def lint(self, file_path, debug=False):
        """Check the property list for syntax errors."""
        return self.execute("-lint", file_path, debug=debug)

    def convert(self, file_path, fmt, output_path=None, debug=False):
        """
        Convert the property list to the specified format.

        Args:
            file_path (str): Path to the property list.
            fmt (str): The target format (e.g., xml1, binary1, json).
            output_path (str): Optional path to save the converted plist.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        args = ["-convert", fmt, file_path]
        if output_path:
            args.extend(["-o", output_path])
        return self.execute(*args, debug=debug)

    def insert(self, file_path, keypath, value_type, value=None, append=False, debug=False):
        """
        Insert a value into the property list at the specified keypath.

        Args:
            file_path (str): Path to the property list.
            keypath (str): The keypath to insert the value.
            value_type (str): The type of the value (e.g., string, array).
            value (str): The value to insert.
            append (bool): Whether to append to an array.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        args = ["-insert", keypath, value_type]
        if value:
            args.append(value)
        if append:
            args.append("-append")
        args.append(file_path)
        return self.execute(*args, debug=debug)

    def replace(self, file_path, keypath, value_type, value, debug=False):
        """
        Replace an existing value in the property list at the specified keypath.

        Args:
            file_path (str): Path to the property list.
            keypath (str): The keypath to replace the value.
            value_type (str): The type of the value.
            value (str): The new value.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        return self.execute("-replace", keypath, value_type, value, file_path, debug=debug)

    def remove(self, file_path, keypath, debug=False):
        """
        Remove a value from the property list at the specified keypath.

        Args:
            file_path (str): Path to the property list.
            keypath (str): The keypath to remove.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        return self.execute("-remove", keypath, file_path, debug=debug)

    def extract(self, file_path, keypath, fmt, expect_type=None, debug=False):
        """
        Extract a value at the specified keypath as a new plist of the specified format.

        Args:
            file_path (str): Path to the property list.
            keypath (str): The keypath to extract.
            fmt (str): The target format (e.g., xml1, binary1, json).
            expect_type (str): Optional expected type for validation.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        args = ["-extract", keypath, fmt]
        if expect_type:
            args.extend(["-expect", expect_type])
        args.append(file_path)
        return self.execute(*args, debug=debug)

    def get_type(self, file_path, keypath, expect_type=None, debug=False):
        """
        Get the type of the value at the specified keypath in the property list.

        Args:
            file_path (str): Path to the property list.
            keypath (str): The keypath to get the type.
            expect_type (str): Optional expected type for validation.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        args = ["-type", keypath]
        if expect_type:
            args.extend(["-expect", expect_type])
        args.append(file_path)
        return self.execute(*args, debug=debug)

    def create(self, fmt, output_path=None, debug=False):
        """
        Create an empty plist of the specified format.

        Args:
            fmt (str): The target format (e.g., xml1, binary1).
            output_path (str): Optional path to save the plist.
            debug (bool): If True, enables debug output.

        Returns:
            str: Command output.
        """
        args = ["-create", fmt]
        if output_path:
            args.append(output_path)
        return self.execute(*args, debug=debug)
