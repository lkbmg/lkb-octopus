#!/usr/bin/env python3
'''
common.py
Written by pollardm
Written: 11/11/24
Description: Base Classes for macOS Local Settings
'''

from core.Adapters.MacOSExecutor import Executor


class Launchctl:
    def __init__(self):
        """Initialize Executor with the default binary path for launchctl."""
        self.launchctl = Executor('/bin/launchctl')

    def bootstrap(self, target, service, debug=False):
        """Bootstraps a domain or service into a domain."""
        return self.launchctl.execute("bootstrap", target, service, debug=debug).strip()

    def bootout(self, target, service, debug=False):
        """Tears down a domain or removes a service from a domain."""
        return self.launchctl.execute("bootout", target, service, debug=debug).strip()

    def enable(self, service, debug=False):
        """Enables an existing service."""
        return self.launchctl.execute("enable", service, debug=debug).strip()

    def disable(self, service, debug=False):
        """Disables an existing service."""
        return self.launchctl.execute("disable", service, debug=debug).strip()

    def kickstart(self, service, debug=False):
        """Forces an existing service to start."""
        return self.launchctl.execute("kickstart", service, debug=debug).strip()

    def attach(self, service, debug=False):
        """Attach the system's debugger to a service."""
        return self.launchctl.execute("attach", service, debug=debug).strip()

    def debug(self, service, debug=False):
        """Configures the next invocation of a service for debugging."""
        return self.launchctl.execute("debug", service, debug=debug).strip()

    def kill(self, signal, service, debug=False):
        """Sends a signal to the service instance."""
        return self.launchctl.execute("kill", signal, service, debug=debug).strip()

    def blame(self, service, debug=False):
        """Prints the reason a service is running."""
        return self.launchctl.execute("blame", service, debug=debug).strip()

    def print_service(self, service, debug=False):
        """Prints a description of a domain or service."""
        return self.launchctl.execute("print", service, debug=debug).strip()

    def list_services(self, debug=False):
        """Lists information about services."""
        return self.launchctl.execute("list", debug=debug).strip()

    def start_service(self, service, debug=False):
        """Starts the specified service."""
        return self.launchctl.execute("start", service, debug=debug).strip()

    def stop_service(self, service, debug=False):
        """Stops the specified service if it is running."""
        return self.launchctl.execute("stop", service, debug=debug).strip()

    def setenv(self, var, value, debug=False):
        """Sets an environment variable for all services within the domain."""
        return self.launchctl.execute("setenv", var, value, debug=debug).strip()

    def getenv(self, var, debug=False):
        """Gets the value of an environment variable from within launchd."""
        return self.launchctl.execute("getenv", var, debug=debug).strip()

    def unsetenv(self, var, debug=False):
        """Unsets an environment variable for all services within the domain."""
        return self.launchctl.execute("unsetenv", var, debug=debug).strip()

    def print_disabled(self, debug=False):
        """Prints which services are disabled."""
        return self.launchctl.execute("print-disabled", debug=debug).strip()

    def version(self, debug=False):
        """Prints the launchd version."""
        return self.launchctl.execute("version", debug=debug).strip()

    def help(self, subcommand=None, debug=False):
        """Prints the usage for a given subcommand, or general help."""
        args = ["help"]
        if subcommand:
            args.append(subcommand)
        return self.launchctl.execute(*args, debug=debug).strip()
