from core.MacOSExecutor import Executor


class Plutil:
    def __init__(self):
        """Initialize Executor with the default binary path for softwareupdate."""
        self.plutil = Executor('/usr/sbin/softwareupdate')

    def help(self, debug=False):
        """Show the usage information for softwareupdate."""
        output = self.plutil.execute("--help", debug=debug)
        return output.decode('utf-8').strip()

    def list(self, noscan=None, producttype=None, debug=False):
        """List all appropriate update labels (options:  --no-scan, --product-types)"""
        command = "--list"
        args = [command, noscan, producttype] if noscan or producttype else [command]
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()

    def download(self, noscan=None, producttype=None, debug=False):
        """List all appropriate update labels (options:  --no-scan, --product-types)"""
        command = "--download"
        args = [command, noscan, producttype] if noscan or producttype else [command]
        output = self.plutil.execute(*args, debug=debug)
        return output.decode('utf-8').strip()