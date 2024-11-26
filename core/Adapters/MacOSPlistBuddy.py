#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.MacOSExecutor import Executor

class PlistBuddy:
    def __init__(self, plist_path):
        """Initialize Executor with the default binary path for PlistBuddy and set the plist file path."""
        self.plist_buddy = Executor('/usr/libexec/PlistBuddy')
        self.plist_path = plist_path

    def execute(self, *args, debug=False):
        """Execute a PlistBuddy command on the specified plist file."""
        return self.plist_buddy.execute("-c", " ".join(args), self.plist_path, debug=debug).decode('utf-8').strip()

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
        """Clear all existing entries in the plist, and set the root type if specified."""
        if plist_type:
            return self.execute(f"Clear {plist_type}", debug=debug)
        else:
            return self.execute("Clear", debug=debug)

    def print(self, entry=None, debug=False):
        """Print the value of the specified entry. If no entry is provided, print the entire plist."""
        if entry:
            return self.execute(f"Print {entry}", debug=debug)
        else:
            return self.execute("Print", debug=debug)

    def set(self, entry, value, debug=False):
        """Set the value of the specified entry to a given value."""
        return self.execute(f"Set {entry} {value}", debug=debug)

    def add(self, entry, entry_type, value=None, debug=False):
        """Add a new entry of the specified type to the plist, with an optional value."""
        if value is not None:
            return self.execute(f"Add {entry} {entry_type} {value}", debug=debug)
        else:
            return self.execute(f"Add {entry} {entry_type}", debug=debug)

    def copy(self, entry_src, entry_dst, debug=False):
        """Copy the specified source entry to the destination entry."""
        return self.execute(f"Copy {entry_src} {entry_dst}", debug=debug)

    def delete(self, entry, debug=False):
        """Delete the specified entry from the plist."""
        return self.execute(f"Delete {entry}", debug=debug)

    def merge(self, file_path, entry=None, debug=False):
        """Merge the contents of the specified plist file into the given entry or the root if no entry is provided."""
        if entry:
            return self.execute(f"Merge {file_path} {entry}", debug=debug)
        else:
            return self.execute(f"Merge {file_path}", debug=debug)

    def import_entry(self, entry, file_path, debug=False):
        """Import the contents of the specified file into the given entry."""
        return self.execute(f"Import {entry} {file_path}", debug=debug)

