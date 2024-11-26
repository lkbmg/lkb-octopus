from .MacOSExecutor import Executor


class SoftwareUpdate:
    """
    A class for interacting with the macOS `softwareupdate` utility.

    Provides methods for managing system updates, querying update information, and controlling update behavior.
    """
    def __init__(self):
        """Initialize Executor with the default binary path for `softwareupdate`."""
        self.softwareupdate = Executor('/usr/sbin/softwareupdate')

    def execute(self, *args, debug=False):
        """
        Execute a `softwareupdate` command with the specified arguments.

        Args:
            *args: Command arguments for `softwareupdate`.
            debug (bool): If True, enables debug output.

        Returns:
            str: The command output as a stripped string.
        """
        return self.softwareupdate.execute(*args, debug=debug).strip()

    # ** Manage Updates **
    def list_updates(self, no_scan=False, product_types=None, debug=False):
        """
        List all available updates.

        Args:
            no_scan (bool): Skip scanning for new updates.
            product_types (str): Comma-separated product types (e.g., "macOS,Safari").
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        args = ["--list"]
        if no_scan:
            args.append("--no-scan")
        if product_types:
            args.extend(["--product-types", product_types])
        return self.execute(*args, debug=debug)

    def download_updates(self, updates=None, no_scan=False, product_types=None, debug=False):
        """
        Download updates.

        Args:
            updates (list): Specific update labels to download.
            no_scan (bool): Skip scanning for new updates.
            product_types (str): Comma-separated product types (e.g., "macOS,Safari").
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        args = ["--download"]
        if no_scan:
            args.append("--no-scan")
        if product_types:
            args.extend(["--product-types", product_types])
        if updates:
            args.extend(updates)
        return self.execute(*args, debug=debug)

    def install_updates(self, updates=None, all_updates=False, restart=False, recommended=False, os_only=False,
                        safari_only=False, stdinpass=None, user=None, debug=False):
        """
        Install updates.

        Args:
            updates (list): Specific update labels to install.
            all_updates (bool): Install all available updates.
            restart (bool): Automatically restart/shut down if required.
            recommended (bool): Install only recommended updates.
            os_only (bool): Install only OS updates.
            safari_only (bool): Install only Safari updates.
            stdinpass (str): Password for authenticating as an owner (Apple Silicon only).
            user (str): Username for authenticating as an owner (Apple Silicon only).
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        args = ["--install"]
        if all_updates:
            args.append("--all")
        if restart:
            args.append("--restart")
        if recommended:
            args.append("--recommended")
        if os_only:
            args.append("--os-only")
        if safari_only:
            args.append("--safari-only")
        if stdinpass:
            args.extend(["--stdinpass", stdinpass])
        if user:
            args.extend(["--user", user])
        if updates:
            args.extend(updates)
        if not all_updates and not updates:
            raise ValueError("You must specify either `all_updates=True` or provide a list of updates.")
        return self.execute(*args, debug=debug)

    def list_full_installers(self, debug=False):
        """
        List all available macOS full installers.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--list-full-installers", debug=debug)

    def fetch_full_installer(self, version=None, debug=False):
        """
        Fetch the latest or specified macOS full installer.

        Args:
            version (str): Specific macOS version to fetch (e.g., "12.3").
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        args = ["--fetch-full-installer"]
        if version:
            args.extend(["--full-installer-version", version])
        return self.execute(*args, debug=debug)

    def install_rosetta(self, debug=False):
        """
        Install Rosetta 2 on Apple Silicon Macs.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--install-rosetta", debug=debug)

    def trigger_background_update(self, debug=False):
        """
        Trigger a background scan and update operation.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--background", debug=debug)

    # ** Other Tools **
    def dump_state(self, debug=False):
        """
        Log the internal state of the SU daemon to /var/log/install.log.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--dump-state", debug=debug)

    def evaluate_products(self, products, debug=False):
        """
        Evaluate a list of product keys.

        Args:
            products (list): Product keys to evaluate.
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        if not products:
            raise ValueError("You must provide a list of product keys.")
        args = ["--evaluate-products", "--products", ",".join(products)]
        return self.execute(*args, debug=debug)

    def history(self, debug=False):
        """
        Show the install history.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--history", debug=debug)

    def reset_ignored_updates(self, debug=False):
        """
        Reset the list of ignored updates.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--reset-ignored", debug=debug)

    # ** Utility Methods **
    def verbose(self, debug=False):
        """
        Enable verbose output.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--verbose", debug=debug)

    def help(self, debug=False):
        """
        Show the usage information for `softwareupdate`.

        Args:
            debug (bool): Enable debug output.

        Returns:
            str: Command output.
        """
        return self.execute("--help", debug=debug)
