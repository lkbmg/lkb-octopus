#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.Adapters.MacOSExecutor import Executor


class PlistBuddy:
    def __init__(self, plist_path):
        """
        Initialize Executor with the default binary path for PlistBuddy 
        and set the plist file path.
        """
        self.plist_buddy = Executor('/usr/libexec/PlistBuddy')
        self.plist_path = plist_path

    def execute(self, *args, debug=False):
        """
        Execute a PlistBuddy command on the specified plist file.

        Args:
            *args: Command arguments for PlistBuddy.
            debug (bool): If True, enables debug output.

        Returns:
            str: The command output as a stripped string.
        """
        command = "-c"
        full_command = [command, " ".join(args), self.plist_path]
        return self.plist_buddy.execute(*full_command, debug=debug).strip()

    def help(self, debug=False):
        """Display help information for PlistBuddy commands."""
        return self.execute("Help", debug=debug)

    def save(self, debug=False):
        """Save the current changes to the plist file."""
        return self.execute("Save", debug=debug)

    def revert(self, debug=False):
        """Revert to the last saved version of the plist file."""
        return self.execute("Revert", debug=debug)

    def clear(self, plist_type=None, debug=False):
        """
        Clear all existing entries in the plist, and set the root type if specified.

        Args:
            plist_type (str): The type to set for the root (e.g., dict, array).

        Returns:
            str: Command output.
        """
        command = f"Clear {plist_type}" if plist_type else "Clear"
        return self.execute(command, debug=debug)

    def print(self, entry=None, debug=False):
        """
        Print the value of the specified entry. If no entry is provided, print the entire plist.

        Args:
            entry (str): The entry to print.

        Returns:
            str: The printed output.
        """
        command = f"Print {entry}" if entry else "Print"
        return self.execute(command, debug=debug)

    def set(self, entry, value, debug=False):
        """
        Set the value of the specified entry to a given value.

        Args:
            entry (str): The entry to set.
            value (str): The value to assign.

        Returns:
            str: Command output.
        """
        return self.execute(f"Set {entry} {value}", debug=debug)

    def add(self, entry, entry_type, value=None, debug=False):
        """
        Add a new entry of the specified type to the plist, with an optional value.

        Args:
            entry (str): The entry to add.
            entry_type (str): The type of the entry (e.g., dict, array).
            value (str): Optional value to assign.

        Returns:
            str: Command output.
        """
        command = f"Add {entry} {entry_type} {value}" if value else f"Add {entry} {entry_type}"
        return self.execute(command, debug=debug)

    def copy(self, entry_src, entry_dst, debug=False):
        """
        Copy the specified source entry to the destination entry.

        Args:
            entry_src (str): The source entry.
            entry_dst (str): The destination entry.

        Returns:
            str: Command output.
        """
        return self.execute(f"Copy {entry_src} {entry_dst}", debug=debug)

    def delete(self, entry, debug=False):
        """
        Delete the specified entry from the plist.

        Args:
            entry (str): The entry to delete.

        Returns:
            str: Command output.
        """
        return self.execute(f"Delete {entry}", debug=debug)

    def merge(self, file_path, entry=None, debug=False):
        """
        Merge the contents of the specified plist file into the given entry or the root if no entry is provided.

        Args:
            file_path (str): The path to the plist file to merge.
            entry (str): Optional entry to merge into.

        Returns:
            str: Command output.
        """
        command = f"Merge {file_path} {entry}" if entry else f"Merge {file_path}"
        return self.execute(command, debug=debug)

    def import_entry(self, entry, file_path, debug=False):
        """
        Import the contents of the specified file into the given entry.

        Args:
            entry (str): The entry to import into.
            file_path (str): The file path to import.

        Returns:
            str: Command output.
        """
        return self.execute(f"Import {entry} {file_path}", debug=debug)
