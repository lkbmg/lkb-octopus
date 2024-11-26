#!/usr/bin/env python3
'''
MacOSName.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.MacOSExecutor import Executor


class Scutil:
    def __init__(self):
        """Initialize Executor with the default binary path for scutil."""
        self.scutil = Executor('/usr/sbin/scutil')

    def get_computer_name(self, debug=False):
        """Retrieves and returns the computer name in uppercase."""
        output = self.scutil.execute("--get", "ComputerName", debug=debug)
        return output.decode('utf-8').strip().upper()
    
    def get_local_hostname(self, debug=False):
        """Retrieves and returns the local hostname in uppercase."""
        output = self.scutil.execute("--get", "LocalHostName", debug=debug)
        return output.decode('utf-8').strip().upper()

    def get_hostname(self, debug=False):
        """Retrieves and returns the hostname in uppercase."""
        output = self.scutil.execute("--get", "HostName", debug=debug)
        return output.decode('utf-8').strip().upper()

    def set_computer_name(self, data, debug=False):
        """Sets the computer name."""
        output = self.scutil.execute("--set", "ComputerName", data, debug=debug)
        return output.decode('utf-8').strip().upper()
    
    def set_local_hostname(self, data, debug=False):
        """Sets the local hostname."""
        output = self.scutil.execute("--set", "LocalHostName", data, debug=debug)
        return output.decode('utf-8').strip().upper()

    def set_hostname(self, data, debug=False):
        """Sets the hostname."""
        output = self.scutil.execute("--set", "HostName", data, debug=debug)
        return output.decode('utf-8').strip().upper()
