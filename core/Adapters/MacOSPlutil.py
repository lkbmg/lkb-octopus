#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.MacOSExecutor import Executor

class Plutil:
    def __init__(self):
        """Initialize Executor with the default binary path for plutil."""
        self.plutil = Executor('/usr/bin/plutil')

    def help(self, debug=False):
        """Show the usage information for plutil."""
        output = self.plutil.execute("-help", debug=debug)
        return output.decode('utf-8').strip()

    def print_plist(self, file_path, debug=False):
        """Print the property list in a human-readable format."""
        output = self.plutil.execute("-p", file_path, debug=debug)
        return output.decode('utf-8').strip()

    def lint(self, file_path, debug=False):
        """Check the property list for syntax errors."""
        output = self.plutil.execute("-lint", file_path, debug=debug)
        return output.decode('utf-8').strip()

    def convert(self, file_path, fmt, output_path=None, debug=False):
        """Convert the property list to the specified format."""
        args = ["-convert", fmt, file_path]
        if output_path:
            args.extend(["-o", output_path])
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()

    def insert(self, file_path, keypath, value_type, value=None, append=False, debug=False):
        """Insert a value into the property list at the specified keypath."""
        args = ["-insert", keypath, value_type]
        if value:
            args.append(value)
        if append:
            args.append("-append")
        args.append(file_path)
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()

    def replace(self, file_path, keypath, value_type, value, debug=False):
        """Replace an existing value in the property list at the specified keypath."""
        output = self.plutil.execute("-replace", keypath, value_type, value, file_path, debug=debug)
        return output.decode('utf-8').strip()

    def remove(self, file_path, keypath, debug=False):
        """Remove a value from the property list at the specified keypath."""
        output = self.plutil.execute("-remove", keypath, file_path, debug=debug)
        return output.decode('utf-8').strip()

    def extract(self, file_path, keypath, fmt, expect_type=None, debug=False):
        """Extract a value at the specified keypath as a new plist of the specified format."""
        args = ["-extract", keypath, fmt]
        if expect_type:
            args.extend(["-expect", expect_type])
        args.append(file_path)
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()

    def get_type(self, file_path, keypath, expect_type=None, debug=False):
        """Get the type of the value at the specified keypath in the property list."""
        args = ["-type", keypath]
        if expect_type:
            args.extend(["-expect", expect_type])
        args.append(file_path)
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()

    def create(self, fmt, output_path=None, debug=False):
        """Create an empty plist of the specified format."""
        args = ["-create", fmt]
        if output_path:
            args.append(output_path)
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()
