#!/usr/bin/env python3
'''
MacOSDefaults.py
Written by pollardm
Written: 11/11/24
Description: Base Class for macOS Defaults
'''
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+'/../'))
from core.MacOSExecutor import Executor

class Defaults:
    def __init__(self):
        """Initialize Executor with the default binary path for defaults."""
        self.defaults = Executor('/usr/bin/defaults')

    def list_domains(self, debug=False):
        """Shows all domains."""
        return self.defaults.execute("domains", debug=debug).decode('utf-8').strip()

    def show_all(self, debug=False):
        """Shows all defaults."""
        return self.defaults.execute("read", debug=debug).decode('utf-8').strip()

    def read(self, domain, key=None, debug=False):
        """Shows defaults for given domain or domain key."""
        args = [domain, key] if key else [domain]
        return self.defaults.execute("read", *args, debug=debug).decode('utf-8').strip()

    def write(self, domain, key, value, value_type="string", debug=False):
        """Writes a value for a domain and key, with type specified."""
        type_flag = {
            "string": "-string", "int": "-int", "integer": "-int",
            "float": "-float", "bool": "-bool", "boolean": "-bool",
            "data": "-data", "date": "-date", "array": "-array", "dict": "-dict"
        }.get(value_type.lower())

        if not type_flag:
            raise ValueError(f"Unsupported value_type '{value_type}'.")

        return self.defaults.execute("write", domain, key, type_flag, str(value), debug=debug).decode('utf-8').strip()

    def delete(self, domain, key=None, debug=False):
        """Deletes a domain or key within a domain."""
        args = [domain, key] if key else [domain]
        return self.defaults.execute("delete", *args, debug=debug).decode('utf-8').strip()

    def export_to_file(self, domain, path, debug=False):
        """Saves domain as a binary plist to a specified path."""
        output = self.defaults.execute("export", domain, path, debug=debug)
        return output.decode('utf-8').strip()

    def export_to_stdout(self, domain, debug=False):
        """Writes domain as an XML plist to stdout."""
        output = self.defaults.execute("export", domain, "-", debug=debug)
        return output.decode('utf-8').strip()

    def delete_domain(self, domain, debug=False):
        """Deletes a domain."""
        output = self.defaults.execute("delete", domain, debug=debug)
        return output.decode('utf-8').strip()
    
    def delete_key(self, domain, key, debug=False):
        """Deletes a key in a domain."""
        output = self.defaults.execute("delete", domain, key, debug=debug)
        return output.decode('utf-8').strip()
